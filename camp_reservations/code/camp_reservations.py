'''
This code will book assateague sites

EXAMPLE USAGE:
# build env
python3 -m venv camp_res
source camp_res/bin/activate 
pip install playwright
playwright install

# run with variables
python3 ./camp_reservations.py "<park>" "<site>" "<arrival>" "<depart>" "<party_size>" "<equipment>" --debug 

# run example
python3 ./camp_reservations.py "assateague" "G195" "07112026" "07202026" "6" "tent" --debug 

'''

import time, json, random, urllib.parse, sys, ntplib, argparse
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from multiprocessing import Process
from threading import Event
from time import ctime


def parse_args():
	parser = argparse.ArgumentParser(description="Generate booking jobs for campsite reservations.")

	parser.add_argument("--sites", required=True, help="Comma-separated list of site IDs (e.g., F143,E119)")
	parser.add_argument("--start_date", required=True, help="Start date in YYYY-MM-DD format")
	parser.add_argument("--nights", type=int, required=True, help="Number of nights")
	parser.add_argument("--people", type=int, required=True, help="Number of people")
	parser.add_argument("--site_type", required=True, help="Site type (e.g., rv, tent)")
	parser.add_argument("--time", type=str, required=True, help="Base time in HH:MM:SS.sss format (e.g., 18:05:00.000)")
	parser.add_argument("--attempts", type=int, default=1, help="Number of attempts per site")

	return parser.parse_args()


def human_delay(min_ms, max_ms):
	time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


def encode_people_count(equipment_category_id, party_size):
    arr = [[equipment_category_id, None, party_size, None]]
    json_str = json.dumps(arr, separators=(',', ':')).replace("None", "null")
    return urllib.parse.quote(json_str)


def book_assateague_site(site_id, start_date, end_date, nights, people, site_type, target_time_str):
	"""
	example use case:
	book_assateague_site("G199", "2025-07-10", "2025-07-24", 14, 5, "rv", "18:04:59.500")
	"""
	reservation_status = False

	# pull up reservation page in chromium
	from playwright.sync_api import sync_playwright
	p = sync_playwright().start()
	browser = p.chromium.launch(headless=False)
	page = browser.new_page()
	if (site_id[0]=="E" or site_id[0]=="F"): map_id = "-2147483645"
	if (site_id[0]=="G"): map_id = "-2147483644"
	if (site_type == "rv"):
		equipment_id = -32768
		sub_equipment_id = -32764
	# build reservation URL
	base_url = "https://parkreservations.maryland.gov/create-booking/results?"
	params = {
		"resourceLocationId": "-2147483648",  # Assateague State Park
		"mapId": map_id,
		"searchTabGroupId": "0",
		"bookingCategoryId": "0",
		"startDate": start_date,
		"endDate": end_date,
		"nights": str(nights),
		"isReserving": "true",
		"equipmentId": str(equipment_id),
		"subEquipmentId": str(sub_equipment_id),
		"peopleCapacityCategoryCounts": encode_people_count(equipment_id, people),
		# Format searchTime to milliseconds precision to match example
		"searchTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
		# Encode flexibleSearch and filterData only once
		"flexibleSearch": urllib.parse.quote('[false,false,null,1]'),
		"filterData": urllib.parse.quote('{}'),
	}
	reservation_url = base_url + "&".join(f"{k}={v}" for k, v in params.items())

	# visit URL
	page.goto(reservation_url)
	human_delay(300,900)
	page.reload()

	# pass cookie consent
	page.click('button:has-text("I Consent")')
	print("Popup dismissed.")

	# select site
	human_delay(300,900)
	site_selector = f'div.resource-label:has-text("{site_id}")'
	page.wait_for_selector(site_selector)
	page.click(site_selector)

	# wait until current time is after reservation time
	while True:
		now = datetime.now().strftime("%H:%M:%S.%f"[:-3])
		if now >= target_time_str:
			page.click('button:has-text("Reserve")')
			break
		time.sleep(0.1)  # Poll every 100ms

	# get failed pop-up dialog close browser
	try:
		page.wait_for_selector("#mat-mdc-dialog-title-0", timeout=10000)
		dialog_text = page.locator("#mat-mdc-dialog-title-0").inner_text()
		if (dialog_text =="Cannot Reserve"):
			human_delay(1000,5000)
			browser.close()
			print(f"Failed to reserve site {site_id}.")
			return reservation_status
	except Exception as e:
		print(f"An error occurred: {e}")

	# wait for user to close possible reservations
	print(f"Reservation in PROGRESS for site {site_id}.")
	Event().wait()
	browser.close()
	p.stop()
	

def get_time_offset(ntp_server='pool.ntp.org'):
	offset = 0
	try:
		client = ntplib.NTPClient()
		response = client.request(ntp_server)
		offset = response.offset  # seconds, can be positive or negative
	except Exception as e:
		print(f"❌ Failed to get NTP time: {e}")
	return offset


def build_booking_jobs(sites_to_try, start_date, nights, people, site_type, base_time, attempts):
    """
    Builds a list of booking job tuples like:
    ("G199", "2025-07-10", "2025-07-24", 14, 5, "rv", "18:04:59.500")
    """

    jobs = []

    # Calculate end date
    end_date_dt = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=nights)
    end_date = end_date_dt.strftime("%Y-%m-%d")

    # Parse base time string into datetime object (using today's date)
    today = datetime.today().date()
    base_dt = datetime.strptime(base_time, "%H:%M:%S.%f")
    base_dt = datetime.combine(today, base_dt.time())

    offset = get_time_offset()  # returns a timedelta
    for site in sites_to_try:
        for attempt in range(attempts):
            attempt_time = base_dt + timedelta(seconds=offset) + timedelta(milliseconds=100 * attempt)
            attempt_time_str = attempt_time.strftime("%H:%M:%S.%f")[:-3]
            job = (
                site,
                start_date,
                end_date,
                nights,
                people,
                site_type,
                attempt_time_str
            )
            jobs.append(job)
    return jobs


def launch_booking_job(args):
	book_assateague_site(*args)

if __name__ == "__main__":
	args = parse_args()

	sites_to_try = args.sites.split(",")
	start_date = args.start_date
	nights = args.nights
	people = args.people
	site_type = args.site_type
	base_time = args.time
	attempts = args.attempts
	booking_jobs = build_booking_jobs(sites_to_try, start_date, nights, people, site_type, base_time, attempts)

	processes = []

	try:
		for args in booking_jobs:
			print(f"Starting reservation attempt using {args}")
			p = Process(target=launch_booking_job, args=(args,))
			p.start()
			processes.append(p)

		for p in processes:
			p.join()
	except KeyboardInterrupt:
		print("\nKeyboardInterrupt received. Cleaning up child processes...")
		for p in processes:
			if p.is_alive():
				p.terminate()
		sys.exit(1)
	print("All booking jobs completed.")

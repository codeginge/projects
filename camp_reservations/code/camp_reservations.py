'''
This code will book assateague sites

TODO: 
- get payment working  (with cli input at start)
- get headless working all the way through payment

EXAMPLE USAGE:
# build environment
python3 -m venv camp_res
source camp_res/bin/activate 
pip install requests
pip install ntplib
pip install playwright
playwright install

# run with example

CHECK SYSTEM TIME IS correct

RESERVE SITE 
python3 ./camp_reservations.py \
  --sites F143,E119 \
  --start_date 2025-07-10 \
  --people 5 \
  --nights 14 \
  --site_type rv \
  --time "09:00:00.000" \
  --attempts 2

RESERVE SITE HEADLESS
python3 ./camp_reservations.py \
  --sites F143,E119 \
  --start_date 2025-07-10 \
  --people 5 \
  --nights 14 \
  --site_type rv \
  --time "09:00:00.000" \
  --attempts 2 \
  --run_headless
'''

import time, json, random, urllib.parse, sys, ntplib, argparse, requests, urllib3
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
	parser.add_argument("--delay", type=int, default=1, help="Number of milliseconds of delay between attempts")
	parser.add_argument("--run_headless", action="store_true", help="Run in headless mode")

	return parser.parse_args()


def human_delay(min_ms, max_ms):
	time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))


def encode_people_count(equipment_category_id, party_size):
	arr = [[equipment_category_id, None, party_size, None]]
	json_str = json.dumps(arr, separators=(',', ':')).replace("None", "null")
	return urllib.parse.quote(json_str)


def get_ntp_clock_offset(ntp_servers=None, timeout=5):
    import ntplib
    client = ntplib.NTPClient()
    ntp_servers = ntp_servers or [
        "time.google.com",
        "time.windows.com",
        "time.apple.com",
        "pool.ntp.org"
    ]
    
    for server in ntp_servers:
        try:
            response = client.request(server, version=3, timeout=timeout)
            return response.offset, response.delay
        except Exception as e:
            print(f"Failed to get NTP from {server}: {e}")
    
    print("All NTP attempts failed.")
    return 0.0, 0.0  # fallback to no offset


def get_site_response_delay(website, attempts=5, timeout=3):
	"""
	Measures the average HTTP HEAD request round-trip delay to the given website.

	Parameters:
		website (str): The target website URL (including http:// or https://).
		attempts (int): Number of attempts to average (default 5).
		timeout (int or float): Request timeout in seconds (default 3).

	Returns:
		float or None: Average delay in seconds, or None if all attempts fail.
	"""
	headers = {
		"User-Agent": (
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
			"(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
		),
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Referer": "https://parkreservations.maryland.gov/"
	}

	# disable verify=False warnings
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	delays = []
	for _ in range(attempts):
		try:
			start = time.time()
			response = requests.get(website, headers=headers, timeout=timeout, verify=False)
			end = time.time()
			delays.append(end - start)
		except requests.RequestException:
			# Ignore this attempt if it fails
			continue

	if delays:
		return sum(delays) / len(delays)
	else:
		return None


def book_assateague_site(site_id, start_date, end_date, nights, people, site_type, target_time_str, run_headless):
	"""
	example use case:
	book_assateague_site("G199", "2025-07-10", "2025-07-24", 14, 5, "rv", "18:04:59.500")

	availability Update Selector = "#mat-mdc-dialog-title-0", Text = "Avaliability Update"
	"""
	reservation_status = False

	# pull up reservation page in chromium
	from playwright.sync_api import sync_playwright
	p = sync_playwright().start()
	browser = p.chromium.launch(headless=run_headless)
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
		#"searchTime": "2025-07-10"
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

	# select site
	human_delay(300,900)
	site_selector = f'div.resource-label:has-text("{site_id}")'
	page.wait_for_selector(site_selector)
	page.click(site_selector)

	# wait until current time is after reservation time
	target_time = datetime.combine(datetime.today().date(), datetime.strptime(target_time_str, "%H:%M:%S.%f").time())
	offset_applied = False
	delay_modified = False
	loop_delay = 0.1
	while True:
		now = datetime.now()
		if (offset_applied == False and (now + timedelta(seconds=30))>=target_time):
			offset_applied = True
			time_offset = timedelta(seconds=get_ntp_clock_offset()[0]) + timedelta(seconds=(get_site_response_delay("https://parkreservations.maryland.gov/") / 2))
			print(f"Calculated latencey: {time_offset}")
			adjusted_target_time = target_time - time_offset
			print(f"Adjusted target time for reserving site {site_id} is {adjusted_target_time.strftime('%H:%M:%S.%f')}")
		if (offset_applied == True and delay_modified==False and (now + timedelta(seconds=5))>=target_time):
			loop_delay = 0.005
			delay_modified == True
		if (offset_applied==True and now >= adjusted_target_time):
			print(f"now: {now} adjusted_target_time {adjusted_target_time}")
			page.click('button:has-text("Reserve")')
			print(f"Reservation attempt for site {site_id} at {(datetime.now()-timedelta(seconds=get_ntp_clock_offset()[0])).strftime('%H:%M:%S.%f')} NTP")
			break
		time.sleep(loop_delay)  # Poll every 100ms

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
	

def build_booking_jobs(sites_to_try, start_date, nights, people, site_type, base_time, attempts, delay, run_headless):
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

	for site in sites_to_try:
		for attempt in range(attempts):
			attempt_time = base_dt + timedelta(milliseconds=delay * attempt)
			attempt_time_str = attempt_time.strftime("%H:%M:%S.%f")
			job = (
				site,
				start_date,
				end_date,
				nights,
				people,
				site_type,
				attempt_time_str,
				run_headless
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
	delay = args.delay
	run_headless = args.run_headless
	booking_jobs = build_booking_jobs(sites_to_try, start_date, nights, people, site_type, base_time, attempts, delay, run_headless)

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

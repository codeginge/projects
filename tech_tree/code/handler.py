'''
Last updated: 7/29/25
By: Michael Roberts
'''

import json, argparse, gspread, nltk, random, string, time

nltk.download('words')
from nltk.corpus import words
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def parse_args():
    parser = argparse.ArgumentParser(description="Setup arguments for data handler.")

    parser.add_argument("--gcreds", required=True, help="Location of google credential json file.")
    parser.add_argument("--sheet_id", required=True, help="Name of google sheet to use.")
    parser.add_argument("--lms_json_file", required=True, help="Location of lms json file.")
    parser.add_argument("--status_json_file", required=True, help="Location of status json file.")
    
    return parser.parse_args()


def create_username(first_name, last_name):
    word_list = [w.lower() for w in words.words()]  # lowercase for consistency
    first_letter_first_name = first_name[0].lower()
    first_letter_last_name = last_name[0].lower()
    first_name_matches = [w for w in word_list if w.startswith(first_letter_first_name.lower())]
    last_name_matches = [w for w in word_list if w.startswith(first_letter_last_name.lower())]
    first_word = random.choice(first_name_matches) if first_name_matches else None
    second_word = random.choice(last_name_matches) if last_name_matches else None
    number = random.randint(10, 999)
    username = f"{first_word}_{second_word}_{number}"
    return username


def create_password(num_words, num_digits):
    word_list = [w.lower() for w in words.words() if w.isalpha() and len(w) >= 4]
    chosen_words = random.sample(word_list, num_words)
    digits = ''.join(random.choices(string.digits, k=num_digits))
    password = ''.join(chosen_words) + digits
    return password


def update_user_creds(json_key_path, sheet_id, status_page):
    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(sheet_id).worksheet(status_page)
    status_data = worksheet.get_all_values()
    headers = status_data[1]
    username_col = headers.index("username") + 1  
    password_col = headers.index("password") + 1
    for i, row in enumerate(status_data[1:], start=2):  # sheet row numbers start at 1
        row_dict = dict(zip(headers, row))
        first_name = str(row_dict.get("first","").lower())
        last_name = str(row_dict.get("last","").lower())
        if not row_dict.get("username","").lower():    
            username = create_username(first_name, last_name)
            print(f"Created username '{username}' for {last_name}, {first_name}")
            worksheet.update_cell(i, username_col, username)
        if not row_dict.get("password","").lower():
            password = create_password(3,4)
            print(f"Created password '{password}' for {last_name}, {first_name}")
            worksheet.update_cell(i, password_col, password)


def pull_gsheet_data (json_key_path, sheet_id, pages):
    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    gsheet_data = []

    for page in pages:
        gsheet_data.append(client.open_by_key(sheet_id).worksheet(page).get_all_values())
    
    return gsheet_data


def update_gsheet_from_json(json_key_path, json_file, sheet_id, pages, headers):
    '''
    update gsheets from json file fill in "id" and "doc_link" items
    '''
    try:
        with open(json_file, "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"{json_file} does not exist. Creating new file in that location.")
        return false

    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)

    for page in pages:
        sheet = client.open_by_key(sheet_id).worksheet(page)
        headers = sheet.row_values(2)  # Assumes headers in row 1
        rows = sheet.get_all_values()
        name_col_index = headers.index("name")
        name_list = [row[name_col_index] for row in rows[2:]]  # Data starts at row 3

        for entry in json_data:
            entry_name = entry["name"]
            entry_id = entry["id"]
            entry_doc_link = entry["doc_link"]

            if len(entry_id) == 0:
                print(f"Missing ID for {entry_name}")
                continue

            if page[0].upper() != entry_id[0]:
                continue  # skip mismatched pages

            if entry_name in name_list:
                row_index = name_list.index(entry_name) + 3  # +3 = skip header + 0-indexed
                # Update only "id" and "doc_link"
                id_col = headers.index("id") + 1
                doc_link_col = headers.index("doc_link") + 1

                existing_id = sheet.cell(row_index, id_col).value
                existing_doc_link = sheet.cell(row_index, doc_link_col).value

                if not existing_id:
                    sheet.update_cell(row_index, id_col, entry_id)
                    print(f"Updated '{entry_name}' in {page} with ID: {entry_id}")
                if not existing_doc_link:
                    sheet.update_cell(row_index, doc_link_col, entry_doc_link)
                    print(f"Updated '{entry_name}' in {page} with doc_link: {entry_doc_link}")
                
            else:
                # Append full row
                row_to_add = [entry.get(col, "") for col in headers]
                sheet.append_row(row_to_add)
                print(f"Added '{entry_name}' to {page}")


def update_json_from_gsheet(json_key_path, json_file, gsheet_data, pages, headers):
    '''
    this function updates json with new gsheet information and removes old json entries and 
    related google resources.
    '''
    try:
        with open(json_file, "r") as file:
            old_data = json.load(file)
    except FileNotFoundError:
        print(f"{json_file} does not exist. Creating new file in that location.")
        old_data = [] 

    # add gsheet info
    gsheet_data_json = []

    # get all ids in google
    all_ids = []
    for page in gsheet_data:
        headers = page[1]  # The header row with keys
        id_index = headers.index("id")  # Find index of "id"
        for row in page[2:]:
            id_value = row[id_index]
            all_ids.append(id_value)

    for page_index, page in enumerate(pages, start=0):
        page_data = gsheet_data[page_index]
        page_headers = page_data[1]
        if (headers != page_headers): 
            print(f"Headers for {page} do not match.\npage_headers = {page_headers}\nprivided_headers{headers}")
            continue
        
        # add data to json file
        for row in page_data[2:]:
            entry = dict(zip(page_headers, row))

            # create resource if it is empty
            if not entry["doc_link"]:
                entry, all_ids = create_resource(json_key_path, entry, page, all_ids)
                print(f"Created resource for {entry["name"]}")

            gsheet_data_json.append(entry)

    # find difference between old data and gsheet data and remove it
    json_diff = [entry for entry in old_data if entry not in gsheet_data_json]
    if json_diff:
        for entry in json_diff:
            clean_resource(json_key_path, entry)
            print(f"Cleaned up resource for {entry["name"]}")
        print(f"The following json data was removed to keep up to date with gsheet. \n{json_diff}")

    try:
        with open(json_file, "w") as file:
            json.dump(gsheet_data_json, file, indent=4)
    except Exception as e:
        print(f"Error writing JSON file: {e}")


def clean_resource(json_key_path, entry):
    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/drive"])
    drive_service = build('drive', 'v3', credentials=creds)

    # find related resources for entry     
    doc_link = entry["doc_link"]
    if doc_link and "/d/" in doc_link:
        document_id =doc_link.split("/d/")[1].split("/")[0]

    # delete resources
    try:
        drive_service.files().delete(fileId=document_id).execute()
        print(f"Document {document_id} deleted.")
    except Exception as e:
        print(f"Error deleting document: {e}")


def create_resource(json_key_path, entry, page, all_ids):
    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/drive"])
    drive_service = build('drive', 'v3', credentials=creds)

    # create id
    page_identifier = page[:1].upper()
    type_identifier = entry["type"][:3].upper()
    for n in range(1,100):
        new_id = f"{page_identifier}{type_identifier}{n:03}"
        if new_id not in all_ids:
            break
    entry["id"] = new_id
    all_ids.append(new_id)

    # find doc_link_template
    file_results = drive_service.files().list(
        q="name = 'doc_link_template'", 
        fields="files(id, name)").execute()
    template_id = file_results.get("files",[])[0]["id"]
    
    # create new doc from template labeled with new_id, add doc_link to entry
    folder_results = drive_service.files().list(
        q="name = 'resources' and mimeType = 'application/vnd.google-apps.folder'", 
        fields="files(id, name)").execute()
    folder_id = folder_results.get("files",[])[0]["id"]
    new_file_metadata = {
        "name": new_id,
        "parents": [folder_id]
    }
    copied_file = drive_service.files().copy(fileId=template_id, body=new_file_metadata).execute()

    new_doc_link = f"https://docs.google.com/document/d/{copied_file["id"]}/view"
    entry["doc_link"] = new_doc_link
    return entry, all_ids


def transform_user_entry(entry):
    # Core fields with fallbacks
    transformed = {
        "first": entry.get("first", ""),
        "last": entry.get("last", ""),
        "class": entry.get("class", ""),  # capitalize handling
        "type": entry.get("type", ""),
        "username": entry.get("username", ""),
        "password": entry.get("password", ""),
        "tech_count": int(entry.get("tech_count", 0) or 0),
        "tech_mastery": int(entry.get("tech_mastery", 0) or 0),
        "tech_completion": int(entry.get("tech_completion", 0) or 0),
        "project_count": int(entry.get("proj_count", 0) or 0),
        "project_mastery": int(entry.get("proj_mastery", 0) or 0),
        "project_completion": int(entry.get("proj_completion", 0) or 0),
        "contract_count": int(entry.get("contract_count", 0) or 0),
        "contract_mastery": int(entry.get("contract_mastery", 0) or 0),
        "contract_completion": int(entry.get("contract_completion", 0) or 0),
        "raw_data": []
    }

    # Find all raw data items and group them
    raw_data = list(entry.items())[15:]
    for i in range(0, len(raw_data), 2):
        key, value = raw_data[i]
        comments = raw_data[i + 1][1] if i + 1 < len(raw_data) else ""
        raw_item = {
            "id": key,
            "points": int(value) if value.strip().isdigit() else 0,
            "comments": comments
        }
        transformed["raw_data"].append(raw_item)

    return [transformed]


def update_status_json_from_gsheet(json_key_path, json_file, sheet_id, status_page):
    try:
        with open(json_file, "r") as file:
            old_data = json.load(file)
    except FileNotFoundError:
        print(f"{json_file} does not exist. Creating new file in that location.")
        old_data = [] 

    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    status_data = client.open_by_key(sheet_id).worksheet(status_page).get_all_values()

    # TODO Start here!
    new_data = []
    headers = status_data[1]
    for row in status_data[2:]:
        entry = dict(zip(headers, row))
        json_entry = transform_user_entry(entry)
        new_data.append(json_entry[0])

    try:
        with open(json_file, "w") as file:
            json.dump(new_data, file, indent=4)
    except Exception as e:
        print(f"Error writing JSON file: {e}")


def update_status_ids(json_key_path, lms_json_file, sheet_id, status_page):
    # get all ids from lms_pages
    try:
        with open(lms_json_file, "r") as file:
            lms_data = json.load(file)
    except FileNotFoundError:
        print(f"{json_file} does not exist. Can not update status ids.")
        return false
    all_ids = []
    for entry in lms_data:
        all_ids.append(entry["id"])
    # for all ids not in status page, add two columns id and id_comments in the header row 
    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(status_page)
    headers = sheet.row_values(2)
    new_headers = []
    for id_entry in all_ids:
        if id_entry not in headers:
            new_headers.append(id_entry)
            new_headers.append(f"{id_entry}_comments")
    updated_headers = headers + new_headers
    sheet.delete_rows(2)  # Remove old header
    sheet.insert_row(updated_headers, 2)  # Add new header


if __name__ == "__main__":
    args = parse_args()
    gcreds = args.gcreds
    sheet_id = args.sheet_id
    lms_json_file = args.lms_json_file
    status_json_file = args.status_json_file

    lms_pages = ["techs", "projects", "contracts"]
    lms_headers = ["name", "type", "sub_type", "core", "id", "dependency", "doc_link"]

    # Pull data from gsheet
    gsheet_data = pull_gsheet_data(gcreds, sheet_id, lms_pages)
    # update local json file and create ids and doc_links that are missing
    update_json_from_gsheet(gcreds, lms_json_file, gsheet_data, lms_pages, lms_headers)
    # update google sheet with new ids and doc_links
    update_gsheet_from_json(gcreds, lms_json_file, sheet_id, lms_pages, lms_headers)
    time.sleep(60)

    # setup/update users
    status_page = "status"
    update_user_creds(gcreds, sheet_id, status_page)
    update_status_ids(gcreds, lms_json_file, sheet_id, status_page)
    time.sleep(60)
    update_status_json_from_gsheet(gcreds, status_json_file, sheet_id, status_page)

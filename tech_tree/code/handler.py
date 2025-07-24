'''
Last updated: 7/7/23
By: Michael Roberts
'''

import json, argparse, gspread

from gspread_formatting import *
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def parse_args():
    parser = argparse.ArgumentParser(description="Setup arguments for data handler.")

    parser.add_argument("--gcreds", required=True, help="Location of google credential json file.")
    parser.add_argument("--sheet_id", required=True, help="Name of google sheet to use.")
    parser.add_argument("--lms_json_file", required=True, help="Location of lms json file.")
    parser.add_argument("--ims_json_file", required=True, help="Location of ims json file.")
    
    return parser.parse_args()


def pull_gsheet_data (json_key_path, sheet_id, pages):
    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    gsheet_data = []

    for page in pages:
        gsheet_data.append(client.open_by_key(sheet_id).worksheet(page).get_all_values())
    
    return gsheet_data


#def update_gsheet_from_json(json_key_path, json_file, gsheet_data, pages, headers):


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

            gsheet_data_json.append(entry)

    # find difference between old data and gsheet data and remove it
    json_diff = [entry for entry in old_data if entry not in gsheet_data_json]
    if json_diff:
        for entry in json_diff:
            clean_resource(json_key_path, entry)
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


if __name__ == "__main__":
    args = parse_args()
    gcreds = args.gcreds
    sheet_id = args.sheet_id
    lms_json_file = args.lms_json_file
    ims_json_file = args.ims_json_file

    lms_pages = ["techs", "projects", "contracts"]
    lms_headers = ["name","type","sub_type","core","id","dependency","doc_link"]
    
    ims_pages = ["materials"]
    ims_headers = ["name","type","sub_type","id","doc_link","unit_cost","stock","room","area","bin","storage_id"]

    gsheet_data = pull_gsheet_data(gcreds, sheet_id, lms_pages)
    update_json_from_gsheet(gcreds, lms_json_file, gsheet_data, lms_pages, lms_headers)
   

""" 
This code will pull both non-course day information and curriculum information from a google sheet,
generatee school days and times, and then combine them into a fully built out schedule given certain 
constraints.

Constraints avaliable:
1. day type priority for certian assignments (morning, lunch, or afternoon)
2. period length prioity for certain assignments (full periods, 45 minute periods, etc)
3. follow current organization of assignments or follow unit structure

Setup ENV Commands:


Terms: HW = homework, CW = classwork, L = lecture, Q = quiz, T = test, F = final
"""

import json
import argparse
import gspread
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_sheet_information(json_key_path, sheet_id):
	creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    worksheet = client.open_by_key(sheet_id).worksheet("techs")
    raw_data = worksheet.get_all_values()

	return sheet_info_json


def generate_school_days(start_day, start_letter, block, end_day, days_off_json):

	return school_days_json


def schedule_curriculum(sheet_info_json, day_type_priority, period_length_priority, unit_priority):
	"""
	priorities are 1 = true and 0 = false. 
	day_type_priority = prioritize  Q and T at lunch then morning, CW in morning, L in afternoon
	period_length_priority = prioritize T and L during full blocks
	unit_priority = follow unit numbering system not list organization
	"""

	return scheduled_curriculum_json


def set_sheet_information(scheduled_curriculum_json):
	uploaded = False

	# aftempt upload to gsheets

	return uploaded


parser = argparse.ArgumentParser(description="Create schedule")
parser.add_argument("google_creds", help="path to the google json api key")
parser.add_argument("sheet_id", help="google sheet id")
args = parser.parse_args()
google_creds = args.google_creds
sheet_id = args.sheet_id

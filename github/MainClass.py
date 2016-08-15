# This script is used to call Github API to get github status via CLI

import os
import configparser
import sys
import http.client
import urllib
import json
import getopt

CONFIG_FILE = os.environ["SCRIPT_PATH"] + "/../githubConf.conf"
ACCOUNT_SECTION = "account"
TOKEN_OPTION = "token"
BASE_URL = "api.github.com"
DECODE_TYPE = "utf-8"

REPO_URL = "/user/repos"
NOTI_URL = "/notifications"

HELP_MESSAGE = """
usage: githubapi [-h, --help] [-r, --repo]

This is used to acquire details from github via CLI.

optional arguments:
-h, --help                 get detailed help usage messages        
-r, --repo				   list all repositories in github
-n, --notification         list number of types for notifications in github
"""

def usage(exit_code):
	print(HELP_MESSAGE)

def load_properties(config_file):
	cf = configparser.ConfigParser()
	cf.read(config_file)
	
	return cf

def request_json(request_url, connection, headers):	
	parameters = None

	connection.request("GET", request_url, parameters, headers)
	response = connection.getresponse()

	output = response.read().decode(DECODE_TYPE)
	json_output = json.loads(output) 
	return json_output

def main(argv):
	cf = load_properties(CONFIG_FILE)
	token = cf.get(ACCOUNT_SECTION, TOKEN_OPTION)

	cnx = http.client.HTTPSConnection(BASE_URL)
	headers = {"Accept": "application/vnd.github.v3+json",
			   "User-Agent": "lovexi",
			   "Authorization": "token %s" % token}
	try:
		opts, args = getopt.getopt(argv, "hrn", ["help", "repo", "notification"])
	except getopt.GetoptError:
		usage(1)

	for opt, arg in opts:
		if opt in ["-h", "--help"]:
			print(HELP_MESSAGE)
		if opt in ["-r", "--repo"]:
			output = request_json(REPO_URL, cnx, headers)
			print("All repos are listed as following:")
			for repo in output:
				repo_name = repo["full_name"]
				print(repo_name[repo_name.find("/") + 1 :])
		if opt in ["-n", "--notification"]:
			output = request_json(NOTI_URL, cnx, headers)
			print("All notifications are listed as following:")
			noti_reasons = {"subscribed": 0,
							"manual": 0,
							"author": 0,
							"comment": 0,
							"mention": 0,
							"team_mention": 0,
							"state_change": 0,
							"assign": 0}
			for noti in output:
				noti_reasons[noti["reason"]] += 1
			for reason in noti_reasons:
				print("Total number for %s notification is %s" % (reason, noti_reasons[reason]))

if __name__ == "__main__":
	main(sys.argv[1:])


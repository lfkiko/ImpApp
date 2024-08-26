import os
import sys

import pyperclip

from Scripts.payload import payload_json
from Scripts.toolBoox import startLog, endLog


def run_payload_json():
	return payload_json.py


def getType(widgetType):
	if widgetType == "Inbox":
		return "GET_INBOX_INSIGHTS"
	elif widgetType in ["story-widget", "story", "recap"]:
		return "GET_INSIGHT_DETAILS"
	else:
		return "GET_INSIGHTS"


def main(argv):
	startLog()
	widgetType = argv[0]
	language = argv[1]
	remoteAssetBool = "true" if argv[2] else "false"
	remoteAssetUrl = argv[3]
	darkMode = "true" if argv[4] else "false"
	json = argv[5]
	apiType = getType(widgetType)
	internationalization = "\"internationalization\":{\"language\": \"" + language + "\"}"
	assets = "\"assets\":{\"useRemoteAssets\":" + remoteAssetBool + ",\"baseUrl\": \"" + remoteAssetUrl + "\"}"
	theme = "\"theme\": {\"darkMode\":" + darkMode + "  }"
	configurations = "\"configurations\": {\"deviceType\": \"web\",\"widgetType\": \"" + widgetType + "\",\"selectorString\": \"#root\",\"params\": {\"payload\": {\"" + apiType + "\": " + json + "}}}"
	payloadString = "window.personetics.startWidget({" + internationalization + "," + assets + "," + theme + "," + configurations + "});"
	pyperclip.copy(payloadString)

	# print(internationalization+"\n\n")
	# print(assets+"\n\n")
	# print(theme+"\n\n")
	# print(configurations+"\n\n")
	# print(payloadString)
	endLog()


if __name__ == "__main__":
	main(sys.argv[1:])

# veriabels:
# 0 - widget Type
# 1 - language
# 2 - Remote Assets Activation
# 3 - Remote Assets Url
# 4 - dark Mode
# 5 - Json file

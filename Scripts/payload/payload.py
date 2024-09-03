import os
import sys

import pyperclip
import Scripts.toolBoox as Tool


def getType(widgetType):
	if widgetType == "Inbox":
		return "GET_INBOX_INSIGHTS"
	elif widgetType in ["story-widget", "story", "recap"]:
		return "GET_INSIGHT_DETAILS"
	else:
		return "GET_INSIGHTS"


def main(argv):
	Tool.startLog()
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
	configurations = "\"configurations\": {\"deviceType\": \"web\",\"widgetType\": \"" + widgetType
	params = "\",\"selectorString\": \"#root\",\"params\": {\"payload\": {\"" + apiType + "\": " + json + "}}}"
	part1 = internationalization + "," + assets + "," + theme
	payloadString = "window.personetics.startWidget({" + part1 + "," + configurations + params + "});"
	pyperclip.copy(payloadString)

	Tool.endLog()


if __name__ == "__main__":
	main(sys.argv[1:])

# veriabels:
# 0 - widget Type
# 1 - language
# 2 - Remote Assets Activation
# 3 - Remote Assets Url
# 4 - dark Mode
# 5 - Json file

import os
import sys

import Scripts.toolBoox as Tool


def main(argv):
	Tool.startLog()
	try:
		solution = Tool.getSolution(Tool.getPath('solution'))  # os.path.join(getSolution(getPath('solution')), 'Insights')
	except Exception as e:
		Tool.pathError(e)
		return
	channels = Tool.getChannels(solution)
	if len(channels) > 3:
		theChannel = Tool.chooseChanel(channels)
		try:
			solution = os.path.join(solution + theChannel, 'Insights')
		except Exception as e:
			Tool.pathError(e)
			return
	else:
		try:
			solution = os.path.join(Tool.getSolution(Tool.getPath('solution')), 'Insights')
		except Exception as e:
			Tool.pathError(e)
			return

	insights = os.listdir(solution)
	insights.remove("SEntities")

	for insight in insights:
		insight_path = os.path.join(solution, insight)
		if "V" in os.listdir(insight_path):
			pass
	pass


if __name__ == "__main__":
	main(sys.argv[1:])

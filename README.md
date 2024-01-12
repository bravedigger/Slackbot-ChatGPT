Please follow the guide over here to setup a Slack app:
https://www.pragnakalp.com/create-slack-bot-using-python-tutorial-with-examples/

Also, the official Slack website for developing app:
https://api.slack.com/start/building/bolt-python

After you have created the app, please fill out the information in .env file:
SLACK_TOKEN = "your slack token"
SIGNING_SECRET = "your slack signing secret"
OPENAI_KEY = "openai key for chatgpt"
SLACK_MEMBER_ID = "U05RV32M8ER"

Then run the bot with $python3 slackbot.py

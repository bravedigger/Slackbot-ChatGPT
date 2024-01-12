import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
import os
from dotenv import load_dotenv
import openai
import queue

#followed this link to build the bot app
#https://www.pragnakalp.com/create-slack-bot-using-python-tutorial-with-examples/

load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SIGNING_SECRET = os.getenv('SIGNING_SECRET')
MAX_QUEUE_SIZE = int(os.getenv('MAX_QUEUE_SIZE'))
OPENAI_KEY = os.getenv('OPENAI_KEY')
SLACK_MEMBER_ID = os.getenv('SLACK_MEMBER_ID')
BOT_NAME = os.getenv('BOT_NAME')

# Set up the OpenAI API client
openai.api_key = OPENAI_KEY

conversations = queue.Queue()

msg_id_queue = queue.Queue()

def check_msg_id(msg_id):
    for x in range(int(msg_id_queue.qsize())):
        if(msg_id_queue.queue[x] == msg_id):
            return True
        
    msg_id_queue.put(msg_id)

    if(msg_id_queue.qsize() > 20):
        msg_id_queue.get()

    return False

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
 
client = slack.WebClient(token=SLACK_TOKEN)
#client.chat_postMessage(channel='#weebott',text='Hello, I am back online')

#the message got from Slack
#{'token': 'CnFOkN2HhnhyEroHxXAlrlbF', 
# 'team_id': 'T04S0AXEHT8', 
# 'context_team_id': 'T04S0AXEHT8', 
# 'context_enterprise_id': None, 
# 'api_app_id': 'A04SZQEJ23S', 
# 'event': {
#           'client_msg_id': 'e2333e2f-9f7d-4927-b08a-0a46e9ecd6db', 
#           'type': 'message', 
#           'text': 'hi', 
#           'user': 'U04S6URKAQ2', 
#           'ts': '1677868617.919749', 
#           'blocks': [{'type': 'rich_text', 'block_id': 'j74', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'hi'}]}]}], 
#           'team': 'T04S0AXEHT8', 
#           'channel': 'C04S0BCBW78', 
#           'event_ts': '1677868617.919749', 
#           'channel_type': 'channel'}, 
# 'type': 'event_callback', 
# 'event_id': 'Ev04SAQASCMR', 
# 'event_time': 1677868617, 
# 'authorizations': [{
#           'enterprise_id': None, 
#           'team_id': 'T04S0AXEHT8', 
#           'user_id': 'U04RVL1M3RD', 
#           'is_bot': True, 
#           'is_enterprise_install': False}],
#  'is_ext_shared_channel': False, 
#  'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDRTMEFYRUhUOCIsImFpZCI6IkEwNFNaUUVKMjNTIiwiY2lkIjoiQzA0UzBCQ0JXNzgifQ'
#  }
#
#3.239.252.135 - - [03/Mar/2023 18:36:58] "POST /slack/events HTTP/1.1" 200 -
# The following the message robot sent
#{'token': 'CnFOkN2HhnhyEroHxXAlrlbF', 
# 'team_id': 'T04S0AXEHT8', 
# 'context_team_id': 'T04S0AXEHT8', 
# 'context_enterprise_id': None, 
# 'api_app_id': 'A04SZQEJ23S', 
# 'event': {
#           'bot_id': 'B04SNQWN3L1', 
#           'type': 'message', 
#           'text': 'Hello', 
#           'user': 'U04RVL1M3RD', 
#           'ts': '1677868618.820579', 
#           'app_id': 'A04SZQEJ23S', 
#           'blocks': [{
#                   'type': 'rich_text', 
#                   'block_id': 'g3Ktg', 
#                   'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'Hello'}]}]}], 
#           'team': 'T04S0AXEHT8', 
#           'bot_profile': {
#                   'id': 'B04SNQWN3L1', 
#                   'deleted': False, 
#                   'name': 'WeeBott', 
#                   'updated': 1677861795, 
#                   'app_id': 'A04SZQEJ23S', 
#                   'icons': {'image_36': 'https://a.slack-edge.com/80588/img/plugins/app/bot_36.png', 
#                   'image_48': 'https://a.slack-edge.com/80588/img/plugins/app/bot_48.png', 
#                   'image_72': 'https://a.slack-edge.com/80588/img/plugins/app/service_72.png'}, 
#                   'team_id': 'T04S0AXEHT8'
#                   }, 
#           'channel': 'C04S0BCBW78', 
#           'event_ts': '1677868618.820579', 
#           'channel_type': 'channel'
#           }, 
# 'type': 'event_callback', 
# 'event_id': 'Ev04S4AA68FQ', 
# 'event_time': 1677868618, 
# 'authorizations': [{
#           'enterprise_id': None, 
#           'team_id': 'T04S0AXEHT8', 
#           'user_id': 'U04RVL1M3RD', 
#           'is_bot': True, 
#           'is_enterprise_install': False}], 
# 'is_ext_shared_channel': False, 
# 'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDRTMEFYRUhUOCIsImFpZCI6IkEwNFNaUUVKMjNTIiwiY2lkIjoiQzA0UzBCQ0JXNzgifQ'}


# The following is a sample of @WeeBott message
#18.209.109.180 - - [03/Mar/2023 21:04:19] "POST /slack/events HTTP/1.1" 200 -
#{'token': 'CnFOkN2HhnhyEroHxXAlrlbF', 
# 'team_id': 'T04S0AXEHT8', 
# 'context_team_id': 'T04S0AXEHT8', 
# 'context_enterprise_id': None, 
# 'api_app_id': 'A04SZQEJ23S', 
# 'event': {
#           'client_msg_id': 'b389d2ea-2fc6-41cf-bf5d-872b9fbe5149', 
#           'type': 'message', 
#           'text': '<@U04RVL1M3RD> hi', 
#           'user': 'U04S6URKAQ2', 
#           'ts': '1677877491.791929', 
#           'blocks': [{'type': 'rich_text', 
#                       'block_id': 'kkeDv', 
#                       'elements': [{
#                                   'type': 'rich_text_section', 
#                                   'elements': [{'type': 'user', 'user_id': 'U04RVL1M3RD'}, 
#                                               {'type': 'text', 'text': ' hi'}]
#                                   }]
#                       }], 
#           'team': 'T04S0AXEHT8', 
#           'channel': 'C04S0BCBW78', 
#           'event_ts': '1677877491.791929', 
#           'channel_type': 'channel'
#           }, 
# 'type': 'event_callback', 
# 'event_id': 'Ev04S8QPCK53', 
# 'event_time': 1677877491, 
# 'authorizations': [{
#           'enterprise_id': None, 
#           'team_id': 
#           'T04S0AXEHT8', 
#           'user_id': 'U04RVL1M3RD', 
#           'is_bot': True, 
#           'is_enterprise_install': False}], 
# 'is_ext_shared_channel': False, 
# 'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDRTMEFYRUhUOCIsImFpZCI6IkEwNFNaUUVKMjNTIiwiY2lkIjoiQzA0UzBCQ0JXNzgifQ'}



@ slack_event_adapter.on('message')
def message(payload):
    #print(payload)

    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    client_msg_id = event.get('client_msg_id')

    print("client_msg_id: ", client_msg_id)
    text = event.get('text')

    mentioned = False

    #sample: <@U04RVL1M3RD> hi
    mention_str = "<@" + SLACK_MEMBER_ID + ">" 
    if(mention_str in text):
        mentioned = True

    new_msg = text
    pos = new_msg.find("<@")
    while pos >= 0:
        pos1 = new_msg.find(">")
        if(pos1 >=0):
            pos1 = pos1 + 1
            new_msg = new_msg[pos1:].strip()
        else:
            break
        
        pos = new_msg.find("<@")
    
    if(len(new_msg) == 0):
        return    
 
    #if text == "hi":
        #client.chat_postMessage(channel=channel_id, text="Hello")

    print("Incoming Message:",  new_msg, flush=True)
  
    # This specifies which GPT model to use, as there are several models available, each with different capabilities and performance characteristics.
    model_engine = "gpt-3.5-turbo"

    if new_msg.startswith("@"+BOT_NAME):
        new_msg = new_msg[8:]
        mentioned = True

    if new_msg.startswith(BOT_NAME):
        new_msg = new_msg[7:]
        mentioned = True

    #openapi_prompt = "Q:" + new_msg + "\nA:"    
    openapi_prompt = new_msg

    if mentioned:
        if check_msg_id(client_msg_id): #already processed
            return
    
    if mentioned:
        # Use the OpenAI API to generate a response to the message
        # Old OpenAI engine
        #response = openai.Completion.create(
        #engine="text-davinci-003",
        #prompt=openapi_prompt,
        #max_tokens=1024,
        #temperature=0.8,
        #top_p=1,
        #frequency_penalty=0.0,
        #presence_penalty=0.0,
        #timeout=20    
        #)

        #response = openai.Completion.create(
        #engine=model_engine, 
        #prompt=openapi_prompt, 
        #max_tokens=300,
        #n=1,
        #stop=None,
        #temperature=0.7  
        #)


        # to do, passing through the last 10 conversations
        # messages=[ {"role": "system", "content": "You are a helpful assistant."}, 
        # {"role": "user", "content": "Who won the world series in 2020?"}, 
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}, 
        # {"role": "user", "content": "Where was it played?"} ]

        #code like:
        messages = [
        #system message first, it helps set the behavior of the assistant
        {"role": "system", "content": "You are a helpful assistant."}, 
        ]
    
        #messages.append({"role":"user", "content": message},)
        #response = openai.ChatCompletion.create(...)
        #messages.append({"role":"assistant", "content": reply})    
    
        for x in range(int(conversations.qsize()/2)):
            messages.append({"role": "user", "content": conversations.queue[2*x]})
            messages.append({"role": "assistant", "content": conversations.queue[2*x + 1]})
    
    
        messages.append({"role": "user", "content": openapi_prompt})
    
        #print(messages, flush=True)

        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        #messages=[{"role": "user", "content": openapi_prompt}],
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
        timeout=20
        )
    
        #reply = response.choices[0].text.strip()
        reply = response.choices[0].message.content.strip()
    
        #print(response, flush=True)
        print(reply, flush=True)
    
        if(len(reply) == 0):
            client.chat_postMessage(channel=channel_id, text="Sorry I don't have an answer")
        else:
            # Send the response as a message
            # await message.channel.send(response.choices[0].text.strip())
            client.chat_postMessage(channel=channel_id, text=reply)

        #rebuild converstions
        conversations.put(openapi_prompt)
        conversations.put(reply)

        if(conversations.qsize() >= MAX_QUEUE_SIZE):
            conversations.get()
            conversations.get()

if __name__ == "__main__":
    #open firewall for TCP port 5000
    #sudo ufw allow 5000/tcp
    app.run(debug=True, host='0.0.0.0', port=5000)
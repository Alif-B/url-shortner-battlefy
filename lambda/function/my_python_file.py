import boto3
import random
import json
from boto3.dynamodb.conditions import Key, Attr
# from flask import Flask, redirect, url_for, render_template, request
from flask_lambda import FlaskLambda


app = FlaskLambda(__name__) 
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('battlefy-urls')


# Checking if the randomly generated link is already assigned to another link
def check_generated_link(link):
    response = table.query(KeyConditionExpression=Key('shortened').eq(link))
    print(response['Items'])
    print(response['Items'])

    if len(response['Items']) == 0:
        return False
    else:
        return True





#1 : POST Method Processing: Checking if the randomly generated short link exists in the database already
#                            If not, then it adds it to the database.
@app.route('/<link>', methods = ['POST'])
def shorten(link):
    new_link = '36fj93'

    while check_generated_link(new_link):
        chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        length = random.randint(5, 10)
        new_link = ''.join(random.choice(chars) for i in range(length))
        print(new_link)

    response = table.put_item(
        Item={
            'shortened': new_link,
            'original': link
        }
    )

    scan = table.scan(
        FilterExpression=Attr('original').eq(link)
    )
        
    if len(scan['Items']) == 0:
        return (
            json.dumps({"message": f"/{new_link}"}),
            200,
            {"Content-Type": "application/json"}
        )
    else:
        return (
            json.dumps({"message": f"{link} already exists! Shortened: /{scan['Items'][0]['shortened']}"}),
            400,
            {"Content-Type": "application/json"}
        )



# 2: GET Method Processing: Resolve the shortened link.
@app.route('/<link>', methods = ['GET'])
def resolve(link):
    response = table.query(KeyConditionExpression=Key('shortened').eq(link))

    if len(response['Items']) == 0:
        return (
            json.dumps({"message": f"{link} is not associated with an address"}),
            404,
            {"Content-Type": "application/json"}
        )

    else:
        return (
            json.dumps({"message": response['Items'][0]['original']}),
            302,
            {"Content-Type": "application/json"}
        )



# 3: Health Check Processing: Just sends a 200 OK responnse
@app.route('/healthcheck')
def healthcheck():
        return (
            json.dumps({"message": 'OK'}),
            200,
            {"Content-Type": "application/json"}
        )





















# def lambda_handler(event, context):

#     """ This function handles which functions AWS Lambda will run based on the parameters of the request """

#     action = event["queryStringParameters"]["action"]
#     link = event["queryStringParameters"]["link"]
#     responseSent = {}
#     responseSent['statusCode'] = 200
#     responseSent['headers'] = {"Access-Control-Allow-Origin" : "*"}
#     responseSent['headers']['Content-Type'] = "application/json"

#     if action == "shorten":
#         response = table.scan(
#             FilterExpression=Attr('original').eq(link)
#         )
        
#         if len(response['Items']) == 0:
#             shorten(link)
#             responseSent['body'] = "Link Shortened!"
#             print("Link Shortened!")
#         else:
#             responseSent['body'] = f"{link} already exists! Shortened: /{response['Items'][0]['shortened']}"
#             print(f"{link} already exists! Shortened: /{response['Items'][0]['shortened']}")

#     elif action == "lengthen":
#         response = table.query(KeyConditionExpression=Key('shortened').eq(link))

#         if len(response['Items']) == 0:
#             responseSent['body'] = f"{link} is not associated with an address"
#             print(f"{link} is not associated with an address")
#         else:
#             responseSent['body'] = f"{response['Items'][0]['original']}"
#             print(response['Items'][0]['original'])


# def main(event):
#     """ This function handles which functions AWS Lambda will run based on the parameters of the request """

#     action = event["queryStringParameters"]["action"]
#     link = event["queryStringParameters"]["link"]
#     responseSent = {}
#     responseSent['statusCode'] = 200
#     responseSent['headers'] = {"Access-Control-Allow-Origin" : "*"}
#     responseSent['headers']['Content-Type'] = "application/json"

#     if action == "shorten":
#         response = table.scan(
#             FilterExpression=Attr('original').eq(link)
#         )
        
#         if len(response['Items']) == 0:
#             shorten(link)
#             responseSent['body'] = "Link Shortened!"
#             print("Link Shortened!")
#         else:
#             responseSent['body'] = f"{link} already exists! Shortened: /{response['Items'][0]['shortened']}"
#             print(f"{link} already exists! Shortened: /{response['Items'][0]['shortened']}")

#     elif action == "lengthen":
#         response = table.query(KeyConditionExpression=Key('shortened').eq(link))

#         if len(response['Items']) == 0:
#             responseSent['body'] = f"{link} is not associated with an address"
#             print(f"{link} is not associated with an address")
#         else:
#             responseSent['body'] = f"{response['Items'][0]['original']}"
#             print(response['Items'][0]['original'])






# if __name__ == "__main__":
    # event = {
    #     "queryStringParameters" : {
    #         "action": "shorten",
    #         "link": "www.twitter.com",
    #     }
    # }

    # event = {
    #     "queryStringParameters" : {
    #         "action": "lengthen",
    #         "link": "dhkliuk63e"
    #     }
    # }

    # app.run(debug=True)

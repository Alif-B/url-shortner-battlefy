import boto3
import random
import json
from boto3.dynamodb.conditions import Key, Attr
from flask_lambda import FlaskLambda
from flask import redirect


app = FlaskLambda(__name__) 
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('battlefy-urls')




# Checking if the randomly generated link is already assigned to another link.
def check_generated_link(link):
    response = table.query(KeyConditionExpression=Key('shortened').eq(link))

    if len(response['Items']) == 0:
        return False
    else:
        return True





#1 : POST Method Processing: Checking if the randomly generated short link exists in the database already
#                            If not, then it adds it to the database.
@app.route('/<link>', methods = ['POST'])
def shorten(link):
    new_link = '36fj93'
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    scan = table.scan(FilterExpression=Attr('original').eq(link))


    if len(scan['Items']) == 0:
        while check_generated_link(new_link):
            length = random.randint(5, 10)
            new_link = ''.join(random.choice(chars) for i in range(length))

        response = table.put_item(
            Item={
                'shortened': new_link,
                'original': link
            }
        )

        return (
            json.dumps({"message": f"/{new_link}"}),
            200,
            {"Content-Type": "application/json"}
        )
    
    else:
        return (
            json.dumps({"message": f"{link} already exists in the database! Shortened: /{scan['Items'][0]['shortened']}"}),
            400,
            {"Content-Type": "application/json"}
        )





# 2: GET Method Processing: Resolve the shortened link and redirects the user to the resolved link.
@app.route('/<link>', methods = ['GET'])
def resolve(link):
    print(link)
    response = table.query(KeyConditionExpression=Key('shortened').eq(link))
    if len(response['Items']) == 0:
        print(response['Items'])
        return (
            json.dumps({"message": f"{link} is not associated with an addresss"}),
            404,
            {"Content-Type": "application/json"}
        )

    else:
        return redirect(f"http://{response['Items'][0]['original']}", code=302)





# 3: Health Check Processing: Just sends a 200 OK responnse.
@app.route('/healthcheck')
def healthcheck():
        return (
            json.dumps({"message": 'OK'}),
            200,
            {"Content-Type": "application/json"}
        )

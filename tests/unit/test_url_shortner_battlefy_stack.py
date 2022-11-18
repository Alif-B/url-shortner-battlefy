import aws_cdk as core
import aws_cdk.assertions as assertions

from url_shortner_battlefy.url_shortner_battlefy_stack import UrlShortnerBattlefyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in url_shortner_battlefy/url_shortner_battlefy_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = UrlShortnerBattlefyStack(app, "url-shortner-battlefy")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

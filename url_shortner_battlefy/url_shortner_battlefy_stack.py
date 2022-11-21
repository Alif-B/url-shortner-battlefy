from aws_cdk import Stack, CfnOutput, aws_lambda, aws_iam, aws_apigateway
from constructs import Construct

class UrlShortnerBattlefyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # Role and Permission Management
        my_role = aws_iam.Role(self, "battlefy-url-shortner-lambda",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com")
        )

        my_role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        my_role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
        my_role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))


        # Creating the Lambda Layer containing the dependencies
        layer = aws_lambda.LayerVersion(self, "BattlefyURLShortnerLayer2)",
            code=aws_lambda.Code.from_asset("lambda/ext_libraries.zip"),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_9],
            description="A layer 2 that contians the dependencies for Battlefy URL shortning app"
        )


        # Lambda Function creation
        url_shortner_function = aws_lambda.Function(
            self,
            id = "battlefy-url-shortner",
            code = aws_lambda.Code.from_asset("lambda/function"),
            handler = "url_shortner.app",
            runtime = aws_lambda.Runtime.PYTHON_3_9,
            role = my_role,
            layers=[layer]
        )



        # # Extracting the existing API Key
        # imported_key = aws_apigateway.ApiKey.from_api_key_id(self, "imported-key", "60yv7ede4j")

        # AWS API Gateway attached to the Lambda function as a trigger
        api = aws_apigateway.LambdaRestApi(self, "battlefy-url-shortner-apigw", handler=url_shortner_function, proxy=False)
        path = api.root.add_resource("{proxy+}")
        get = path.add_method("GET")
        post = path.add_method("POST", authorization_type=aws_apigateway.AuthorizationType.IAM)



        # Creating an admin group that can access the post method
        group = aws_iam.Group(self, "url-shortner-admins")
        group.attach_inline_policy(aws_iam.Policy(self, "AllowBooks",
            statements=[
                aws_iam.PolicyStatement(
                    actions=["execute-api:Invoke"],
                    effect=aws_iam.Effect.ALLOW,
                    resources=[post.method_arn]
                )
            ]
        ))


        CfnOutput(self, "API Endpoint", value=api.url)

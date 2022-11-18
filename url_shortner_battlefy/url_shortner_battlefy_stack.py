from aws_cdk import Stack, aws_lambda, aws_iam
from constructs import Construct

class UrlShortnerBattlefyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        my_role = aws_iam.Role(self, "battlefy-url-shortner-lambda",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com")
        )

        my_role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        my_role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
        my_role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))

        url_shortner_function = aws_lambda.Function(
            self,
            id = "battlefy-url-shortner",
            code = aws_lambda.Code.from_asset("lambda/function"),
            handler = "my_python_file.app",
            runtime = aws_lambda.Runtime.PYTHON_3_9,
            role = my_role
        )

        # function_url = url_shortner_function.add_function_url(
        #     auth_type=aws_lambda.FunctionUrlAuthType.NONE
        # )

        # CfnOutput(self, "TheUrl", value=fn_url.url)




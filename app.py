from aws_cdk import App, Environment

from infra.stack import Ec2InstanceStack
from parameters.from_environment import StackParameters

parameters = StackParameters()

app = App()
Ec2InstanceStack(
    app,
    construct_id=f"{parameters.prefix}-stack",
    prefix=parameters.prefix,
    ip_address=parameters.ip_address,
    ami=parameters.ami,
    instance_type=parameters.instance_type,
    env=Environment(account=parameters.account_id, region=parameters.aws_region),
)
app.synth()

from aws_cdk import CfnOutput, Environment, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct


class Ec2InstanceStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        prefix: str,
        ip_address: str,
        ami: str,
        instance_type: str,
        env: Environment,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)

        vpc = ec2.Vpc(
            self,
            f"{prefix}-vpc",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{prefix}-public-subnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
        )

        # Create security group that allows SSH from a specific IP.
        security_group = ec2.SecurityGroup(
            self,
            f"{prefix}-security-group",
            vpc=vpc,
            description="Allow ssh access to ec2 instances",
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            ec2.Peer.ipv4(cidr_ip=f"{ip_address}/32"),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access only",
        )

        cfn_key_pair = ec2.KeyPair(
            self,
            id=f"{prefix}-key-pair",
            key_pair_name=f"{prefix}-key",
        )

        role = iam.Role(
            self,
            f"{prefix}-ec2-role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonS3ReadOnlyAccess"
                ),
            ],
        )

        instance = ec2.Instance(
            self,
            f"{prefix}-instance",
            instance_type=ec2.InstanceType(instance_type),
            machine_image=ec2.MachineImage.generic_linux({env.region: ami}),
            vpc=vpc,
            security_group=security_group,
            associate_public_ip_address=True,
            key_pair=cfn_key_pair,
            require_imdsv2=True,
            role=role,
        )

        CfnOutput(self, "InstanceId", value=instance.instance_id)

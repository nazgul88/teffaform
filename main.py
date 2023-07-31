import boto3
import json
import csv
from pprint import pprint

client = boto3.client('ec2')

response = client.describe_subnets(MaxResults=1000)

subnets = []

fields = {"body": [
    "SubnetId",
    "VpcId",
    "CidrBlock",
    "AvailableIpAddressCount"
],
    "tags": [
    "Name",
]
}

for subnet in response["Subnets"]:
    temp = {}
    for field in fields["body"]:
        temp[field] = subnet.get(field, None)
    if "Tags" in subnet:
        tags = {tag["Key"]: tag["Value"] for tag in subnet["Tags"]}
        for field in fields["tags"]:
            temp[field] = tags.get(field, None)
    subnets.append(temp)

with open('subnets.csv', 'w', newline='') as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=[
                            *fields["body"], *fields["tags"]])

    writer.writeheader()
    writer.writerows(subnets)

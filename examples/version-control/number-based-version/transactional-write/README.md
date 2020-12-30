# How to implement version control using Amazon DynamoDB

Please read this blog post for detailed description about how to design and implement time-based and number-based version using Amazon DynamoDB. https://aws.amazon.com/blogs/database/implementing-version-control-using-amazon-dynamodb/


## Deployment

First and foremost, you need a S3 bucket where you can upload the Lambda functions packaged as ZIP before you deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```

Now build your Lambda function

```bash
sam build
```

Provided you have a S3 bucket created, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name number-based-transactional-write-version-control \
    --capabilities CAPABILITY_IAM
```

> **See [Serverless Application Model (SAM) HOW TO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**


## Usage

First, run **NumberBased-TransactionalWrite-AddEquipment** function with this test event:

```json
{
  "ID": "Equipment#1",
  "Name": "EquipmentName",
  "FactoryID": "F#12345",
  "LineID": "L#12345"
}
```

Next, use the below test event for running **NumberBased-TransactionalWrite-AddNewVersion** function. Add as many versions as you want for an equipment, by changing the test event:

```json
{
  "ID": "Equipment#1",
  "State": "WARNING1",
  "Time": "2020-11-10T09:00:00"
}
```

Then, to retrieve the latest version, run **NumberBased-TransactionalWrite-GetLatestVersion** function with the following test event:

```json
{
  "ID": "Equipment#1"
}
```

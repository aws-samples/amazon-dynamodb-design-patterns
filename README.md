# Amazon DynamoDB Design Patterns

This repo contains sample data models to demonstrate design patterns for Amazon DynamoDB.

## Data Models

The data model for each of the use cases below is built step by step, and the data model for each step is provided in `json` format that can be imported to NoSQL Workbench for Amazon DynamoDB.

Sample data models are listed under `/data-models` folder.
- Device State Log - [*Introductory*]
- An Online Shop - [*Advanced*]


## NoSQL Design

When designing a data model for Amazon DynamoDB, it is important to understand the use case and requirements, and then identify entities and the relationships between them. One way to illustrate the relations is to draw an Entity Relation Diagram (ERD). It is also recommended to identify the access patterns needed to fulfill the requirements up front and then go through them one by one to store data in such format that the access pattern can be handled. 

It is a good practice to use [NoSQL Workbench for Amazon DynamoDB](#nosql-workbench-for-amazon-dynamodb) when designing and reviewing the data model for an application. Once the data model is completed, the next step is to review and apply any improvements to the data model. A good design is achieved after multiple review iterations.

In general, maintain as few tables as possible in an Amazon DynamoDB application, and if it suits the use case then store all the entities in a single table. By overloading a table with several entities, the number of network round trips from the application to Amazon DynamoDB can be reduced as each item collection can contain relations between several entities and can be retrieved in one query operation. Item collection refers to item(s) that have the same partition key. It is also a common pattern to overload global secondary indexes (GSI) to handle access patterns that can not be addressed by the table.

## NoSQL Workbench for Amazon DynamoDB
 
[NoSQL Workbench for Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html) is a cross-platform client-side GUI application for modern database development and operations. NoSQL Workbench is available for Windows, macOS, and Linux. 

The data model including table(s), global secondary indexes and any data populated in the table(s) can be exported in `json` format. This file can be shared within a team and can of course be added to a version control tool in order to keep track of different review versions. The data model can be committed to Amazon DynamoDB in an AWS account or to DynamoDB Local from NoSQL Workbench.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.

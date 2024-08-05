# Question Engine Service

### Local setup:
* Install local DynamoDB engine by following installation steps specified here https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html
* Run local dynamodb like this: dynamodb-local -sharedDb
* Use http://localhost:8000/shell/ to create Dynamo DB table with the following query:


```javascript
var params = {
    TableName: 'local-question-engine-user-answer',
    KeySchema: [ // The type of of schema.  Must start with a HASH type, with an optional second RANGE.
        { // Required HASH type attribute
            AttributeName: 'quizId',
            KeyType: 'HASH',
        },
        { // Optional RANGE key type for HASH + RANGE tables
            AttributeName: 'username', 
            KeyType: 'RANGE', 
        }
    ],
    AttributeDefinitions: [ // The names and types of all primary and index key attributes only
        {
            AttributeName: 'username',
            AttributeType: 'S'
        },
        {
            AttributeName: 'quizId',
            AttributeType: 'S'
        },
        {
            AttributeName: 'sourceId',
            AttributeType: 'S', // (S | N | B) for string, number, binary
        },
        {
            AttributeName: 'usernameSourceId',
            AttributeType: 'S', // (S | N | B) for string, number, binary
        },
        {
            AttributeName: 'createdDate',
            AttributeType: 'N', // (S | N | B) for string, number, binary
        },
        
        // ... more attributes ...
    ],
    ProvisionedThroughput: { // required provisioned throughput for the table
        ReadCapacityUnits: 10, 
        WriteCapacityUnits: 10, 
    },
    GlobalSecondaryIndexes: [ // optional (list of GlobalSecondaryIndex)
        { 
            IndexName: 'UsernameSourceIdGlobalIndex', 
            KeySchema: [
                { // Required HASH type attribute
                    AttributeName: 'usernameSourceId',
                    KeyType: 'HASH',
                },
                { // Optional RANGE key type for HASH + RANGE secondary indexes
                    AttributeName: 'createdDate', 
                    KeyType: 'RANGE', 
                }
            ],
            Projection: { // attributes to project into the index
                ProjectionType: 'ALL', // (ALL | KEYS_ONLY | INCLUDE)
            },
            ProvisionedThroughput: { // throughput to provision to the index
                ReadCapacityUnits: 1,
                WriteCapacityUnits: 1,
            },
        },
        // ... more global secondary indexes ...
    ],
    LocalSecondaryIndexes: [ // optional (list of LocalSecondaryIndex)
        { 
            IndexName: 'CreatedDateLocalIndex',
            KeySchema: [ 
                { // Required HASH type attribute - must match the table's HASH key attribute name
                    AttributeName: 'quizId',
                    KeyType: 'HASH',
                },
                { // alternate RANGE key attribute for the secondary index
                    AttributeName: 'createdDate', 
                    KeyType: 'RANGE', 
                }
            ],
            Projection: { // required
                ProjectionType: 'ALL', // (ALL | KEYS_ONLY | INCLUDE)
            },
        },
        // ... more local secondary indexes ...
    ],
};
dynamodb.createTable(params, function(err, data) {
    if (err) ppJson(err); // an error occurred
    else ppJson(data); // successful response

});
```


* Run `com.ladbrokescoral.oxygen.questionengine.Application` with IntelliJ IDEA or
 `./gradlew bootRun`

* To build run `./gradlew clean build`

### ! Important
* You changes could **only** be applied trough Pull Request (PR)
* Please ensure that **build passes** before creating PR
* Please ensure that you picked **Fast Forward** merge strategy once you're merging your feature branch into **develop**.

/**
 * replaces creator and/or updater with ObjectId
 */

db = db.getSiblingDB('bma');

var collectionNames = db.getCollectionNames();
collectionNames.forEach(function (value) {
    print("Updating " + value)
    db[value].update(
        {
            "$or": [
                {"createdBy": "test.admin@coral.co.uk"},
                {"updatedBy": "test.admin@coral.co.uk"}
            ]
        },
        {
            "$set": {
                "createdBy": ObjectId("5a6aec27c9e77c00013749b7"),
                "updatedBy": ObjectId("5a6aec27c9e77c00013749b7")
            }
        },
        {
            multi: true // update all documents that matched criteria
        });
});

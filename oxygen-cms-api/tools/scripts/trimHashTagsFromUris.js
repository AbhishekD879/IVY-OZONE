/**
 * Scripts goes through all collections in "bma" db and
 * searches for fields which have "/#/" inside or "#/ at the beginning.
 *
 * Updates all of the matched fields by stripping hash (see {@link stripHashtag}
 */

db = db.getSiblingDB('bma');

var res = {};
var collectionNames = db.getCollectionNames();

function hashShouldBeStripped(value) {
    return (value.match(/\/#\//) || value.match(/^#\//)) && !value.match(/</);
}

//strips "/#/" from string by replacing it with a single "/"
// and strips "#/" by replcing it with "/" if it is at the start of the string
// for ex.:
// "https://bet.coral.co.uk/#/americanfootball/event/7534337" -> "https://bet.coral.co.uk/americanfootball/event/7534337"
// "#/home/football" -> "/home/football"
function stripHashtag(original) {
    return original.replace(/\/#\//, "/").replace(/^#\//, "/")
}

// goes through all fields of all collections to find candidates for update (stripping hashtag).
// result is stored in "res" object
collectionNames.forEach(function (col) {
    var currentCursor = db[col].find();

    currentCursor.forEach(function (item) {

        // If the item is null then the cursor is exhausted/empty and closed
        if (item == null) {

            // Show that the cursor is closed
            currentCursor.toArray(function (err, items) {
                assert.ok(err != null);

                // Let's close the db
                db.close();
            });
        } else {
            for (var key in item) {
                var value = item[key];
                if (value != null && typeof value.match === "function")
                    if (hashShouldBeStripped(value)) {
                        // print(key + "=" + value)
                        if (!res[col]) {
                            res[col] = []
                        }
                        var newItem = {}
                        newItem.id = item["_id"]
                        newItem.fieldName = key
                        newItem.oldFieldValue = value
                        newItem.newFieldValue = stripHashtag(value)

                        res[col].push(newItem)
                    }
            }
        }
    });
})

/**
 * Executes update operation by setting {@param field} to {@param value}
 * for document with id = {@param id} in collection {@param collection}
 */
function doUpdate(collection, id, field, value) {
    var setJson = {};
    setJson[field] = value;

    var writeResult = db[collection].update(
        {
            "_id": id
        },
        {
            $set: setJson
        }
    );

    if (writeResult["nModified"] > 0) {
        print("Updated " + col + "[" + record.id + "]" + "."
            + record.fieldName + " (" + record.oldFieldValue + " -> " + record.newFieldValue + ")")

    } else {
        print("Not updated " + id + ". wr = " + writeResult + ". " + field)
    }
}

//updates all found entries
for (var col in res) {
    if (col) {
        for (var recordIdx in res[col]) {
            var record = res[col][recordIdx]
            doUpdate(col, record.id, record.fieldName, record.newFieldValue);
        }
    }
}

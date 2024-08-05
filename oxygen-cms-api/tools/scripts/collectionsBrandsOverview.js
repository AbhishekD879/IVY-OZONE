//NOTE collections overview - check if there are 'brand' properties
var logVar = "";
function log(message) {
    logVar = logVar + '\n' + message;
}

var hierarchyMenus = [];
var all =[];
var hasBrand = [];
//level could be 1 or 2
var collectionNames = db.getCollectionNames();
for(i in collectionNames) {
    var collectionName = collectionNames[i];
    all.push(collectionName)
    var hierarchyElement = db.getCollection(collectionName).findOne({"level" : {$exists : true}});
    if(hierarchyElement) {
        hierarchyMenus.push(collectionName);
    }
    var brandElement = db.getCollection(collectionName).findOne({"brand" : {$exists : true}});
    if(brandElement) {
        hasBrand.push(collectionName);
    }
}

var noBrand = [];
noBrand = collectionNames.filter( (el) => !hasBrand.includes(el));

log("Whole Collection:");
log(collectionNames.join());
log("With hierarchy:");
log(hierarchyMenus.join());
log("With brand:");
log(hasBrand.join());
log("Without brand:");
log(noBrand.join());

print(logVar);

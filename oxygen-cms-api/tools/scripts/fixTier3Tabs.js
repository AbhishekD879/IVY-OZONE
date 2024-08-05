var categoriesToUpdate = [42];

var log = [];
var allowedTabs = ["matches", "coupons", "outrights"];
var tabTemplates = {
    "matches" : {
        "name" : "matches",
        "displayName" : "Events",
        "sortOrder" : 1.0
    },
    "coupons" : {
        "name" : "coupons",
        "displayName" : "Coupons",
        "sortOrder" : 2.0
    },
    "outrights" : {
        "name" : "outrights",
        "displayName" : "Outrights",
        "sortOrder" : 3.0
    }
};

var docTemplate = {
    "_class" : "com.ladbrokescoral.oxygen.cms.api.entity.SportTab",
    "brand" : "ladbrokes",
    "enabled" : true,
    "checkEvents" : true,
    "hasEvents" : false,
    "createdBy" : "5cde7ee5c9e77c0001d68756",
    "updatedBy" : "5cde7ee5c9e77c0001d68756"
};


for(i in categoriesToUpdate) {
    var existingTabs = [];
    var sportId = NumberInt(categoriesToUpdate[i]);
    log.push("sportId " + sportId)
    db.getCollection('sporttabs')
        .find({"brand" : "ladbrokes", "sportId" : sportId}, {"name" : 1, "_id" : 0})
        .forEach(function(value) {
            existingTabs.push(value.name);
        });

    for(j in existingTabs) {
        if(allowedTabs.indexOf(existingTabs[j]) < 0) {
            var result = db.getCollection('sporttabs')
                .remove({'brand' : 'ladbrokes', 'sportId' : sportId, 'name' : existingTabs[j]});
            log.push("Removed " + result.nRemoved + " " + existingTabs[j] + " from " + sportId);
        }
    }
    for(k in allowedTabs) {
        if(existingTabs.indexOf(allowedTabs[k]) < 0) {
            var newTab = Object.assign({}, docTemplate);
            newTab["sportId"] = sportId;
            newTab = Object.assign(newTab, tabTemplates[allowedTabs[k]]);
            var result = db.getCollection('sporttabs').insert(newTab);
            log.push("Inserted " + result.nInserted + " " + allowedTabs[k] + " to " + sportId);
//          log.push(newTab);
        }
    }
};
print(log);

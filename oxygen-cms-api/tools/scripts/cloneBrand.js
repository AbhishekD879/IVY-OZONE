//NOTE copy bma to %newBrand%
// script will create exact copies of existing documents from collections with `brand` properties

var newBrand = "vanilla";
var oldBrand = "bma";

var newBrandDash = "-" + newBrand;
var oldBrandDash = "-" + oldBrand;

var brandLikeProperties = ["imageTitle_brand", "title_brand", "linkTitle_brand", "url_brand", "type_brand"];

var globalCounter = 0;
var logVar = "";
function log(message) {
    logVar = logVar + '\n' + message;
}

function updateDoc(element) {
    delete element["_id"];
    element["brand"] = newBrand;
    return element;
}

function updateBrandLikeProperties(element) {
    brandLikeProperties.forEach(function(e,i) {
        if(element[e]) {
            element[e] = element[e].replace(oldBrandDash, newBrandDash);
        }
    });
    return element;
}

function getParentId(doc) {
    if(!doc['parent'].str) {
        return doc['parent'];
    }
    return doc['parent'].str;
}

//covers all (except for 'specialCase') collections that have 'brand' property
var hasBrand = ['bankingmenus', 'bottommenus', 'brandMenu', 'bybMarkets', 'bybSwitchers',
    'bybTabAvailability', 'competition', 'configs', 'connectmenus', 'countries', 'couponmarketselectors', 'coupons', 'desktop quicklinks', 'edpmarkets',
    'eventhubs', 'externallinks', 'features', 'football3dbanners', 'footerlogos', 'footermenus', 'games', 'header-submenus',
    'headercontactmenus', 'headermenus', 'highlightCarousel', 'hr quicklinks', 'leftmenus', 'ln quicklinks', 'maintenancepages', 'moduleribbontabs',
    'navigationPoint', 'onBoardingGuides', 'otf-ios-app-toggle', 'payment-methods',
    'qualification-rule', 'quicklinks', 'quiz', 'renderconfig', 'rightmenus', 'seopages', 'splashPage', 'sportmodules',
    'sportquicklinks', 'sports', 'sporttabs', 'ssopages', 'static-text-otf', 'staticblocks', 'streamAndBet', 'structures', 'surfaceBet', 'teamKits',
    'topgames', 'topmenus', 'usermenus', 'widgets', 'ycleagues', 'ycmarkets', 'ycstaticblocks'];

//fully intersects in hasBrand
var hasBrandLikeKeys = ['bankingmenus', 'banners', 'bottommenus', 'connectmenus', 'features', 'footermenus', 'footermenus', 'header-submenus', 'headercontactmenus',
    'headermenus', 'leftmenus', 'moduleribbontabs', 'promotions', 'rightmenus', 'seopages', 'ssopages', 'staticblocks', 'usermenus', 'widgets', 'ycstaticblocks'];
//fully intersects in hasBrandLikeKeys, docs in those collections could have links to docs in another collections
var hierarchyMenus = ['connectmenus', 'headermenus', 'leftmenus'];

//not used - there will be no updates for those
var noBrand = ['app_updates', 'brands', 'competitionModule', 'competitionParticipant', 'competitionSubTab', 'competitionTab', 'dashboards',
    'dbchangelog', 'galleries', 'homemodules', 'homepage', 'indexnumbers', 'mainmenus', 'menucategories', 'moduleribbons', 'mongobeelock',
    'postcategories', 'posts', 'sportsfeaturedtab', 'users'];

//not used - docs from those collections could refer by id to another collections (some of those, are the `source` ,e.g. sportcategories)
var specialCase = ['sportcategories', 'banners', 'betreceiptbanners', 'betreceiptbannertablets', 'leagues', 'promotion', 'promotionSection', 'featuredeventstypes',
    'odds-boost-configuration', 'offers', 'offermodules'];

function main() {
    var simpleCopyCollections = [];
    simpleCopyCollections = hasBrand.filter((el) => !hasBrandLikeKeys.includes(el));

    var brandLikeCollections = [];
    brandLikeCollections = hasBrandLikeKeys.filter((el) => !hierarchyMenus.includes(el));

// log("Simple:");
// log(simpleCopyCollections.join());
// log("With brand like:");
// log(brandLikeCollections.join());
// log("Hierarchy:");
// log(hierarchyMenus.join());

// Copiing batches of elements
    for(i in hasBrand) {
        var collectionName = hasBrand[i];
        var newBrandDoc = db.getCollection(collectionName).findOne({'brand' : newBrand});
        if(!newBrandDoc) {
            var originalDocs = db.getCollection(collectionName).find({'brand' : oldBrand});
            if(originalDocs.size() > 0) {
//         =====================================
                if(hierarchyMenus.indexOf(collectionName) > -1) {
                    copyHierarchyMenus(originalDocs, collectionName);
                } else if (brandLikeCollections.indexOf(collectionName) > -1) {
                    copyBrandLikeCollection(originalDocs, collectionName);
                } else {
                    copySimpleCollection(originalDocs, collectionName);
                }
//          ====================================
            } else {
                log('Collection ' + collectionName + ' currently has no docs by brand ' + oldBrand);
            }
        } else {
            log('[ERROR] collection ' + collectionName + ' already has doc(s) of brand ' + newBrand + ' in order to avoid duplications, skipping cloning.');
        }
    }

    specialCase0();
    specialCase1();
    specialCase2();
    specialCase3();
    specialCase4();
    specialCase5();
//
    log('Total inserted: ' + globalCounter);
}

function copySimpleCollection(originalDocs, collectionName) {
    var batchUpdate = [];
    originalDocs.forEach(function(e,i) {
        e = updateDoc(e);
        batchUpdate.push(e);
    });
    var result = db.getCollection(collectionName).insert(batchUpdate);
    log('Inserting docs in ' + collectionName + ', prepared/successfull: ' + batchUpdate.length + '/' + result['nInserted']);
    globalCounter+=result['nInserted'];
}

function copyBrandLikeCollection(originalDocs, collectionName) {
    var batchUpdate = [];
    originalDocs.forEach(function(e,i) {
        e = updateDoc(e);
        e = updateBrandLikeProperties(e);
        batchUpdate.push(e);
    });
    var result = db.getCollection(collectionName).insert(batchUpdate);
    log('Inserting docs in ' + collectionName + ', prepared/successfull: ' + batchUpdate.length + '/' + result['nInserted']);
    globalCounter+=result['nInserted'];
}

function copyHierarchyMenus(originalDocs, collectionName) {
    var level1Docs = [];
    var level2Docs = [];
    originalDocs.forEach(function(e,i) {
        if (e['level'] == '1') {
            level1Docs.push(e);
        } else if(e['level'] == '2') {
            level2Docs.push(e);
        }
    });

    var batchUpdate = [];
    var idMap={};
    level1Docs.forEach(function(e,i) {
        var oldIdStr = e['_id'].str;
        e = updateDoc(e);
        e = updateBrandLikeProperties(e);
        var newId = new ObjectId();
        e['_id'] = newId;
        idMap[oldIdStr] = newId.str;
        batchUpdate.push(e);
    });
    level2Docs.forEach(function(e,i) {
        e = updateDoc(e);
        e = updateBrandLikeProperties(e);
        e['parent'] = idMap[getParentId(e)];
        batchUpdate.push(e);
    });
    var result = db.getCollection(collectionName).insert(batchUpdate);
    log('Inserting docs in ' + collectionName + ', prepared/successfull: ' + batchUpdate.length + '/' + result['nInserted']);
    globalCounter+=result['nInserted'];
}

var sportCategoryIdMap={};
//banners[categoryId] ->sportcategories
function specialCase0() {
    var sportСategories = 'sportcategories';
    var banner = 'banners';
    var batchUpdate = [];
    var sportDocs = db.getCollection(sportСategories).find({'brand' : oldBrand});
    sportDocs.forEach(function(e,i) {
        var oldId = e['_id'];
        e = updateDoc(e);
        var newId = new ObjectId();
        e['_id'] = newId;
        sportCategoryIdMap[oldId] = newId;
        batchUpdate.push(e);
    });
    performInsert(sportСategories, batchUpdate);
    batchUpdate = [];
//     and now, time for banners
    var bannerDocs = db.getCollection(banner).find({'brand' : oldBrand});
    bannerDocs.forEach(function(e,i){
        e = updateDoc(e);
        e['imageTitle_brand'] = e['imageTitle_brand'] + newBrandDash;
        if(sportCategoryIdMap[e['categoryId']]) {
            e['categoryId'] = sportCategoryIdMap[e['categoryId']];
        }
        batchUpdate.push(e);
    });
    performInsert(banner, batchUpdate);
}
//leagues[banner] & leagues[tabletBanner] -> betreceiptbanners & betreceiptbannertablets
function specialCase1() {
    var leagues = 'leagues';
    var banner = 'betreceiptbanners';
    var tabletBanner = 'betreceiptbannertablets';
    var batchUpdate = [];
    var bannerIdMap = {};
    var tabletBannerIdMap = {};

    var bannerDocs = db.getCollection(banner).find({'brand' : oldBrand});
    bannerDocs.forEach(function(e,i) {
        var oldId = e['_id'];
        e = updateDoc(e);
        var newId = new ObjectId();
        e['_id'] = newId;
        bannerIdMap[oldId.str] = newId.str;
        batchUpdate.push(e);
    });
    performInsert(banner, batchUpdate);
    batchUpdate = [];

    var tabletBannerDocs = db.getCollection(tabletBanner).find({'brand' : oldBrand});
    tabletBannerDocs.forEach(function(e,i){
        var oldId = e['_id'];
        e = updateDoc(e);
        var newId = new ObjectId();
        e['_id'] = newId;
        tabletBannerIdMap[oldId.str] = newId.str;
        batchUpdate.push(e);
    });
    performInsert(tabletBanner, batchUpdate);
    batchUpdate = [];
    var leaguesDocs = db.getCollection(leagues).find({'brand' : oldBrand});
    leaguesDocs.forEach(function(e,i) {
        e = updateDoc(e);
        if(e['banner']) {
            e['banner'] = bannerIdMap[e['banner']];
        }
        if(e['tabletBanner']) {
            e['tabletBanner'] = tabletBannerIdMap[e['tabletBanner']];
        }
        batchUpdate.push(e);
    });
    performInsert(leagues, batchUpdate);
}
//promotionSection[_id:bma, unassignedPromotionIds] ->promotions[categoryId] -> sportCategories
function specialCase2() {
    var promotions = 'promotions';
    var promotionSection = 'promotionSection';
    var batchUpdate = [];

    var promotionIdMap = {};
    var promotionDocs = db.getCollection('promotions').find({'brand' : oldBrand});
    promotionDocs.forEach(function(e,i){
        var oldId = e['_id'];
        e = updateDoc(e);
        e['promoKey'] = e['promoKey'] + newBrandDash;
        e = updateBrandLikeProperties(e);
        if(e['categoryId'] && e['categoryId'].length > 0) {
            e['categoryId'].forEach(function(e,i){
                e = sportCategoryIdMap[e];
            });
        }
        var newId = new ObjectId();
        e['_id'] = newId;
        promotionIdMap[oldId.str] = newId.str;
        batchUpdate.push(e);
    });
    performInsert(promotions, batchUpdate);
    batchUpdate = [];

    var promotionSectionDoc = db.getCollection(promotionSection).findOne({'_id' : oldBrand});
    promotionSectionDoc = updateDoc(promotionSectionDoc);
    promotionSectionDoc['_id'] = newBrand;
    for(i in promotionSectionDoc['unassignedPromotionIds']) {
        if(promotionIdMap[promotionSectionDoc['unassignedPromotionIds'][i]]) {
            promotionSectionDoc['unassignedPromotionIds'][i] = promotionIdMap[promotionSectionDoc['unassignedPromotionIds'][i]];
        }
    }
    var result = db.getCollection(promotionSection).insert(promotionSectionDoc);
    log('Inserted promotion section with id ' + newBrand + ', succefull: ' + result['nInserted']);
    globalCounter++;
//     now other promotionSections
    var promotionSectionDocs = db.getCollection(promotionSection).find({'brand' : oldBrand, '_id' : {'$ne' : oldBrand}});
    promotionSectionDocs.forEach(function(e,i){
        e = updateDoc(e);
        batchUpdate.push(e);
    });
    performInsert(promotionSection, batchUpdate);
}

//featuredeventstypes[categoryId] - for some reason only one element in collection
function specialCase3() {
    var batchUpdate = [];
    var docs = db.getCollection('featuredeventstypes').find({'brand' : oldBrand});
    docs.forEach(function(e,i) {
        e = updateDoc(e);
        e['categoryId'] = sportCategoryIdMap[e['categoryId']];
        batchUpdate.push(e);
    });
    performInsert('featuredeventstypes', batchUpdate);
}

//offers[module] -> ?offermodules
function specialCase4() {
    var offers = 'offers';
    var offerModules = 'offermodules';
    var offerModuleIdMap = {};
    var batchUpdate = [];

    var offerModuleDocs = db.getCollection(offerModules).find({'brand' : oldBrand});
    offerModuleDocs.forEach(function(e,i) {
        var oldId = e['_id'];
        e = updateDoc(e);
        var newId = new ObjectId();
        e['_id'] = newId;
        offerModuleIdMap[oldId] = newId;
        batchUpdate.push(e);
    });
    performInsert(offerModules, batchUpdate);
    batchUpdate = [];

    var offerDocs = db.getCollection(offers).find({'brand' : oldBrand});
    offerDocs.forEach(function(e,i){
        e = updateDoc(e);
        if(offerModuleIdMap[e['module']]) {
            e['module'] = offerModuleIdMap[e['module']];
        }
        batchUpdate.push(e);
    });
    performInsert(offers, batchUpdate);
}

//odds-boost-configuration
function specialCase5() {
    var oddsBoost = db.getCollection('odds-boost-configuration').findOne({'_id' : oldBrand});
    oddsBoost = updateDoc(oddsBoost);
    oddsBoost['_id'] = newBrand;
    var result = db.getCollection('odds-boost-configuration').insert(oddsBoost);
    log('Inserted odds-boost-configuration with id ' + newBrand + ', succefull: ' + result['nInserted']);
    globalCounter++;
}

function performInsert(collectionName, batchUpdate) {
//     log('Batch update for ' + collectionName + ' with size: ' + batchUpdate.length);
    var result = db.getCollection(collectionName).insert(batchUpdate);
    log('Inserting docs in ' + collectionName + ', prepared/successfull: ' + batchUpdate.length + '/' + result['nInserted']);
    globalCounter+=result['nInserted'];
}

main();
print(logVar);

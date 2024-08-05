// NOTE Grand flush by brand
var brand = 'vanilla';

var logVar = "";
function log(message) {
    logVar = logVar + '\n' + message;
}

var hasBrand = ['bankingmenus', 'banners', 'betreceiptbanners', 'betreceiptbannertablets', 'bottommenus', 'brandMenu', 'bybMarkets', 'bybSwitchers',
    'bybTabAvailability', 'competition', 'configs', 'connectmenus', 'countries', 'couponmarketselectors', 'coupons', 'desktop quicklinks', 'edpmarkets',
    'eventhubs', 'externallinks', 'featuredeventstypes', 'features', 'football3dbanners', 'footerlogos', 'footermenus', 'games', 'header-submenus',
    'headercontactmenus', 'headermenus', 'highlightCarousel', 'hr quicklinks', 'leagues', 'leftmenus', 'ln quicklinks', 'maintenancepages', 'moduleribbontabs',
    'navigationPoint', 'odds-boost-configuration', 'offermodules', 'offers', 'onBoardingGuides', 'otf-ios-app-toggle', 'payment-methods', 'promotionSection',
    'promotions', 'qualification-rule', 'quicklinks', 'quiz', 'renderconfig', 'rightmenus', 'seopages', 'splashPage', 'sportcategories', 'sportmodules',
    'sportquicklinks', 'sports', 'sporttabs', 'ssopages', 'static-text-otf', 'staticblocks', 'streamAndBet', 'structures', 'surfaceBet', 'teamKits',
    'topgames', 'topmenus', 'usermenus', 'widgets', 'ycleagues', 'ycmarkets', 'ycstaticblocks'];

// odds-boost-configuration
// promotionSection

function main() {
    var globalCounter = 0;
    for(i in hasBrand) {
        var collectionName = hasBrand[i];
        var result = db.getCollection(collectionName).remove({'brand' : brand});
        log('Removed ' + result['nRemoved'] + ' from ' + collectionName);
        globalCounter +=result['nRemoved'];
    }
    log('Total removed: ' + globalCounter);
};

main();
print(logVar);

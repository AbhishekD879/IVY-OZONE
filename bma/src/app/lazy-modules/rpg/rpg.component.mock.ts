import { IRpgConfig } from "./rpg.model";

export const rpgConfigMock: IRpgConfig = {
  title: 'Recently Played Games',
  seeMoreLink: 'https://gaming.coral.co.uk',
  gamesAmount: 5
};

export const rpgResponseMock: any =
{
  "statusCode": 0,
  "status": "Success",
  "errorMessage": null,
  "games": [
      {
          "gamevariant": "ivybookofhorus",
          "displayname": "Book Of Horus",
          "lobbytype": "instantCasino",
          "isgameavailable": null,
          "imageUrl": "https://casinogames.ladbrokes.com/htmllobby/images/newlmticons/supersquare/ivybookofhorus.jpg"
      },
      {
          "gamevariant": "yggwinterberries",
          "displayname": "Winter Berries",
          "lobbytype": "default",
          "isgameavailable": null,
          "imageUrl": "https://casinogames.ladbrokes.com/htmllobby/images/newlmticons/supersquare/yggwinterberries.jpg"
      },
      {
          "gamevariant": "netentstarbursthtml",
          "displayname": "Starburst",
          "lobbytype": "default",
          "isgameavailable": null,
          "imageUrl": "https://casinogames.ladbrokes.com/htmllobby/images/newlmticons/supersquare/netentstarbursthtml.jpg"
      },
      {
          "gamevariant": "coralbigbanker1",
          "displayname": "Big Banker",
          "lobbytype": "default",
          "isgameavailable": null,
          "imageUrl": "https://casinogames.ladbrokes.com/htmllobby/images/newlmticons/supersquare/coralbigbanker1.jpg"
      },
      {
          "gamevariant": "nyxrainbowriches",
          "displayname": "Rainbow Riches",
          "lobbytype": "default",
          "isgameavailable": null,
          "imageUrl": "https://casinogames.ladbrokes.com/htmllobby/images/newlmticons/supersquare/nyxrainbowriches.jpg"
      },
      {
          "gamevariant": "pngbookofdead",
          "displayname": "Book of Dead",
          "lobbytype": "default",
          "isgameavailable": null,
          "imageUrl": "https://casinogames.ladbrokes.com/htmllobby/images/newlmticons/supersquare/pngbookofdead.jpg"
      }
  ]
};

export const disabledGamesResponseMock: any = 
{
  "games": [
      "igthexbreak3r",
      "nyxdragonspinpicknmix",
      "nyxmonopolybringhousedown",
      "igtkittyglitter",
      "pariplaythequeensbanquet",
      "nyxtikitastic",
      "nyxdemongems",
      "slingoslingosharkweek",
      "nyxbookofultimateinfinity",
      "nyxcashstampede",
      "netentjackandthebeanstalkhtml",
      "playtechbookofkings",
      "mgstreasureskyland",
      "nyxmonopolyheights",
      "rtgarcadebombjp",
      "nyx2fatcatslostark",
      "nyxkodiaksroar",
      "coralfourleaffortunescratchcard",
      "nyxblackknightii_prt",
      "igtcrazywizard",
      "nyxsuperstarturns",
      "eusmdgoldenprnshtml",
      "pariplaydreamsofmacau",
      "eusmdstarlitefrtmm",
      "gameiomkrakatoa"
  ]
};

export const gymlResponseMock: any = 
{
  "statusCode": 0,
  "status": "SUCCESS",
  "errorMessage": "",
  "categoryid": "LMC_HOME",
  "subcategoryid": "LMC_UNQ_POKERLOBBY",
  "gamelist": [
      {
          "game": "playtechpremiumeuropeanrlt",
          "name": "Premium European Roulette",
          "provider": "Playtech"
      },
      {
          "game": "playtechpremiumblackjack",
          "name": "Premium Blackjack",
          "provider": "Playtech"
      },
      {
          "game": "coralbigbanker1",
          "name": "Big Banker",
          "provider": "CORAL"
      },
      {
          "game": "blueprintfishinfrenzyjpk",
          "name": "Fishin Frenzy Jackpot King",
          "provider": "Blueprint"
      },
      {
          "game": "pngbookofdead",
          "name": "Book of Dead",
          "provider": "PLAYNGO"
      },
      {
          "game": "ivycryptocash",
          "name": "Crypto Cash",
          "provider": "INHOUSE"
      },
      {
          "game": "blueprinteyeofhorusjp",
          "name": "Eye of Horus Jackpot King",
          "provider": "Blueprint"
      },
      {
          "game": "playtechlivequantumroulette",
          "name": "Quantum Roulette Live",
          "provider": "Playtech"
      },
      {
          "game": "playtechjacksorbetter",
          "name": "Jacks or Better",
          "provider": "Playtech"
      },
      {
          "game": "playtechaotggodofstorms",
          "name": "Age of the Gods God of Storms",
          "provider": "Playtech"
      },
      {
          "game": "prgbigbassbonanza",
          "name": "Big Bass Bonanza",
          "provider": "PRAGMATICPLAY"
      },
      {
          "game": "eusmd9potsofgolduk",
          "name": "9 Pots of Gold",
          "provider": "Microgaming"
      },
      {
          "game": "rtgdynamiterichesmwjp",
          "name": "Dynamite Riches MegaWays",
          "provider": "REDTIGER"
      },
      {
          "game": "playtechcasinoholdem",
          "name": "Casino Hold 'Em",
          "provider": "Playtech"
      },
      {
          "game": "nyxgoldcashfreespins",
          "name": "Gold Cash Freespins",
          "provider": "NYX"
      }
  ]
};

export const clientConfigMock: any =
{
  "bmaUserInterfaceConfig": {
    "rtsLink": "/mobileportal/transactions",
    "accountUpgradeLink": {
      "imc": "/mobileportal/initaccountupgrade?source=guard",
      "omc": "/mobileportal/virtualcard"
    },
    "preloadPortalModule": true,
    "portalModuleLoadDelay": 5000,
    "cspSegmentExpiry": 14,
    "gameImageUrl": "https://tr-casino-clrouter.ivycomptech.co.in/",
    "maxNumberOfGames": 10,
    "minNumberOfGames": 4,
    "lobbyType": "UniqueGames",
    "gymlCategoryId": "LMC_HOME",
    "gymlSubCategoryId": "LMC_RECOMMENDED"
  },
  "bmaCasinoGamesConfig": {
    "miniGamesEnabled": true,
    "miniGamesHost": "https://trunkialcg-casino-clrouter.ivycomptech.co.in",
    "miniGamesTemplate": "/htmllobby/minilobby/index.html?brand=CORAL&lobbyType=instantMini&invokerProduct=BETTING&frontend=cl&userIp=$USERIP$&currency=$CURRENCY$&channelName=WC&sessionKey=$SESSION_KEY$&lang=en_US&HOSTURL=$HOSTURL$&pLang=en&accountName=$accountName$&deviceType=DESKTOP&sportsminigame=true",
    "recentlyPlayedGamesEnabled": true,
    "recentlyPlayedGamesUrl": "/games/casinowidget/recentgameswidget?.box=1&invokerProduct=betting&_disableFeature=GlobalSearch",
    "userHostAddress": "10.151.144.9",
    "seeAllEnabled": true,
    "rpgPayload": {
      "accountName": "$ACCOUNTNAME$",
      "productId": "CASINO",
      "brandId": "CORAL",
      "feId": "cl",
      "channelId": "$CHANNELID$",
      "lang": "en_US",
      "noofgames": 10,
      "lobbyType": "instantCasino",
      "reqSource": "LCG_SPORTS"
    },
    "seeAllUrl": "/games"
  },
  "bmaHtmlInjectionConfig": {
    "headTags": {
      "scripts": {
        "newrelic": "<script src=\"//scmedia.itsfogo.com/$-$/d0b49037ddd446be92d2945fd75a24c5.tpl\" data-app async></script>"
      }
    }
  },
  "bmaTrackingConfig": {
    "gtmConfigs": {},
    "newRelicConfigs": {}
  },
  "vnTrackerId": {
    "btagCallEnabled": true,
    "queryStrings": [
      "trackerid",
      "wmid",
      "wm"
    ]
  },
  "vnRememberMe": {
    "isEnabled": true,
    "apiHost": "https://qa4.sports.coral.co.uk"
  },
  "vnAppInfo": {
    "brand": "CORAL",
    "channel": "WC",
    "frontend": "cl",
    "product": "SPORTSBOOK"
  },
  "vnLazyStyles": {
    "stylesheets": [
      {
        "url": "/ClientDist/coralDesktop/styles.36b34918e2fd1e4a.css",
        "lazyLoad": "Important"
      },
      {
        "url": "/ClientDist/coralDesktop/media-xs.1d8ce4a083a46631.css",
        "lazyLoad": "Secondary",
        "media": "lt-sm"
      },
      {
        "url": "/ClientDist/coralDesktop/media-sm.81a2aa84701ba189.css",
        "lazyLoad": "Secondary",
        "media": "gt-xs"
      },
      {
        "url": "/ClientDist/coralDesktop/media-md.69ba9862dbcf8101.css",
        "lazyLoad": "Secondary",
        "media": "gt-sm"
      },
      {
        "url": "/ClientDist/coralDesktop/media-mw.d45657a85c733ac4.css",
        "lazyLoad": "Secondary",
        "media": "gt-lg"
      },
      {
        "url": "/ClientDist/coralDesktop/media-lg.3584beb9cd425388.css",
        "lazyLoad": "Secondary",
        "media": "gt-md"
      },
      {
        "url": "/ClientDist/coralDesktop/media-xl.a4d63f6ddbd2f26c.css",
        "lazyLoad": "Secondary",
        "media": "gt-mw"
      },
      {
        "url": "/ClientDist/coralDesktop/belowthefold.4b1013239810f0f5.css",
        "lazyLoad": "Secondary"
      },
      {
        "url": "/ClientDist/coralDesktop/portalStyles.646469d651d933b9.css",
        "lazyLoad": "Custom",
        "alias": "portalStyles"
      },
      {
        "url": "/ClientDist/coralDesktop/themes-coral-native-app.ca0cdeae55ab26e8.css",
        "lazyLoad": "Custom",
        "alias": "native-app"
      },
      {
        "url": "/ClientDist/coralDesktop/themes-coral-authentication.d70b628b3e89af73.css",
        "lazyLoad": "Custom",
        "alias": "authentication"
      },
      {
        "url": "/ClientDist/coralDesktop/themes-coral-navigation-layout.518bc0dfe08121eb.css",
        "lazyLoad": "Custom",
        "alias": "navigation-layout"
      },
      {
        "url": "/ClientDist/coralDesktop/casino-main.3e8fe1ccac52cc49.css",
        "lazyLoad": "Custom",
        "alias": "casinoStyles"
      }
    ]
  },
  "vnLazyScripts": {
    "scripts": []
  },
  "vnBadge": {
    "cssClass": "badge-danger"
  },
  "vnClaims": {
    "http://api.bwin.com/v3/user/usertoken": "f0a2e060ecc440c9989fb4477afe9b68",
    "http://api.bwin.com/v3/user/sessiontoken": "5d9818105a19415e8a06462c05b32846",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/country": "GB",
    "http://api.bwin.com/v3/user/language": "EN",
    "http://api.bwin.com/v3/user/culture": "en-GB",
    "http://api.bwin.com/v3/user/utcoffset": "60",
    "http://api.bwin.com/v3/user/timezone": "GMT Standard Time",
    "http://api.bwin.com/v3/user/currency": "GBP",
    "http://api.bwin.com/v3/user/nameidentifier": "0",
    "http://api.bwin.com/v3/user/pg/nameidentifier": "124109626",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": "cl_testgvc_fav",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name": "testgvc_fav",
    "http://api.bwin.com/v3/user/ssotoken": "85bf2cd0df134d8086185cf15afb9386",
    "http://api.bwin.com/v3/user/workflowtype": "0",
    "http://api.bwin.com/v3/user/rsaAssigned": "False",
    "http://api.bwin.com/v3/user/jurisdiction": "GBR",
    "http://api.bwin.com/v3/user/isMigratedFromExternalPlatform": "False",
    "http://api.bwin.com/v3/user/realplayer": "True",
    "http://api.bwin.com/v3/user/accountcategoryId": "0",
    "http://api.bwin.com/v3/user/playercategoryId": "1",
    "http://api.bwin.com/v3/user/screenname": "qwe12377",
    "http://api.bwin.com/v3/user/isPartiallyRegistered": "False",
    "http://api.bwin.com/v3/user/pg/globalsession": "1555012309202266JWNa5h356",
    "http://api.bwin.com/v3/user/twoFactorStatus": "False",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/locality": "Swindon",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/stateorprovince": "ZZ",
    "http://api.bwin.com/v3/user/title": "Mrs",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname": "PUJITHA",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname": "PALLE",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/dateofbirth": "1998-12-04",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/postalcode": "SN1 1HN",
    "http://api.bwin.com/v3/user/mobilecountrycode": "44",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/mobilephone": "7489350340",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/privatepersonalidentifier": " ",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/streetaddress": "The Tri Centre, New Bridge Square",
    "http://api.bwin.com/v3/user/address2": " ",
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/email": "prathu@internalgvc.com",
    "http://api.bwin.com/v3/user/accBusinessPhase": "online",
    "http://api.bwin.com/v3/user/tierCode": "9",
    "http://api.bwin.com/v3/user/playerPriority": "P0",
    "http://api.bwin.com/v3/user/gamingDeclarationFlag": "NA",
    "http://api.bwin.com/v3/user/bs": "false",
    "http://api.bwin.com/v3/user/isUkGcPlayer": "True",
    "http://api.bwin.com/v3/user/isFundProtected": "True",
    "http://api.bwin.com/v3/user/isRgLimitSet": "False",
    "http://api.bwin.com/v3/user/isTncAccepted": "True",
    "http://api.bwin.com/v3/user/armStatus": "NONE",
    "http://api.bwin.com/v3/user/registrationCompleted": "true",
    "http://api.bwin.com/v3/user/registrationStep": "0"
  },
  "vnCommonMessages": {
    "AccountBalance": "Balance:",
    "ActiveSessionText": "The current active session will be terminated, please scan your card again after the process is completed.",
    "ActiveSessionTitle": "Active session",
    "AltHeaderText": "Welcome to Coral",
    "Back": "Back",
    "BalanceTransferText": "By logging in, you confirm any terminal balance will be added to your wallet (deposit limits apply)",
    "Cancel": "Cancel",
    "ClockText": "Current time: ",
    "Close": "Close",
    "Completed": "Completed",
    "Confirm": "Confirm",
    "Continue": "Continue",
    "ContinueToLabel": "CONTINUE TO __LABEL__",
    "CounterAssistance": "Please visit the counter for assistance.",
    "DarkModeText": "Night Mode",
    "DateDayPlaceholder": "DD",
    "DateMonthPlaceholder": "MM",
    "DateYearPlaceholder": "YYYY",
    "Day": "day",
    "Day_Plural": "days",
    "Day_short": "d",
    "Decline": "Decline",
    "Delete": "Delete",
    "DepositLimitType:DAILY": "daily",
    "DepositLimitType:HOURLY": "hourly",
    "DepositLimitType:MONTHLY": "monthly",
    "DepositLimitType:WEEKLY": "weekly",
    "DuplicateEmail": "This email is <b>already registered</b>. Please, <b>try to login</b>",
    "GCSkeleton": "<div class=\"bg-home-skeleton sk-bingo-container portal-center-wrapper pt-3 pb-3\">'\n       <div class=\"sk-title w-90\"></div>\n        <div class=\"sk-games\">\n                <div class=\"sk-game-card\"></div>\n                <div class=\"sk-game-card\"></div>\n                <div class=\"sk-game-card\"></div>\n                <div class=\"sk-game-card\"></div>\n          </div>\n                <div class=\"sk-title w-90\"></div>\n                <div class=\"sk-title w-90\"></div>\n</div>",
    "GCSkeletonRedesign": "<div class=\"navigation-content-wrapper\">\n<div class=\"portal-center-wrapper\">' \n                <div class=\"sk-block-card mt-3 h-40px\"></div>\n                <div class=\"sk-block-card mt-3 h-40px\"></div> \n                <div class=\"sk-block-card mt-3 h-40px\"></div> \n                <div class=\"sk-block-card mt-3 h-40px\"></div>\n </div>\n</div>",
    "GeneralValidationError": "The value you entered was incorrect. Please recheck your data and try again.",
    "Hour": "hour",
    "Hour_Plural": "hours",
    "Hour_short": "h",
    "Hours": "hour(s)",
    "IAmHere": "I am here",
    "InvalidCard": "Unknown code",
    "KeepPlaying": "Keep playing",
    "LanguageSwitcherHeading": "",
    "LanguageSwitcherTitle": "Select Language",
    "LastSessionInfo": "Your last session was on <b>{0}</b>",
    "LiveChatDisabledText": "Our live chat is currently unavailable",
    "LiveChatLink": "Start Live Chat",
    "LiveChatText": "Need help?",
    "LoadingIndicatorFallbackMessage": "Loading...",
    "LoadingPage": "Loading...",
    "LoginDuration": "You've been logged in for",
    "LoginStartTime": "You've been Logged in since: {login_start_time}",
    "LoginToView": "To view this page, please log into your account",
    "LogOut": "LOG OUT",
    "MinReq": "Minimum Requirements",
    "Minute": "minute",
    "Minute_Plural": "minutes",
    "Minute_short": "m",
    "Minutes": "minutes",
    "MobileCountryCodeLabel": "Code",
    "MobileNumberLabel": "Mobile Number",
    "MoreInfo": "More Info",
    "NavigationLayout_Home": "Home",
    "NavigationLayout_MyAccount": "My Account",
    "Next": "Next",
    "NotAvailable": "N/A",
    "Ok": "No",
    "Okay": "OK",
    "PlayerLimitType:LOGIN_TIME_PER_DAY_IN_MINUTES": "daily",
    "PlayerLimitType:LOGIN_TIME_PER_MONTH_IN_MINUTES": "monthly",
    "PlayerLimitType:LOGIN_TIME_PER_WEEK_IN_MINUTES": "weekly",
    "PleaseLogIn": "You must log in first",
    "PleaseSelect": "Please select ...",
    "PleaseWait": "Please wait...",
    "PopoverCloseText": "GOT IT",
    "PopoverNextText": "NEXT TIP",
    "PopoverPreviousText": "PREVIOUS",
    "Previous": "Previous",
    "QuickDepositTitle": "Deposit",
    "RegisterNow": "Register now!",
    "ReturnToLabel": "RETURN TO __CURRENTLABEL__",
    "Save": "Save",
    "Second": "second",
    "Second_Plural": "seconds",
    "Second_short": "s",
    "SelectDate": "Select date",
    "SelectDateRange": "Select date range",
    "SelectLanguage": "Select language",
    "Send": "Send",
    "SessionError": "Your session expired. Please log in again.",
    "SessionTimeoutDescription": "To keep your account secure, your session will expire in,",
    "SessionTimeoutTitle": "Are you still there?",
    "SignIn": "Sign in",
    "SignOut": "Log out",
    "SplashScreenAltLoading": "Loading",
    "StopPlaying": "Stop playing",
    "Submit": "Submit",
    "TechnicalError": "A technical error has occurred. Please try again or contact our Customer Service team if the error persists.",
    "WinningsLosses": "The winnings/losses balance for your session is"
  },
  "vnTracking": {
    "isEnabled": true,
    "dataLayerName": "dataLayer",
    "notTrackedQueryStrings": [
      "sessionKey"
    ],
    "tagManagerRenderers": [
      "GoogleTagManagerRenderer"
    ],
    "eventCallbackTimeoutInMilliseconds": 1000,
    "pageViewDataProviderTimeout": 2000,
    "clientInjectionExcludes": [
      "GoogleTagManagerRenderer"
    ],
    "clientTagManagers": [
      {
        "name": "GoogleTagManagerRenderer",
        "script": "(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})\r\n(window,document,'script','dataLayer','GTM-N48RN3R');\r\n"
      }
    ]
  },
  "vnDevice": {
    "isMobile": false,
    "isTouch": false,
    "isMobilePhone": false,
    "isTablet": false,
    "isRobot": false,
    "model": "Chrome - Windows",
    "logInfoEnabled": false
  },
  "vnLastKnownProduct": {
    "enabled": "!((c.Request.PathAndQuery.includes('/mobileportal/')))",
    "product": "sports",
    "url": "http://qa4.sports.coral.co.uk/en"
  },
  "vnNativeApp": {
    "applicationName": "unknown",
    "product": "UNKNOWN",
    "nativeMode": "Unknown",
    "isNative": false,
    "isNativeApp": false,
    "isNativeWrapper": false,
    "isDownloadClient": false,
    "isDownloadClientApp": false,
    "isDownloadClientWrapper": false,
    "isTerminal": false,
    "enableAppsFlyer": false,
    "enableWrapperEmulator": false,
    "appSettingsSupported": false,
    "appSettingsTimeout": 0,
    "partnerSessionIdSupported": false,
    "sendOpenLoginDialogEvent": false,
    "enableCCBDebug": true,
    "loggedNativeEvents": [],
    "disabledEvents": []
  },
  "vnPage": {
    "useSharedFeatures": false,
    "lang": "en",
    "languageCode": "en",
    "htmlLang": "en",
    "culture": "en-GB",
    "useBrowserLanguage": true,
    "browserPreferredCulture": "en-US",
    "locale": "en-GB",
    "domain": ".coral.co.uk",
    "isProduction": false,
    "isInternal": true,
    "clientIP": "10.100.19.37",
    "defaultLanguage": {
      "culture": "en-GB",
      "nativeName": "English (United Kingdom)",
      "routeValue": "en",
      "sitecoreContentLanguage": "en",
      "htmlLangAttribute": "en",
      "angularLocale": "en-GB"
    },
    "uiLanguages": [
      {
        "culture": "en-GB",
        "nativeName": "English (United Kingdom)",
        "routeValue": "en"
      }
    ],
    "languages": [
      "en"
    ],
    "homePage": "http://qa4.sports.coral.co.uk/en/sports",
    "loginUrl": "/en/labelhost/login",
    "product": "sports",
    "isAnonymousAccessRestricted": false,
    "logging": {
      "isEnabled": true,
      "maxErrorsPerBatch": 10,
      "debounceInterval": 2000,
      "url": "/log"
    },
    "loadingIndicator": {
      "defaultDelay": 600000,
      "externalNavigationDelay": 500,
      "spinnerContent": "&nbsp;"
    },
    "currency": {
      "default": "symbol",
      "zar": "symbol-narrow"
    },
    "userDisplayNameProperties": [
      "firstName"
    ],
    "isProfilingEnabled": false,
    "isSingleDomainApp": true,
    "imageProfiles": {
      "default": {
        "prefix": "width",
        "widthBreakpoints": [
          320,
          480,
          640,
          800,
          1024,
          1280
        ]
      },
      "teaser": {
        "prefix": "pc-teaser-width-",
        "widthBreakpoints": [
          600,
          960,
          1280,
          1920
        ]
      },
      "teaser-fullsize": {
        "prefix": "pc-teaser-fullsize-width-",
        "widthBreakpoints": [
          480,
          600,
          960,
          1280,
          1920
        ]
      }
    },
    "cookies": {
      "sameSiteMode": "None",
      "secure": true
    },
    "scrollBehaviorEnabledCondition": "true",
    "theme": "coral",
    "singleSignOnDomains": [],
    "idleModeCaptureEnabled": false,
    "itemPathDisplayModeEnabled": false
  },
  "vnProducts": {
    "sports": {
      "enabled": true,
      "apiBaseUrl": "https://qa4.sports.coral.co.uk"
    },
    "casino": {
      "enabled": true,
      "apiBaseUrl": "https://qa4.www.coral.co.uk"
    },
    "poker": {
      "enabled": true,
      "apiBaseUrl": "https://qa4.poker.coral.co.uk"
    },
    "portal": {
      "enabled": true,
      "apiBaseUrl": "https://qa4.myaccount.coral.co.uk"
    },
    "bingo": {
      "enabled": true,
      "apiBaseUrl": "https://qa4.bingo.coral.co.uk"
    },
    "promo": {
      "enabled": true,
      "apiBaseUrl": "https://qa4.promo.coral.co.uk"
    },
    "shared": {
      "enabled": true,
      "apiBaseUrl": "https://qa4.shared-features-api.coral.co.uk"
    },
    "host": {
      "enabled": true,
      "apiBaseUrl": ""
    },
    "coralsports": {
      "enabled": true,
      "apiBaseUrl": ""
    }
  },
  "vnProductHomepages": {
    "sports": "http://qa4.sports.coral.co.uk/en",
    "casino": "https://qa4.www.coral.co.uk/en",
    "portal": "https://qa4.sports.coral.co.uk/en",
    "poker": "https://qa4.poker.coral.co.uk/en",
    "bingo": "https://qa4.bingo.coral.co.uk/en",
    "promo": "https://promo.coral.co.uk/en/promo/offers"
  },
  "vnRtms": {
    "isEnabled": true,
    "host": "https://lc-tr-rtms-fe.ivycomptech.co.in:8000/gateway",
    "keepAliveMilliseconds": 5000,
    "reconnectMilliseconds": 15000,
    "tracingEnabled": true,
    "tracingBlacklistPattern": "ping",
    "disabledEvents": {},
    "remoteLogLevels": [
      "debug"
    ],
    "backgroundEvents": [
      "PLAY_BREAK_START_EVENT",
      "PLAY_BREAK_END_EVENT",
      "PLAY_BREAK_GRACE_PERIOD_EVENT",
      "LONG_SESSION_INTERACTION_EVENT",
      "AUTO_LOGOUT_EVENT"
    ],
    "establishConnectionOnlyInLoginState": true
  },
  "vnUser": {
    "lang": "en",
    "returning": true,
    "isAuthenticated": true,
    "isAnonymous": false,
    "workflowType": 0,
    "userTimezoneUtcOffset": 60,
    "xsrfToken": "5d9818105a19415e8a06462c05b32846",
    "loyalty": "B",
    "loyaltyPoints": 0,
    "balanceProperties": {
      "accountCurrency": {
        "id": "GBP",
        "name": "Pound Sterling"
      },
      "accountBalance": 381.47,
      "balanceForGameType": 381.47,
      "bonusWinningsRestrictedBalance": 0,
      "cashoutRestrictedBalance": 0,
      "cashoutableBalance": 381.47,
      "cashoutableBalanceReal": 381.47,
      "availableBalance": 381.47,
      "depositRestrictedBalance": 0,
      "inPlayAmount": 0,
      "releaseRestrictedBalance": 0,
      "playMoneyBalance": -1,
      "playMoneyInPlayAmount": -1,
      "owedAmount": 0,
      "taxWithheldAmount": 0,
      "pokerWinningsRestrictedBalance": 0,
      "cashoutRestrictedCashBalance": 0,
      "cashoutableBalanceAtOnline": 381.47,
      "cashoutableBalanceAtRetail": 381.47,
      "creditCardDepositBalance": 0,
      "creditCardWinningsBalance": 0,
      "debitCardDepositBalance": 0,
      "mainRealBalance": 381.47,
      "uncollectedFunds": 0,
      "payPalBalance": 0,
      "payPalRestrictedBalance": 0,
      "payPalCashoutableBalance": 0,
      "sportsExclusiveBalance": 0,
      "sportsDepositBalance": 0,
      "gamesDepositBalance": 0,
      "sportsWinningsBalance": 0,
      "sportsRestrictedBalance": 0,
      "pokerWinningsBalance": 0,
      "pokerRestrictedBalance": 0,
      "slotsWinningsBalance": 0,
      "slotsRestrictedBalance": 0,
      "allWinningsBalance": 0,
      "maxLimitExceededBalance": 0
    },
    "loginDuration": null,
    "remainingLoginTime": null,
    "isFirstLogin": false,
    "registrationDate": "2/15/2022 1:48 PM",
    "daysRegistered": 220,
    "customerId": 0,
    "segmentId": 0,
    "lifeCycleStage": null,
    "eWarningVip": null,
    "microSegmentId": 0,
    "churnRate": 0,
    "futureValue": 0,
    "potentialVip": 0,
    "tierCode": 9,
    "playerPriority": "0",
    "lastLoginTimeFormatted": "9/23/2022 6:54 AM",
    "lastLoginTime": "2022-09-23T05:54:48Z"
  }
};
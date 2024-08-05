import { ForYou } from "../for-you/for-you-personalized/for-you-personalized.model";
import { INSIGTHTS_CONSTANTS } from "../sport-tab-popular-bets/sport-tab-popular-bets-filter.constants";
 

export const INSIGHTS_DEFAULT_DATA = [
  {
    trendingTabName: INSIGTHTS_CONSTANTS.popularBets, //used in FE as Sub swithers tabname 
    headerDisplayName: INSIGTHTS_CONSTANTS.headerDisplayName, //used as const field to sagrigate the tabs
    enabled: true,
    href: INSIGTHTS_CONSTANTS.insightsPopular, //used for routings in CMS
    popularTabs: [
      {
        enabled: true,
        showNewFlag: true,
        popularTabName: INSIGTHTS_CONSTANTS.popularTab, //used in FE to sagrigate the subtab
        headerDisplayName: "",
        startsInText: "",
        backedInLastText: "",
        showMoreText: "",
        showLessText: "",
        backedUpTimesText: "",
        informationTextDesc: "",
        numbOfDefaultPopularBets: null,
        numbOfShowMorePopularBets: null,
        priceRange: "",
        noPopularBetsMsg: "",
        lastUpdatedTime: "",
        betSlipBarBetsAddedDesc: "",
        betSlipBarCTALabel: "",
        betSlipBarDesc: "",
        betSlipBarRemoveBetsCTALabel: "",
        suspendedBetsAddedText: "",
        suspendedBetsDesc: "",
        backedInLastFilter: [],
        eventStartsFilter: [],
        enableAddToBetSlipBar : true,
        enableArrowIcon: false,
        enableBackedUpTimes:false,
        noBettingDescTitle:''
      },
    ],
  },
  {
    trendingTabName: INSIGTHTS_CONSTANTS.forYou, //used in FE as Sub swithers tabname 
    headerDisplayName: INSIGTHTS_CONSTANTS.for_you_tab, //used as const field to sagrigate the tabs
    enabled: true,
    href: INSIGTHTS_CONSTANTS.insights_forYou, //used for routings in CMS
    popularTabs: [
        {
            betSlipBarBetsAddedDesc: "",
            betSlipBarCTALabel: "",
            betSlipBarDesc: "",
            showNewFlag: true,
            betSlipBarRemoveBetsCTALabel: "",
            suspendedBetsDesc: "",
            suspendedBetsAddedText: "",
            href: INSIGTHTS_CONSTANTS.for_you_personalized_bets, //used for routings in CMS
            enabled: true,
            popularTabName: INSIGTHTS_CONSTANTS.for_you_personalized_bets, //used in FE to sagrigate the subtab
            headerDisplayName: INSIGTHTS_CONSTANTS.foryou_personalized, // we are making const this field to show in table initially
            startsInText: "",
            backedInLastText: "",
            showMoreText: "",
            showLessText: "",
            backedUpTimesText: "",
            informationTextDesc: "",
            numbOfDefaultPopularBets: null,
            numbOfShowMorePopularBets: null,
            priceRange: "",
            noPopularBetsMsg: null,
            lastUpdatedTime: "",
            nonLoginHeader: "",
            nonLoginCTA: "",
            noBettingHeader: "",
            noBettingDesc: "",
            noBettingCTA: "",
            backedInLastFilter: [],
            eventStartsFilter: [],
            enableArrowIcon: false,
            enableBackedUpTimes:false,
            noBettingDescTitle:''
        }
    ]
 }
];
//used in insights-personalized.component.ts//
export const FOR_YOU_DETAILS: ForYou = {
  popularTabName:'',
  headerDisplayName: '',
  showMoreText: '',
  showLessText: '',
  backedUpTimesText: '',
  numbOfDefaultPopularBets: null,
  numbOfShowMorePopularBets: null,
  priceRange: '',
  lastUpdatedTime: '',
  informationTextDesc: '',
  betSlipBarDesc: '',
  betSlipBarCTALabel: '',
  betSlipBarBetsAddedDesc: '',
  betSlipBarRemoveBetsCTALabel: '',
  suspendedBetsAddedText: '',
  suspendedBetsDesc: '',
  isUntiedSport: true,
  enabled: true,
  checkEvents: true,
  nonLoginHeader: '',
  noBettingCTA: '',
  noBettingHeader: '',
  noBettingDesc: '',
  enableArrowIcon:false,
  enableBackedUpTimes:false,
  noBettingDescTitle:''
}
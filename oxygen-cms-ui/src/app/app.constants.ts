interface IAppConfig {
  HIDE_DURATION: number;
  ERROR_HIDE_DURATION: number;
  ADD_COMPONENT_MODAL_WINDOW_WIDTH: string;
  LIMIT_EXCEED_MSG: string;
  FOOTER_MENU: string;
  FOOTER_MENU_SAVED: string;
  SUPER_BUTTON_SAVING: string;
  SUPER_BUTTON_SAVED: string;
  SPECIAL_SUPER_BUTTON_SAVING: string;
  SPECIAL_SUPER_BUTTON_SAVED: string;
  SURFACE_BET: string;
  REMOVE_SURFACE_BET: string;
  POPULAR_BETS: string;
}

export const AppConstants: IAppConfig = {
  HIDE_DURATION: 3000, // Duration for snack bar
  ERROR_HIDE_DURATION: 10000, // Duration for error message,
  ADD_COMPONENT_MODAL_WINDOW_WIDTH: '767px',
  LIMIT_EXCEED_MSG: 'Limit exceeded',
  FOOTER_MENU: 'Footer Menu',
  FOOTER_MENU_SAVED: 'Footer Menu is Saved',
  SUPER_BUTTON_SAVING: 'Super Button Saving',
  SUPER_BUTTON_SAVED: 'Super Button is Successfully Saved.',
  SPECIAL_SUPER_BUTTON_SAVING: 'Special Super Button Saving',
  SPECIAL_SUPER_BUTTON_SAVED: 'Special Super Button is Successfully Saved.',
  SURFACE_BET: 'Surface Bet',
  REMOVE_SURFACE_BET: 'Are You Sure You Want to Remove Surface Bet?',
  POPULAR_BETS: 'popularbets'
};

export const Brand = {
  CORAL: 'bma',
  LADBROKES: 'ladbrokes',
};

export const TimeLine = {
  SHOW_LEFT_SIDE_RED_LINE_TEXT: 'Show Left Side Red Line',
  SHOW_LEFT_SIDE_BLUE_LINE_TEXT: 'Show Left Side Blue Line',
  POST_RED_LINE: 'post--red-line',
  POST_BLUE_LINE: 'post--blue-line',
  POST_WITH_ICON: 'post--with-icon'
};

export const FreeRideConstants = {
  POT_CREATION: 'Pot Creation',
  FREE_RIDE: 'Free Ride',
  FREE_RIDE_CAMPAIGN_URL: '/free-ride/campaign',
  POT_CREATION_URL: '/potCreation',
  LOCAL_STORAGE_EVENT_ID_KEY: 'spotlight_event_id',
  LOCAL_STORAGE_CLASS_IDS_KEY: 'spotlight_class_ids',
  DIALOG_TITLE_REFRESH_SUCCESS: 'Events data re-fetched',
  DIALOG_MESSAGE_REFRESH_NULL: 'No events found!',
  DIALOG_MESSAGE_REFRESH_SUCCESS: 'Successfully re-fetched Spotlight-related events from SiteServe!',
  FETCH_CLASSIDS_STRING: 'Separate classIds by comma',
  RESTRICT_UK_IRE: 'Restrict to UK And IRE',
  REFRESH_BOX_ICON: 'refresh_box',
  REFRESH_EVENTS: 'Refetch Events',
  CREATE_POTS_BTN: 'Create Pots',
  HORSE_SELECTION: 'HORSE SELECTION',
  DIALOG_CREATE_TITLE: 'Pots to Campaign level',
  DIALOG_CREATE_MESSAGE: 'Pots to Campaign level Created!'
};

export const CSPSegmentConstants = {
  UNIVERSAL: 'UNIVERSAL',
  SEGMENTED: 'SEGMENTED',
  TOOLTIP: 'Enter segments by , separated',
  UNIVERSAL_TITLE: 'Universal',
  SEGMENT_TITLE: 'Segment(s) Inclusion',
  EMPTY_FIELD: 'Empty field not allowed',
  VALID_SEGMENT: 'Please enter valid segment containing Alpha numeric, -, _ only.',
  EXTRA_COMMAS: 'Input contains extra commas',
  SHOW_IN_SPORTS_RIBBON_COLUMN: 'Show in Sports Ribbon'
};

export const CSPSegmentLSConstants = {
  FOOTER_MENU_RIBBON: 'footer-menu-ribbon',
  SUPER_BUTTON: 'super-button',
  MODULE_RIBBON_TAB:  'module-ribbon-tab',
  SURFACE_BET_TAB: 'surface-bet-tab',
  HIGHLIGHT_CAROUSEL: 'hightlight-carousel',
  SPORTS_QUICK_LINK: 'sports-quick-link',
  FEATURED_TAB_MODULE: 'featured-tab-module',
  INPLAY_SPORTS_MODULE: 'inplay-sports-module',
  NEXT_EVENT_CAROUSEL: 'next-event-carousel',
};

export const TIME_SEPARATOR: string = 'T';

export const MarketMapping = [
  {
    id: "5df8e237c9e77c000101bd24",
    createdBy: "5d2c3a16c9e77c00014681eb",
    createdByUserName: null,
    updatedBy: "5d2c3a16c9e77c00014681eb",
    updatedByUserName: null,
    createdAt: "2019-12-17T14:12:07.836Z",
    updatedAt: "2019-12-17T14:14:34.525Z",
    sortOrder: -1,
    couponId: "222",
    marketTemplateName: "23",
    brand: "bma",
  },
  {
    id: "5df8e237c9e77c000101bd24",
    createdBy: "5d2c3a16c9e77c00014681eb",
    createdByUserName: null,
    updatedBy: "5d2c3a16c9e77c00014681eb",
    updatedByUserName: null,
    createdAt: "2019-12-17T14:12:07.836Z",
    updatedAt: "2019-12-17T14:14:34.525Z",
    sortOrder: -1,
    couponId: "224",
    marketTemplateName: "26",
    brand: "bma",
  },
  {
    id: "5df8e237c9e77c000101bd24",
    createdBy: "5d2c3a16c9e77c00014681eb",
    createdByUserName: null,
    updatedBy: "5d2c3a16c9e77c00014681eb",
    updatedByUserName: null,
    createdAt: "2019-12-17T14:12:07.836Z",
    updatedAt: "2019-12-17T14:14:34.525Z",
    sortOrder: -1,
    couponId: "122",
    marketTemplateName: "23",
    brand: "bma",
  },
  {
    id: "5df8e237c9e77c000101bd24",
    createdBy: "5d2c3a16c9e77c00014681eb",
    createdByUserName: null,
    updatedBy: "5d2c3a16c9e77c00014681eb",
    updatedByUserName: null,
    createdAt: "2019-12-17T14:12:07.836Z",
    updatedAt: "2019-12-17T14:14:34.525Z",
    sortOrder: -1,
    couponId: "222",
    marketTemplateName: "21",
    brand: "bma",
  },
];

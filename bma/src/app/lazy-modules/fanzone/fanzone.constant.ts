export const IMIN: string = 'I M IN';
export const RemindMeLater: string = 'Remind Me Later';
export const DontShowMeAgain: string = 'Dont show me this again';
export const storageKeyValue: string = 'fanzone';
export const GTM_DATA = {
  TRACKEVENT: 'trackEvent',
  EVENTACTION: 'rendered',
  EVENTCATEGORY: 'show your colours',
  EVENTLABEL: ''
};
export const GTM_DATA_FZ_BANNER = {
  TRACKEVENT: 'trackEvent',
  EVENT_ACTION_FZ_ENTRY: 'entry banner',
  EVENTCATEGORY: 'fanzone',
  EVENTLABEL: 'render',
  EVENT_DETAILS: ''
};
export const OPTIN_EMAIL = {
  TITLE: 'Fanzone Optin Email',
  DESCRIPTION: 'Hey, You are not subscribed with the Email Notification. Please click on "Optin Email" to keep updated with the latest email offers and promotions from Ladbrokes.',
  OPTIN_EMAIL: 'OPTIN EMAIL',
  CANCEL: 'CANCEL',
  RemindMeLater: 'Remind Me Later',
  DontShowMeAgain: 'Don\'t show me this again'
};
export const fanzonePath = '/fanzone';

export const BUTTONS = {
  optin: 'optin',
  rml: 'rml',
  dsme: 'dsme'
}

export const FZ_COMM_URL = '?source=fanzone&redirectionUrl=';

export const FZ_POST_MAPPER = {
  "remindMeLaterPrefDate": "REMINDME_LATER_PREF_DATE",
  "remindMeLaterCount": "REMINDME_LATER_COUNT",
  "dontShowMeAgainPref": "DONT_SHOW_ME_AGAIN_PREF",
  "undisplayFanzoneGamePopup": false,
  "newSignPostingSeenDate": "/Date()/",
  "showRelegatedPopupDate": "/Date()/",
  "showSYCPopupDate": "/Date()/",
  "undisplayFanzoneGamesTooltip": false
}

export const FZ_GET_MAPPER = {
  "remindMeLaterPrefDate": null,
  "remindMeLaterCount": 0,
  "dontShowMeAgainPref": false,
  "undisplayFanzoneGamePopup": false,
  "newSignPostingSeenDate": null,
  "showRelegatedPopupDate": null,
  "showSYCPopupDate": null,
  "undisplayFanzoneGamesTooltip": false
}

export const Default_Optin_Fields = {
  "remindMeLaterPrefDate": null,
  "remindMeLaterCount": 0,
  "dontShowMeAgainPref": false,
}

export const FANZONE_GAMES = {
  SUPPORTED_GAMES: [
    { 
      GAME_NAME: 'SLOT_RIVALS',
      CMS_FLAG_NAME: 'showSlotRivals',
      GAME_VARIANT_NAME: 'slotmasterfanzone',
      GAME_DISPLAY_NAME: 'Fanzone Clash of the Day'
    },
    {
      GAME_NAME: 'SCRATCH_CARDS',
      CMS_FLAG_NAME: 'showScratchCards',
      GAME_VARIANT_NAME: 'pariplayfanzonescratch',
      GAME_DISPLAY_NAME: 'Fanzone Golden Goals'
    }
  ],
  SUPPRESS_GAMES_RGY_USERS: ['SLOT_RIVALS'],
  CHANNELID: {
    ANDROID: 'AW',
    IOS: 'IW',
    IN: 'IN',
    AN: 'AN'
  },
  PREVIOUS_CASINO_GAME_CLOSED: 'PREVIOUS_CASINO_GAME_CLOSED',
  PREVIOUS_CASINO_GAME_CLOSED_ACK: 'PREVIOUS_CASINO_GAME_CLOSED_ACK',
  CASINO_GAME_CLOSED: 'CASINO_GAME_CLOSED'
};

export const GTM_DATA_FZ_GAMES = {
  EVENT: 'Event.Tracking',
  CATEGORY_EVENT : 'fanzone',
  LABEL_EVENT: 'fanzone games',
  ACTION_EVENT: 'click',
  URL_CLICKED: 'not applicable',
  LOCATION_NAMES: {
    SLOT_RIVALS : 'slot rivals',
    SCRATCH_CARDS: 'Scratch Cards'
  },
  CTA_NAME: 'play now cta'
}


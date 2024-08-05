export enum PROPERTY_TYPE {
  BACKGROUND_IMAGE = 'backgroundImage',
  INNER_HTML = 'innerHTML',
  SCROLL = 'overflow'
}

export const FREE_RIDE_DIALOG_CONSTS = {
    SPLASH_POPUP: 'splash-popup',
    SPLASHPOPUP_MODEL_OPEN: 'splashPopup-modal-open',
    FREERIDE_OVERLAY: 'freeRideOverlay',
};

export const FREE_RIDE_HTML = {
  DIV: 'div',
  SPAN: 'span',
  CLICK: 'click',
  BUTTON: 'button',
  HIDDEN: 'hidden',
};

export const FREE_RIDE_MESSAGES = {
  ERROR_MSG: 'We are sorry but something has gone wrong with your Free Ride. Please try again later'
};

export const FREE_RIDE_CONSTS ={
    FREE_RIDE_OVERLAY: '#freeRideOverlay',
    HIDE_OVERLAY: 'hideOverlay',
    CONTENT_AREA: '.content-area',
    LOADING_CHAT: '.loadingChat',
    MAIN_IMAGE: '.mainImage',
    SUB_HEADING: '.subHeading',
    HEADING_IMAGE: '.headingImage',
    BANNER_CONTAINER: '.bannerContainer',
    FREE_RIDE_CAMPAIGN: 'freeride-campaign',
    FREE_RIDE_SPLASH: 'freeride-splashpage',
    OPTION_CONTAINER_CLS: '.optionContainer',
    BODY: 'html',
    RESET_VALUE: 0,
    START_INDEX: 1,
    SECOND_INDEX: 2,
    OPTION_NUM: 5,
    HORSE_TYPE_NUM: 6,
    SHORT_DELAY: 500,
    SELECTION_DELAY: 200,
    DELAY: 2000,
    LONG_DELAY: 3600,
    FREE_RIDE_TAG: 'FRRIDE',
    SOURCE: 'source',
    CONTENT: 'content',
    SRC: 'src',
    QUESTION: 'question',
    SUMMARY: 'summary',
    STEP_COUNT: 'stepCount',
    OPTION_CONTAINER: 'optionContainer',
    HORSE_SUMMARY: 'summary',
    HORSE_SUMMARY_DATA: 'summaryData',
    HORSE_SUMMARY_DETAILS: 'summaryDetails',
    RATE_RATING: 'Rating: ',
    HORSE_TYPE: 'Horse: ',
    HORSE_ODDS: 'Odds: ',
    SILK_IMG: 'silk-img',
    JOCKEY_PREFIX: 'J: ',
    CATEGORY_NAME: 'Horse Racing',
    CTA_TO_RACECARD: 'GO RACING',
    CTA_BTN: 'ctaBtn',
    CTA_CONTAINER: 'ctaContainer',
    ANSWER_OPTION: 'answer-option',
    SELECTED_ANSWER: 'selectedAnswer',
    YES: 'Y',
    SOUND_EFFECTS: 'Sound effects',
    NEW_DISPLAY: 'newDisplay',
    ANSWER: 'answer',
    DEFAULT_JERSEY: './assets/defaultJersey.svg',
    FREERIDE_DETAILS: 'FR_Details',
    FR_CAMPAIGN_DATA: 'CampData',
    FREE_RIDE_MODULE: 'Free Ride'
};

export const RESULT_DATA_CONFIG = [
    {
      parentElem: 'resultElem',
      childElem: 'heading'
    },
    {
      parentElem: 'textSpan',
      childElem: 'ans1'
    },
    {
      parentElem: 'textSpan',
      childElem: 'ans2'
    },
    {
      parentElem: 'textSpan',
      childElem: 'ans3'
    },
    {
      parentElem: 'textSpan',
      childElem: 'ans4'
    },
    {
      parentElem: 'imageSpan',
      childElem: 'silkImage'
    },
    {
      parentElem: 'resultElem',
      childElem: 'imageSpan'
    },
    {
      parentElem: 'resultElem',
      childElem: 'textSpan'
    }
  ];

export const HORSE_DATA_SUMMARY_CONFIG = [
  { 'savedDetailsElem': [FREE_RIDE_HTML.DIV, '', FREE_RIDE_CONSTS.SUMMARY] },
  { 'ans1': [FREE_RIDE_HTML.SPAN, FREE_RIDE_CONSTS.RATE_RATING, FREE_RIDE_CONSTS.HORSE_SUMMARY_DETAILS ]},
  { 'ans2': [FREE_RIDE_HTML.SPAN, FREE_RIDE_CONSTS.HORSE_TYPE, FREE_RIDE_CONSTS.HORSE_SUMMARY_DETAILS ]},
  { 'ans3': [FREE_RIDE_HTML.SPAN, FREE_RIDE_CONSTS.HORSE_ODDS, FREE_RIDE_CONSTS.HORSE_SUMMARY_DETAILS ]}
];

export const HORSE_DATA_CONFIG = [
    {'resultElem': ['div', '', 'resultContainer', 'question']},
    {'textSpan': ['span', '', 'resultText']},
    {'imageSpan': ['span', '', 'resultImg']},
    {'silkImage': ['div', '', 'silk-img']},
];


import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';
export const FIVE_A_SIDE_CHANNELS = {
  EVENT: 'sEVENT',
  SCOREBOARD: 'sSCBRD',
  CLOCK: 'sCLOCK',
  MARKET: 'sEVMKT',
  SELECTION: 'sSELCN'
};

export const RULES_TABS: ITab[] = [{
  id: 'prizes',
  label: 'PRIZES',
  title: 'PRIZES',
  isFiveASideNewIconAvailable: false,
  url: ''
}, {
  id: 'faqs',
  label: 'FAQs',
  title: 'FAQs',
  isFiveASideNewIconAvailable: false,
  url: ''
}, {
  id: 'terms-and-conditions',
  label: 'T&Cs',
  title: 'T&Cs',
  isFiveASideNewIconAvailable: false,
  url: ''
}
];

export const RULES_DOM = {
  backButton: '.back-btn',
  returnToLobby:'.return-to-lobby',
  rulesParent: '.rules-parent',
  firstRule: '.rules-info-1',
  thirdRule: '.rules-info-3',
  minAmount: '.min-amount',
  buildButton: '.build-btn',
  iconContent: '.icon-content',
  textContent: '.text-content',
  rulesInfo: '.rules-info',
  rulesSubHeader: 'rules-sub-header',
  userEntries: {
    normal: '.user-entries-normal',
    bold: '.user-entries-bold',
    parent: '.entries-per-user'
  },
  totalEntries: {
    normal: '.total-entries-normal',
    bold: '.total-entries-bold',
    parent: '.total-entries'
  },
  buildButtonDisabledColor: '#c5de91',
  displayNone: 'none',
  iconWidth: '8%',
  textWidth: '92%',
  btnMargin: '10px 90px',
  buildButtonWidth: '516px'
};

export const GTM_EVENTS = {
  BUILD: {
    category: '5-A-Side Showdown',
    action: 'Build',
    label: '/5-a-side'
  },
  LOGIN: {
    category: '5-A-Side Showdown',
    action: 'Login',
    label: '/5-a-side'
  },
  RULES: {
    category: '5-A-Side Showdown',
    action: 'click',
    label: 'rules'
  },
  HOME_WIDGET: {
    category: '5-A-Side Showdown',
    action: 'click',
    label: 'HomePage'
  },
  FOOTBALL_WIDGET: {
    category: '5-A-Side Showdown',
    action: 'click',
    label: 'FootballPage'
  },
  OPENBET: {
    category: '5-A-Side Showdown',
    action: 'click',
    label: 'MyBetsPage'
  },
  POSITION_SUMMARY_WIDGET: {
    category: '5-A-Side Showdown',
    action: 'Open',
    label: 'ViewAllEntries'
  },
  JUMP_TO_ENTRY: {
    category: '5-A-Side Showdown',
    action: 'Click',
    label: 'JumpToEntry'
  },
  WIDGET: {
    category: '5-A-Side Showdown',
    action: 'click',
    label: '/5-a-side/live-leader-board'
  },
  FAQ: {
    category: '5-A-Side Showdown',
    action: 'FAQs'
  },
  OPENENTRY: {
    category: '5-A-Side Showdown',
    action: 'open team'
  },
  NEXT_STEP_1_LABEL: 'next – step 1',
  NEXT_STEP_2_LABEL: 'next – step 2',
  NEXT_STEP_3_LABEL: 'next – step 3',
  NEXT_STEP_3_FINAL_LABEL: 'next – step 3 final',
  NEXT_STEP_4_LABEL: 'next – step 4'
};

export const REMOVE_ELEMENTS = ['.back-btn', '.build-btn', '.rules-btn'];
export const PRIZEPOOL = {
  prizeTypeDesc: {
    cash: '',
    freebet: 'Free Bet',
    ticket: 'Ticket',
    voucher: 'Voucher',
  },
  freebet: 'freebet',
  ticket: 'ticket',
  voucher: 'voucher',
  cash: 'cash',
  userCurrency: '£',
  firstSuffixRange: '1',
  secondSuffixRange: '2',
  thirdSuffixRange: '3'
};

export const LIVE_SERV_CHANNELS = {
  EVENT: 'sEVENT',
  SCOREBOARD: 'sSCBRD',
  CLOCK: 'sCLOCK',
  MARKET: 'sEVMKT',
  SELECTION: 'sSELCN'
};

export const SHOWDOWN_CHANNELS = {
  EVENT: 'EVENT',
  SCORE: 'SCORE',
  CLOCK: 'CLOCK'
};

export const SHOWDOWN_LS_CHANNELS = {
  EVENT: 'EVENT::',
  SCORE: 'SCORE::',
  CLOCK: 'CLOCK::'
};

export const PRIORITY_SIGNPOSTINGS = {
  summary: false,
  size: false,
  totalPrizes: false,
  teams: false,
  firstPlace: false,
  vouchers: false,
  tickets: false,
  freeBets: false
};

export const SHOWDOWN_CARDS = {
  SIMPLE: 'Simple',
  POUND: 'POUND',
  POUND_ENTRY: 'POUND_ENTRY',
  SUMMARY: 'SUMMARY',
  SIZE: 'SIZE',
  CONTEST_SIZE: 'CONTEST_SIZE',
  TOTAL_PRIZES: 'TOTAL_PRIZES',
  ENTRIES: 'ENTRIES',
  TOFIRST: 'TOFIRST',
  VOUCHERS: 'VOUCHERS',
  TICKETS: 'TICKETS',
  FREEBETS: 'FREEBETS',
  SPONSOR_LOGO: 'https://cdn.zeplin.io/60103c71f2dbeb25375e487b/assets/C1F11368-4393-44F2-8E37-0F544AB2A48B.png',
  VOUCHER_LOGO: 'https://cdn.zeplin.io/60103c71f2dbeb25375e487b/assets/60C42072-871C-459B-AEBC-7958C5FF8FBF.png',
  EXTRA_TIME_PERIODS : ['EXTRA_TIME_FIRST_HALF', 'EXTRA_TIME_SECOND_HALF',
  'EXTRA_TIME_HALF_TIME'],
  GA_TRACKING: {
    eventCategory: '5-A-Side Showdown',
    eventAction: 'showdown card'
  },
  TUTORIAL_GA_TRACKING: {
    eventCategory: '5-A-Side Showdown',
    eventAction: 'click',
    eventLabel: 'tutorial'
  },
  LEADERBOARD_BASE_URL: '/5-a-side/leaderboard',
  LEADERBOARD_URL: '/5-a-side/pre-leader-board',
  LIVE_LEADERBOARD_URL: '/5-a-side/live-leader-board',
  POST_LEADERBOARD_URL: '/5-a-side/post-leader-board',
  MYSHOWDOWNS: 'MY_SHOWDOWNS',
  LAST7DAYS: 'LAST7DAYS',
  LAST_7_DAYS: 'Last 7 Days',
  TODAY: 'Today',
  DAYS: { 'today': 'Today', 'tomorrow': 'Tomorrow' },
  DAY_CATEGORIES: [
    'today', 'tomorrow'
  ],
  MY_SHOWDOWNS: 'MY SHOWDOWNS (',
  MY_LEADERBOARDS: 'MY LEADERBOARDS (',
  TITLE: '5-A-SHOWDOWN',
  ANIMATION_DELAY: 5000
};

export const LEADERBOARD_WIDGET = {
  LEADERBOARD_URL: '/5-a-side/leaderboard',
  INITIAL_ENTRY_CHANNEL: 'MYENTRIES',
  LOBYY_URL: '/5-a-side/lobby',
  HOME: '/'
};

export const PRIZE_TYPES = {
  FREEBET: 'freebet',
  TICKET: 'ticket',
  VOUCHER: 'voucher',
  CASH: 'cash',
};

export const ENTRYINFO = {
  DETAILS: 'details',
  SUMMARY: 'summary',
  STATUS: { status: 'Won' },
  PAGE_TITLE: 'LiveLeaderBoard',
  PAGE_CATEGORY: 'Leaderboard',
  MAIN_LEADERBOARD: 'main leaderboard',
  OPEN_ACTION: 'open',
  CLOSE_ACTION: 'close',
  MY_ENTRIES: 'my entries'
};

export const STATUS = {
  LOST: 'LOST',
  WON: 'WON'
};

export const LIVESERVELISTNERS = {
  INITIAL_DATA: 'LDRBRD_INITIAL_DATA',
  MY_INITIAL_DATA: 'MYENTRIES',
  ENTRYINFO: 'ENTRYINFO'
};

export const DYNAMIC_CLASSES = {
  DIGIT_THREE: 'digitThree',
  DIGIT_FIVE: 'digitFive',
  DIGIT_SIX: 'digitSix',
  DIGIT_SEVEN: 'digitSeven',
  DEFAULT: 'defaultrankStyle'
};

export const EVENTSTATUS = {
  POST: 'post',
  LIVE: 'live',
  PRE: 'pre'
};

export const ENTRY_CONFIRMATION = {
  entryConfirmation: 'EntryConfirmation',
  entryConfirmationTerms:'Player restrictions apply. Full T&Cs apply.*',
  viewShowDown: 'VIEW ENTRY',
  ctaGtmTracking: {
    eventCategory: '5-A-Side Showdown',
    eventLabel: 'click',
    eventAction: 'view entry'
  },
  loadViewEntry: {
    eventCategory: '5-A-Side Showdown',
    eventLabel: 'load',
    eventAction: 'view entry'
  },
  realUser: 'realUser',
  testUser: 'testUser',
  testAccount: 'testAccount',
  realAccount: 'realAccount',
  testAccountTokens: ['testgvccl', 'testgvcld', '@internalgvc.com'],
  slideUpClassName: 'entryconfirm-slide-up',
  contestSelectionClassname: 'contestselwrapper-slide-up'
};

export const DEFAULT_TEAM_COLOURS = {
  primary: '#777',
  secondary: '#675d5d'
};

export const LIVE_SERVE_KEY = {
  LEADERBOARD: 'leaderboard',
  MYENTRIES: 'myentries',
  LDRBRD: 'LDRBRD'
};

export const MULTI_PROGRESS_COLOURS = {
  lostcolor: '#c81a21', //  red
  winnigcolor: '#78b200' // green
};

export const PUBSUB_API = {
  LEADERBOARD_EVENT_RESULTED: 'LEADERBOARD_EVENT_RESULTED',
  LEADERBOARD_EVENT_STARTED: 'LEADERBOARD_EVENT_STARTED',
  // Showdown Lobby
  SHOWDOWN_LIVE_CLOCK_UPDATE: 'SHOWDOWN_LIVE_CLOCK_UPDATE',
  SHOWDOWN_LIVE_SCORE_UPDATE: 'SHOWDOWN_LIVE_SCORE_UPDATE',
  SHOWDOWN_LIVE_EVENT_UPDATE: 'SHOWDOWN_LIVE_EVENT_UPDATE',
  SHOWDOWN_EVENT_STARTED: 'SHOWDOWN_EVENT_STARTED',

  // Showdown
  CLOSE_ALL_ENTRIES: 'CLOSE_ALL_ENTRIES',
  CLOSE_ALL_ENTRIES_OVERLAY: 'CLOSE_ALL_ENTRIES_OVERLAY',
  LEG_OUTCOME_UPDATES:'LEG_OUTCOME_UPDATES',
  MY_ENTRY_UPDATE:'MY_ENTRY_UPDATE',
  OUTCOME_CHANGES:'OUTCOME_CHANGES',
  CLOSE_EVERY_ENTRY_DETAILS:'CLOSE_EVERY_ENTRY_DETAILS',
  SHOWDOWN_LIVE_EVENT_RESULTED: 'SHOWDOWN_LIVE_EVENT_RESULTED',
  CLOSE_OVERLAY_MY_ENTRIES: 'CLOSE_OVERLAY_MY_ENTRIES',
  PUBLISH_LEADERBOARD: 'PUBLISH_LEADERBOARD',
  LEADERBOARD_UPDATE: 'LEADERBOARD_UPDATE'
};

export const GTM_RULES_DATA = {
  eventCategory: '5-A-Side Showdown',
  eventAction: 'click',
  eventLabel: 'rules'
};

export const TIME_OUTS = {
  progressbar: 4000,
  showOverlay: 1000
};

export const welcome_GA_Tag = {
  videoGA: {
    eventCategory: '5-A-Side Showdown',
    eventAction: 'Play Button',
    eventLabel: '5-A-Side Leaderboard Welcome Overlay'
  },
  getStartedGa: {
    eventCategory: '5-A-Side Showdown',
    eventAction: 'tutorial',
    eventLabel: 'get started'
  },
};

export const LOBBY_OVERLAY = {
  ID: 'fiveaside-lobby-tutorial',
  CLASS: 'fiveaside-lobby-overlay',
  ARROW_PRIZES: '#arrow-prizes',
  SIGN_POST: 'fiveaside-sign-posting',
  ID_SIGN_POST: '#sign-postings',
  ARROW_SIGNPOST: '#arrow-signposting',
  SIGNPOST_CONTENT: '#signposting-content',
  ARROW_ENTRY: '#arrow-entry-prizes',
  ARROW_CARD: '#showdown-card-arrow',
  CARD_INFO_ID: '#card-info-content',
  BANNER_ID: '#banner-section',
  ID_CARD_TOTAL_PRIZES: '#card-total-prizes',
  ID_ENTRY_PRIZES: '#entry-prizes',
  ID_CARD_ENTRY_INFO: '#card-entry-info',
  ID_ENTRY_INFO: '#entry-info',
  ID_CARD_MAIN: '#showdown-card-main',
  ID_CARD_INFO: '#showdown-card-info',
  FINISH: 'finish',
  STYLE: {
    TRANSFORM: 'transform',
    TOP: 'top',
    BOTTOM: 'bottom',
    LEFT: 'left',
    RIGHT: 'right',
    HEIGHT: 'height',
    WIDTH: 'width',
    BG_COLOR: 'background-color',
    SIGN_ROTATION: 'rotate(270deg)',
    ENTRY_ROTATION: 'rotate(180deg)',
    DEFAULT_BLACK: '#000000e0',
    UNSET: 'unset'
  },
  CLASS_LEADERBOARD_CONTAINER: '.leaderboard-container',
  LOBBY_DATA_RELOADED: 'LOBBY_DATA_RELOADED',
  LOBBY_DATA_RELOADED_COMPLETED: 'LOBBY_DATA_RELOADED_COMPLETED'
};

export const LIVE_OVERLAY = {
  YOUTUBE: 'https://www.youtube.com/embed/',
  ID: 'fiveaside-live-tutorial',
  CLASS: 'five-a-side-live-event-overlay',
  OVERLAY: 'liveOverlay',
  WELCOME_OVERLAY: 'showdownOverlay',
  ID_SUMMARY_EXPANDED: '#entry-details',
  ID_MY_ENTRY_YOUR_TEAM_EXPAND: '#my-entry-your-team-expand',
  SEL_ENTRY_SUMMARY: 'fiveaside-entry-summary',
  ID_MY_ENTRY_YOUR_TEAM: '#my-entry-your-team',
  SEL_MYENTRY_PROGRESS: 'fiveaside-multientry-progress',
  ID_ENTRY_PROGRESS_INFO: '#entry-progress-info',
  ID_LEADERBOARD_INFO: '#leaderboard-info',
  ID_LEADERBOARD_TITLE: '#live-leaderboard-title',
  ID_CARD_INFO_CONTENT: '#card-info-content',
  ID_MY_ENTRY_TEAM_ARROW: '#my-entry-team-arrow',
  ID_ARROW_ENTRY_EXPAND: '#arrow-entry-expand',
  ID_EXPAND_TEAM_PROGRESS: '#expand-team-progress-step',
  ID_PROGRESS_ARROW: '#progressbar-arrow',
  ID_ENTRY_TOP_PROGRESS_CONTENT: '#entry-top-progress-info',
  FINISH: 'finish',
  SEL_MYENTRY_WIDGET: 'fiveaside-myentry-widget',
  SET_STYLE: 'setStyle',
  FOCUS: '#live-overlay-click',
  ID_PROGRESSBAR_OVERLAY: '#progres-bar-overlay',
  ID_LIVE_LEADERBOARD_ITEM: '#live-leaderboard-item',
  CLASS_LIVE_LEADERBOARD_TITLE: '.leader-board-title',
  ID_LEGS_LIST_DISPLAY: '#legs-list-overlay',
  CLASS_LEADERBOARD_CONTAINER: '.leaderboard-container',
  ENTRY_OPENED_TUTORIAL_OVERLAY: 'ENTRY_OPENED_TUTORIAL_OVERLAY',
  LAUNCH_LIVE_TUTORIAL: 'LAUNCH_LIVE_TUTORIAL',
  TIMEOUT_DURATION: 5000,
  TUTORIAL_GA_TRACKING: {
    eventCategory: '5-A-Side Showdown',
    eventAction: 'click',
    eventLabel: 'Live-Event Leaderboard Tutorial Link',
    location: 'live-leaderboard'
  }
};

export const CONTEST_SELECTION = {
 STATIC_BLOCK_URL : 'contest-selection-betslip-info',
 CAROUSAL_ID :  'contest-carousel',
 FIRST_PRIZE : 'First Prize',
 ENTRY_FEE_COMMA_SEP : 'Entry Fee,',
 ENTRY_FEE : 'Entry Fee',
 CASH : 'Cash',
 VOUCHER : 'Voucher',
 TICKET : 'Ticket',
 FREEBET : 'FreeBet',
 EURO: '£',
 MORE: ' + More ',
 PENCE: 'p'
};

export const SELECTED_CONTEST_CHANGE = 'selectedContestChange';

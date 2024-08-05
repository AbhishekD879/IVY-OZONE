export const FANZONE = {
  football: 'football',
  activeTab: {
    id: 'now-next',
    title: 'NOW & NEXT',
    url: '/fanzone/sport-football/$teamName/now-next',
    visible: true,
    showTabOn: 'both'
  },
  activeTabId: 'now-next',
  defaultTab: 'now-next',
  fanzoneDisplay: 'now-next',
  nowandnext: {
    tabName: 'NOW & NEXT',
    id: 'now-next',
    url: '/fanzone/sport-football/$teamName/now-next'
  },
  club: {
    tabName: 'CLUB',
    id: 'club',
    url: '/fanzone/sport-football/$teamName/club'
  },
  stats: {
    tabName: 'STATS',
    id: 'stats',
    url: '/fanzone/sport-football/$teamName/stats'
  },
  games: {
    tabName: 'Fanzone Games',
    id: 'games',
    url: '/fanzone/sport-football/$teamName/games'
  },
  initstateoffanzone: {
    directiveName: null,
    modules: [],
    showTabOn: null,
    title: null,
    visible: null
  },
  Notification_DATA : {
    firstPopUpTitle: "Notification pop up",
    secondPopUpTitle: "Pop UP",
    firstNotificationPopUpDescription: 'A message telling the user they can receive push notifications on mobile device to receive "x, y, z" over on their mobile app.',
    secondNotificationPopUpDescription: "Lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum please write your team name below.",
    PopUpSubscribe: "Subscribe",
    PopUpExit: "EXIT",
    PopUpConfirm: "CONFIRM"
  },
  FanzoneRoutes: {
    homepath: '',
    nowandnextpath: '',
    clubpath: 'club',
    statspath: 'stats',
    gamespath: 'games',
    showyourcolors: 'show-your-colours'
  },
  fanzoneId: 'Manchester',
  modulePath: 'content/teasers?path=fanzone',
  desktopPath: 'content/teasers?path=fanzone',
  fanzoneIndex: 'fanzone',
  dialogbuttonpreferences: {
    imIn: 'i-m-in',
    remindMeLater: 'remind-later',
    dontShowMeAgain: 'dont-show-me'
  }
};
export const fanzone = 'fanzone';
export const FANZONE_CATEGORY_ID = 160;
export const fanzoneRoutePath = '/show-your-colours';
export const fanzoneVacationPath = '/vacation';
export const pubSubChannelName = 'fanzoneHome';
export const clubErrorMsg = 'No Clubs available at the moment';
export const fanzoneHeading = 'Fanzone';
export const userData = 'USER';
export const CUSTOM_TEAM_ID = 'FZ001';
export const UNSUBSCRIBE_CUSTOM_TEAM_ID = 'FZ001_UNSUBSCRIBE';
export const fanzoneEmailKey = 'fzOptin';
export const SHOW_YOUR_COLORS = {
  FANZONE: 'Fanzone',
  SHOW_YOUR_COLORS: 'show-your-colours',
  I_DONOT_SUPPORT_ANY_TEAM: 'iDonotSupportAnyTeam',
  SELECTED_TEAM: 'selectedTeam',
  CUSTOM_TEAM_NAME:'customTeamName',
  DAYS_TO_CHANGE_TEAM: 'daysToChangeTeam',
  TEAM_NAME: 'teamName',
  TEAM_ID: 'teamId',
  CUSTOM_TEAM_ID: 'FZ001',
  FOOTBALL_LANDING_PAGE_PATH:'/sport/football',
  CTA_BUTTONS: {
      IM_IN: "I'm In",
      CONFIRM: "CONFIRM",
      EXIT: "EXIT",
      LOGIN: "LOG IN TO CONFIRM",
      SELECT_DIFFERENT_TEAM: "SELECT DIFFERENT TEAM"
  },
  DIALOG_NAME: {
      TEAM_CONFIRMATION: 'teamConfirmation',
      NO_SUPPORT_TO_TEAM: 'NoSupport2AnyTeam'
  },
  FOOTBALL_SPORT_ID: 16,
  GTA: {
    TRACK_EVENT: 'trackEvent',
    SELECT: 'select',
    DE_SELECT: 'de-select',
    SHOW_UR_COLORS: 'show your colors',
    I_DONT_SUPPORT: 'iDonotSupportAnyTeam',
    TIME_NOT_COMPLETE: 'time to change selection not completed',
    FREE_TEXT_INPUT: 'free text input',
    CONFIRMATION_SCREEN: 'confirmation screen'
  },
  USER_DATA: {
    IM_IN: 'iMIn',
    TEAM_ID: 'teamId',
    TEAM_NAME: 'teamName'
  },
  FANZONE_SYT_POPUP: 'fanzone',
  SYC_PAGE: 'sycPage',
  CHANGE_TEAM: 'CHANGE TEAM'
}
export const headerChannelName = 'fanzoneHeader';
export const bmaChannelName = 'fanzoneBmaMainBanner';
export const GTM_DATA_FZ_TAB = {
  EVENT: 'trackEvent',
  EVENT_ACTION: 'tab',
  EVENT_CATEGORY: 'fanzone',
  EVENT_LABEL:''
}
export const FanzoneHomeTagName = 'FanzoneAppHomeComponent';
export const FANZONETEASERDATA = [
  {
      "type": "segmentDefault",
      "teasers": [
          {
              "backgroundImage": {
                  "src": "https://scmedia.cms.test.env.works/$-$/576b7e3d75394650b21d13f3bdc17a50.jpg",
                  "alt": "MarqueeFootBall",
                  "width": 672,
                  "height": 336
              },
              "bannerLink": {
                  "url": "https://sports.ladbrokes.com/home/featured",
                  "attributes": {}
              },
              "itemId": "{32ACDBCF-D0CD-4194-91EA-A49182D0473D}",
              "itemName": "t1"
          }
      ]
  }
];
export const FANZONETEASEREMPTYDATA = [
  {
      "type": "segmentDefault",
      "teasers": null
  }
];
export const FANZONE_OUTRIGHTS = {
  PUBSUB_CHANNEL_NAME: 'FanzoneAppOutrightsComponent',
  PUBSUB_MODULE_NAME: 'fanzone-outrights',
  BY_LEAGUE_EVENTS_ORDER: ['displayOrder', 'startTime', 'name'],
  PREMIER_LEAGUE: {
    TRACK_EVENT: 'trackEvent',
    PREMIER_LEAGUE: 'Premier League',
    LEAGUE_TABLE: 'league table',
    INLINE_STATS: 'in-line stats',
    CATEGORYID: '16',
    TYPEID: '442'
  }
};

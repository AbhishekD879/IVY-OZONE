export const POSITIONS = {
  Goalkeeper: 'GK',
  Defender: 'DF',
  Midfielder: 'MF',
  Forward: 'FW'
};

export const GOALKEEPER_MARKETS = ['To Keep A Clean Sheet', 'To Concede'];
export const NO_BUTTONS_MARKETS = ['To Be Carded', 'To Keep A Clean Sheet'];

export const MARKETS = {
  Passes: 'passes',
  Tackles: 'tackles',
  Shots: 'shots',
  'Shots On Target': 'shotsOnTarget',
  'Shots Outside The Box': 'shots',
  Assists: 'assists',
  Offsides: 'offsides',
  Crosses: 'passes',
  'Goals Inside The Box': 'goals',
  'Goals Outside The Box': 'goals',
  'To Concede': 'conceeded',
  'To Keep A Clean Sheet': 'cleanSheets',
  'To Be Carded': 'cards',
  'Goals': 'goals'
};

export const STATS_TITLES = {
  'To Concede': 'Goals Conceded per game',
  'To Keep A Clean Sheet': 'Clean Sheets',
  Tackles: 'Tackles per game',
  Passes: 'Passes per game',
  Crosses: 'Passes per game',
  Assists: 'Assists',
  Shots: 'Shots per game',
  'Shots On Target': 'Shots On Target per game',
  'Shots Outside The Box': 'Shots per game',
  Goals: 'Goals',
  'Goals Inside The Box': 'Goals',
  'Goals Outside The Box': 'Goals',
  'To Be Carded': 'Cards',
  Offsides: 'Offsides per game'
};

export const DEFAULT_TEAM_COLOURS = {
  primary: '#777',
  secondary: '#675d5d'
};

export const PLAYER_STATS_NAMES = {
  '13': 'To Be Carded',
  '14': 'To Concede',
  '15': 'To Keep A Clean Sheet'
};

export const PLAYER_STATS_IDS = {
  clean_sheet_id: 15
};

export const JOURNEY_SLIDER_MODE = {
  done: 'Done',
  next: 'Next'
};

export const JOURNEY_FREE_BET_SB_TITLE = 'five-a-side-free-bet';

export const PLAYER_STATS_EXCLUDE = [11];
export const OFFSIDES = 'offsides';

export const PITCH_NAVIGATION = {
  playerPage: 'player-page',
  playerList: 'player-list'
};

export const LINE_UPS = {
  overlayKey:'line-ups',
  overlayWrapper: 'div#opta-scoreboard-overlay-wrapper',
  overlay: 'scoreboard-overlay',
  styles: {
    visible: 'visible',
    overlayShown: 'opta-scoreboard-overlay-shown'
  },
  wrapper: {
    parent: 'div',
    parentAttributeId: 'id',
    parentAttributeValue: 'opta-scoreboard-overlay-wrapper'
  },
  scoreboardData: {
    key: 'sb-data',
    provider: 'digital'
  }
};

export const PLAYER_MARKETS = {
  shotsOutside: {
    longTerm: 'shots outside the box',
    shortTerm: 'Shots Outside'
  },
  goalsInside: {
    longTerm: 'goals inside the box',
    shortTerm: 'Goals Inside'
  },
  goalsOutside: {
    longTerm: 'goals outside the box',
    shortTerm: 'Goals Outside'
  }
};

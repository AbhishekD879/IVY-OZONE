export enum flagLabels {
    FLAG_ROUND = '#flag_round_'
}
export enum Time {
    HALF_TIME = 'HT',
    FULL_TIME = 'FT',
    PENALITES = 'PEN'
}
export enum teamSplitter {
    SPLIT ='/ v | vs | - /'
}

export enum IPageYOffset {
    offSetPValue = 80,
    offSetValue = 98,
}

export enum RULES_TAB {
    PRIZES = 'prizes',
    FAQ = 'faqs',
    TERMS_CONDITIONS = 'terms-and-conditions'
}

export enum PROPERTY_TYPE {
    TEXT_CONTENT = 'textContent',
    DISPLAY = 'display',
    BACKGROUND_COLOR = 'background-color',
    INNER_HTML = 'innerHTML',
    CLASS = 'class',
    WIDTH = 'width',
    MARGIN = 'margin'
}

export enum RENDERER_METHOD {
    PROPERTY = 'setProperty',
    STYLE = 'setStyle',
    CLASS = 'addClass'
}

export enum BUTTON_TYPE {
    RULES = 'rules-btn',
    BACK = 'back-btn',
    BUILD = 'build-btn',
    OVERLAY = 'overlay-context',
    WELCOME_CARD = 'welcome-cards',
    RETURN_TO_LOBBY = 'return-to-lobby',
    UNKNOWN = 'unknown'
}

export enum LIVE_EVENT_VALUE {
    UPDATE_COUNT = 20,
    TIME_INTERVAL = 40,
    INITIAL_COUNT = 0,
    LEADERBOARD_LIMIT = 100,
    PUBLISH_LEADERBOARD = 'PUBLISH_LEADERBOARD'
}

export enum FIVEASIDE_STATS_CATEGORIES {
    Score = 'Goals',
    Corners = 'Corners',
    RedCards = 'RedCards',
    CardIndex = 'Booking Points',
    Booking = 'Cards',
    Shots = 'Shots',
    ShotsOnTarget = 'Shots On Target',
    Assists = 'Assists',
    Passes = 'Passes',
    Tackles = 'Tackles',
    Crosses = 'Crosses',
    GoalsInsideBox = 'Goals Inside Box',
    GoalsOutsideBox = 'Goals Outside Box',
    GoalConceded = 'Goals Conceded',
    ShotsOutsideBox = 'Shots Outside Box',
    ShotsWoodwork = 'Shots Woodwork',
    Offsides = 'Offsides'
  }

  export enum FIVEASIDE_STATS_CATEGORIES_SINGULAR {
    Score = 'Goal',
    Corners = 'Corner',
    RedCards = 'RedCard',
    CardIndex = 'Booking Point',
    Booking = 'Card',
    Shots = 'Shot',
    ShotsOnTarget = 'Shot On Target',
    Assists = 'Assist',
    Passes = 'Pass',
    Tackles = 'Tackle',
    Crosses = 'Cross',
    GoalsInsideBox = 'Goal Inside Box',
    GoalsOutsideBox = 'Goal Outside Box',
    GoalConceded = 'Goal Conceded',
    ShotsOutsideBox = 'Shot Outside Box',
    ShotsWoodwork = 'Shot Woodwork',
    Offsides = 'Offside'
  }

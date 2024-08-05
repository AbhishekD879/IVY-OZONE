export const varReasonId_config = {
    101: { svgId: "Var_Goal", description: "Goal" },
    102: { svgId: "Var_Goal", description: "No Goal" },
    301: { svgId: "", description: "Penalty" },
    302: { svgId: "", description: "No Penalty" },
    501: { svgId: "Var_RedCard", description: "Red Card confirmed" },
    502: { svgId: "", description: "No Red Card" },
    601: { svgId: "Var_cardUpdate", description: "Red Card" },
    602: { svgId: "Var_yellowcard", description: "No Red Card" },
    701: { svgId: "Var_jersey", description: "Player originally cautioned/sent off confirmed" },
    702: { svgId: "Var_jersey", description: "Ref cautions/sends off different player" }
};
export const betLegConstants = {
    football: 'FOOTBALL',
    matchCmtryDisplaytime: 60000,
    matchCmtryTimeIdRefreshTime : 0,
    mybets:'myBetsTab',
    cashoutsection:'cashOutSection',
    openBets:'openBets',
    OPTA : 'OPTA',
    underScoreRegex: /__|_/g,
    replacedText: ' ',
    varCode: 601,
    min: 'min',
    mins: 'mins',
    plus: '+',
    mFACTS : 'mFACTS',
    handleVarReasoningUpdates: 'handle-var-reasoning-updates',
    footballId : '16',
    NA:'N/A'
};     
export const enum MYBETS_AREAS {
    WIDGET = 'widget',
    EDP = 'edp'
}

export const enum ALERTS_GTM {
    EVENT_TRACKING = 'Event.Tracking',
    SPORT_ALERT = 'sports alerts',
    MATCH_ALERT = 'match alerts',
    CLICK = 'click',
    BETSLIP = 'betslip',
    QUICK_BET = 'quick bet',
    OPEN_BETS = 'my bets - open bets',
    CASHOUT = 'my bets - cashout',
    EVENT_SCREEN = 'event screen',
    MATCH_ALERT_ICON = 'match alerts icon',
    WIN_ALERT_ICON = 'win alert info icon',
    WIN_ALERT = 'win alert',
    TOGGLE_ON = 'toggle on',
    TOGGLE_OFF = 'toggle off',
    NA = 'not applicable' 
}
export const MATCH_TIME_CONFIG = {
    STOP_FIRST_HALF : 'Half Time',
    STOP_SECOND_HALF: 'FULL TIME',
    STOP_FIRST_HALF_EXTRA_TIME:'Extra Time Half Time',
    STOP_SECOND_HALF_EXTRA_TIME:'STOP SECOND HALF EXTRA TIME',
    START_PENALTY_SHOOTOUT:'GOING TO PENALITY SHOOT OUT',
    STOP_PENALTY_SHOOTOUT:'Penalty Shootout',
    PLAYERS_LINED_UP: 'Match Is Starting Soon',
    START_FIRST_HALF_EXTRA_TIME: 'Going Into Extra Time'
}
export const ALTERD_MATCHFACTS = {
    FREE_KICK_AWARDED: 'FREE KICK',
    GOAL_KICK_AWARDED: 'GOAL KICK',
    SHOT_BLOCKED:'Blocked Shot',
    GOAL_CANCELLED: 'Goal Cancelled'
}
export const UNIQUE_TEMPLATE = {
    200: 'Kick off',
    102:'INJURY_TIME',
    103:'Injury',
    215:'SUBSTITUTION',
    220:'Throw In'
}

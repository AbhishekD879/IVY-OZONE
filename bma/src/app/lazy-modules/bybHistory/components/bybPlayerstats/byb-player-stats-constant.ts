export const BYB_MARKETS = {
    'Appearances': 'appearances',
    'Tackles per game': 'tackles',
    'Goals': 'goals',
    'Assists': 'assists',
    'Shots per game': 'shots',
    'Passes per game': 'passes',
    'Shots On Target per game': 'shotsonTarget',
    'Cards': 'cards',
    'Goals Conceded per game': 'conceeded',
    'Clean Sheets': 'cleanSheets',
    'Penalty Saves': 'penaltysaves',
    'Saves per game': 'saves'
};
export const MARKET_ORDER = {
    saves: ['Appearances', 'Goals Conceded per game', 'Clean Sheets', 'Saves per game', 'Penalty Saves'],
    concede: ['Goals Conceded per game', 'Appearances', 'Clean Sheets', 'Saves per game', 'Penalty Saves'],
    cleansheet: ['Clean Sheets', 'Appearances', 'Goals Conceded per game', 'Saves per game', 'Penalty Saves'],
    assists: ['Assists', 'Appearances', 'Goals', 'Shots per game', 'Passes per game'],
    goals: ['Goals', 'Appearances', 'Assists', 'Shots per game', 'Passes per game'],
    'goals inside the box': ['Goals', 'Appearances', 'Assists', 'Shots per game', 'Passes per game'],
    'goals outside the box': ['Goals', 'Appearances', 'Assists', 'Shots per game', 'Passes per game'],
    offsides: ['Appearances', 'Goals', 'Assists', 'Shots per game', 'Passes per game'],
    passes: ['Passes per game', 'Appearances', 'Goals', 'Assists', 'Shots per game'],
    shots: ['Shots per game', 'Appearances', 'Goals', 'Assists', 'Passes per game'],
    'shots outside the box': ['Shots per game', 'Appearances', 'Goals', 'Assists', 'Passes per game'],
    'shots on target': ['Shots On Target per game', 'Appearances', 'Goals', 'Assists', 'Shots per game', 'Passes per game'],
    tackles: ['Tackles per game', 'Appearances', 'Goals', 'Assists', 'Shots per game', 'Passes per game'],
    goalscorer: ['Goals', 'Appearances', 'Assists', 'Shots per game', 'Passes per game'],
    'to be shown a card': ['Cards', 'Appearances', 'Goals', 'Assists', 'Shots per game', 'Passes per game']
};
export const PLAYER_DATA = {
    id: 1, name: '', teamName: '', teamColors: { primaryColour: '', secondaryColour: '' }, appearances: undefined,
    cleanSheets: undefined, tackles: undefined, passes: undefined, crosses: undefined, assists: undefined,
    shots: undefined, shotsOnTarget: undefined, shotsOutsideTheBox: undefined, goalsInsideTheBox: undefined,
    goalsOutsideTheBox: undefined, goals: undefined, cards: undefined, cardsRed: undefined, cardsYellow: undefined,
    position: { long: '', short: '' }, penaltySaves: undefined, conceeded: undefined, saves: undefined, isGK: false
};
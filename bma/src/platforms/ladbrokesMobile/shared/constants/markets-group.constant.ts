/**
 * Config for Football Markets Group
 */
export const MARKETS_GROUP = [
  {
    name: 'Both Teams To Score Other Markets',
    localeName: 'bothTeamsToScore',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'bothHalves',
        marketsNames: 'Both Teams to Score in Both Halves'
      },
      {
        localeName: 'secondHalf',
        marketsNames: 'Both Teams to Score in Second Half'
      }
    ]
  },
  {
    name: '1st Half/ 2nd Half Total Goals',
    localeName: 'halfTotalGoals',
    marketsAvailable: false,
    template: 'row',
    marketSort: ['name'],
    outcomesSort: ['sortOrder'],
    sortOrder: { '0-1': 1, 2: 2, '3+': 3 },
    periods: [
      {
        localeName: 'firstHalf',
        marketsNames: 'First Half Total Goals'
      },
      {
        localeName: 'secondHalf',
        marketsNames: 'Second Half Total Goals'
      }
    ]
  },
  {
    name: 'Draw No Bet',
    localeName: 'drawNoBet',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'matchResult',
        marketsNames: 'Draw No Bet'
      },
      {
        localeName: 'firstHalf',
        marketsNames: 'Half-Time Draw No Bet'
      },
      {
        localeName: 'secondHalf',
        marketsNames: 'Second-Half Draw No Bet'
      }
    ]
  },
  {
    name: 'Double Chance',
    localeName: 'doubleChance',
    marketsAvailable: false,
    template: 'card',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'matchResult',
        marketsNames: ['Double Chance', 'Double chance']
      },
      {
        localeName: 'firstHalf',
        marketsNames: 'Half-Time Double Chance'
      },
      {
        localeName: 'secondHalf',
        marketsNames: 'Second-Half Double Chance'
      }
    ]
  },
  {
    name: 'Player to Score 2 or More Goals',
    localeName: 'playerToScore2',
    marketsAvailable: false,
    template: 'card',
    type: 'teams',
    lessCount: 5,
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    marketsNames: ['Goalscorer - 2 or More', 'Goalscorer - 2 Or More']
  },
  {
    name: 'Player to Score in Both Halves',
    localeName: 'scoreInBothHalves',
    marketsAvailable: false,
    template: 'card',
    type: 'teams',
    lessCount: 5,
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    marketsNames: 'ScoreInBothHalves'
  },
  {
    name: 'Player to Outscore the Opposition',
    localeName: 'outscoreTheBothOpposition',
    marketsAvailable: false,
    template: 'card',
    type: 'teams',
    lessCount: 5,
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    marketsNames: 'PlayerToOutscoreTheOpposition'
  },
  {
    name: '1st Half / 2nd Half Result',
    localeName: 'firstHalfResult',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'firstHalfResult',
        marketsNames: 'First-Half Result'
      },
      {
        localeName: 'secondHalfResult',
        marketsNames: 'Second-Half Result'
      }
    ]
  },
  {
    name: 'Half time/ Full Time Result Market',
    localeName: 'halfFullResult',
    marketsAvailable: false,
    template: 'card',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    marketsNames: 'Half-Time/Full-Time'
  },
  {
    name: 'Total Goals Odd/ Even',
    localeName: 'totalGoalsOddEven',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'matchResult',
        marketsNames: 'Total Goals Odd/Even'
      },
      {
        localeName: 'firstHalfResult',
        marketsNames: 'First Half Total Goals Odd/Even'
      },
      {
        localeName: 'secondHalfResult',
        marketsNames: 'Second Half Total Goals Odd/Even'
      }
    ]
  },
  {
    name: 'Home Team No Bet',
    localeName: 'homeTeamNoBet',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'firstHalfResult',
        marketsNames: 'First-Half Home No Bet'
      },
      {
        localeName: 'secondHalfResult',
        marketsNames: 'Second-Half Home No Bet'
      }
    ]
  },
  {
    name: 'Away Team No Bet',
    localeName: 'awayTeamNoBet',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'firstHalfResult',
        marketsNames: 'First-Half Away No Bet'
      },
      {
        localeName: 'secondHalfResult',
        marketsNames: 'Second-Half Away No Bet'
      }
    ]
  },
  {
    name: 'Result After 15, 30, 60 & 75 Mins',
    localeName: 'resultAfter',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    periods: [
      {
        localeName: 'minsA',
        marketsNames: '15 Minutes Betting'
      },
      {
        localeName: 'minsB',
        marketsNames: '30 Minutes Betting'
      },
      {
        localeName: 'minsC',
        marketsNames: '60 Minutes Betting'
      },
      {
        localeName: 'minsD',
        marketsNames: '75 Minutes Betting'
      }
    ]
  },
  {
    name: 'Handicap Results',
    localeName: 'handicapResults',
    marketsAvailable: false,
    lessCount: 4,
    type: ['handicapNamePlus', 'minorCode'],
    template: 'cardHeader',
    header: [{ name: 'Home' }, { name: 'Tie' }, { name: 'Away' }],
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['-name'],
    periods: [
      {
        localeName: 'matchResult',
        marketsNames: 'Handicap Match Result'
      },
      {
        localeName: 'firstHalfResult',
        marketsNames: 'Handicap First Half'
      },
      {
        localeName: 'secondHalfResult',
        marketsNames: 'Handicap Second Half'
      }
    ]
  },
  {
    name: 'Total Goals by Team',
    localeName: 'totalGoalsByTeam',
    marketsAvailable: false,
    type: ['minorCode', 'marketName'],
    outcomesSort: ['name'],
    marketSort: ['name'],
    template: 'cardHeader',
    header: [{ name: '0' }, { name: '1' }, { name: '2+' }],
    periods: [
      {
        localeName: 'total',
        marketsNames: ['Home Team Total Goals', 'Away Team Total Goals']
      },
      {
        localeName: 'firstHalfResult',
        marketsNames: ['First Half Home Team Total Goals', 'First Half Away Team Total Goals']
      },
      {
        localeName: 'secondHalfResult',
        marketsNames: ['Second Half Home Team Total Goals', 'Second Half Away Team Total Goals']
      }
    ]
  },
  {
    name: 'Match Result & Over/Under 2.5 Goals market',
    localeName: 'matchResultOverUnder25',
    marketsAvailable: false,
    template: 'cardHeader',
    type: 'overUnderMarket',
    outcomesSort: ['sortOrder'],
    marketSort: ['name'],
    sortByHeader: true,
    header: [{ name: 'over', sortOrder: 1 }, { name: 'under', sortOrder: 2 }],
    marketsNames: 'Match Result and Over/Under 2.5 Goals'
  },
  {
    name: 'Match Result & Over/Under 3.5 Goals market',
    localeName: 'matchResultOverUnder35',
    marketsAvailable: false,
    template: 'cardHeader',
    type: 'overUnderMarket',
    outcomesSort: ['sortOrder'],
    marketSort: ['name'],
    sortByHeader: true,
    header: [{ name: 'over', sortOrder: 1 }, { name: 'under', sortOrder: 2 }],
    marketsNames: 'Match Result and Over/Under 3.5 Goals'
  },
  {
    name: 'First Team Goalscorer',
    localeName: 'firstTeamHomeGoalscorer',
    marketsAvailable: false,
    template: 'card',
    type: 'teamSwitch',
    outcomesSort: ['outcomeMeaningMinorCode'],
    marketSort: ['name'],
    lessCount: 5,
    periods: [
      {
        localeName: '',
        marketsNames: 'FirstTeamHomeGoalscorer'
      },
      {
        localeName: '',
        marketsNames: 'FirstTeamAwayGoalscorer'
      }
    ]
  },
  {
    name: 'Player to Score Exact Goals',
    localeName: 'playerToScoreExactGoals',
    marketsAvailable: false,
    template: 'cardHeader',
    type: ['marketHeader', 'teams'],
    outcomesSort: ['sortOrder'],
    marketSort: ['name'],
    headerToMarket: {
      ToScoreExactly1: { name: 1, sortOrder: 1 },
      ToScoreExactly2: { name: 2, sortOrder: 2 },
      ToScoreExactly3: { name: 3, sortOrder: 3 }
    },
    lessCount: 5,
    marketsNames: ['ToScoreExactly1', 'ToScoreExactly2', 'ToScoreExactly3']
  },
  {
    name: 'Player to Score and Their Team to Win',
    localeName: 'playerToScoreResult',
    marketsAvailable: false,
    template: 'cardHeader',
    type: ['marketHeader', 'teams'],
    outcomesSort: ['sortOrder'],
    marketSort: ['name'],
    lessCount: 5,
    headerToMarket: {
      ScoreAndTeamWin: { name: 'Home', sortOrder: 1 },
      ScoreAndTeamDraw: { name: 'Draw', sortOrder: 2 },
      ScoreAndTeamLose: { name: 'Away', sortOrder: 3 }
    },
    marketsNames: ['ScoreAndTeamWin', 'ScoreAndTeamDraw', 'ScoreAndTeamLose']
  },
  {
    name: 'Player to Score First & Result',
    localeName: 'playerToScoreFirst',
    marketsAvailable: false,
    template: 'cardHeader',
    type: ['marketHeader', 'teams'],
    outcomesSort: ['sortOrder'],
    marketSort: ['name'],
    lessCount: 5,
    headerToMarket: {
      ScoreFirstAndTeamWin: { name: 'Home', sortOrder: 1 },
      ScoreFirstAndTeamDraw: { name: 'Draw', sortOrder: 2 },
      ScoreFirstAndTeamLose: { name: 'Away', sortOrder: 3 }
    },
    marketsNames: ['ScoreFirstAndTeamWin', 'ScoreFirstAndTeamDraw', 'ScoreFirstAndTeamLose']
  },
  {
    name: 'Total Goals by Team Other Markets',
    localeName: 'totalGoalsByTeamOther',
    marketsAvailable: false,
    template: 'cardHeader',
    type: ['goalName', 'teamSwitch', 'minorCode'],
    outcomesSort: ['-name'],
    marketSort: ['name'],
    header: [{ name: 'Yes' }, { name: 'No' }],
    periods: [
      {
        localeName: '',
        marketsNames: ['Home Team to Score 2+ Goals', 'Home Team to Score 3+ Goals', 'Home Team to Score 4+ Goals',
          'Home Team to Score 5+ Goals']
      },
      {
        localeName: '',
        marketsNames: ['Away Team to Score 2+ Goals', 'Away Team to Score 3+ Goals', 'Away Team to Score 4+ Goals',
          'Away Team to Score 5+ Goals']
      }
    ]
  },
  {
    name: 'Goal to Be Scored',
    localeName: 'goalToBeScored',
    marketsAvailable: false,
    template: 'row',
    outcomesSort: ['outcomeMeaningMinorCode'],
    periods: [
      {
        localeName: 'bothHalves',
        marketsNames: 'Score Goal in Both Halves'
      },
      {
        localeName: 'firstHalfResult',
        marketsNames: 'Score Goal in First Half'
      },
      {
        localeName: 'secondHalfResult',
        marketsNames: 'Score Goal in Second Half'
      }
    ]
  },
  {
    name: 'Over/Under Total Goals',
    localeName: 'overUnderTotalGoals',
    marketsAvailable: false,
    lessCount: 4,
    type: ['handicapName', 'minorCode'],
    template: 'cardHeader',
    marketSort: ['name'],
    outcomesSort: ['outcomeMeaningMinorCode'],
    header: [{ name: 'over' }, { name: 'under' }],
    headerLabel: 'Total Goals',
    periods: [
      {
        localeName: 'matchResult',
        marketsNames: 'Over/Under Total Goals'
      },
      {
        localeName: 'firstHalf',
        marketsNames: 'Over/Under First Half'
      },
      {
        localeName: 'secondHalf',
        marketsNames: 'Over/Under Second Half'
      }
    ]
  },
  {
    name: 'Over/Under Goals',
    localeName: 'overUnderGoalsTeamA',
    marketsAvailable: false,
    lessCount: 4,
    template: 'cardHeader',
    type: ['headerTeamName', 'handicapName', 'minorCode'],
    marketSort: ['name'],
    outcomesSort: ['outcomeMeaningMinorCode'],
    header: [{ name: 'over' }, { name: 'under' }],
    headerLabel: 'Total Goals',
    periods: [
      {
        localeName: 'matchResult',
        marketsNames: 'Over/Under Home Team Total Goals'
      },
      {
        localeName: 'firstHalf',
        marketsNames: 'Over/Under First Half Home Team Total Goals'
      },
      {
        localeName: 'secondHalf',
        marketsNames: 'Over/Under Second Half Home Team Total Goals'
      }
    ]
  },
  {
    name: 'Over/Under Goals',
    localeName: 'overUnderGoalsTeamB',
    marketsAvailable: false,
    lessCount: 4,
    template: 'cardHeader',
    type: ['headerTeamName', 'handicapName', 'minorCode'],
    marketSort: ['name'],
    outcomesSort: ['outcomeMeaningMinorCode'],
    header: [{ name: 'over' }, { name: 'under' }],
    headerLabel: 'Total Goals',
    periods: [
      {
        localeName: 'matchResult',
        marketsNames: 'Over/Under Away Team Total Goals'
      },
      {
        localeName: 'firstHalf',
        marketsNames: 'Over/Under First Half Away Team Total Goals'
      },
      {
        localeName: 'secondHalf',
        marketsNames: 'Over/Under Second Half Away Team Total Goals'
      }
    ]
  },
  {
    name: 'Popular Goalscorer Markets',
    localeName: 'popularGoalscorerMarkets',
    marketsAvailable: false,
    lessCount: 5,
    template: 'cardHeader',
    type: ['marketHeader', 'teams', 'noGoalscorer'],
    marketSort: ['outcomePrice', 'name'],
    outcomesSort: ['sortOrder'],
    headerToMarket: {
      'First Goalscorer': { name: '1st', sortOrder: 1 },
      'Anytime Goalscorer': { name: 'Anytime', sortOrder: 2 },
      'Goalscorer - 2 Or More': { name: '2 or More', sortOrder: 3 }
    },
    headerLabel: 'PLAYERS',
    marketsNames: ['First Goalscorer', 'Anytime Goalscorer', 'Goalscorer - 2 Or More']
  },
  {
    name: 'Other Goalscorer Markets',
    localeName: 'otherGoalscorerMarkets',
    marketsAvailable: false,
    lessCount: 5,
    template: 'cardHeader',
    type: ['marketHeader', 'teams', 'noGoalscorer'],
    marketSort: ['outcomePrice', 'name'],
    outcomesSort: ['sortOrder'],
    headerToMarket: {
      'Last Goalscorer': { name: 'Last', sortOrder: 1 },
      'Hat trick': { name: 'Hat trick', sortOrder: 2 }
    },
    headerLabel: 'PLAYERS',
    marketsNames: ['Hat trick', 'Last Goalscorer']
  },
  {
    name: 'Number of Teams to Score',
    localeName: 'numberOfTeamsToScore',
    marketsAvailable: false,
    template: 'row',
    marketSort: ['name'],
    outcomesSort: ['sortOrder'],
    sortOrder: { None: 1, One: 2, Both: 3 },
    marketsNames: 'Number of Teams to Score'
  },
  {
    name: 'Half With Most Goals',
    localeName: 'halfWithMostGoals',
    marketsAvailable: false,
    template: 'row',
    marketSort: ['name'],
    outcomesSort: ['sortOrder'],
    sortOrder: { '1st Half': 1, Tie: 2, '2nd Half': 3 },
    marketsNames: 'Half With Most Goals'
  },
  {
    name: 'Time of 1st Home Team Goal',
    localeName: 'TimeOf1stHomeTeamGoal',
    marketsAvailable: false,
    template: 'card',
    marketSort: ['name'],
    outcomesSort: ['name'],
    marketsNames: 'Time of 1st Home Team Goal'
  },
  {
    name: 'Time of 1st Away Team Goal',
    localeName: 'TimeOf1stAwayTeamGoal',
    marketsAvailable: false,
    template: 'card',
    marketSort: ['name'],
    outcomesSort: ['name'],
    marketsNames: 'Time of 1st Away Team Goal'
  }
];

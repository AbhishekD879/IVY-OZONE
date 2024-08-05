import { IBybConfig } from '@lazy-modules/bybHistory/models/byb-selection.model';

/**
 *  BYB and 5-a-side markets config using for stats tracking
 *  Match OPTA statistics to Banach markets
 */

export const BYB_5ASIDE_MARKETS_CONFIG: Map<string, IBybConfig> = new Map(
  [
    [ 'build your bet match betting',
      {
        name: 'Build Your Bet MATCH BETTING',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'matchBettingStatusHandler'
      }
    ],
    [ 'build your bet first half betting',
      {
        name: 'Build Your Bet FIRST HALF BETTING',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'matchBettingStatusHandler'
      }
    ],
    [ 'build your bet second half betting',
        {
          name: 'Build Your Bet SECOND HALF BETTING',
          hasLine: false,
          statCategory: 'Score',
          template: 'binary',
          period: '2h',
          generalInformationRequired: 'teams',
          methodName: 'matchBettingStatusHandler'
        }
    ],
    [ 'build your bet total goals',
        {
          name: 'Build Your Bet TOTAL GOALS',
          hasLine: true,
          statCategory: 'Score',
          template: 'range',
          period: 'total',
          generalInformationRequired: 'teams',
          methodName: 'totalGoalsStatusHandler'
        }
    ],
    [ 'build your bet to be sent off',
        {
          name: 'Build Your Bet TO BE SENT OFF',
          hasLine: true,
          statCategory: 'RedCards',
          template: 'binary',
          period: 'total',
          generalInformationRequired: 'player',
          methodName: 'redCardsPlayerStatusHandler'
        }
    ],
    [ 'build your bet to be shown a card',
        {
          name: 'Build Your Bet TO BE SHOWN A CARD',
          hasLine: true,
          statCategory: 'Booking',
          template: 'binary',
          period: 'total',
          generalInformationRequired: 'player',
          methodName: 'shownCardStatusHandler'
        }
    ],
    [ 'build your bet player to get first booking',
      {
        name: 'Build Your Bet PLAYER TO GET FIRST BOOKING',
        hasLine: false,
        statCategory: 'Booking',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'playerToGetFirstBooking'
      }
    ],
    [ 'build your bet 1st half total goals',
      {
        name: 'Build Your Bet 1ST HALF TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet 2nd half total goals',
      {
        name: 'Build Your Bet 2ND HALF TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet exact total goals',
      {
        name: 'Build Your Bet EXACT TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet total cards',
      {
        name: 'Build Your Bet TOTAL CARDS',
        hasLine: true,
        statCategory: 'Booking',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'totalCards'
      }
    ],
    [ 'build your bet total corners',
      {
        name: 'Build Your Bet TOTAL CORNERS',
        hasLine: true,
        statCategory: 'Corners',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'totalCornersStatusHandler'
      }
    ],
    [ 'build your bet handicap betting',
      {
        name: 'Build Your Bet HANDICAP BETTING',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'handicapBettingStatusHandler'
      }
    ],
    [ 'build your bet correct score',
      {
        name: 'Build Your Bet CORRECT SCORE',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'correctScoreStatusHandler'
      }
    ],
    [ 'build your bet 1st half correct score',
      {
        name: 'Build Your Bet 1ST HALF CORRECT SCORE',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'correctScoreStatusHandler'
      }
    ],
    [ 'build your bet 2nd half correct score',
      {
        name: 'Build Your Bet 2ND HALF CORRECT SCORE',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'correctScoreStatusHandler'
      }
    ],
    [ 'build your bet corners match bet',
      {
        name: 'Build Your Bet CORNERS MATCH BET',
        hasLine: false,
        statCategory: 'Corners',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'cornersMatchBetStatusHandler'
      }
    ],
    [ 'build your bet 1st half corners match bet',
      {
        name: 'Build Your Bet 1ST HALF CORNERS MATCH BET',
        hasLine: false,
        statCategory: 'Corners',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'cornersMatchBetStatusHandler'
      }
    ],
    [ 'build your bet 2nd half corners match bet',
      {
        name: 'Build Your Bet 2ND HALF CORNERS MATCH BET',
        hasLine: false,
        statCategory: 'Corners',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'cornersMatchBetStatusHandler'
      }
    ],
    [ 'build your bet first goalscorer',
      {
        name: 'Build Your Bet FIRST GOALSCORER',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'first',
        generalInformationRequired: 'player',
        methodName: 'goalscorersStatusHandler'
      }
    ],
    [ 'build your bet last goalscorer',
      {
        name: 'Build Your Bet LAST GOALSCORER',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'last',
        generalInformationRequired: 'player',
        methodName: 'goalscorersStatusHandler'
      }
    ],
    [ 'build your bet anytime goalscorer',
      {
        name: 'Build Your Bet ANYTIME GOALSCORER',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'goalscorersStatusHandler'
      }
    ],
    [ 'build your bet to score 2 or more goals',
      {
        name: 'Build Your Bet TO SCORE 2 OR MORE GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalGoalsByPlayerStatusHandler'
      }
    ],
    [ 'build your bet to score 3 or more goals',
      {
        name: 'Build Your Bet TO SCORE 3 OR MORE GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalGoalsByPlayerStatusHandler'
      }
    ],
    [ 'build your bet team to get 1st goal',
      {
        name: 'Build Your Bet TEAM TO GET 1ST GOAL',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'teamToGetFirstGoal'
      }
    ],
    [ 'build your bet team to get 1st booking',
      {
        name: 'Build Your Bet TEAM TO GET 1ST BOOKING',
        hasLine: true,
        statCategory: 'Booking',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'teamToGetFirstBooking'
      }
    ],
    [ 'build your bet team to get 1st corner',
      {
        name: 'Build Your Bet TEAM TO GET 1ST CORNER',
        hasLine: true,
        statCategory: 'Corners',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'team',
        // methodName: 'teamToGetFirstCornerHandler' // not enough stats to handle this market
      }
    ],
    [ 'build your bet red card in match',
      {
        name: 'Build Your Bet RED CARD IN MATCH',
        hasLine: true,
        statCategory: 'RedCards',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'redCardsStatusHandler'
      }
    ],
    [ 'build your bet participant_1 red card',
      {
        name: 'Build Your Bet PARTICIPANT_1 RED CARD',
        hasLine: true,
        statCategory: 'RedCardsByTeamWithYellowCardsWorkAround',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'players', // before was team for statCategory: RedCards
        methodName: 'redCardsParticipantStatusHandler'
      }
    ],
    [ 'build your bet participant_2 red card',
      {
        name: 'Build Your Bet PARTICIPANT_2 RED CARD',
        hasLine: true,
        statCategory: 'RedCardsByTeamWithYellowCardsWorkAround',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'players', // before was team for statCategory: RedCards
        methodName: 'redCardsParticipantStatusHandler'
      }
    ],
    [ 'build your bet most goals 0 - 30 minutes',
      {
        name: 'Build Your Bet MOST GOALS 0 - 30 MINUTES',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'mostGoalsInRange',
      }
    ],
    [ 'build your bet most goals 30 - 60 minutes',
      {
        name: 'Build Your Bet MOST GOALS 30 - 60 MINUTES',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'mostGoalsInRange',
      }
    ],
    [ 'build your bet participant_1 total goals',
      {
        name: 'Build Your Bet PARTICIPANT_1 TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet participant_2 total goals',
      {
        name: 'Build Your Bet PARTICIPANT_2 TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet both teams to score',
      {
        name: 'Build Your Bet BOTH TEAMS TO SCORE',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'bothTeamsToScoreStatusHandler'
      }
    ],
    [ 'build your bet team to get 2nd goal',
      {
        name: 'Build Your Bet TEAM TO GET 2ND GOAL',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'teamToGetSecondGoal'
      }
    ],
    [ 'build your bet participant_1 total corners',
      {
        name: 'Build Your Bet PARTICIPANT_1 TOTAL CORNERS',
        hasLine: true,
        statCategory: 'Corners',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'totalCornersStatusHandler'
      }
    ],
    [ 'build your bet participant_2 total corners',
      {
        name: 'Build Your Bet PARTICIPANT_2 TOTAL CORNERS',
        hasLine: true,
        statCategory: 'Corners',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'totalCornersStatusHandler'
      }
    ],
    [ 'build your bet participant_1 1st half total goals',
      {
        name: 'Build Your Bet PARTICIPANT_1 1ST HALF TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet participant_2 1st half total goals',
      {
        name: 'Build Your Bet PARTICIPANT_2 1ST HALF TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet participant_1 2nd half total goals',
      {
        name: 'Build Your Bet PARTICIPANT_1 2ND HALF TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet participant_2 2nd half total goals',
      {
        name: 'Build Your Bet PARTICIPANT_2 2ND HALF TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet participant_1 1st half total corners',
      {
        name: 'Build Your Bet PARTICIPANT_1 1ST HALF TOTAL CORNERS',
        hasLine: true,
        statCategory: 'Corners',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'team',
        methodName: 'totalCornersStatusHandler'
      }
    ],
    [ 'build your bet participant_2 1st half total corners',
      {
        name: 'Build Your Bet PARTICIPANT_2 1ST HALF TOTAL CORNERS',
        hasLine: true,
        statCategory: 'Corners',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'team',
        methodName: 'totalCornersStatusHandler'
      }
    ],
    [ 'build your bet participant_1 2nd half total corners',
      {
        name: 'Build Your Bet PARTICIPANT_1 2ND HALF TOTAL CORNERS',
        hasLine: true,
        statCategory: 'Corners',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'team',
        methodName: 'totalCornersStatusHandler'
      }
    ],
    [ 'build your bet participant_2 2nd half total corners',
      {
        name: 'Build Your Bet PARTICIPANT_2 2ND HALF TOTAL CORNERS',
        hasLine: true,
        statCategory: 'Corners',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'team',
        methodName: 'totalCornersStatusHandler'
      }
    ],
    [ 'build your bet red card in 1st half',
      {
        name: 'Build Your Bet RED CARD IN 1ST HALF',
        hasLine: true,
        statCategory: 'RedCards',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'redCardsStatusHandler'
      }
    ],
    [ 'build your bet red card in 2nd half',
      {
        name: 'Build Your Bet RED CARD IN 2ND HALF',
        hasLine: true,
        statCategory: 'RedCards',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'redCardsStatusHandler'
      }
    ],
    [ 'build your bet match booking pts',
      {
        name: 'Build Your Bet MATCH BOOKING PTS',
        hasLine: true,
        statCategory: 'CardIndex',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'matchBookingPointsStatusHandler'
      }
    ],
    [ 'build your bet participant_1 booking pts',
      {
        name: 'Build Your Bet PARTICIPANT_1 BOOKING PTS',
        hasLine: true,
        statCategory: 'CardIndex',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'matchBookingPointsStatusHandler'
      }
    ],
    [ 'build your bet participant_2 booking pts',
      {
        name: 'Build Your Bet PARTICIPANT_2 BOOKING PTS',
        hasLine: true,
        statCategory: 'CardIndex',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'matchBookingPointsStatusHandler'
      }
    ],
    [ 'build your bet double chance',
      {
        name: 'Build Your Bet DOUBLE CHANCE',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'doubleChanceStatusHandler'
      }
    ],
    [ 'build your bet to win to nil',
      {
        name: 'Build Your Bet TO WIN TO NIL',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'toWinToNil'
      }
    ],
    [ 'build your bet total goals range',
      {
        name: 'Build Your Bet TOTAL GOALS RANGE',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet 1st half total goals range',
      {
        name: 'Build Your Bet 1ST HALF TOTAL GOALS RANGE',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet 2nd half total goals range',
      {
        name: 'Build Your Bet 2ND HALF TOTAL GOALS RANGE',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet total goals odd/even',
      {
        name: 'Build Your Bet TOTAL GOALS ODD/EVEN',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsOddsEvenStatusHandler'
      }
    ],
    [ 'build your bet 1st half total goals odd/even',
      {
        name: 'Build Your Bet 1ST HALF TOTAL GOALS ODD/EVEN',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsOddsEvenStatusHandler'
      }
    ],
    [ 'build your bet 2nd half total goals odd/even',
      {
        name: 'Build Your Bet 2ND HALF TOTAL GOALS ODD/EVEN',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'totalGoalsOddsEvenStatusHandler'
      }
    ],
    [ 'build your bet to score exactly 1 goal',
      {
        name: 'Build Your Bet TO SCORE EXACTLY 1 GOAL',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalGoalsByPlayerStatusHandler'
      }
    ],
    [ 'build your bet to score exactly 2 goals',
      {
        name: 'Build Your Bet TO SCORE EXACTLY 2 GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalGoalsByPlayerStatusHandler'
      }
    ],
    [ 'build your bet to score exactly 3 goals',
      {
        name: 'Build Your Bet TO SCORE EXACTLY 3 GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalGoalsByPlayerStatusHandler'
      }
    ],
    [ 'build your bet to score 1 or more goals in 1st half',
      {
        name: 'Build Your Bet TO SCORE 1 OR MORE GOALS IN 1ST HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'player',
        methodName: 'playerToScoreInPeriod'
      }
    ],
    [ 'build your bet to score 1 or more goals in 2nd half',
      {
        name: 'Build Your Bet TO SCORE 1 OR MORE GOALS IN 2ND HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'player',
        methodName: 'playerToScoreInPeriod'
      }
    ],
    [ 'build your bet to score in both halves',
      {
        name: 'Build Your Bet TO SCORE IN BOTH HALVES',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'playerToScoreInBothHalves'
      }
    ],
    [ 'build your bet first team to score in 1st half',
      {
        name: 'Build Your Bet FIRST TEAM TO SCORE IN 1ST HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'team',
        methodName: 'firstTeamToScore'
      }
    ],
    [ 'build your bet first team to score in 2nd half',
      {
        name: 'Build Your Bet FIRST TEAM TO SCORE IN 2ND HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'team',
        methodName: 'firstTeamToScore'
      }
    ],
    [ 'build your bet half time double chance',
      {
        name: 'Build Your Bet HALF TIME DOUBLE CHANCE',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'doubleChanceStatusHandler'
      }
    ],
    [ 'build your bet 2nd half double chance',
      {
        name: 'Build Your Bet 2ND HALF DOUBLE CHANCE',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'doubleChanceStatusHandler'
      }
    ],
    [ 'build your bet both teams to score in both halves',
      {
        name: 'Build Your Bet BOTH TEAMS TO SCORE IN BOTH HALVES',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'bothTeamsToScoreByHalvesStatusHandler'
      }
    ],
    [ 'build your bet both teams to score in 1st half',
      {
        name: 'Build Your Bet BOTH TEAMS TO SCORE IN 1ST HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'bothTeamsToScoreByHalvesStatusHandler'
      }
    ],
    [ 'build your bet both teams to score in 2nd half',
      {
        name: 'Build Your Bet BOTH TEAMS TO SCORE IN 2ND HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'bothTeamsToScoreByHalvesStatusHandler'
      }
    ],
    [ 'build your bet team to score in both halves',
      {
        name: 'Build Your Bet TEAM TO SCORE IN BOTH HALVES',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'teamToScoreInBothHalves'
      }
    ],
    [ 'build your bet 1st half handicap betting',
      {
        name: 'Build Your Bet 1ST HALF HANDICAP BETTING',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams',
        methodName: 'handicapBettingStatusHandler'
      }
    ],
    [ 'build your bet 2nd half handicap betting',
      {
        name: 'Build Your Bet 2ND HALF HANDICAP BETTING',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams',
        methodName: 'handicapBettingStatusHandler'
      }
    ],
    [ 'build your bet which half will produce the first goal',
      {
        name: 'Build Your Bet WHICH HALF WILL PRODUCE THE FIRST GOAL',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'halfToProduceFirstGoal'
      }
    ],
    [ 'build your bet win both halves',
      {
        name: 'Build Your Bet WIN BOTH HALVES',
        isBoth: true,
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'winHalvesStatusHandler'
      }
    ],
    [ 'build your bet win either half',
      {
        name: 'Build Your Bet WIN EITHER HALF',
        hasLine: false,
        isBoth: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'winHalvesStatusHandler'
      }
    ],
    [ 'build your bet score a goal in both halves',
      {
        name: 'Build Your Bet SCORE A GOAL IN BOTH HALVES',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams',
        methodName: 'scoreAGoalInBothHalvesHandler'
      }
    ],
    [ 'build your bet score a goal in first half',
      {
        name: 'Build Your Bet SCORE A GOAL IN FIRST HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '1h',
        generalInformationRequired: 'teams'
      }
    ],
    [ 'build your bet score a goal in second half',
      {
        name: 'Build Your Bet SCORE A GOAL IN SECOND HALF',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '2h',
        generalInformationRequired: 'teams'
      }
    ],
    [ 'build your bet number of teams to score',
      {
        name: 'Build Your Bet NUMBER OF TEAMS TO SCORE',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'teams'
      }
    ],
    [ 'build your bet clean sheet',
      {
        name: 'Build Your Bet CLEAN SHEET',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'cleanSheetStatusHandler'
      }
    ],
    [ 'build your bet 1st half participant_1 total goals',
      {
        name: 'Build Your Bet 1ST HALF PARTICIPANT_1 TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet 2nd half participant_1 total goals',
      {
        name: 'Build Your Bet 2ND HALF PARTICIPANT_1 TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet 1st half participant_2 total goals',
      {
        name: 'Build Your Bet 1ST HALF PARTICIPANT_2 TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '1h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet 2nd half participant_2 total goals',
      {
        name: 'Build Your Bet 2ND HALF PARTICIPANT_2 TOTAL GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: '2h',
        generalInformationRequired: 'team',
        methodName: 'totalGoalsStatusHandler'
      }
    ],
    [ 'build your bet participant_1 to score 2+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_1 TO SCORE 2+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet participant_1 to score 3+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_1 TO SCORE 3+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet participant_1 to score 4+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_1 TO SCORE 4+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet participant_1 to score 5+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_1 TO SCORE 5+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet participant_2 to score 2+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_2 TO SCORE 2+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet participant_2 to score 3+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_2 TO SCORE 3+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet participant_2 to score 4+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_2 TO SCORE 4+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet participant_2 to score 5+ goals',
      {
        name: 'Build Your Bet PARTICIPANT_2 TO SCORE 5+ GOALS',
        hasLine: true,
        statCategory: 'Score',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'team',
        methodName: 'participantToScoreNGoals'
      }
    ],
    [ 'build your bet result after 15 mins',
      {
        name: 'Build Your Bet RESULT AFTER 15 MINS',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '15 mins',
        generalInformationRequired: 'teams',
        methodName: 'getResultAfterNMinutes'
      }
    ],
    [ 'build your bet result after 30 mins',
      {
        name: 'Build Your Bet RESULT AFTER 30 MINS',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '30 mins',
        generalInformationRequired: 'teams',
        methodName: 'getResultAfterNMinutes'
      }
    ],
    [ 'build your bet result after 60 mins',
      {
        name: 'Build Your Bet RESULT AFTER 60 MINS',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '60 mins',
        generalInformationRequired: 'teams',
        methodName: 'getResultAfterNMinutes'
      }
    ],
    [ 'build your bet result after 75 mins',
      {
        name: 'Build Your Bet RESULT AFTER 75 MINS',
        hasLine: true,
        statCategory: 'Score',
        template: 'binary',
        period: '75 mins',
        generalInformationRequired: 'teams',
        methodName: 'getResultAfterNMinutes'
      }
    ],
    [ 'build your bet player to outscore the opposition',
      {
        name: 'Build Your Bet PLAYER TO OUTSCORE THE OPPOSITION',
        hasLine: false,
        statCategory: 'Score',
        template: 'binary',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'playerToOutscoreStatusHandler'
      }
    ],
    [ 'build your bet player total passes',
      {
        name: 'Build Your Bet PLAYER TOTAL PASSES',
        hasLine: true,
        statCategory: 'Passes',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalPassesStatusHandler'
      }
    ],
    [ 'build your bet player total tackles',
      {
        name: 'Build Your Bet PLAYER TOTAL TACKLES',
        hasLine: true,
        statCategory: 'Tackles',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalTacklesStatusHandler'
      }
    ],
    [ 'build your bet player total shots',
      {
        name: 'Build Your Bet PLAYER TOTAL SHOTS',
        hasLine: true,
        statCategory: 'Shots',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalShotsStatusHandler'
      }
    ],
    [ 'build your bet player total shots on target',
      {
        name: 'Build Your Bet PLAYER TOTAL SHOTS ON TARGET',
        hasLine: true,
        statCategory: 'ShotsOnTarget',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalShotsOnTargetStatusHandler'
      }
    ],
    [ 'build your bet player total shots outside box',
      {
        name: 'Build Your Bet PLAYER TOTAL SHOTS OUTSIDE BOX',
        hasLine: true,
        statCategory: 'ShotsOutsideBox',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'shotsOutsideBoxStatusHandler'
      }
    ],
    [ 'build your bet player total assists',
      {
        name: 'Build Your Bet PLAYER TOTAL ASSISTS',
        hasLine: true,
        statCategory: 'Assists',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalAssistsStatusHandler'
      }
    ],
    [ 'build your bet player total crosses',
      {
        name: 'Build Your Bet PLAYER TOTAL CROSSES',
        hasLine: true,
        statCategory: 'Crosses',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalCrossesStatusHandler'
      }
    ],
    [ 'build your bet player total offsides',
      {
        name: 'Build Your Bet PLAYER TOTAL OFFSIDES',
        hasLine: true,
        statCategory: 'Offsides',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'totalOffsidesStatusHandler'
      }
    ],
    [ 'build your bet player total goals inside box',
      {
        name: 'Build Your Bet PLAYER TOTAL GOALS INSIDE BOX',
        hasLine: true,
        statCategory: 'GoalsInsideBox',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'goalsInsideBoxStatusHandler'
      }
    ],
    [ 'build your bet player total goals outside box',
      {
        name: 'Build Your Bet PLAYER TOTAL GOALS OUTSIDE BOX',
        hasLine: true,
        statCategory: 'GoalsOutsideBox',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'goalsOutsideBoxStatusHandler'
      }
    ],
    [ 'build your bet player shots woodwork',
      {
        name: 'Build Your Bet PLAYER SHOTS WOODWORK',
        hasLine: true,
        statCategory: 'ShotsWoodwork',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'shotsWoodworkStatusHandler'
      }
    ],
    [ 'build your bet player total goals conceded',
      {
        name: 'Build Your Bet PLAYER TOTAL GOALS CONCEDED',
        hasLine: true,
        statCategory: 'GoalConceded',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'goalsConcededStatusHandler'
      }
    ],
    [ 'build your bet player to keep a clean sheet',
      {
        name: 'Build Your Bet PLAYER TO KEEP A CLEAN SHEET',
        hasLine: true,
        statCategory: 'GoalConceded',
        template: 'range',
        period: 'total',
        generalInformationRequired: 'player',
        methodName: 'goalsConcededStatusHandler'
      }
    ],
  ]
);

export const PERIODS = {
  total: 'total',
  '1ST_HALF': '1h',
  '2ND_HALF': '2h',
  '15 mins': '15:00',
  '30 mins': '30:00',
  '60 mins': '60:00',
  '75 mins': '75:00',
  first: 'first',
  last: 'last',
  halftime: 'ht'
};

export enum TEAMS {
  AWAY = 'Away',
  DRAW = 'Draw',
  HOME = 'Home',
  NO_GOAL = 'No Goal',
  NO_CARDS = 'no cards'
}

export enum DOUBLE_TEAMS {
  HOME_OR_DRAW = 'Home or Draw',
  AWAY_OR_DRAW = 'Away or Draw',
  HOME_OR_AWAY = 'Home or Away'
}

export enum ODD_EVEN {
  ODD = 'Odd',
  EVEN = 'Even'
}

export enum STATUSES {
  WON = 'Won',
  WINNING = 'Winning',
  LOSE = 'Lose',
  LOSING = 'Losing'
}

export enum STATS_CATEGORIES {
  Score = 'Goals',
  Corners = 'Corners',
  RedCards = 'RedCards',
  CardIndex = 'Booking Points',
  Booking = 'Total Cards',
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

export enum STATS_CATEGORIES_SINGULAR {
  Score = 'Goal',
  Corners = 'Corner',
  RedCards = 'RedCard',
  CardIndex = 'Booking Point',
  Booking = 'Total Card',
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

export enum CARDS_INDEX {
  red = 25,
  yellow = 10
}

export enum PLAYER_SHOTS {
  TOTAL = 'total',
  ON_TARGET = 'onTarget'
}

export enum BET_STATUSES {
  SETTLED = 'Y',
  OUTCOME_NAME_YES = 'YES'
}

export enum HALF_LABELS {
  NO_GOALS = 'No Goals',
  '1ST_HALF' = 'First Half',
  '2ND_HALF' = 'Second Half',
}

export enum PRE_PLAY {
  PRE_PLAY_2H = 'prePlay2h'
}

export enum BET_STATS_LIMIT {
  COUNTER = 5,
  FIRST_POSSIBLE_POINT = 10,
  SECOND_POSSIBLE_POINT = 20,
  LEAST_POSSIBLE_POINT = 0,
  INITIAL_COUNTER = 1
}

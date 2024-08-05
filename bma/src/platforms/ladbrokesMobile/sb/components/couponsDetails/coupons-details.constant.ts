export const FOOTBALL_COUPONS = {
  DEFAULT_SELECTED_OPTION: 'Match Result',
  MARKETS_NAME_ORDER: [
    'Match Result',
    'Both Teams to Score',
    'Match Result and Both Teams To Score',
    'Total Goals Over/Under 1.5',
    'Total Goals Over/Under 2.5',
    'Total Goals Over/Under 3.5',
    'Draw No Bet',
    'First-Half Result',
    'To Win to Nil',
    'Score Goal in Both Halves',
    '2Up&Win Early Payout'
  ],
  MARKETS_NAMES: {
    'Match Result': 'Match Result',
    'Both Teams to Score': 'Both Teams to Score',
    'Match Result and Both Teams To Score': 'Match Result & Both Teams To Score',
    'Over/Under Total Goals 1.5': 'Total Goals Over/Under 1.5',
    'Over/Under Total Goals 2.5': 'Total Goals Over/Under 2.5',
    'Over/Under Total Goals 3.5': 'Total Goals Over/Under 3.5',
    'Draw No Bet': 'Draw No Bet',
    'First-Half Result': '1st Half Result',
    'To Win to Nil': 'To Win To Nil',
    'Score Goal in Both Halves': 'Goal in Both Halves',
    '2Up&Win Early Payout': '2Up&Win - Early Payout'
  },
  DEFAULT_MARKETS: [
    {
      title: 'Match Result',
      templateMarketName: 'Match Betting',
      header: ['Home', 'Draw', 'Away'],
    },
    {
      title: 'Both Teams to Score',
      templateMarketName: 'Both Teams to Score',
      header: ['Yes', 'No'],
    },
    {
      title: 'Match Result & Both Teams To Score',
      templateMarketName: 'Match Result and Both Teams To Score',
      header: ['Home', 'Draw', 'Away'],
    },
    {
      title: 'Total Goals Over/Under 1.5',
      templateMarketName: 'Over/Under Total Goals 1.5',
      header: ['Over', 'Under'],
    },
    {
      title: 'Total Goals Over/Under 2.5',
      templateMarketName: 'Over/Under Total Goals 2.5',
      header: ['Over', 'Under'],
    },
    {
      title: 'Total Goals Over/Under 3.5',
      templateMarketName: 'Over/Under Total Goals 3.5',
      header: ['Over', 'Under'],
    },
    {
      title: 'Draw No Bet',
      templateMarketName: 'Draw No Bet',
      header: ['Home', 'Away'],
    },
    {
      title: '1st Half Result',
      templateMarketName: 'First-Half Result',
      header: ['Home', 'Draw', 'Away'],
    },
    {
      title: 'To Win To Nil',
      templateMarketName: 'To Win to Nil',
      header: ['Home', 'Away'],
    },
    {
      title: 'Goal in Both Halves',
      templateMarketName: 'Score Goal in Both Halves',
      header: ['Yes', 'No']
    },
    {
      title: '2Up&Win - Early Payout',
      templateMarketName: '2Up&Win Early Payout',
      header: ['Home', 'Draw', 'Away']
    }
  ]
};

export const COUPON_NAMES_CONFIG = {
  goalscorerCouponName: 'Goalscorer Coupon',
  overUnderOriginalName: 'Over / Under Total Goals',
  ukCoupon: 'UK Coupon'
};

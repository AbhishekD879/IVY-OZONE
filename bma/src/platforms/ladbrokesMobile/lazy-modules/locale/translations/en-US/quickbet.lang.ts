import { quickbet as appQuickbet } from '@app/lazy-modules/locale/translations/en-US/quickbet.lang';

export const quickbet = {
  ...appQuickbet,
  tax5: 'A fee of 5.00 % is applicable on winnings',
  potentialResults: 'Total Potential Returns',
  totalStake: 'Stake for this bet: ',
  snbSummaryStake: 'Stake: ',
  snbBetId: 'Bet ID: ',
  snbSuccessMsg: 'Bet Placed Successfully',
  snbDone: 'DONE',
  potentialReturns: 'Potential Returns',
  potentialReturnsWithColon: 'Potential Returns: ',
  betPlacementErrors: {
    ...appQuickbet.betPlacementErrors,
    BAD_FREEBET_TOKEN: 'The free bet token is invalid or not applicable',
  },
  betId: 'Receipt No: ',
  bybType: {
    fiveASide: '5-A-Side',
    byb: 'Bet Builder'
  }
};

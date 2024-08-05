export const TAG_NAMES_CONFIG = [
  {
    marketFlag: 'MKTFLAG_FI',
    eventFlag: 'EVFLAG_FIN',
    flagName: 'FI',
    promoName: 'fallersInsurance',
    iconId: '#icon-promotion-offers'
  },
  {
    marketFlag: 'MKTFLAG_BBAL',
    eventFlag: 'EVFLAG_BBL',
    flagName: 'BBAL',
    promoName: 'beatenByLength',
    iconId: '#icon-beatenByLen-offers'
  },
  {
    marketFlag: 'MKTFLAG_EPR',
    eventFlag: 'EVFLAG_EPR',
    flagName: 'EPR',
    promoName: 'extraPlace',
    iconId: '#extra-place-icon'
  },
  {
    marketFlag: 'MKTFLAG_PB',
    eventFlag: 'EVFLAG_PB',
    flagName: 'PB',
    promoName: 'priceBoost',
    iconId: '#price-boost'
  },
  {
    marketFlag: 'MKTFLAG_MB',
    eventFlag: 'EVFLAG_MB',
    flagName: 'MB',
    promoName: 'moneyBack',
    iconId: '#money-back'
  },
  {
    marketFlag: 'MKTFLAG_DYW',
    eventFlag: 'EVFLAG_DYW',
    flagName: 'DYW',
    promoName: 'doubleWinnings',
    iconId: '#icon-promotion-offers'
  },

      /*
    * Adding 'marketName' new property to identify the 2UP market as there is no marketFlag in specific to identify 2UP.
    * marketName will be configured in CMS for 2UPMarket.
    *  if both brands have different market names then we add marketnames in array for marketName.
    */
  {
    marketFlag: 'two-up',
    eventFlag: 'two-up',
    flagName: 'two-up',
    marketName: ['2Up - Instant Win', '2Up&Win - Early Payout'], // array of 2up names with diff brands.
    promoName: 'twoUpMarketName',
    iconId: '#two-up',
    greyIconId:'#two-up-grey'
  },
  {
    marketFlag: 'YOUR_CALL',
    eventFlag: 'YOUR_CALL',
    flagName: 'YOUR_CALL',
    promoName: 'yourCall',
    iconId: '#yourcall-icon'
  }
];

export const enum DRILLDOWNTAGNAMES {
  HR_BIR = 'EVFLAG_IHR'
}
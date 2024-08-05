import { IBetReceiptEntity } from '@app/betslip/services/betReceipt/bet-receipt.model';

export const mostRacingTipsMock = [
  {
    cashoutAvail: 'Y',
    categoryCode: 'HORSE_RACING',
    categoryDisplayOrder: '4',
    categoryId: '16',
    categoryName: 'Horse Racing',
    classDisplayOrder: 0,
    classId: 223,
    className: 'Horse Racing - Live',
    eventStatusCode: 'A',
    id: 1,
    liveServChannels: 'sEVENT0001024863,',
    liveServChildrenChannels: 'SEVENT0001024863,',
    localTime: '12:00',
    typeName: 'test name',
    nameOverride: 'tset over',
    markets: [
      {
        liveServChannels: 'sEVENT0001024863,',
        minAccumulators: '1',
        name: 'Win or Each Way',
        ncastTypeCodes: 'CT,SF,CF,RF,TC,',
        outcomes: [
          {
            cashoutAvail: 'N',
            correctPriceType: 'SP',
            displayOrder: 1,
            icon: false,
            id: '125825053',
            liveServChannels: 'sEVENT0001024863,'
          },
        ],
        children: [
          {
            outcome: {
              liveServChannels:'sSELCN1256080108,',
              displayOrder: 1,
              icon: false,
              id: '125825053',
              name: 'a',
              runnerNumber: '2',
              silkName: '123.png',
              prices: [
                {
                  priceNum: '9',
                  priceDen: '2',
                },
              ],
            },
          },
          {
            outcome: {
              liveServChannels:'sSELCN1256080108,',
              displayOrder: 1,
              icon: false,
              id: '125825053',
              name: 'b',
              silkName: '123.png',
              runnerNumber: '5',
              prices: [
                {
                  priceNum: '9',
                  priceDen: '2',
                },
              ],
            },
          },
        ],
        priceTypeCodes: 'SP,',
      },
    ],
    mediaTypeCodes: 'VST,',
    name: 'Southwell',
    originalName: '12:00 Southwell',
    horses: [
      {
        horseName: 'a',
        isMostTipped: true,
        silk: '123.png',
      },
      {
        horseName: 'b',
        isMostTipped: false,
        silk: '123.png',

      },
    ]
  }
];

export const mostRacingTipDataComp = [{
  cashoutAvail: 'Y',
  categoryCode: 'HORSE_RACING',
  categoryDisplayOrder: '4',
  categoryId: '21',
  categoryName: 'Horse Racing',
  classDisplayOrder: 0,
  classId: 223,
  className: 'Horse Racing - Live',
  eventStatusCode: 'A',
  id: 1,
  liveServChannels: 'sEVENT0001024863,',
  liveServChildrenChannels: 'SEVENT0001024863,',
  localTime: '12:00',
  typeName: 'test name',
  nameOverride: 'tset over',
  markets: [
    {
      minAccumulators: '1',
      name: 'Win or Each Way',
      ncastTypeCodes: 'CT,SF,CF,RF,TC,',
      outcomes: [
        {
          cashoutAvail: 'N',
          correctPriceType: 'SP',
          displayOrder: 1,
          icon: false,
          id: '125825053',

        }
      ],
      children: [
        {
          outcome: {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825053',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          }
        }
      ],
      priceTypeCodes: 'SP,'
    },
  ],
  mediaTypeCodes: 'VST,',
  name: 'Southwell',
  originalName: '12:00 Southwell',
  horses: [{ horseName: 'Sancta Sedes', isMostTipped: true, silk: '123.png' }, { horseName: 'b', isMostTipped: false, silk: '123.png' }]
},
{
  id: 2,
  liveServChannels: 'sEVENT0001024863,',
  liveServChildrenChannels: 'SEVENT0001024863,',
  localTime: '12:00',
  markets: [
    {
      outcomes: [
        {
          icon: false,
          id: '125825053',
        }
      ],
      priceTypeCodes: 'SP,',
    }
  ],
  horses: [{ horseName: 'a', isMostTipped: true, silk: '123.png' }, { horseName: 'b', isMostTipped: false, silk: '123.png' }]
}
];
export const mostRacingTipsWithOutHorsesMock = [
  {
  cashoutAvail: 'Y',
  categoryCode: 'HORSE_RACING',
  categoryDisplayOrder: '4',
  categoryId: '16',
  categoryName: 'Horse Racing',
  classDisplayOrder: 0,
  classId: 223,
  className: 'Horse Racing - Live',
  eventStatusCode: 'A',
  id: 1,
  liveServChannels: 'sEVENT0001024863,',
  liveServChildrenChannels: 'SEVENT0001024863,',
  localTime: '12:00',
  typeName: 'test name',
  nameOverride: 'tset over',
  markets: [
    {
      minAccumulators: '1',
      name: 'Win or Each Way',
      ncastTypeCodes: 'CT,SF,CF,RF,TC,',
      outcomes: [
        {
          cashoutAvail: 'N',
          correctPriceType: 'SP',
          displayOrder: 1,
          icon: false,
         id: '125825053',

        }
      ],
      children: [
        {
          outcome: {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825053',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          }
        }
      ],
      priceTypeCodes: 'SP,'
    },
  ],
  mediaTypeCodes: 'VST,',
  name: 'Southwell',
  originalName: '12:00 Southwell',
  horses: []
},
{
  id: 2,
  liveServChannels: 'sEVENT0001024863,',
  liveServChildrenChannels: 'SEVENT0001024863,',
  localTime: '12:00',
  markets: [
    {
      outcomes: [
        {
          icon: false,
          id: '125825053',
        }
      ],
      priceTypeCodes: 'SP,',
    }
  ],
  horses: []
}
];

export const mainBetSingleMock = [
  {
    betId: '123',
    betType: 'type',
    receipt: 'O/22',
    betTypeName: 'Single',
    stake: '5.00',
    odds: {
      frac: '5/2',
      dec: '3.50',
    },
    eventMarket: 'Match Result',
    numLegs: '1',
    potentialPayout: '5.00',
    leg: [
      {
        part: [{ event: { id: 1, categoryId: '16' }, marketId: '123123' }],
        odds: {
          frac: '5/2',
          dec: '3.50',
        }
      }
    ]
  }
];

export const mostTippedHorsesEventsMock = [
  {
    liveServChannels:'sSELCN1256080108,',
    cashoutAvail: 'Y',
    typeId: '29027',
    categoryCode: 'HORSE_RACING',
    categoryDisplayOrder: '4',
    categoryId: '21',
    eventIsLive: false,
    eventStatusCode: 'A',
    id: 1024863,
    isActive: true,
    localTime: '12:00',
    typeName:'test',
    startTime: 'Wed Jul 15 2020 11:51:57 GMT+0530',
    name: 'Southwell',
    nameOverride: 'test over',
    horses: [
      {
        horseName: 'a',
        isMostTipped: true,
        silk: '123.png',
      },
      {
        horseName: 'b',
        isMostTipped: false,
        silk: '123.png',

      },
    ],
    powerHorse: {
      horseName: 'Sancta Sedes',
      silk: '123.png',
      trainer: 'a',
      jockey: '1',
      isBeatenFavourite: true
   },
    markets: [
      {
        liveServChannels:'sSELCN1256080108,',
        cashoutAvail: 'N',
        correctPriceTypeCode: 'SP',
        displayOrder: 0,
        eachWayFactorDen: '4',
        eachWayFactorNum: '1',
        eachWayPlaces: '3',
        eventId: '1024863',
        marketName: 'Win or Each Way',
        id: '35033769',
        children: [
          {
            outcome: {
              liveServChannels:'sSELCN1256080108,',
              displayOrder: 1,
              icon: false,
              id: '125825053',
              name: 'Sancta Sedes',
              silkName: '123.png',
              prices: [{
                priceNum: '9',
                priceDen: '2'
              }
            ]
            }

          }
        ],
        outcomes: [
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825051',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '12582505',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825053',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          }
        ],
        priceTypeCodes: 'SP,',
      },
      {
        liveServChannels:'sSELCN1256080108,',
        cashoutAvail: 'N',
        correctPriceTypeCode: 'SP',
        displayOrder: 0,
        eachWayFactorDen: '4',
        eachWayFactorNum: '1',
        eachWayPlaces: '3',
        eventId: '1024863',
        marketName: 'Win or Each Way',
        id: '35033769',
        children: [
          {
            outcome: {
              liveServChannels:'sSELCN1256080108,',
              displayOrder: 1,
              icon: false,
              id: '125825053',
              name: 'Sancta Sedes',
              silkName: '123.png',
              prices: [{
                priceNum: '9',
                priceDen: '2'
              }
            ]
            }

          }
        ],
        outcomes: [
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825051',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '12582505',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825053',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          }
        ],
        priceTypeCodes: 'SP,',
      },
      {
        liveServChannels:'sSELCN1256080108,',
        cashoutAvail: 'N',
        correctPriceTypeCode: 'SP',
        displayOrder: 0,
        eachWayFactorDen: '4',
        eachWayFactorNum: '1',
        eachWayPlaces: '3',
        eventId: '1024863',
        marketName: 'Win or Each Way',
        id: '35033769',
        children: [
          {
            outcome: {
              liveServChannels:'sSELCN1256080108,',
              displayOrder: 1,
              icon: false,
              id: '125825053',
             name: 'Sancta Sedes',
              silkName: '123.png',
              prices: [{
                priceNum: '9',
                priceDen: '2'
              }
            ]
            }

          }
        ],
        outcomes: [
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825051',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
             priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '12582505',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            liveServChannels:'sSELCN1256080108,',
            displayOrder: 1,
            icon: false,
            id: '125825053',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          }
        ],
        priceTypeCodes: 'SP,',
      }
    ],
    isMostPowerHorse: true
  },
  {
    cashoutAvail: 'Y',
    categoryCode: 'HORSE_RACING',
    categoryDisplayOrder: '4',
    categoryId: '21',
    eventStatusCode: 'A',
    id: 1024864,
    isActive: true,
    eventIsLive: undefined,
    localTime: '12:00',
    typeName:'test',
    startTime: 'Wed Jul 15 2020 11:51:57 GMT+0530',
    name: 'Southwell',
    nameOverride: 'test over',
    horses: [
      {
        horseName: 'a',
        isMostTipped: true,
        silk: '123.png',
      },
      {
        horseName: 'b',
        isMostTipped: false,
        silk: '123.png',

      },
    ],
    powerHorse: {
      horseName: 'Sancta Sedes',
      silk: '123.png',
      trainer: 'a',
      jockey: '1',
      isBeatenFavourite: true
    },
    markets: [
      {
        cashoutAvail: 'N',
        correctPriceTypeCode: 'SP',
        displayOrder: 0,
        eachWayFactorDen: '4',
        eachWayFactorNum: '1',
        eachWayPlaces: '3',
        eventId: '1024863',
        marketName:'Win or Each Way',
        id: '35033769',
        children: [
          {
            outcome: {
              liveServChannels:'sSELCN1256080108,',
              displayOrder: 1,
              icon: false,
              id: '125825053',
              name: 'Sancta Sedes',
              silkName: '123.png',
              prices: [{
                priceNum: '9',
                priceDen: '2'
              }
            ]
            }

          }
        ],
        outcomes: [
          {
            displayOrder: 1,
            icon: false,
            id: '125825051',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            displayOrder: 1,
            icon: false,
            id: '12582505',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          },
          {
            displayOrder: 1,
            icon: false,
            id: '125825053',
            name: 'Sancta Sedes',
            silkName: '123.png',
            prices: [{
              priceNum: '9',
              priceDen: '2'
            }]
          }
        ],
        priceTypeCodes: 'SP,',
      },
    ],
    isMostPowerHorse: true
  }
];

export const quickBetPlacedOnHR = {
  categoryId: '21',
  categoryName: 'Horse Racing',
  classId: '223',
  className: 'Horse Racing - Live',
  clientUserAgentService: {},
  currency: '£',
  disabled: false,
  eachWayFactorDen: 4,
  eachWayFactorNum: 1,
  eventId: '16757379',
  eventIsLive: undefined,
  eventName: '9:15 Sunshine Coast ',
  eventStatusCode: 'A',
  fracToDecService: {},
  freebet: 0,
  freebetValue: 0,
  hasGP: false,
  hasLP: true,
  hasSP: false,
  hasSPLP: false,
  isBoostActive: undefined,
  isEachWay: false,
  isEachWayAvailable: true,
  isLP: true,
  isLpAvailable: true,
  isRacingSport: true,
  isSpAvailable: false,
  isUnnamedFavourite: false,
  marketId: '410900235',
  marketName: 'Win or Each Way',
  marketStatusCode: 'A',
  markets: [{}],
  newOddsValue: '11/8',
  oddsBoost: undefined,
  oddsSelector: [{}],
  oldOddsValue: '5/4',
  oldPrice: { id: '1', isActive: 'true', displayOrder: '1', priceType: 'LP', priceNum: 5 },
  outcomeId: '1326936821',
  outcomeMeaningMinorCode: undefined,
  outcomeName: 'Saltoree',
  outcomeStatusCode: 'A',
  potentialPayout: '0.23',
  'price': { id: '1', priceType: 'LP', priceNum: 11, priceDen: 8, priceDec: 2.37 },
  reboost: undefined,
  requestData: {},
  selectionType: 'simple',
  stake: '0.10',
  stakeAmount: 0.1,
  startTime: '2021-02-05T09:15:00Z',
  timeSyncService: {},
  toolsService: {},
  typeId: '29027',
  typeName: 'Sunshine Coast',
  userService: {}
};
export const betPlacedOnHR = [
{
      availableFreeBets: [],
      className: 'Horse Racing - Live',
      competition: 'Lingfield',
      disabled: false,
      eachWayFactorDen: '5',
      eachWayFactorNum: '1',
      error: undefined,
      errorMsg: null,
      categoryId:'21',
      eventIds: {
          categoriesIds: ['21'],
          classIds: ['223'],
          eventIds: ['16532551'],
          marketIds: ['405024116'],
          outcomeIds: ['1308214442'],
          typeIds: ['1945']
      },
      eventName: 'Lingfield',
      handicapError: undefined,
      handicapErrorMsg: null,
      id: 'SGL|1308214442',
      isBPGAvailable: 'true',
      isEachWayAvailable: true,
      isMarketBetInRun: 'true',
      isOfferRemovable: undefined,
      isRacingSport: true,
      isSP: false,
      isSPLP: true,
      isStarted: undefined,
      isSuspended: false,
      liveServChannels: {marketliveServChannels: Array(1), eventliveServChannels: Array(1), outcomeliveServChannels: Array(1)},
      localTime: '13:45',
      marketId: 405024116,
      marketName: 'Win or Each Way',
      outcomeId: '1308214442',
      outcomeIds: ['1308214442'],
      outcomeName: 'Spurofthemoment',
      potentialPayout: 3.75,
      price: {id: '25', priceType: 'LP', priceNum: 11, priceDen: 4, priceDec: '3.75'},
      priceDec: '3.75',
      pricesAvailable: true,
      removed: undefined,
      selectedFreeBet: null,
      sport: 'HORSE_RACING',
      sportId: '21',
      stakeMultiplier: 1,
      type: 'SGL',
      typeId: '1945',
      typeInfo: '',
      winOrEach: false
  }
];

export const receiptEventsMock = {
  multiples: [
    {
      betTypeName: 'Double',
      betType: 'SGL',
      receipt: 'O/11',
      numLines: '1',
      stake: '5.00',
      numLegs: '1',
      odds: {
        frac: '5/23',
        dec: '3.2',
      },
      potentialPayout: '5.00',
      leg: [
        {
         part: [{ event: { id: 1, }, marketId: '123123' }],
          odds: {
            frac: '5/2',
            dec: '3.50',
          }
        }
      ]
    }
  ]
} as IBetReceiptEntity;

export const updatedPriceMock = {
  price: [
    {
      'id': '125825053',
      'name': 'A.Rinderknech',
      'outcomeMeaningMajorCode': 'HH',
      'outcomeMeaningMinorCode': 'H',
      'outcomeStatusCode': 'A',
      'liveServChannels': 'sSELCN1310067201,',
      'correctPriceType': 'LP',
      'correctedOutcomeMeaningMinorCode': 1,
      'prices': [
        {
          'id': '45',
          'priceType': 'LP',
          'priceNum': 25,
          'priceDen': 1,
          'priceDec': 26,
          'liveShowTimer': {
            'type': ''
          }
        }
      ],
      'displayOrder': 1,
      'active': false,
      'isRacing': false
    },
  ]
};

export const UnsuspendedRacesMock = [
  {
    'id': '232301079',
    'name': '13:00 Southwell',
    'eventStatusCode': 'A',
    'isActive': true,
    'displayOrder': 780,
    'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
    'eventSortCode': 'MTCH',
    'startTime': '2021-02-24T13:00:00Z',
    'rawIsOffCode': 'N',
    'classId': '223',
    'typeId': '1972',
    'sportId': '21',
    'liveServChannels': 'sEVENT0232301079,',
    'liveServChildrenChannels': 'SEVENT0232301079,',
    'categoryId': '21',
    'categoryCode': 'HORSE_RACING',
    'categoryName': 'Horse Racing',
    'className': 'Horse Racing - Live',
    'classDisplayOrder': -9500,
    'classSortCode': 'HR',
    'classFlagCodes': 'UF,CN,LI,',
    'typeName': 'Southwell',
    'typeDisplayOrder': -31180,
    'typeFlagCodes': 'UK,NE,QL,AVA,',
    'isOpenEvent': true,
    'isNext24HourEvent': true,
    'isLiveNowOrFutureEvent': true,
    'drilldownTagNames': 'EVFLAG_BL,EVFLAG_AVA,',
    'isAvailable': true,
    'mediaTypeCodes': 'VST,',
    'cashoutAvail': 'Y',
    'responseCreationTime': '2021-02-23T22:42:49.243Z',
    'markets': [
      {
        'children': [
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '56',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 7,
                    'priceDen': 1,
                    'priceDec': 8
                  }
                }
              ],
              'id': '1256080106',
              'marketId': '508150681',
              'name': 'Catapult',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 8,
              'displayOrder': 8,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080106,',
              'liveServChildrenChannels': 'SSELCN1256080106,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '56',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 7,
                  'priceDen': 1,
                  'priceDec': 8
                }
              ]
            }
          },
          {
            'outcome': {
              'id': '1256080107',
              'marketId': '508150681',
              'name': 'Unnamed 2nd Favourite',
              'outcomeMeaningMajorCode': '--',
              'outcomeMeaningMinorCode': '2',
              'displayOrder': 10,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080107,',
              'liveServChildrenChannels': 'SSELCN1256080107,',
              'isAvailable': true
            }
          },
          {
            'outcome': {
              'id': '1256080108',
              'marketId': '508150681',
              'name': 'Unnamed Favourite',
              'outcomeMeaningMajorCode': '--',
             'outcomeMeaningMinorCode': '1',
              'displayOrder': 9,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080108,',
              'liveServChildrenChannels': 'SSELCN1256080108,',
              'isAvailable': true
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '57',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 40,
                    'priceDen': 1,
                    'priceDec': 41
                  }
                }
              ],
              'id': '1256080109',
              'marketId': '508150681',
              'name': 'Signore Piccolo',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 3,
              'displayOrder': 3,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080109,',
              'liveServChildrenChannels': 'SSELCN1256080109,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '57',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 40,
                  'priceDen': 1,
                  'priceDec': 41
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '58',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 2,
                    'priceDen': 5,
                    'priceDec': 1.4
                  }
                }
              ],
              'id': '1256080110',
              'marketId': '508150681',
              'name': 'Owhatanight',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 4,
              'displayOrder': 4,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080110,',
              'liveServChildrenChannels': 'SSELCN1256080110,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '58',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 2,
                  'priceDen': 5,
                  'priceDec': 1.4
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '59',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 33,
                    'priceDen': 1,
                    'priceDec': 34
                  }
                }
              ],
              'id': '1256080111',
              'marketId': '508150681',
              'name': 'Shortbackandsides',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 6,
              'displayOrder': 6,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080111,',
              'liveServChildrenChannels': 'SSELCN1256080111,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '59',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 33,
                  'priceDen': 1,
                  'priceDec': 34
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '60',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 13,
                    'priceDen': 2,
                    'priceDec': 7.5
                 }
                }
              ],
              'id': '1256080112',
              'marketId': '508150681',
              'name': 'Jazz Legend',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 5,
              'displayOrder': 5,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080112,',
              'liveServChildrenChannels': 'SSELCN1256080112,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '60',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '61',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 50,
                    'priceDen': 1,
                    'priceDec': 51
                  }
                }
              ],
              'id': '1256080113',
              'marketId': '508150681',
              'name': 'Bahuta Acha',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 2,
              'displayOrder': 2,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080113,',
              'liveServChildrenChannels': 'SSELCN1256080113,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '61',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 50,
                  'priceDen': 1,
                  'priceDec': 51
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '62',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 13,
                    'priceDen': 2,
                    'priceDec': 7.5
                  }
                }
              ],
              'id': '1256080114',
              'marketId': '508150681',
              'name': 'Puchita',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 1,
              'displayOrder': 1,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080114,',
              'liveServChildrenChannels': 'SSELCN1256080114,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '62',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '63',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 25,
                    'priceDen': 1,
                    'priceDec': 26
                  }
                }
              ],
              'id': '1256080115',
              'marketId': '508150681',
              'name': 'Outofthegloom',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 7,
              'displayOrder': 7,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080115,',
              'liveServChildrenChannels': 'SSELCN1256080115,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '63',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 25,
                  'priceDen': 1,
                  'priceDec': 26
                }
              ]
            }
          }
        ],
        'id': '508150681',
        'eventId': '232301079',
        'templateMarketId': 136955,
        'templateMarketName': 'Win or Each Way',
        'marketMeaningMajorCode': '-',
        'marketMeaningMinorCode': '--',
        'name': 'Win or Each Way',
        'isLpAvailable': true,
        'isSpAvailable': true,
        'isGpAvailable': true,
        'isEachWayAvailable': true,
        'isPlaceOnlyAvailable': false,
        'eachWayFactorNum': 1,
        'eachWayFactorDen': 5,
        'eachWayPlaces': 3,
        'isMarketBetInRun': true,
        'displayOrder': 0,
        'marketStatusCode': 'A',
        'isActive': true,
        'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
        'liveServChannels': 'sEVMKT0508150681,',
        'liveServChildrenChannels': 'SEVMKT0508150681,',
        'priceTypeCodes': 'LP,GP,SP,',
        'ncastTypeCodes': 'CT,SF,CF,RF,TC,',
        'isAvailable': true,
        'maxAccumulators': 25,
        'minAccumulators': 1,
        'cashoutAvail': 'Y',
        'outcomes': [
          {
            'children': [
              {
                'price': {
                  'id': '56',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 7,
                  'priceDen': 1,
                  'priceDec': 8
                }
              }
            ],
            'id': '1256080106',
            'marketId': '508150681',
            'name': 'Catapult',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 8,
            'displayOrder': 8,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080106,',
            'liveServChildrenChannels': 'SSELCN1256080106,',
            'isAvailable': true,
            'prices': [
              {
                'id': '56',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 7,
                'priceDen': 1,
                'priceDec': 8
              }
            ]
          },
          {
            'id': '1256080107',
            'marketId': '508150681',
            'name': 'Unnamed 2nd Favourite',
            'outcomeMeaningMajorCode': '--',
            'outcomeMeaningMinorCode': '2',
            'displayOrder': 10,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080107,',
            'liveServChildrenChannels': 'SSELCN1256080107,',
            'isAvailable': true
          },
          {
            'id': '1256080108',
            'marketId': '508150681',
            'name': 'Unnamed Favourite',
            'outcomeMeaningMajorCode': '--',
            'outcomeMeaningMinorCode': '1',
            'displayOrder': 9,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080108,',
            'liveServChildrenChannels': 'SSELCN1256080108,',
            'isAvailable': true
          },
          {
            'children': [
              {
                'price': {
                  'id': '57',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 40,
                  'priceDen': 1,
                  'priceDec': 41
                }
              }
            ],
            'id': '1256080109',
            'marketId': '508150681',
            'name': 'Signore Piccolo',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 3,
            'displayOrder': 3,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080109,',
            'liveServChildrenChannels': 'SSELCN1256080109,',
            'isAvailable': true,
            'prices': [
              {
                'id': '57',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 40,
                'priceDen': 1,
                'priceDec': 41
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '58',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 2,
                  'priceDen': 5,
                  'priceDec': 1.4
                }
              }
            ],
            'id': '1256080110',
            'marketId': '508150681',
            'name': 'Owhatanight',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 4,
            'displayOrder': 4,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080110,',
            'liveServChildrenChannels': 'SSELCN1256080110,',
            'isAvailable': true,
            'prices': [
              {
                'id': '58',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 2,
                'priceDen': 5,
                'priceDec': 1.4
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '59',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 33,
                  'priceDen': 1,
                  'priceDec': 34
                }
              }
            ],
            'id': '1256080111',
            'marketId': '508150681',
            'name': 'Shortbackandsides',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 6,
            'displayOrder': 6,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080111,',
            'liveServChildrenChannels': 'SSELCN1256080111,',
            'isAvailable': true,
            'prices': [
              {
                'id': '59',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 33,
                'priceDen': 1,
                'priceDec': 34
              }
            ]
          },
         {
            'children': [
              {
                'price': {
                  'id': '60',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              }
            ],
            'id': '1256080112',
            'marketId': '508150681',
            'name': 'Jazz Legend',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 5,
            'displayOrder': 5,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080112,',
            'liveServChildrenChannels': 'SSELCN1256080112,',
            'isAvailable': true,
            'prices': [
              {
                'id': '60',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 13,
                'priceDen': 2,
                'priceDec': 7.5
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '61',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 50,
                  'priceDen': 1,
                  'priceDec': 51
                }
              }
            ],
            'id': '1256080113',
            'marketId': '508150681',
            'name': 'Bahuta Acha',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 2,
            'displayOrder': 2,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080113,',
            'liveServChildrenChannels': 'SSELCN1256080113,',
            'isAvailable': true,
            'prices': [
              {
                'id': '61',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 50,
                'priceDen': 1,
                'priceDec': 51
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '62',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              }
            ],
            'id': '1256080114',
            'marketId': '508150681',
            'name': 'Puchita',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 1,
            'displayOrder': 1,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080114,',
            'liveServChildrenChannels': 'SSELCN1256080114,',
            'isAvailable': true,
            'prices': [
              {
                'id': '62',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 13,
                'priceDen': 2,
                'priceDec': 7.5
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '63',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 25,
                  'priceDen': 1,
                  'priceDec': 26
                }
              }
            ],
            'id': '1256080115',
            'marketId': '508150681',
            'name': 'Outofthegloom',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 7,
            'displayOrder': 7,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080115,',
            'liveServChildrenChannels': 'SSELCN1256080115,',
            'isAvailable': true,
            'prices': [
              {
                'id': '63',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 25,
                'priceDen': 1,
                'priceDec': 26
              }
            ]
          }
        ]
      }
    ],
    'courseName': 'SOUTHWELL (A.W)',
    'goingCode': 'SD',
    'going': 'Standard',
    'obStartTime': '2021-02-24T13:00:00',
    'rpCourseId': 394,
    'horses': [
      {
        'trainer': 'Antony Brittain',
        'rating': '73',
        'weight': '9-10',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/230347.png',
        'horseAge': 6,
        'jockey': 'Angus Villiers',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/230347.png',
        'silk': '230347.png',
        'starRating': '4',
        'rpJockeyId': 99322,
        'rpHorseId': 1384730,
        'rpTrainerId': 30941,
        'weightLbs': 136,
        'courseDistanceWinner': 'CD',
        'horseName': 'Puchita',
        'spotlight': 'All five career wins came over C&D last year and she',
        'owner': 'Antony Brittain',
        'isBeatenFavourite': false,
        'horseSuffix': 'IRE'
      },
      {
        'trainer': 'Michael Mullineaux',
        'rating': '70',
        'weight': '9-9',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/182276.png',
        'horseAge': 6,
        'jockey': 'Phil Dennis',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/182276.png',
        'silk': '182276.png',
        'starRating': '1',
        'rpJockeyId': 92884,
        'rpHorseId': 1417683,
        'rpTrainerId': 7001,
        'weightLbs': 135,
        'courseDistanceWinner': 'D',
        'horseName': 'Bahuta Acha',
        'spotlight': 'Failed to beat a rival in his three',
        'owner': 'G Cornes',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Lucinda Egerton',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/146786d.png',
        'horseAge': 10,
        'jockey': 'Lewis Edmunds',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/146786d.png',
        'silk': '146786d.png',
        'starRating': '1',
        'rpJockeyId': 94663,
        'rpHorseId': 840983,
        'rpTrainerId': 28224,
        'weightLbs': 133,
        'courseDistanceWinner': 'D',
        'horseName': 'Signore Piccolo',
        'owner': 'Mike And Eileen Newbould',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Mike Murphy',
        'rating': '72',
       'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
        'horseAge': 4,
        'jockey': 'Daniel Muscutt',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
        'silk': '205046.png',
        'starRating': '5',
        'rpJockeyId': 91857,
        'rpHorseId': 2537454,
        'rpTrainerId': 19116,
        'weightLbs': 133,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Owhatanight',
        'spotlight': 'Ready winner on first visit here ten days ago',
        'owner': 'Ms Denise Tibbett',
        'isBeatenFavourite': false,
        'isMostTipped': true,
        'horseSuffix': 'GB'
      },
      {
       'trainer': 'Mandy Rowland',
        'rating': '73',
        'weight': '9-0',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/50710.png',
        'horseAge': 8,
        'jockey': 'Josephine Gordon',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/50710.png',
        'silk': '50710.png',
        'starRating': '3',
        'rpJockeyId': 92801,
        'rpHorseId': 890191,
        'rpTrainerId': 9028,
        'weightLbs': 126,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Jazz Legend',
        'owner': 'Miss M E Rowland',
        'isBeatenFavourite': false,
        'horseSuffix': 'USA'
      },
      {
        'trainer': 'Lisa Williamson',
        'rating': '68',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/203850.png',
        'horseAge': 6,
        'jockey': 'Cam Hardie',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/203850.png',
        'silk': '203850.png',
        'starRating': '1',
        'rpJockeyId': 92732,
        'rpHorseId': 1596675,
        'rpTrainerId': 9170,
        'weightLbs': 119,
        'courseDistanceWinner': 'D',
        'horseName': 'Shortbackandsides',
        'owner': 'Ian Furlong',
        'isBeatenFavourite': false,
        'horseSuffix': 'IRE'
      },
      {
        'trainer': 'Brian Rothwell',
        'rating': '54',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/252871.png',
        'horseAge': 4,
        'jockey': 'Faye McManoman',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/252871.png',
        'silk': '252871.png',
        'starRating': '1',
        'rpJockeyId': 96409,
        'rpHorseId': 2917899,
        'rpTrainerId': 5696,
        'weightLbs': 119,
        'horseName': 'Outofthegloom',
        'owner': 'S P Hudson & Brian Rothwell',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Shaun Keightley',
        'rating': '69',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/287296.png',
        'horseAge': 6,
        'jockey': 'Molly Presland',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/287296.png',
        'silk': '287296.png',
        'starRating': '3',
        'rpJockeyId': 99804,
        'rpHorseId': 1479808,
        'rpTrainerId': 15327,
        'weightLbs': 119,
        'courseDistanceWinner': 'C,D',
        'horseName': 'Catapult',
        'owner': 'S L Keightley',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      }
    ],
    'raceName': 'Play 4 To Win At Betway Handicap (0-60) (6) 4yo+',
    'yards': 1336,
    'distance': '6f 16y',
    'time': '2021-02-24T13:00:00',
    'rpRaceId': 776848,
    'powerHorses': [
      {
        'trainer': 'Mike Murphy',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
        'horseAge': 4,
        'jockey': 'Daniel Muscutt',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
        'silk': '205046.png',
        'starRating': '5',
        'rpJockeyId': 91857,
        'rpHorseId': 2537454,
        'rpTrainerId': 19116,
        'weightLbs': 133,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Owhatanight',
        'owner': 'Ms Denise Tibbett',
        'isBeatenFavourite': false,
        'isMostTipped': true,
        'horseSuffix': 'GB'
      }
    ],
    'powerHorse': {
      'trainer': 'Mike Murphy',
      'rating': '72',
      'weight': '9-7',
      'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
      'horseAge': 4,
      'jockey': 'Daniel Muscutt',
      'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
      'silk': '205046.png',
      'starRating': '5',
      'rpJockeyId': 91857,
      'rpHorseId': 2537454,
      'rpTrainerId': 19116,
      'weightLbs': 133,
      'courseDistanceWinner': 'CD,D',
      'horseName': 'Owhatanight',
      'owner': 'Ms Denise Tibbett',
      'isBeatenFavourite': false,
      'isMostTipped': true,
      'horseSuffix': 'GB'
    },
    'isMostPowerHorse': true
  }
];

export const outcomeUnsuspendedRacesMock = [
  {
    'id': '232301079',
    'name': '13:00 Southwell',
    'eventStatusCode': 'A',
    'isActive': true,
    'displayOrder': 780,
    'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
    'eventSortCode': 'MTCH',
    'startTime': '2021-02-24T13:00:00Z',
    'rawIsOffCode': 'N',
    'classId': '223',
    'typeId': '1972',
    'sportId': '21',
    'liveServChannels': 'sEVENT0232301079,',
   'liveServChildrenChannels': 'SEVENT0232301079,',
    'categoryId': '21',
    'categoryCode': 'HORSE_RACING',
    'categoryName': 'Horse Racing',
    'className': 'Horse Racing - Live',
    'classDisplayOrder': -9500,
    'classSortCode': 'HR',
    'classFlagCodes': 'UF,CN,LI,',
    'typeName': 'Southwell',
    'typeDisplayOrder': -31180,
    'typeFlagCodes': 'UK,NE,QL,AVA,',
    'isOpenEvent': true,
    'isNext24HourEvent': true,
    'isLiveNowOrFutureEvent': true,
    'drilldownTagNames': 'EVFLAG_BL,EVFLAG_AVA,',
    'isAvailable': true,
    'mediaTypeCodes': 'VST,',
    'cashoutAvail': 'Y',
    'responseCreationTime': '2021-02-23T22:42:49.243Z',
    'markets': [
      {
        'children': [
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '56',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 7,
                    'priceDen': 1,
                    'priceDec': 8
                  }
                }
              ],
              'id': '1256080106',
              'marketId': '508150681',
              'name': 'Catapult',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 8,
              'displayOrder': 8,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080106,',
              'liveServChildrenChannels': 'SSELCN1256080106,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '56',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 7,
                  'priceDen': 1,
                  'priceDec': 8
                }
              ]
            }
          },
          {
            'outcome': {
              'id': '1256080107',
              'marketId': '508150681',
              'name': 'Unnamed 2nd Favourite',
              'outcomeMeaningMajorCode': '--',
              'outcomeMeaningMinorCode': '2',
              'displayOrder': 10,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080107,',
              'liveServChildrenChannels': 'SSELCN1256080107,',
              'isAvailable': true
            }
          },
          {
            'outcome': {
              'id': '1256080108',
              'marketId': '508150681',
              'name': 'Unnamed Favourite',
              'outcomeMeaningMajorCode': '--',
              'outcomeMeaningMinorCode': '1',
              'displayOrder': 9,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080108,',
              'liveServChildrenChannels': 'SSELCN1256080108,',
              'isAvailable': true
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '57',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 40,
                    'priceDen': 1,
                    'priceDec': 41
                  }
                }
              ],
              'id': '1256080109',
              'marketId': '508150681',
              'name': 'Signore Piccolo',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 3,
              'displayOrder': 3,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080109,',
              'liveServChildrenChannels': 'SSELCN1256080109,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '57',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 40,
                  'priceDen': 1,
                  'priceDec': 41
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '58',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 2,
                    'priceDen': 5,
                    'priceDec': 1.4
                  }
                }
              ],
              'id': '1256080110',
              'marketId': '508150681',
              'name': 'Owhatanight',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 4,
              'displayOrder': 4,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080110,',
              'liveServChildrenChannels': 'SSELCN1256080110,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '58',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 2,
                  'priceDen': 5,
                  'priceDec': 1.4
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '59',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 33,
                    'priceDen': 1,
                    'priceDec': 34
                  }
                }
              ],
              'id': '1256080111',
              'marketId': '508150681',
              'name': 'Shortbackandsides',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 6,
              'displayOrder': 6,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080111,',
              'liveServChildrenChannels': 'SSELCN1256080111,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '59',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 33,
                  'priceDen': 1,
                  'priceDec': 34
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '60',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 13,
                    'priceDen': 2,
                    'priceDec': 7.5
                  }
                }
              ],
              'id': '1256080112',
              'marketId': '508150681',
              'name': 'Jazz Legend',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 5,
              'displayOrder': 5,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080112,',
              'liveServChildrenChannels': 'SSELCN1256080112,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '60',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '61',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 50,
                    'priceDen': 1,
                    'priceDec': 51
                  }
                }
              ],
              'id': '1256080113',
              'marketId': '508150681',
              'name': 'Bahuta Acha',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 2,
              'displayOrder': 2,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080113,',
              'liveServChildrenChannels': 'SSELCN1256080113,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '61',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 50,
                  'priceDen': 1,
                  'priceDec': 51
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '62',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 13,
                    'priceDen': 2,
                    'priceDec': 7.5
                  }
                }
              ],
              'id': '1256080114',
              'marketId': '508150681',
              'name': 'Puchita',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 1,
              'displayOrder': 1,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080114,',
              'liveServChildrenChannels': 'SSELCN1256080114,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '62',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '63',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 25,
                    'priceDen': 1,
                    'priceDec': 26
                  }
                }
              ],
              'id': '1256080115',
              'marketId': '508150681',
              'name': 'Outofthegloom',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 7,
              'displayOrder': 7,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080115,',
              'liveServChildrenChannels': 'SSELCN1256080115,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '63',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 25,
                  'priceDen': 1,
                  'priceDec': 26
                }
              ]
            }
          }
        ],
        'id': '508150681',
        'eventId': '232301079',
        'templateMarketId': 136955,
        'templateMarketName': 'Win or Each Way',
        'marketMeaningMajorCode': '-',
        'marketMeaningMinorCode': '--',
        'name': 'Win or Each Way',
        'isLpAvailable': true,
        'isSpAvailable': true,
        'isGpAvailable': true,
        'isEachWayAvailable': true,
        'isPlaceOnlyAvailable': false,
        'eachWayFactorNum': 1,
        'eachWayFactorDen': 5,
        'eachWayPlaces': 3,
        'isMarketBetInRun': true,
        'displayOrder': 0,
        'marketStatusCode': 'A',
        'isActive': true,
        'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
        'liveServChannels': 'sEVMKT0508150681,',
        'liveServChildrenChannels': 'SEVMKT0508150681,',
        'priceTypeCodes': 'LP,GP,SP,',
        'ncastTypeCodes': 'CT,SF,CF,RF,TC,',
        'isAvailable': true,
        'maxAccumulators': 25,
        'minAccumulators': 1,
        'cashoutAvail': 'Y',
        'outcomes': [
          {
            'children': [
              {
                'price': {
                  'id': '56',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 7,
                  'priceDen': 1,
                  'priceDec': 8
                }
              }
            ],
            'id': '1256080106',
            'marketId': '508150681',
            'name': 'Catapult',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 8,
            'displayOrder': 8,
            'outcomeStatusCode': 'S',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080106,',
            'liveServChildrenChannels': 'SSELCN1256080106,',
            'isAvailable': true,
            'prices': [
              {
                'id': '56',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 7,
                'priceDen': 1,
                'priceDec': 8
              }
            ]
          },
          {
            'id': '1256080107',
            'marketId': '508150681',
            'name': 'Unnamed 2nd Favourite',
            'outcomeMeaningMajorCode': '--',
            'outcomeMeaningMinorCode': '2',
            'displayOrder': 10,
            'outcomeStatusCode': 'S',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080107,',
            'liveServChildrenChannels': 'SSELCN1256080107,',
            'isAvailable': true
          },
          {
            'id': '1256080108',
            'marketId': '508150681',
            'name': 'Unnamed Favourite',
            'outcomeMeaningMajorCode': '--',
            'outcomeMeaningMinorCode': '1',
            'displayOrder': 9,
            'outcomeStatusCode': 'S',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080108,',
            'liveServChildrenChannels': 'SSELCN1256080108,',
            'isAvailable': true
          },
          {
            'children': [
              {
                'price': {
                  'id': '57',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 40,
                  'priceDen': 1,
                  'priceDec': 41
                }
              }
            ],
            'id': '1256080109',
            'marketId': '508150681',
            'name': 'Signore Piccolo',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 3,
            'displayOrder': 3,
            'outcomeStatusCode': 'S',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080109,',
            'liveServChildrenChannels': 'SSELCN1256080109,',
            'isAvailable': true,
            'prices': [
              {
                'id': '57',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 40,
                'priceDen': 1,
                'priceDec': 41
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '58',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 2,
                  'priceDen': 5,
                  'priceDec': 1.4
                }
              }
            ],
            'id': '1256080110',
            'marketId': '508150681',
           'name': 'Owhatanight',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 4,
            'displayOrder': 4,
            'outcomeStatusCode': 'S',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080110,',
            'liveServChildrenChannels': 'SSELCN1256080110,',
            'isAvailable': true,
            'prices': [
              {
                'id': '58',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 2,
                'priceDen': 5,
                'priceDec': 1.4
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '59',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 33,
                  'priceDen': 1,
                  'priceDec': 34
                }
              }
            ],
            'id': '1256080111',
            'marketId': '508150681',
            'name': 'Shortbackandsides',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 6,
            'displayOrder': 6,
            'outcomeStatusCode': 'S',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080111,',
            'liveServChildrenChannels': 'SSELCN1256080111,',
            'isAvailable': true,
            'prices': [
              {
                'id': '59',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 33,
                'priceDen': 1,
                'priceDec': 34
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '60',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              }
            ],
            'id': '1256080112',
            'marketId': '508150681',
            'name': 'Jazz Legend',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 5,
            'displayOrder': 5,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080112,',
            'liveServChildrenChannels': 'SSELCN1256080112,',
            'isAvailable': true,
            'prices': [
              {
                'id': '60',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 13,
                'priceDen': 2,
                'priceDec': 7.5
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '61',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 50,
                  'priceDen': 1,
                  'priceDec': 51
                }
              }
            ],
            'id': '1256080113',
            'marketId': '508150681',
            'name': 'Bahuta Acha',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 2,
            'displayOrder': 2,
            'outcomeStatusCode': 'S',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080113,',
            'liveServChildrenChannels': 'SSELCN1256080113,',
            'isAvailable': true,
            'prices': [
             {
                'id': '61',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 50,
                'priceDen': 1,
                'priceDec': 51
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '62',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              }
            ],
            'id': '1256080114',
            'marketId': '508150681',
            'name': 'Puchita',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 1,
            'displayOrder': 1,
            'outcomeStatusCode': 'S',
            'isActive': false,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080114,',
            'liveServChildrenChannels': 'SSELCN1256080114,',
            'isAvailable': true,
            'prices': [
              {
                'id': '62',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 13,
                'priceDen': 2,
                'priceDec': 7.5
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '63',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 25,
                  'priceDen': 1,
                  'priceDec': 26
                }
              }
            ],
            'id': '1256080115',
            'marketId': '508150681',
            'name': 'Outofthegloom',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 7,
            'displayOrder': 7,
            'outcomeStatusCode': 'A',
            'isActive': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080115,',
            'liveServChildrenChannels': 'SSELCN1256080115,',
            'isAvailable': true,
            'prices': [
              {
                'id': '63',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 25,
                'priceDen': 1,
                'priceDec': 26
              }
            ]
          }
        ]
      }
    ],
    'courseName': 'SOUTHWELL (A.W)',
    'goingCode': 'SD',
    'going': 'Standard',
    'obStartTime': '2021-02-24T13:00:00',
    'rpCourseId': 394,
    'horses': [
      {
        'trainer': 'Antony Brittain',
        'rating': '73',
        'weight': '9-10',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/230347.png',
        'horseAge': 6,
        'jockey': 'Angus Villiers',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/230347.png',
        'silk': '230347.png',
        'starRating': '4',
        'rpJockeyId': 99322,
        'rpHorseId': 1384730,
        'rpTrainerId': 30941,
        'weightLbs': 136,
        'courseDistanceWinner': 'CD',
        'horseName': 'Puchita',
        'spotlight': 'All five career wins came over C&D last year and she',
        'owner': 'Antony Brittain',
        'isBeatenFavourite': false,
        'horseSuffix': 'IRE'
      },
      {
        'trainer': 'Michael Mullineaux',
        'rating': '70',
        'weight': '9-9',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/182276.png',
        'horseAge': 6,
        'jockey': 'Phil Dennis',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/182276.png',
        'silk': '182276.png',
        'starRating': '1',
        'rpJockeyId': 92884,
        'rpHorseId': 1417683,
        'rpTrainerId': 7001,
        'weightLbs': 135,
        'courseDistanceWinner': 'D',
        'horseName': 'Bahuta Acha',
        'spotlight': 'Failed to beat a rival in his three',
        'owner': 'G Cornes',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Lucinda Egerton',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/146786d.png',
        'horseAge': 10,
        'jockey': 'Lewis Edmunds',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/146786d.png',
        'silk': '146786d.png',
        'starRating': '1',
        'rpJockeyId': 94663,
        'rpHorseId': 840983,
        'rpTrainerId': 28224,
        'weightLbs': 133,
        'courseDistanceWinner': 'D',
        'horseName': 'Signore Piccolo',
        'owner': 'Mike And Eileen Newbould',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Mike Murphy',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
        'horseAge': 4,
        'jockey': 'Daniel Muscutt',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
        'silk': '205046.png',
        'starRating': '5',
        'rpJockeyId': 91857,
        'rpHorseId': 2537454,
        'rpTrainerId': 19116,
        'weightLbs': 133,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Owhatanight',
        'spotlight': 'Ready winner on first visit here ten days ago',
        'owner': 'Ms Denise Tibbett',
        'isBeatenFavourite': false,
        'isMostTipped': true,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Mandy Rowland',
        'rating': '73',
        'weight': '9-0',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/50710.png',
        'horseAge': 8,
        'jockey': 'Josephine Gordon',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/50710.png',
        'silk': '50710.png',
        'starRating': '3',
        'rpJockeyId': 92801,
        'rpHorseId': 890191,
        'rpTrainerId': 9028,
        'weightLbs': 126,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Jazz Legend',
        'owner': 'Miss M E Rowland',
        'isBeatenFavourite': false,
        'horseSuffix': 'USA'
      },
      {
        'trainer': 'Lisa Williamson',
        'rating': '68',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/203850.png',
        'horseAge': 6,
        'jockey': 'Cam Hardie',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/203850.png',
        'silk': '203850.png',
        'starRating': '1',
        'rpJockeyId': 92732,
        'rpHorseId': 1596675,
        'rpTrainerId': 9170,
        'weightLbs': 119,
        'courseDistanceWinner': 'D',
        'horseName': 'Shortbackandsides',
        'owner': 'Ian Furlong',
        'isBeatenFavourite': false,
        'horseSuffix': 'IRE'
      },
      {
        'trainer': 'Brian Rothwell',
        'rating': '54',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/252871.png',
        'horseAge': 4,
        'jockey': 'Faye McManoman',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/252871.png',
        'silk': '252871.png',
        'starRating': '1',
        'rpJockeyId': 96409,
        'rpHorseId': 2917899,
        'rpTrainerId': 5696,
        'weightLbs': 119,
        'horseName': 'Outofthegloom',
        'owner': 'S P Hudson & Brian Rothwell',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Shaun Keightley',
        'rating': '69',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/287296.png',
        'horseAge': 6,
        'jockey': 'Molly Presland',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/287296.png',
        'silk': '287296.png',
        'starRating': '3',
        'rpJockeyId': 99804,
        'rpHorseId': 1479808,
        'rpTrainerId': 15327,
        'weightLbs': 119,
        'courseDistanceWinner': 'C,D',
        'horseName': 'Catapult',
        'owner': 'S L Keightley',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      }
    ],
    'raceName': 'Play 4 To Win At Betway Handicap (0-60) (6) 4yo+',
    'yards': 1336,
    'distance': '6f 16y',
    'time': '2021-02-24T13:00:00',
    'rpRaceId': 776848,
    'powerHorses': [
      {
        'trainer': 'Mike Murphy',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
        'horseAge': 4,
        'jockey': 'Daniel Muscutt',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
        'silk': '205046.png',
        'starRating': '5',
        'rpJockeyId': 91857,
        'rpHorseId': 2537454,
        'rpTrainerId': 19116,
        'weightLbs': 133,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Owhatanight',
        'owner': 'Ms Denise Tibbett',
        'isBeatenFavourite': false,
        'isMostTipped': true,
        'horseSuffix': 'GB'
      }
    ],
    'powerHorse': {
      'trainer': 'Mike Murphy',
      'rating': '72',
      'weight': '9-7',
      'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
      'horseAge': 4,
      'jockey': 'Daniel Muscutt',
      'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
      'silk': '205046.png',
      'starRating': '5',
      'rpJockeyId': 91857,
      'rpHorseId': 2537454,
      'rpTrainerId': 19116,
      'weightLbs': 133,
      'courseDistanceWinner': 'CD,D',
      'horseName': 'Owhatanight',
      'owner': 'Ms Denise Tibbett',
      'isBeatenFavourite': false,
      'isMostTipped': true,
      'horseSuffix': 'GB'
    },
    'isMostPowerHorse': true
  }
];

export const suspendedRacesMock = [
  {
    'id': '232301079',
    'name': '13:00 Southwell',
    'eventStatusCode': 'S',
    'isActive': true,
    'displayOrder': 780,
    'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
    'eventSortCode': 'MTCH',
    'startTime': '2021-02-24T13:00:00Z',
    'rawIsOffCode': 'N',
    'classId': '223',
    'typeId': '1972',
    'sportId': '21',
    'liveServChannels': 'sEVENT0232301079,',
    'liveServChildrenChannels': 'SEVENT0232301079,',
    'categoryId': '21',
    'categoryCode': 'HORSE_RACING',
    'categoryName': 'Horse Racing',
    'className': 'Horse Racing - Live',
    'classDisplayOrder': -9500,
    'classSortCode': 'HR',
    'classFlagCodes': 'UF,CN,LI,',
    'typeName': 'Southwell',
    'typeDisplayOrder': -31180,
    'typeFlagCodes': 'UK,NE,QL,AVA,',
    'isOpenEvent': true,
    'isNext24HourEvent': true,
    'isLiveNowOrFutureEvent': true,
    'drilldownTagNames': 'EVFLAG_BL,EVFLAG_AVA,',
    'isAvailable': true,
    'mediaTypeCodes': 'VST,',
    'cashoutAvail': 'Y',
    'responseCreationTime': '2021-02-23T22:42:49.243Z',
    'markets': [
      {
        'children': [
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '56',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 7,
                    'priceDen': 1,
                    'priceDec': 8
                  }
                }
              ],
              'id': '1256080106',
              'marketId': '508150681',
              'name': 'Catapult',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 8,
              'displayOrder': 8,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080106,',
              'liveServChildrenChannels': 'SSELCN1256080106,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '56',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 7,
                  'priceDen': 1,
                  'priceDec': 8
                }
              ]
            }
          },
          {
            'outcome': {
              'id': '1256080107',
              'marketId': '508150681',
              'name': 'Unnamed 2nd Favourite',
              'outcomeMeaningMajorCode': '--',
              'outcomeMeaningMinorCode': '2',
              'displayOrder': 10,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080107,',
              'liveServChildrenChannels': 'SSELCN1256080107,',
              'isAvailable': true
            }
         },
          {
            'outcome': {
              'id': '1256080108',
              'marketId': '508150681',
              'name': 'Unnamed Favourite',
              'outcomeMeaningMajorCode': '--',
              'outcomeMeaningMinorCode': '1',
              'displayOrder': 9,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080108,',
              'liveServChildrenChannels': 'SSELCN1256080108,',
              'isAvailable': true
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '57',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 40,
                    'priceDen': 1,
                    'priceDec': 41
                  }
                }
              ],
              'id': '1256080109',
              'marketId': '508150681',
              'name': 'Signore Piccolo',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 3,
              'displayOrder': 3,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080109,',
              'liveServChildrenChannels': 'SSELCN1256080109,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '57',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 40,
                  'priceDen': 1,
                  'priceDec': 41
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '58',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 2,
                    'priceDen': 5,
                    'priceDec': 1.4
                  }
                }
              ],
              'id': '1256080110',
              'marketId': '508150681',
              'name': 'Owhatanight',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 4,
              'displayOrder': 4,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080110,',
              'liveServChildrenChannels': 'SSELCN1256080110,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '58',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 2,
                  'priceDen': 5,
                  'priceDec': 1.4
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '59',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 33,
                    'priceDen': 1,
                    'priceDec': 34
                  }
                }
              ],
              'id': '1256080111',
              'marketId': '508150681',
              'name': 'Shortbackandsides',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 6,
              'displayOrder': 6,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080111,',
              'liveServChildrenChannels': 'SSELCN1256080111,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '59',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 33,
                  'priceDen': 1,
                  'priceDec': 34
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '60',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 13,
                    'priceDen': 2,
                    'priceDec': 7.5
                  }
                }
              ],
              'id': '1256080112',
              'marketId': '508150681',
              'name': 'Jazz Legend',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 5,
              'displayOrder': 5,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080112,',
              'liveServChildrenChannels': 'SSELCN1256080112,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '60',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '61',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 50,
                    'priceDen': 1,
                    'priceDec': 51
                  }
                }
              ],
              'id': '1256080113',
              'marketId': '508150681',
              'name': 'Bahuta Acha',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 2,
              'displayOrder': 2,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080113,',
              'liveServChildrenChannels': 'SSELCN1256080113,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '61',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 50,
                  'priceDen': 1,
                  'priceDec': 51
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '62',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 13,
                    'priceDen': 2,
                    'priceDec': 7.5
                  }
                }
              ],
              'id': '1256080114',
              'marketId': '508150681',
              'name': 'Puchita',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 1,
              'displayOrder': 1,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080114,',
              'liveServChildrenChannels': 'SSELCN1256080114,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '62',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              ]
            }
          },
          {
            'outcome': {
              'children': [
                {
                  'price': {
                    'id': '63',
                    'isActive': true,
                    'displayOrder': 1,
                    'priceType': 'LP',
                    'priceNum': 25,
                    'priceDen': 1,
                    'priceDec': 26
                  }
                }
              ],
              'id': '1256080115',
              'marketId': '508150681',
              'name': 'Outofthegloom',
              'outcomeMeaningMajorCode': '--',
              'runnerNumber': 7,
              'displayOrder': 7,
              'outcomeStatusCode': 'A',
              'isActive': true,
              'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
              'liveServChannels': 'sSELCN1256080115,',
              'liveServChildrenChannels': 'SSELCN1256080115,',
              'isAvailable': true,
              'prices': [
                {
                  'id': '63',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 25,
                  'priceDen': 1,
                  'priceDec': 26
                }
              ]
            }
          }
        ],
        'id': '508150681',
        'eventId': '232301079',
        'templateMarketId': 136955,
        'templateMarketName': 'Win or Each Way',
        'marketMeaningMajorCode': '-',
        'marketMeaningMinorCode': '--',
        'name': 'Win or Each Way',
        'isLpAvailable': true,
        'isSpAvailable': true,
        'isGpAvailable': true,
        'isEachWayAvailable': true,
        'isPlaceOnlyAvailable': false,
        'eachWayFactorNum': 1,
        'eachWayFactorDen': 5,
        'eachWayPlaces': 3,
        'isMarketBetInRun': true,
        'displayOrder': 0,
        'marketStatusCode': 'S',
        'isActive': true,
        'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
        'liveServChannels': 'sEVMKT0508150681,',
        'liveServChildrenChannels': 'SEVMKT0508150681,',
        'priceTypeCodes': 'LP,GP,SP,',
        'ncastTypeCodes': 'CT,SF,CF,RF,TC,',
        'isAvailable': true,
        'maxAccumulators': 25,
        'minAccumulators': 1,
        'cashoutAvail': 'Y',
        'outcomes': [
          {
            'children': [
              {
                'price': {
                  'id': '56',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 7,
                  'priceDen': 1,
                  'priceDec': 8
                }
              }
            ],
            'id': '1256080106',
            'marketId': '508150681',
            'name': 'Catapult',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 8,
            'displayOrder': 8,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080106,',
            'liveServChildrenChannels': 'SSELCN1256080106,',
            'isAvailable': true,
            'prices': [
              {
                'id': '56',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 7,
                'priceDen': 1,
                'priceDec': 8
              }
            ]
          },
          {
            'id': '1256080107',
            'marketId': '508150681',
            'name': 'Unnamed 2nd Favourite',
            'outcomeMeaningMajorCode': '--',
            'outcomeMeaningMinorCode': '2',
            'displayOrder': 10,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080107,',
            'liveServChildrenChannels': 'SSELCN1256080107,',
            'isAvailable': true
          },
          {
            'id': '1256080108',
            'marketId': '508150681',
            'name': 'Unnamed Favourite',
            'outcomeMeaningMajorCode': '--',
            'outcomeMeaningMinorCode': '1',
            'displayOrder': 9,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080108,',
            'liveServChildrenChannels': 'SSELCN1256080108,',
            'isAvailable': true
          },
          {
            'children': [
              {
                'price': {
                  'id': '57',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 40,
                  'priceDen': 1,
                  'priceDec': 41
                }
              }
            ],
            'id': '1256080109',
            'marketId': '508150681',
            'name': 'Signore Piccolo',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 3,
            'displayOrder': 3,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080109,',
            'liveServChildrenChannels': 'SSELCN1256080109,',
            'isAvailable': true,
            'prices': [
              {
                'id': '57',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 40,
                'priceDen': 1,
                'priceDec': 41
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '58',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 2,
                  'priceDen': 5,
                  'priceDec': 1.4
                }
              }
            ],
            'id': '1256080110',
            'marketId': '508150681',
            'name': 'Owhatanight',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 4,
            'displayOrder': 4,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080110,',
            'liveServChildrenChannels': 'SSELCN1256080110,',
            'isAvailable': true,
            'prices': [
              {
                'id': '58',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 2,
                'priceDen': 5,
                'priceDec': 1.4
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '59',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 33,
                  'priceDen': 1,
                  'priceDec': 34
                }
              }
            ],
            'id': '1256080111',
            'marketId': '508150681',
            'name': 'Shortbackandsides',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 6,
            'displayOrder': 6,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080111,',
            'liveServChildrenChannels': 'SSELCN1256080111,',
            'isAvailable': true,
            'prices': [
              {
                'id': '59',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 33,
                'priceDen': 1,
                'priceDec': 34
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '60',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              }
            ],
            'id': '1256080112',
            'marketId': '508150681',
            'name': 'Jazz Legend',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 5,
            'displayOrder': 5,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080112,',
            'liveServChildrenChannels': 'SSELCN1256080112,',
            'isAvailable': true,
            'prices': [
              {
                'id': '60',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 13,
                'priceDen': 2,
                'priceDec': 7.5
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '61',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 50,
                  'priceDen': 1,
                  'priceDec': 51
                }
              }
            ],
            'id': '1256080113',
            'marketId': '508150681',
            'name': 'Bahuta Acha',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 2,
            'displayOrder': 2,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080113,',
            'liveServChildrenChannels': 'SSELCN1256080113,',
            'isAvailable': true,
            'prices': [
              {
                'id': '61',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 50,
                'priceDen': 1,
                'priceDec': 51
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '62',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 13,
                  'priceDen': 2,
                  'priceDec': 7.5
                }
              }
            ],
            'id': '1256080114',
            'marketId': '508150681',
            'name': 'Puchita',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 1,
            'displayOrder': 1,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080114,',
            'liveServChildrenChannels': 'SSELCN1256080114,',
            'isAvailable': true,
            'prices': [
              {
                'id': '62',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 13,
                'priceDen': 2,
                'priceDec': 7.5
              }
            ]
          },
          {
            'children': [
              {
                'price': {
                  'id': '63',
                  'isActive': true,
                  'displayOrder': 1,
                  'priceType': 'LP',
                  'priceNum': 25,
                  'priceDen': 1,
                  'priceDec': 26
                }
              }
            ],
            'id': '1256080115',
            'marketId': '508150681',
            'name': 'Outofthegloom',
            'outcomeMeaningMajorCode': '--',
            'runnerNumber': 7,
            'displayOrder': 7,
            'outcomeStatusCode': 'S',
            'isResulted': true,
            'siteChannels': 'C,D,E,H,I,M,P,p,Q,R,W,X,Z,',
            'liveServChannels': 'sSELCN1256080115,',
            'liveServChildrenChannels': 'SSELCN1256080115,',
            'isAvailable': true,
            'prices': [
              {
                'id': '63',
                'isActive': true,
                'displayOrder': 1,
                'priceType': 'LP',
                'priceNum': 25,
                'priceDen': 1,
                'priceDec': 26
              }
            ]
          }
        ]
      }
    ],
    'courseName': 'SOUTHWELL (A.W)',
    'goingCode': 'SD',
    'going': 'Standard',
    'obStartTime': '2021-02-24T13:00:00',
    'rpCourseId': 394,
    'horses': [
      {
        'trainer': 'Antony Brittain',
        'rating': '73',
        'weight': '9-10',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/230347.png',
        'horseAge': 6,
        'jockey': 'Angus Villiers',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/230347.png',
        'silk': '230347.png',
        'starRating': '4',
        'rpJockeyId': 99322,
        'rpHorseId': 1384730,
        'rpTrainerId': 30941,
        'weightLbs': 136,
        'courseDistanceWinner': 'CD',
        'horseName': 'Puchita',
        'spotlight': 'All five career wins came over C&D last year and she',
        'owner': 'Antony Brittain',
        'isBeatenFavourite': false,
        'horseSuffix': 'IRE'
      },
      {
        'trainer': 'Michael Mullineaux',
        'rating': '70',
        'weight': '9-9',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/182276.png',
        'horseAge': 6,
        'jockey': 'Phil Dennis',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/182276.png',
        'silk': '182276.png',
        'starRating': '1',
        'rpJockeyId': 92884,
        'rpHorseId': 1417683,
        'rpTrainerId': 7001,
        'weightLbs': 135,
        'courseDistanceWinner': 'D',
        'horseName': 'Bahuta Acha',
        'spotlight': 'Failed to beat a rival in his three',
        'owner': 'G Cornes',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Lucinda Egerton',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/146786d.png',
        'horseAge': 10,
        'jockey': 'Lewis Edmunds',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/146786d.png',
        'silk': '146786d.png',
        'starRating': '1',
        'rpJockeyId': 94663,
        'rpHorseId': 840983,
        'rpTrainerId': 28224,
        'weightLbs': 133,
        'courseDistanceWinner': 'D',
        'horseName': 'Signore Piccolo',
        'owner': 'Mike And Eileen Newbould',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Mike Murphy',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
        'horseAge': 4,
        'jockey': 'Daniel Muscutt',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
        'silk': '205046.png',
        'starRating': '5',
        'rpJockeyId': 91857,
        'rpHorseId': 2537454,
        'rpTrainerId': 19116,
        'weightLbs': 133,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Owhatanight',
        'spotlight': 'Ready winner on first visit here ten days ago',
        'owner': 'Ms Denise Tibbett',
        'isBeatenFavourite': false,
        'isMostTipped': true,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Mandy Rowland',
        'rating': '73',
        'weight': '9-0',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/50710.png',
        'horseAge': 8,
        'jockey': 'Josephine Gordon',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/50710.png',
        'silk': '50710.png',
        'starRating': '3',
        'rpJockeyId': 92801,
        'rpHorseId': 890191,
        'rpTrainerId': 9028,
        'weightLbs': 126,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Jazz Legend',
        'owner': 'Miss M E Rowland',
        'isBeatenFavourite': false,
        'horseSuffix': 'USA'
      },
      {
        'trainer': 'Lisa Williamson',
        'rating': '68',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/203850.png',
        'horseAge': 6,
        'jockey': 'Cam Hardie',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/203850.png',
        'silk': '203850.png',
        'starRating': '1',
        'rpJockeyId': 92732,
        'rpHorseId': 1596675,
        'rpTrainerId': 9170,
        'weightLbs': 119,
        'courseDistanceWinner': 'D',
        'horseName': 'Shortbackandsides',
        'owner': 'Ian Furlong',
        'isBeatenFavourite': false,
        'horseSuffix': 'IRE'
      },
      {
        'trainer': 'Brian Rothwell',
        'rating': '54',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/252871.png',
        'horseAge': 4,
        'jockey': 'Faye McManoman',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/252871.png',
        'silk': '252871.png',
        'starRating': '1',
        'rpJockeyId': 96409,
        'rpHorseId': 2917899,
        'rpTrainerId': 5696,
        'weightLbs': 119,
        'horseName': 'Outofthegloom',
        'owner': 'S P Hudson & Brian Rothwell',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      },
      {
        'trainer': 'Shaun Keightley',
        'rating': '69',
        'weight': '8-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/287296.png',
        'horseAge': 6,
        'jockey': 'Molly Presland',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/287296.png',
        'silk': '287296.png',
        'starRating': '3',
        'rpJockeyId': 99804,
        'rpHorseId': 1479808,
        'rpTrainerId': 15327,
        'weightLbs': 119,
        'courseDistanceWinner': 'C,D',
        'horseName': 'Catapult',
        'owner': 'S L Keightley',
        'isBeatenFavourite': false,
        'horseSuffix': 'GB'
      }
    ],
    'raceName': 'Play 4 To Win At Betway Handicap (0-60) (6) 4yo+',
    'yards': 1336,
    'distance': '6f 16y',
    'time': '2021-02-24T13:00:00',
    'rpRaceId': 776848,
    'powerHorses': [
      {
        'trainer': 'Mike Murphy',
        'rating': '72',
        'weight': '9-7',
        'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
        'horseAge': 4,
        'jockey': 'Daniel Muscutt',
        'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
        'silk': '205046.png',
        'starRating': '5',
        'rpJockeyId': 91857,
        'rpHorseId': 2537454,
        'rpTrainerId': 19116,
        'weightLbs': 133,
        'courseDistanceWinner': 'CD,D',
        'horseName': 'Owhatanight',
        'owner': 'Ms Denise Tibbett',
        'isBeatenFavourite': false,
        'isMostTipped': true,
        'horseSuffix': 'GB'
      }
    ],
    'powerHorse': {
      'trainer': 'Mike Murphy',
      'rating': '72',
      'weight': '9-7',
      'silkCoral': 'https://silks.coral.co.uk/RP/images/205046.png',
      'horseAge': 4,
      'jockey': 'Daniel Muscutt',
      'silkLadbrokes': 'https://silks.ladbrokes.com/RP/images/205046.png',
      'silk': '205046.png',
      'starRating': '5',
      'rpJockeyId': 91857,
      'rpHorseId': 2537454,
      'rpTrainerId': 19116,
      'weightLbs': 133,
      'courseDistanceWinner': 'CD,D',
      'horseName': 'Owhatanight',
      'owner': 'Ms Denise Tibbett',
      'isBeatenFavourite': false,
      'isMostTipped': true,
      'horseSuffix': 'GB'
    },
    'isMostPowerHorse': true
  }
];

export const priceUpdate = {

  cashoutAvail: 'N',
  correctPriceTypeCode: 'SP',
  displayOrder: 0,
  eachWayFactorDen: '4',
  eachWayFactorNum: '1',
  eachWayPlaces: '3',
  eventId: '1024863',
  id: '125825053',
  prices: {
    priceDec: Number(1),
    priceDen: Number(11),
    priceNum: Number(3),
    isDisplayed: true,
    priceType: 'LP'
  },
  children: [
    {
      outcome: {
        liveServChannels:'sSELCN1256080108,',
        displayOrder: 1,
        icon: false,
        id: '125825053',
        name: 'Sancta Sedes',
        silkName: '123.png',
        prices: [{
          priceNum: '9',
          priceDen: '2'
        }
        ]
      }

    }
  ],
  outcomes: [
    {
      displayOrder: 1,
      icon: false,
      id: '125825053',
      name: 'Sancta Sedes',
      silkName: '123.png',
      'outcomeMeaningMajorCode': 'HH',
      'outcomeMeaningMinorCode': 'H',
      'outcomeStatusCode': 'A',
      'liveServChannels': 'sSELCN1310067201,',
      'correctPriceType': 'LP',
      'correctedOutcomeMeaningMinorCode': 1,
      prices: [{
        'id': '45',
        'priceType': 'LP',
        'priceNum': 25,
        'priceDen': 1,
        'priceDec': 2.5,
        'liveShowTimer': {
          'type': ''
        }
      },
      {
        'id': '45',
        'priceType': 'LP',
        'priceNum': 24,
        'priceDen': 1,
        'priceDec': 2.4,
        'liveShowTimer': {
          'type': ''
        }
      },
      {
        'id': '45',
        'priceType': 'LP',
        'priceNum': 23,
        'priceDen': 1,
        'priceDec': 2.4,
        'liveShowTimer': {
          'type': ''
        }
      },
      {
        'id': '45',
        'priceType': 'LP',
        'priceNum': 25,
        'priceDen': 1,
        'priceDec': 2.5,
        'liveShowTimer': {
          'type': ''
        }
      },
      ]
    },
    {
      displayOrder: 1,
      icon: false,
      id: '125825053',
      name: 'Sancta Sedes',
      silkName: '123.png',
      'outcomeMeaningMajorCode': 'HH',
      'outcomeMeaningMinorCode': 'H',
      'outcomeStatusCode': 'A',
      'liveServChannels': 'sSELCN1310067201,',
      'correctPriceType': 'LP',
      'correctedOutcomeMeaningMinorCode': 1,
      prices: [{
        'id': '45',
        'priceType': 'LP',
        'priceNum': 24,
        'priceDen': 1,
        'priceDec': 2.5,
        'liveShowTimer': {
          'type': ''
        }
      },
      {
        'id': '45',
        'priceType': 'LP',
        'priceNum': 24,
        'priceDen': 1,
        'priceDec': 2.4,
        'liveShowTimer': {
          'type': ''
        }
      }
      ]
    },
    {
      displayOrder: 1,
      icon: false,
      id: '125825053',
      name: 'Sancta Sedes',
      silkName: '123.png',
      'outcomeMeaningMajorCode': 'HH',
      'outcomeMeaningMinorCode': 'H',
      'outcomeStatusCode': 'A',
      'liveServChannels': 'sSELCN1310067201,',
      'correctPriceType': 'LP',
      'correctedOutcomeMeaningMinorCode': 1,
      prices: [{
        'id': '45',
        'priceType': 'LP',
        'priceNum': 26,
        'priceDen': 1,
        'priceDec': 2.5,
        'liveShowTimer': {
          'type': ''
        }
      },
      {
        'id': '45',
        'priceType': 'LP',
        'priceNum': 26,
        'priceDen': 1,
        'priceDec': 2.4,
        'liveShowTimer': {
          'type': ''
        }
      }
      ]
    }
  ]
};

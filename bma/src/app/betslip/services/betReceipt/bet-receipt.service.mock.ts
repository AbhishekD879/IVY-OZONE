export const events = [{
  categoryCode: 'BASKETBALL',
  categoryId: '6',
  classId: 51,
  typeId: 136,
  id: '111',
  selectionId: 1,
  marketId: 1,
  name: 'EventName1'
}, {
  categoryCode: 'FOOTBALL',
  categoryId: '16',
  classId: 97,
  typeId: 435,
  id: '222',
  selectionId: 1,
  marketId: 1,
  name: 'EventName2'
}];

const bets = [{
  betId: '381522',
  stake: '1.00',
  numLegs: '1',
  numLines: '1',
  stakePerLine: '1.00',
  betType: 'SGL',
  potentialPayout: '1.50',
  status: 'A',
  leg: [{
    part: [{
      outcome: '449905491',
      priceNum: '1',
      priceDen: '2',
      handicap: '',
      eventId: '6702230',
      event: {categoryName: 'Football'}
    }]
  }]
}, {
  betId: '381523',
  stake: '1.00',
  numLegs: '1',
  numLines: '1',
  stakePerLine: '1.00',
  betType: 'SGL',
  potentialPayout: '3.00',
  status: 'A',
  leg: [{
    legSort: 'SF',
    part: [{
      outcome: '449905612',
      priceNum: '2',
      priceDen: '1',
      handicap: '',
      eventId: '6702260',
      event: {categoryName: 'Football'}
    }]
  }]
}, {
  betId: '381524',
  stake: '1.00',
  numLegs: '2',
  numLines: '1',
  stakePerLine: '1.00',
  betType: 'DBL',
  potentialPayout: '4.50',
  status: 'A',
  leg: [{
    part: [{
      outcome: '449905491',
      priceNum: '1',
      priceDen: '2',
      handicap: '',
      eventId: '6702230',
      event: {categoryName: 'Football'}
    }]
  }, {
    part: [{
      outcome: '449905612',
      priceNum: '2',
      priceDen: '1',
      handicap: '',
      eventId: '6702260',
      event: {categoryName: 'Football'}
    }]
  }]
}];

export const overaskPlaceBets = [{
  betId: '381522',
  stake: '1.00',
  numLegs: '1',
  numLines: '1',
  isReferred: 'Y',
  stakePerLine: '1.00',
  betType: 'SGL',
  potentialPayout: '1.50',
  status: 'A',
  leg: [{
    part: [{
      outcome: '449905491',
      priceNum: '1',
      priceDen: '2',
      handicap: '',
      eventId: '6702230'
    }]
  }]
}];

export const prePlayPlaceBets = [{
  betId: '381522',
  stake: '1.00',
  numLegs: '1',
  numLines: '1',
  isConfirmed: 'Y',
  stakePerLine: '1.00',
  betType: 'SGL',
  potentialPayout: '1.50',
  status: 'A',
  leg: [{
    part: [{
      outcome: '449905491',
      priceNum: '1',
      priceDen: '2',
      handicap: '',
      eventId: '6702230',
      event:{categoryName: 'test'}
    }]
  }]
}];

export const inPlayPlaceBets = [{
  betId: '381522',
  stake: '1.00',
  numLegs: '1',
  numLines: '1',
  isConfirmed: 'N',
  stakePerLine: '1.00',
  betType: 'SGL',
  potentialPayout: '1.50',
  status: 'A',
  leg: [{
    part: [{
      outcome: '449905491',
      priceNum: '1',
      priceDen: '2',
      handicap: '',
      eventId: '6702230',
      eventDesc: ' ',
      description: ' ',
      eventMarketDesc: ' ',
    }]
  }]
}];

export const inPlayReadBets = [{
  betId: '381522',
  stake: '1.00',
  numLegs: '1',
  numLines: '1',
  isConfirmed: 'Y',
  stakePerLine: '1.00',
  betType: 'SGL',
  potentialPayout: '1.50',
  status: 'A',
  leg: [{
    part: [{
      outcome: '449905491',
      priceNum: '1',
      priceDen: '2',
      handicap: '',
      eventId: '6702230'
    }]
  }]
}];

export const betReceiptsMock = {
  receiptEventsMock: {
    multiples: [
      {
        betTypeName: 'Double',
        receipt: 'O/33',
        stake: { amount: '5.00'},
        numLegs: '1',
        numLines: '1',
        potentialPayout: '5.00',
        leg: [
          { part: [ { event: events[1], isFootball: true, outcome: 1, marketId: 1, eventMarketDesc: 'Test Market Name' } ] },
          { part: [ { event: events[0], outcome: 1, marketId: 1, eventMarketDesc: 'Test Market Name' } ] }
        ]
      }
    ],
    singles: [
      {
        betId: '123',
        betType: 'type',
        receipt: 'O/22',
        betTypeName: 'Single',
        stake: { amount: '5.00'},
        eventMarket: 'Match Result',
        numLegs: '1',
        numLines: '1',
        potentialPayout: '5.00',
        leg: [
          { part: [ { event: events[0], outcome: 1, marketId: 1 } ] }
        ],
        oddsBoosted: true
      },
      {
        betId: '456',
        betType: 'type',
        receipt: 'O/22',
        betTypeName: 'Single',
        stake: { amount: '10.00'},
        eventMarket: 'Match Result',
        numLegs: '1',
        numLines: '1',
        potentialPayout: '20.00',
        leg: [
          { part: [ { event: events[1], outcome: 1, marketId: 1 } ] }
        ],
        isFootball: true
      }
    ]
  },
  eventsInReceipt: [...events, events[1], events[1]],
  ids: [ 381480, 381481],
  receiptData: {
    response: {
      respTransGetBetDetail: {
        bet: bets
      }
    }
  },
  eventIds: [6702230, 6702260, 6702230, 6702260],
  events: [
    { id: 6702260, name: 'Crystal Palace v West Brom', categoryId: '16', categoryCode: 'FOOTBALL' },
    { id: 6702230, name: 'Chelsea v Hull', categoryId: '16', categoryCode: 'FOOTBALL' }
  ],
};
export const receiptDataMock = {
  bet: [{
      betId: "910821",
      betType: "SGL",
      receipt: "O/0342060/0000011",
      settled: "N",
      betTags: {
          betTag: [
              {
                  tagName: "CAPPED",
                  tagValue: ""
              }
          ]
      },
  }, {
      betId: "910822",
      betType: "DBL",
      receipt: "O/0342060/0000012",
      betTags: {
          betTag: [
              {
                  tagName: "CAPPED",
                  tagValue: ""
              }
          ]
      },
  }]
}
export const receiptDataMock2 = {
  bet: [{
      betId: "910821",
      betType: "SGL",
      settled: "N",
      betTags: {
      },
  }, {
      betId: "910822",
      betType: "DBL",
      betTags: {
      },
  }]
}
export const receiptDataMock3 = {
  bet: [{
      betId: "910821",
      betType: "SGL",
      receipt: "O/0342060/0000011",
      settled: "N",
      betTags: {
          betTag: [{}]
      },
  }, {
      betId: "910822",
      betType: "DBL",
      receipt: "O/0342060/0000012",
      betTags: {
          betTag: [{}]
      },
  }]
}
export const receiptDataMock4 = {
  bet: [{
      betId: "910821",
      betType: "SGL",
      receipt: "O/0342060/0000011",
      settled: "N",
      betTags: {
          betTag: [
              {
                  tagName: "",
                  tagValue: ""
              }
          ]
      },
  }, {
      betId: "910822",
      betType: "DBL",
      receipt: "O/0342060/0000012",
      betTags: {
          betTag: [
              {
                  tagName: "",
                  tagValue: ""
              }
          ]
      },
  }]
}
export const receiptDataMock5 = {
  bet: [{
      betId: "910821",
      betType: "SGL",
      receipt: null,
      settled: "N",
      betTags: {
          betTag: [
              {
                  tagName: "",
                  tagValue: ""
              }
          ]
      },
  }, {
      betId: "910822",
      betType: "DBL",
      receipt: null,
      betTags: {
          betTag: [
              {
                  tagName: "",
                  tagValue: ""
              }
          ]
      },
  }]
}

export const betsRacingMock = [{
  betId: '574707',
  betType: 'SGL',
  betTypeName: 'Single',
  betTermsChange: [],
  bonus: '',
  callId: '',
  cashoutStatus: '',
  cashoutValue: '0.90',
  currency: 'GBP',
  date: '2018-12-27 07:24:19',
  eventMarket: 'Win or Each Way',
  eventName: '08:10 Steepledowns',
  ipaddr: '10.80.62.7',
  leg:   [ {
    legNo: 'Win or Each Way',
    legSort: 'Win or Each Way',
    
    part: [{
      birIndex: ' ',
      deadHeatEachWayDeductions: ' ',
      deadHeatWinDeductions: ' ',
      description: ' ',
      dispResult: ' ',
      eachWayDen: ' ',
      eachWayNum: ' ',
      eachWayPlaces: ' ',
      eventCategoryId: '21',
      event: {
        cashoutAvail: ' ',
        categoryCode: ' ',
        categoryId: '21',
        categoryName: ' ',
        displayOrder: 1,
        eventSortCode: ' ',
        eventStatusCode: ' ',
        id: 1,
        liveServChannels: ' ',
        liveServChildrenChannels: ' ',
        typeId: ' ',
        typeName: ' ',
        name: ' ',
        startTime: ' ',
      },
      eventClassName: ' ',
      eventDesc: ' ',
      eventId: ' ',
      eventMarketDesc: ' ',
      eventMarketSort: ' ',
      eventTypeDesc: ' ',
      fbResult: ' ',
      handicap: ' ',
      marketId: ' ',
      outcome: ' ',
      partNo: ' ',
      priceDen: ' ',
      priceNum: ' ',
      priceType: ' ',
      result: ' ',
      resultConf: ' ',
      resultPlaces: ' ',
      rule4Deductions: ' ',
      runnerNum: ' ',
      startPriceDen: ' ',
      startPriceNum: ' ',
      startTime: ' ',
    }]
  } ],
  legType: 'W',
  name: 'EMILY MOLLIE',
  numLegs: '1',
  numLines: '1',
  numLinesLose: '0',
  numLinesVoid: '0',
  numLinesWin: '0',
  numSelns: '1',
  odds: {
    frac: '5/2',
    dec: '3.50',
  },
  oddsBoosted: false,
  paid: 'Y',
  placedBy: '',
  potentialPayout: '3.50',
  receipt: 'O/0208872/0000115',
  refund: '0.00',
  settleInfo: '',
  settled: 'N',
  settledAt: '',
  source: 'M',
  stake: '1.00',
  stakePerLine: '1.00',
  startTime: '2018-12-27 08:10:00',
  asyncAcceptStatus: 'A',
  status: 'A',
  tax: '0.00',
  taxRate: '0.00',
  taxType: 'S',
  stakeValue: 1.00,
  tokenValue: '0.00',
  uniqueId: '625520283007346341076352773621',
  userId: '',
  winnings: '0.00',
}];



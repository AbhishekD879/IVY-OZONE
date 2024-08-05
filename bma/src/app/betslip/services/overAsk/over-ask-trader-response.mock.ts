export const requestedBetMock = {
  'addr': '10.80.62.4',
  'documentId': 1,
  'id': 751693,
  'isConfirmed': 'N',
  'isFunded': 'Y',
  'isOffer': 'Y',
  'isReferred': 'N',
  'isSettled': 'N',
  'receipt': 'O/0218908/0000891',
  'provider': 'OpenBetSports',
  'timeStamp': '2019-08-23T13:32:07.000Z',
  'offerExpiresAt': '2019-08-23T14:42:21.000+01:00',
  'betTypeRef': {
    'id': 'DBL'
  },
  'stake': {
    'stakePerLine': '5.00',
    'amount': '5.00',
    'currencyRef': {
      'id': 'GBP'
    }
  },
  'payout': [
    {
      'bonus': '',
      'refunds': '0.00',
      'winnings': '0.00',
      'potential': '11.25'
    }
  ],
  'lines': {
    'number': 1
  },
  'cashoutValue': {
    'status': 'BET_NO_CASHOUT 751693',
    'amount': 'CASHOUT_BET_NO_CASHOUT'
  },
  'leg': [
    {
      'sportsLeg': {
        'winPlaceRef': {
          'id': 'WIN'
        },
        'outcomeCombiRef': {},
        'legPart': [
          {
            'outcomeRef': {
              'id': 553364979,
              'outcomeDesc': 'Atletico MG',
              'eventDesc': 'Atletico MG v Bahia Salvador BA',
              'marketDesc': 'Match Result',
              'marketId': '148272520',
              'eventId': '9998877'
            }
          }
        ],
        'prices': [
          {
            'priceNum': 1,
            'priceDen': 2,
            'legType': '-',
            'priceTypeRef': {
              'id': 'LP'
            }
          }
        ],
        'price': {
          'priceNum': 1,
          'priceDen': 2,
          'legType': '-',
          'priceTypeRef': {
            'id': 'LP'
          }
        }
      },
      'documentId': 1
    },
    {
      'sportsLeg': {
        'winPlaceRef': {
          'id': 'WIN'
        },
        'outcomeCombiRef': {},
        'legPart': [
          {
            'outcomeRef': {
              'id': 553384143,
              'outcomeDesc': 'Gremio',
              'eventDesc': 'Gremio v Atletico PR',
              'marketDesc': 'Match Result',
              'marketId': '148278625',
              'eventId': '9998917'
            }
          }
        ],
        'prices': [
          {
            'priceNum': 3,
            'priceDen': 10,
            'legType': '-',
            'priceTypeRef': {
              'id': 'LP'
            }
          }
        ],
        'price': {
          'priceNum': 3,
          'priceDen': 10,
          'legType': '-',
          'priceTypeRef': {
            'id': 'LP'
          }
        }
      },
      'documentId': 2
    }
  ],
  'partialCashout': {
    'available': 'N'
  }
} as any;

export const offeredBetMock = {
  'betOfferRef': {
    'documentId': '1',
    'provider': 'OpenBetSports'
  },
  'addr': '10.80.62.4',
  'id': 751693,
  'isConfirmed': 'N',
  'isFunded': 'Y',
  'isOffer': 'N',
  'isReferred': 'Y',
  'isSettled': 'N',
  'receipt': 'O/0218908/0000891',
  'provider': 'OpenBetSports',
  'timeStamp': '2019-08-23T13:32:07.000Z',
  'betTypeRef': {
    'id': 'DBL'
  },
  'stake': {
    'stakePerLine': '5.00',
    'amount': '5.00',
    'currencyRef': {
      'id': 'GBP'
    }
  },
  'payout': [
    {
      'bonus': '',
      'refunds': '0.00',
      'winnings': '0.00',
      'potential': '20.25'
    }
  ],
  'lines': {
    'number': 1
  },
  'cashoutValue': {
    'status': 'BET_NO_CASHOUT 751693',
    'amount': 'CASHOUT_BET_NO_CASHOUT'
  },
  'leg': [
    {
      'sportsLeg': {
        'winPlaceRef': {
          'id': 'WIN'
        },
        'outcomeCombiRef': {},
        'legPart': [
          {
            'outcomeRef': {
              'id': 553364979,
              'outcomeDesc': 'Atletico MG',
              'eventDesc': 'Atletico MG v Bahia Salvador BA',
              'marketDesc': 'Match Result',
              'marketId': '148272520',
              'eventId': '9998877'
            }
          }
        ],
        'prices': [
          {
            'priceNum': 4,
            'priceDen': 5,
            'legType': '-',
            'priceTypeRef': {
              'id': 'LP'
            }
          }
        ],
        'price': {
          'priceNum': 4,
          'priceDen': 5,
          'legType': '-',
          'priceTypeRef': {
            'id': 'LP'
          }
        }
      },
      'documentId': 1
    },
    {
      'sportsLeg': {
        'winPlaceRef': {
          'id': 'WIN'
        },
        'outcomeCombiRef': {},
        'legPart': [
          {
            'outcomeRef': {
              'id': 553384143,
              'outcomeDesc': 'Gremio',
              'eventDesc': 'Gremio v Atletico PR',
              'marketDesc': 'Match Result',
              'marketId': '148278625',
              'eventId': '9998917'
            }
          }
        ],
        'prices': [
          {
            'priceNum': 3,
            'priceDen': 10,
            'legType': '-',
            'priceTypeRef': {
              'id': 'LP'
            }
          }
        ],
        'price': {
          'priceNum': 3,
          'priceDen': 10,
          'legType': '-',
          'priceTypeRef': {
            'id': 'LP'
          }
        }
      },
      'documentId': 2
    }
  ],
  'partialCashout': {
    'available': 'N'
  }
};

export const betDataMock = {
  betId: 751693,
  outcomeIds: [553364979, 553384143],
  Bet: {
    legs: [
      {
        docId: 1,
        firstOutcomeId: 553364979,
        price: {
          props: {
            'priceNum': 4,
            'priceDen': 5
          },
          'priceNum': 4,
          'priceDen': 5
        },
        parts: [{}]
      },
      {
        docId: 2,
        firstOutcomeId: 553384143,
        price: {
          props: {
            'priceNum': 3,
            'priceDen': 10
          },
          'priceNum': 3,
          'priceDen': 10
        },
        parts: [{}]
      }
    ]
  },
  oldLegs: undefined
};

export const confirmedBetMock = {
  bet: [
    {
      isConfirmed: 'Y',
      isCancelled: 'N',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    },
    {
      isConfirmed: 'Y',
      isCancelled: 'N',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    },
    {
      isConfirmed: 'Y',
      isCancelled: 'N',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    }
  ]
};

export const confirmedAndCancelledBetMock = {
  bet: [
    {
      isConfirmed: 'Y',
      isCancelled: 'Y',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    },
    {
      isConfirmed: 'Y',
      isCancelled: 'Y',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    },
    {
      isConfirmed: 'Y',
      isCancelled: 'Y',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    }
  ]
};

export const notConfirmedAndNotCancelledBetMock = {
  bet: [
    {
      isConfirmed: 'N',
      isCancelled: 'N',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    },
    {
      isConfirmed: 'N',
      isCancelled: 'N',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    },
    {
      isConfirmed: 'N',
      isCancelled: 'N',
      leg: {
        sportsLeg: { outcomeCombiRef: { id: '10' } },
        legPart: { outcomeRef: { id: '123' } }
      },
      lines: '1'
    }
  ]
};

export const mockedFreeBets = {
    freeBetItem: {
        freebetTokenExpiryDate: '2050-12-11T22:00:00.000Z',
        expires: null,
        usedBy: null
    },
    freeBetData: [
        {
            tokenId: 32,
            freebetTokenExpiryDate: 11-11-2019
        }
    ],
    mockFreeBet: [
        {
            tokenId: '2200000778',
            freebetTokenId: '2200000778',
            freebetOfferId: '28985',
            freebetOfferName: 'CRM-Offer-1',
            freebetOfferDesc: 'LASPRETLASPONONFRBNN',
            freebetTokenDisplayText: '',
            freebetTokenValue: '5.00',
            freebetAmountRedeemed: '0.00',
            freebetTokenRedemptionDate: '2022-03-29 06:47:43',
            freebetRedeemedAgainst: '2022-03-29 06:47:43',
            freebetTokenExpiryDate: '2022-03-29 06:47:43',
            freebetMinPriceNum: '',
            freebetMinPriceDen: '',
            freebetTokenAwardedDate: '2022-03-29 06:47:43',
            freebetTokenStartDate: '2022-03-29 06:47:43',
            freebetTokenType: 'BETBOOST',
            freebetTokenRestrictedSet: {
                level: '',
                id: ''
            },
            freebetGameName: '',
            freebetTokenStatus: '',
            currency: '',
            tokenPossibleBet: {
                name: '',
                betLevel: '',
                betType: '',
                betId: '',
                channels: ''
            },
            tokenPossibleBets: [
                {
                    name: '',
                    betLevel: '',
                    betType: '',
                    betId: '',
                    channels: ''
                }
            ],
            freebetOfferType: '',
            tokenPossibleBetTags: {
                'tagName': 'FRRIDE'
        },
        freebetOfferCategories:{
          freebetOfferCategory : 'Bet Pack'
        }
      }
    ],
    siteServerData: [
        {
          id: '111',
          event: {
            children: [
              { market: { id: 'market_1' } },
              { market: { id: 'market_2' } },
            ]
          }
        }
    ],
    getCategoriesData: ['112', '111, 114'],
    categoryData: {
        MARKET: {
          111: {
            categoryId: 12,
            categoryName: 'test',
            betNowLink: '/testUrl'
          },
          31: {
            categoryId: 12,
            categoryName: 'test',
            betNowLink: '/testUrl'
          },
        }
    },
    categoryDataSample: {
        CATEGORY: {
          111: {
            categoryId: 12,
            categoryName: 'test',
            betNowLink: '/testUrl'
          },
          31: {
            categoryId: 12,
            categoryName: 'test',
            betNowLink: '/testUrl'
          },
        }
    },
    categoryDataSample2: {
        MARKET: {
          5: {
            categoryId: 12,
            categoryName: 'test',
            betNowLink: '/testUrl'
          },
          31: {
            categoryId: 12,
            categoryName: 'test',
            betNowLink: '/testUrl'
          },
        }
    },
    tokenSample: [
        {
            tokenId: '1',
            tokenPossibleBet:
                {
                    betLevel: 'MARKET',
                    betId: '111'
                }
        }
    ],
    tokenCategorySample: [
        {
            tokenId: '1',
            tokenPossibleBet:
                {
                    betLevel: 'CATEGORY',
                    betId: '111'
                }
            },
    ],
    expectedTokenSample: [
        {
          tokenId: '1',
          tokenPossibleBet: { betLevel: 'MARKET', betId: '111' },
          betNowLink: '/'
        }, {
          tokenId: '81',
          tokenPossibleBet: { betLevel: 'EVENT', betId: '112' },
          betNowLink: '/'
        },
        {
          tokenId: '94',
          tokenPossibleBet: { betLevel: 'CATEGORY', betId: '114' },
          betNowLink: '/'
        },
        { tokenId: '4', betNowLink: '/' }
    ],
    getEventData: {
        categoryId: 112,
        categoryName: 'test',
        betNowLink: 'sports/test'
    },
    sportEventMock: {
        categoryId: '12',
        event: {
          categoryId: '12',
          categoryName: 'test',
          children: [
            { market: { id: '31', children: [{ outcome: { id: '31' } }] } },
            { market: { id: '5', children: [{ outcome: { id: '5' } }, { outcome: { id: '7' } }] } },
            { market: { children: [{ outcome: { id: '10' } }] } },
          ]
        },
    },
    sportEventMockWithClass: {
        categoryId: '12',
        event: {
          categoryId: '12',
          categoryName: 'test',
          children: [
            { market: { id: '31', children: [{ outcome: { id: '31' } }] } },
            { market: { id: '5', children: [{ outcome: { id: '5' } }, { outcome: { id: '7' } }] } },
            { market: { children: [{ outcome: { id: '10' } }] } },
          ]
        },
        class: {
          children: [
            {
                type: {
                    id: '31',
                    name: 'CATEGORY'
                }
            }
          ]
        }
    },
    categoryToken: {
        tokenPossibleBet: {
          betId: '1',
          betLevel: 'CATEGORY'
        }
    },
    marketToken: {
        tokenPossibleBet: {
            betId: '1',
            betLevel: 'MARKET'
        }
    },
    horseRacingToken: {
      tokenPossibleBet: {
          betId: '1',
          betLevel: 'ANY_POOLS'
      }
  },
  anySportsandanyPools: {
      tokenPossibleBets: [
        {
          betId: '1',
          betLevel: 'ANY_POOLS'
      },
      {
        betId: '1',
        betLevel: 'ANY_SPORTS'
    }]
  }
};

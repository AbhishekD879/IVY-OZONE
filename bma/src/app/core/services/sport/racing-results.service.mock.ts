export const virtualRacingResultMock = [
  {
    resultedEvent: {
      drilldownTagNames:'EVFLAG_AVD',
      children: [{
        resultedMarket: {
          id: 3,
          children: [{
            resultedOutcome: {
              id: 2,
              children: [{
                resultedPrice: {
                  priceTypeCode: 'LP',
                  priceNum: 4,
                  priceDec: '1.2'
                }
              },
                {
                  resultedPrice: {
                    priceTypeCode: 'LP',
                    priceNum: 3
                  }
                }],
              position: 3,
              resultCode: 'P'
            }
          }, {
            resultedOutcome: {
              id: 3,
              children: [{
                resultedPrice: {
                  priceTypeCode: 'LP',
                  priceNum: 4
                }
              }],
              resultCode: 'L'
            }
          }, {
            resultedOutcome: {
              id: 1,
              children: [{
                resultedPrice: {
                  priceTypeCode: 'LP',
                  priceNum: 1,
                  priceDec: 3.4
                }
              }],
              resultCode: 'W',
              position: 1
            }
          }, {
            resultedOutcome: {
              id: 4,
              children: [{
                resultedPrice: {
                  priceTypeCode: 'LP',
                  priceNum: 2.3
                }
              }],
              resultCode: 'P',
              position: 3
            }
          }, {
            resultedOutcome: {
              id: 7,
              children: [{
                resultedPrice: {
                  priceTypeCode: 'LP'
                }
              }],
              resultCode: 'V'
            }
          }]
        }
      }]
    }
  }
] as any;

export const expectedResultedOutcomes = [{
  id: 1,
  nonRunner: true
}, {
  id: 2,
  name: 'lorem'
}, {
  id: 3,
  name: 'ipsum'
}, {
  id: 5,
  name: 'dolor'
}, {
  id: 4,
  name: 'ameno',
  nonRunner: true
}, {
  id: 7,
  name: 'avizo'
}] as any;

export const expectedResultedWEWMarket = {
  id: 3,
  outcomes: [
    {
      id: 2,
      position: 3,
      resultCode: 'P',
      results: {
        priceTypeCode: 'LP',
        priceNum: 4,
        priceDec: '1.2',
        position: 3,
        resultCode: 'P'
      }
    }, {
      id: 3,
      resultCode: 'L',
      results: { resultCode: 'L' }
    }, {
      id: 1,
      resultCode: 'W',
      position: 1,
      results: {
        priceTypeCode: 'LP',
        priceNum: 1,
        priceDec: 3.4,
        position: 1,
        resultCode: 'W'
      }
    }, {
      id: 4,
      resultCode: 'P',
      position: 3,
      results: { position: 3, resultCode: 'P' }
    }, {
      id: 7,
      resultCode: 'V',
      results: { resultCode: 'V' }
    }
  ],
  hasResults: true,
  hasPositions: true
} as any;

export const resultedMarketWinorEachWay = {
    resultedMarket: {
      id: 3,
      children: [{
        resultedOutcome: {
          id: 2,
          children: [{
            resultedPrice: {
              priceTypeCode: 'LP',
              priceNum: 4,
              priceDec: '1.2'
            }
          },
            {
              resultedPrice: {
                priceTypeCode: 'LP',
                priceNum: 3
              }
            }],
          position: 3,
          resultCode: 'P'
        }
      }, {
        resultedOutcome: {
          id: 3,
          children: [{
            resultedPrice: {
              priceTypeCode: 'LP',
              priceNum: 4
            }
          }],
          resultCode: 'L'
        }
      }, {
        resultedOutcome: {
          id: 1,
          children: [{
            resultedPrice: {
              priceTypeCode: 'LP',
              priceNum: 1,
              priceDec: 3.4
            }
          }],
          resultCode: 'W',
          position: 1
        }
      }, {
        resultedOutcome: {
          id: 4,
          children: [{
            resultedPrice: {
              priceTypeCode: 'LP',
              priceNum: 2.3
            }
          }],
          resultCode: 'P',
          position: 3
        }
      }, {
        resultedOutcome: {
          id: 7,
          children: [{
            resultedPrice: {
              priceTypeCode: 'LP'
            }
          }],
          resultCode: 'V'
        }
      }]
    }
  } as any;


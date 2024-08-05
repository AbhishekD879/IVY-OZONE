import { QuickbetSelectionBuilder } from './quickbet-selection-builder.service';

describe('QuickbetSelectionBuilder', () => {
  let service;

  let filtersService;
  let userService;
  let fracToDecService;
  let localeService;
  let clientUserAgentService;
  let toolsService;
  let quickbetDataMock;
  let storedStateStub;
  let scorecastEvent;
  let timeService;
  let timeSyncService;
  const eventMock = {
    id: '8208340',
    name: '18:21 Club Hipico',
    typeId: '2009',
    categoryName: 'Horse Racing',
    className: 'Horse Racing - Live',
    drilldownTagNames: 'EVFLAG_EPR',
    classId: '223',
    eventStatusCode: 'A',
    displayOrder: 0,
    startTime: '2018-06-30T16:57:00Z',
    categoryId: '21',
    isLiveNowEvent: 'true',
    typeName: '(USA) Club Hipico',
    markets: [
      {
        eachWayFactorDen: 5,
        eachWayFactorNum: 1,
        id: '137767829',
        isEachWayAvailable: true,
        isGpAvailable: false,
        isLpAvailable: false,
        isSpAvailable: true,
        marketStatusCode: 'A',
        name: 'Win or Each Way'
      }
    ]
  };
  const virtualEventMock = {
    id: '8208340',
    name: '18:21 Club Hipico',
    typeId: '2009',
    categoryName: 'Horse Racing',
    className: 'Horse Racing - Live',
    drilldownTagNames: 'EVFLAG_EPR',
    classId: '223',
    eventStatusCode: 'A',
    displayOrder: 0,
    startTime: '2018-06-30T16:57:00Z',
    categoryId: '39',
    isLiveNowEvent: 'true',
    typeName: '(USA) Club Hipico',
    markets: [
      {
        eachWayFactorDen: 5,
        eachWayFactorNum: 1,
        id: '137767829',
        isEachWayAvailable: true,
        isGpAvailable: false,
        isLpAvailable: false,
        isSpAvailable: true,
        marketStatusCode: 'A',
        name: 'Win or Each Way'
      }
    ]
  };
  const quickbetDataMock2 = {
    event: {
      id: '8726515',
      name: '14:40 Nottingham',
      markets: [
        {
          id: '136802272',
          name: 'Win or Each Way',
          outcomes: [
            {
              id: '513274440',
              name: 'Samovar',
              outcomeStatusCode: 'A',
              outcomeMeaningMajorCode: 'CS'
            },
            {
              id: '12345678',
              name: 'Smth else',
              outcomeStatusCode: 'B',
              outcomeMeaningMajorCode: 'DS'
            }
          ],
          marketStatusCode: 'A',
          isSpAvailable: true,
          isLpAvailable: false,
          isGpAvailable: false,
          isEachWayAvailable: true,
          eachWayFactorNum: 1,
          eachWayFactorDen: 4,
          isMarketBetInRun: true,
          outcomeName: 'bla-bla-bla'
        }
      ],
      isStarted: true,
      eventStatusCode: 'A',
      startTime: '2018-10-31T14:40:00Z',
      typeId: '1957',
      typeName: 'Nottingham',
      categoryId: '21',
      categoryName: 'Horse Racing',
      classId: '223',
      className: 'Horse Racing - Live',
      isLiveNowEvent: 'true',
      isRacingSport: 'true',
    },
    request: {
      outcomeIds: [
        513274440
      ],
      selectionType: 'simple'
    },
    selectionPrice: { price: { priceNum:4, priceDen:8, handicapValueDec: '0.999' },handicapValueDec: 'some/tese/string' },
    oddsBoost: { betBoostMaxStake: 'test boost string' }
  };

  beforeEach(() => {
    filtersService = {
      clearEventName: jasmine.createSpy('clearEventName'),
      currencyPosition: jasmine.createSpy('currencyPosition'),
      makeHandicapValue: jasmine.createSpy('makeHandicapValue', {outcomeMeaningMajorCode: 'HL'} as any)
    };
    userService = {
      username: 'user'
    };
    fracToDecService = {
      fracToDec: jasmine.createSpy('fracToDec'),
      getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('getFormattedValue')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    clientUserAgentService = {};
    toolsService = {
      roundTo: jasmine.createSpy('roundTo').and.callFake(v => `${v}`),
      roundDown: jasmine.createSpy('roundDown').and.callFake(v => `${v}`)
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('12:10')
    };
    storedStateStub = {
      userEachWay: false,
      userStake: '',
      isLP: false,
    };
    quickbetDataMock = {
      event: {
        id: '8726515',
        name: '14:40 Nottingham',
        markets: [
          {
            id: '136802272',
            name: 'Win or Each Way',
            outcomes: [
              {
                id: '513274440',
                name: 'Samovar',
                outcomeStatusCode: 'A',
                outcomeMeaningMajorCode: 'CS'
              }
            ],
            marketStatusCode: 'A',
            isSpAvailable: true,
            isLpAvailable: false,
            isGpAvailable: false,
            isEachWayAvailable: true,
            eachWayFactorNum: 1,
            eachWayFactorDen: 4,
            isMarketBetInRun: true
          }
        ],
        isStarted: true,
        eventStatusCode: 'A',
        startTime: '2018-10-31T14:40:00Z',
        typeId: '1957',
        typeName: 'Nottingham',
        categoryId: '21',
        categoryName: 'Horse Racing',
        classId: '223',
        className: 'Horse Racing - Live'
      },
      request: {
        outcomeIds: [
          513274440
        ],
        selectionType: 'simple'
      }
    };
    scorecastEvent = {
      event: {
        id: '12558702',
        categoryId: '16',
        categoryName: 'Football',
        classId: '97',
        typeId: '442',
        className: 'Football England',
        markets: [
          {
            isMarketBetInRun: true,
            isEachWayAvailable: false,
            id: '298567684',
            outcomes: [
              {
                id: '962746317',
                outcomeMeaningMajorCode: 'CS',
                name: 'Man City 1-0',
                outcomeStatusCode: 'A',
                outcomeMeaningMinorCode: 'S'
              }
            ],
            isGpAvailable: false,
            marketStatusCode: 'A',
            isLpAvailable: true,
            name: 'Correct Score',
            isSpAvailable: false
          },
          {
            isEachWayAvailable: false,
            id: '299758665',
            outcomes: [
              {
                id: '967012514',
                outcomeMeaningMajorCode: 'FS',
                name: 'Sergio Aguero',
                outcomeStatusCode: 'A',
                outcomeMeaningMinorCode: 'H'
              }
            ],
            isGpAvailable: false,
            marketStatusCode: 'A',
            isLpAvailable: true,
            name: 'First Goal Scorer',
            isSpAvailable: false
          }
        ],
        eventStatusCode: 'A',
        startTime: '2019-05-06T19:00:00Z',
        name: 'Man City v Leicester',
        typeName: 'Premier League'
      },
      request: {
        outcomeIds: [
          967012514,
          962746317
        ],
        selectionType: 'scorecast',
        additional: {
          scorecastMarketId: 299758666
        }
      },
      selectionPrice: {
        priceDec: 19,
        priceDen: 1,
        priceNum: 18
      }
    };
    timeSyncService = {
      ip: '192.168.3.1'
    };

    service = new QuickbetSelectionBuilder(
      filtersService,
      userService,
      fracToDecService,
      localeService,
      clientUserAgentService,
      toolsService,
      timeService,
      timeSyncService
    );
  });

  describe('#isRacing', () => {
    it('Should checks if passed category id is not racing type', () => {
      expect(service.isRacing('3')).toBeFalsy();
      expect(service.isRacing('4')).toBeFalsy();
    });

    it('Should checks if passed category id is racing type', () => {
      expect(service.isRacing('19')).toBeTruthy();
      expect(service.isRacing('21')).toBeTruthy();
    });
  });

  describe('#isVirtual', () => {
    it('Should checks if passed category id is not Virtual type', () => {
      expect(service.isVirtual('3')).toBeFalsy();
    });

    it('Should checks if passed category id is Virtual sport', () => {
      expect(service.isVirtual('39')).toBeTruthy();
    });
  });

  it('Should build handicapValueDec str', () => {
    quickbetDataMock.selectionPrice = { handicapValueDec : 'test/handi/cap'}
    const response = service.build(quickbetDataMock, storedStateStub);
    expect(response.constructor.name).toEqual('IQuickbetSelectionModel');
  });

  it('Should build handicapValueDec +ve', () => {
    quickbetDataMock.selectionPrice = { handicapValueDec : '0.5'}
    const response = service.build(quickbetDataMock, storedStateStub);
    expect(response.constructor.name).toEqual('IQuickbetSelectionModel');
  });
  it('Should build handicapValueDec -ve', () => {
    quickbetDataMock.selectionPrice = { handicapValueDec : '-0.5'}
    const response = service.build(quickbetDataMock, storedStateStub);
    expect(response.constructor.name).toEqual('IQuickbetSelectionModel');
  });

  it('Should checks if outcome name is Unnamed favourite type', () => {
    // ['unnamed favourite', 'unnamed 2nd favourite']
    expect(service.isUnnamedFavourite('unnamed favourite')).toBeTruthy();
    expect(service.isUnnamedFavourite('unnamed 2nd favourite')).toBeTruthy();
  });

  it('Should checks if outcome name is not Unnamed favourite type', () => {
    // ['unnamed favourite', 'unnamed 2nd favourite']
    expect(service.isUnnamedFavourite('unnamed')).toBeFalsy();
    expect(service.isUnnamedFavourite('unnamed2')).toBeFalsy();
  });

  it('Should checks if passed status code or list of status codes are suspended type', () => {
    expect(service.isSuspended('S')).toBeTruthy();
    expect(service.isSuspended(['S', 'A'])).toBeTruthy();
  });

  it('Should checks if passed status code or list of status codes are not suspended type', () => {
    expect(service.isSuspended('O')).toBeFalsy();
    expect(service.isSuspended(['O', 'A'])).toBeFalsy();
  });

  describe('parseEventData', () => {
    it('should handle undefined param', () => {
      expect(service.parseEventData()).toEqual(jasmine.objectContaining({
        eventName: undefined,
        isRacingSport: false
      }));
    });

    it('should parse horse racing event', () => {
      const result = service.parseEventData(quickbetDataMock.event);
      expect(result).toEqual({
        categoryId: '21',
        categoryName: 'Horse Racing',
        classId: '223',
        className: 'Horse Racing - Live',
        eventId: '8726515',
        eventIsLive: undefined,
        eventName: '14:40 Nottingham',
        eventStatusCode: 'A',
        isRacingSport: true,
        isStarted: true,
        startTime: '2018-10-31T14:40:00Z',
        typeId: '1957',
        typeName: 'Nottingham',
        markets: quickbetDataMock.event.markets
      });
    });

    it('should parse horse racing event', () => {
      expect(service.parseEventData(eventMock)).toEqual(jasmine.objectContaining({
        eventName: '18:21 Club Hipico',
        typeName: '(USA) Club Hipico',
        drilldownTagNames: 'EVFLAG_EPR',
        eventIsLive: 'true',
        isRacingSport: true,
      }));
    });

    it('should parse virtual event', () => {
      filtersService.clearEventName.and.returnValue('test');
      expect(service.parseEventData(virtualEventMock)).toEqual(jasmine.objectContaining({
        eventName: '12:10 test',
        typeName: '(USA) Club Hipico',
        drilldownTagNames: 'EVFLAG_EPR',
        eventIsLive: 'true',
        isRacingSport: false,
      }));
    });
  });

  describe('parseSimpleSelection', () => {
    it('should handle undefined param', () => {
      expect(service.parseSimpleSelection()).toEqual(jasmine.objectContaining({
        marketName: undefined,
        outcomeId: undefined
      }));
    });

    it('should handle empty list of markets and outcomes', () => {
      expect(service.parseSimpleSelection([])).toEqual(jasmine.objectContaining({
        marketName: undefined,
        outcomeId: undefined
      }));
    });

    it('should parse selection with markets', () => {
      const result = service.parseSimpleSelection(quickbetDataMock.event.markets);
      expect(result).toEqual({
        eachWayFactorDen: 4,
        eachWayFactorNum: 1,
        hasGP: false,
        hasLP: false,
        isEachWayAvailable: true,
        isLpAvailable: false,
        isMarketBetInRun: true,
        isSpAvailable: true,
        marketId: '136802272',
        marketName: 'Win or Each Way',
        marketStatusCode: 'A',
        outcomeId: '513274440',
        outcomeMeaningMinorCode: undefined,
        outcomeName: 'Samovar',
        outcomeStatusCode: 'A',
      });
    });

    it('should check if market has LP based on isSpAvailable', () => {
      quickbetDataMock.event.markets[0].isLpAvailable = true;
      quickbetDataMock.event.markets[0].isSpAvailable = true;

      expect(service.parseSimpleSelection(quickbetDataMock.event.markets)).toEqual(jasmine.objectContaining({
        hasLP: false
      }));
    });

    it('should check if market has LP based on isLpAvailable', () => {
      quickbetDataMock.event.markets[0].isLpAvailable = true;
      quickbetDataMock.event.markets[0].isSpAvailable = false;

      expect(service.parseSimpleSelection(quickbetDataMock.event.markets)).toEqual(jasmine.objectContaining({
        hasLP: true
      }));
    });
  });

  describe('parseScorecastSelection', () => {
    it('should handle undefined param', () => {
      expect(service.parseScorecastSelection()).toEqual(jasmine.objectContaining({
        marketId: '',
        marketStatusCode: 'A',
        isEachWayAvailable: false,
        eachWayFactorDen: '',
        eachWayFactorNum: '',
        hasLP: true,
        hasGP: false,
        isSpAvailable: false,
        outcomeId: ''
      }));
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('should parse correct scorer and scorecast selections with no suspended statuses', () => {
      const result = service.parseScorecastSelection(scorecastEvent.event.markets);

      expect(result).toEqual(jasmine.objectContaining({
        marketId: '298567684,299758665',
        marketStatusCode: 'A',
        isEachWayAvailable: false,
        eachWayFactorDen: '',
        eachWayFactorNum: '',
        hasLP: true,
        hasGP: false,
        isSpAvailable: false,
        outcomeId: '962746317,967012514',
        outcomeName: 'Sergio Aguero, Man City 1-0',
        outcomeStatusCode: 'A'
      }));
      expect(localeService.getString).toHaveBeenCalledWith('quickbet.FS');
    });

    it('should parse correct scorer and scorecast selections with suspended status for market', () => {
      scorecastEvent.event.markets[1].marketStatusCode = 'S';

      expect(service.parseScorecastSelection(scorecastEvent.event.markets)).toEqual(jasmine.objectContaining({
        marketId: '298567684,299758665',
        marketStatusCode: 'S',
        isEachWayAvailable: false,
        eachWayFactorDen: '',
        eachWayFactorNum: '',
        hasLP: true,
        hasGP: false,
        isSpAvailable: false,
        outcomeId: '962746317,967012514',
        outcomeName: 'Sergio Aguero, Man City 1-0',
        outcomeStatusCode: 'A'
      }));
    });

    it('should parse correct scorer and scorecast selections with suspended status for outcome', () => {
      scorecastEvent.event.markets[0].outcomes[0].outcomeStatusCode = 'S';

      expect(service.parseScorecastSelection(scorecastEvent.event.markets)).toEqual(jasmine.objectContaining({
        marketId: '298567684,299758665',
        marketStatusCode: 'A',
        isEachWayAvailable: false,
        eachWayFactorDen: '',
        eachWayFactorNum: '',
        hasLP: true,
        hasGP: false,
        isSpAvailable: false,
        outcomeId: '962746317,967012514',
        outcomeName: 'Sergio Aguero, Man City 1-0',
        outcomeStatusCode: 'S'
      }));
    });
  });

  describe('build', () => {
    describe('should build scorecast selection', () => {
      let storedState, result;
      beforeEach(() => {
        storedState = {
          isLP: true,
          userEachWay: false,
          userStake: '5'
        };
      });
      it('and restore original order of markets/outcomes as in request', () => {
        result = service.build(scorecastEvent, storedState);
        expect(result).toEqual(jasmine.objectContaining({
          marketId: '299758665,298567684',
          selectionType: 'scorecast',
          disabled: false,
          hasLP: true,
          hasSP: false,
          hasSPLP: false,
          isEachWay: false,
          isEachWayAvailable: false,
          isLP: true,
          isRacingSport: false,
          isSpAvailable: false,
          isUnnamedFavourite: false,
          outcomeId: '967012514,962746317',
          stake: storedState.userStake,
          requestData: scorecastEvent.request
        }));

        expect(result.markets).toEqual([
          jasmine.objectContaining({ id: '299758665', outcomes: [jasmine.objectContaining({ id: '967012514' })] }),
          jasmine.objectContaining({ id: '298567684', outcomes: [jasmine.objectContaining({ id: '962746317' })] })
        ]);
      });
      it('and should not fail if original outcome ids are unavailable', () => {
        scorecastEvent.request.outcomeIds = undefined;
        result = service.build(scorecastEvent, storedState);
        expect(result).toEqual(jasmine.objectContaining({
          marketId: '298567684,299758665',
          selectionType: 'scorecast',
          outcomeId: '962746317,967012514'
        }));

        expect(result.markets).toEqual([
          jasmine.objectContaining({ id: '298567684', outcomes: [jasmine.objectContaining({ id: '962746317' })] }),
          jasmine.objectContaining({ id: '299758665', outcomes: [jasmine.objectContaining({ id: '967012514' })] })
        ]);
      });
      it('and should not fail if original outcome ids have unexpected data (coverage case)', () => {
        scorecastEvent.request.outcomeIds[0] = 123456789;
        result = service.build(scorecastEvent, storedState);
        expect(result).toEqual(jasmine.objectContaining({
          marketId: '298567684,299758665',
          selectionType: 'scorecast',
          outcomeId: '962746317,967012514'
        }));

        expect(result.markets).toEqual([
          jasmine.objectContaining({ id: '298567684', outcomes: [jasmine.objectContaining({ id: '962746317' })] }),
          jasmine.objectContaining({ id: '299758665', outcomes: [jasmine.objectContaining({ id: '967012514' })] })
        ]);
      });
      it('and should not fail if event data is unavailable (coverage case)', () => {
        scorecastEvent.event = undefined;
        scorecastEvent.request.outcomeIds[0] = 123456789;
        result = service.build(scorecastEvent, storedState);
        expect(result).toEqual(jasmine.objectContaining({
          marketId: '',
          selectionType: 'scorecast',
          outcomeId: ''
        }));

        expect(result.markets).toEqual(undefined);
      });
    });

    it('should return some object', () => {
      const storedState = {
        userEachWay: true,
        userStake: 'userStake',
        isLP: true
      };
      quickbetDataMock.selectionPrice = { priceNum:4, priceDen:8, handicapValueDec: '0.9' };
      const res = service.build(
        quickbetDataMock,
        storedState
      ) as any;
      const expectedMock = {
        currency: undefined,
        disabled: false,
        eachWayFactorDen: 4,
        eachWayFactorNum: 1,
        eventId: '8726515',
        eventStatusCode: 'A',
        freebet: 0,
        freebetValue: 0,
        hasGP: false,
        hasLP: false,
        hasSP: true,
        hasSPLP: false,
        isEachWay: true,
        isEachWayAvailable: true,
        isLP: false,
        isLpAvailable: false,
        isMarketBetInRun: true,
        isRacingSport: true,
        isSpAvailable: true,
        isStarted: true,
        isUnnamedFavourite: false,
        marketName: 'Win or Each Way',
        marketStatusCode: 'A',
        outcomeStatusCode: 'A',
        potentialPayout: 'N/A',
        selectionType: 'simple',
        stake: 'userStake'
      };

      expect(res).toEqual(jasmine.objectContaining(expectedMock));
    });

    it('should test objects with equal name', () => {
      const storedState = {
        userEachWay: true,
        userStake: 'userStake',
        isLP: true
      } as any;
      const testObj = {
        hasSP: true,
        hasSPLP: false,
        isUnnamedFavourite: true,
        isLP: false,
        price: { handicapValueDec: 'some/tese/string' }
      };
      const scorecastTestObj = {
        isEachWayAvailable: false,
        eachWayFactorNum: '',
        eachWayFactorDen: '',
      };

      spyOn((service as any), 'getCombinedModel').and.returnValue(testObj);
      spyOn((service as any), 'parseScorecastSelection').and.returnValue(scorecastTestObj);
      service.build(quickbetDataMock, storedState);

      expect(testObj).toEqual({
        hasSP: true,
        hasSPLP: false,
        isUnnamedFavourite: true,
        isLP: false,
        price: { handicapValueDec: 'some/tese/string' }
      });

      expect(scorecastTestObj).toEqual({
        isEachWayAvailable: false,
        eachWayFactorNum: '',
        eachWayFactorDen: '',
      });
    });

    it('is defined state and is LP', () => {
      const storedState = {
        userEachWay: true,
        userStake: '1',
        isLP: true,
      } as any;
      const testObj = {
        hasSP: true,
        hasSPLP: true,
        eachWayFactorNum: '4',
        eachWayFactorDen: '6',
        isUnnamedFavourite: true,
        isLP: false,
        price: { priceNum:4, priceDen:8, handicapValueDec: '0.999' }
      };
      const scorecastTestObj = {
        isEachWayAvailable: false,
        price: { priceNum:4, priceDen:8, handicapValueDec: '0.999' }
      };
      spyOn((service as any), 'getCombinedModel').and.returnValue(testObj);
      spyOn((service as any), 'parseScorecastSelection').and.returnValue(scorecastTestObj);
      service.build(quickbetDataMock, storedState);

      expect(testObj).toEqual({
        hasSP: true,
        hasSPLP: false,
        isUnnamedFavourite: true,
        eachWayFactorNum: '4',
        eachWayFactorDen: '6',
        isLP: true,
        price: { priceNum:4, priceDen:8, handicapValueDec: '0.999' }
      });

      expect(scorecastTestObj).toEqual({
        isEachWayAvailable: false,
        price: { priceNum:4, priceDen:8, handicapValueDec: '0.999' }
      });
    });

    it('if is no selection price', () => {
      const storedState = {
        userEachWay: true,
        userStake: 'userStake',
        isLP: true
      } as any;
      const testObj = {
        hasSP: true,
        hasSPLP: true,
        eachWayFactorNum: '2',
        eachWayFactorDen: '2',
        isUnnamedFavourite: true,
        isLP: false,
        price: { priceNum:4, priceDen:8, handicapValueDec: '0.9' }
      }
      quickbetDataMock.selectionPrice = { priceNum:4, priceDen:8, handicapValueDec: '0.9' };

      spyOn((service as any), 'getCombinedModel').and.returnValue(testObj);
      service.build(quickbetDataMock, storedState);

      expect(testObj).toEqual({
        hasSP: true,
        hasSPLP: false,
        eachWayFactorNum: '2',
        eachWayFactorDen: '2',
        isUnnamedFavourite: true,
        isLP: true,
        price: { priceNum:4, priceDen:8, handicapValueDec: '0.9' }
      });
    });
  });

  it('Should parseSimpleSelection negative case', () => {
    const result = service.parseSimpleSelection(quickbetDataMock2.event.markets) as any;
    quickbetDataMock2.event.markets[0].isSpAvailable = false;
    expect(result).toEqual({
      eachWayFactorDen: 4,
      eachWayFactorNum: 1,
      isEachWayAvailable: true,
      isLpAvailable: false,
      isMarketBetInRun: true,
      isSpAvailable: true,
      marketStatusCode: 'A',
      marketName: 'Win or Each Way',
      marketId: '136802272',
      hasLP: false,
      hasGP: false,
      outcomeId: '513274440',
      outcomeName: 'Samovar',
      outcomeStatusCode: 'A',
      outcomeMeaningMinorCode: undefined
    } as any);
  });

  it('Call parseSimpleSelection with no data', () => {
    const result = service.parseSimpleSelection([]) as any;
    expect(result).toEqual({
      marketName: undefined,
      marketId: undefined,
      hasLP: undefined,
      hasGP: undefined,
      outcomeId: undefined,
      outcomeName: undefined,
      outcomeStatusCode: undefined,
      outcomeMeaningMinorCode: undefined,
    } as any);
  });


  describe('parseScorecastSelection', () => {
    it('shold parse scorecast with markets', () => {
      expect(service.parseScorecastSelection(quickbetDataMock2.event.markets)).toEqual({
        marketName: undefined,
        marketId: '136802272',
        marketStatusCode: 'A',
        isEachWayAvailable: false,
        eachWayFactorDen: '',
        eachWayFactorNum: '',
        hasLP: true,
        hasGP: false,
        isSpAvailable: false,
        outcomeId: '513274440,12345678',
        outcomeName: 'Smth else, Samovar',
        outcomeStatusCode: 'A',
      });
    });
  });

  describe('getCombinedModel', () => {
    it('getCombinedModel possitive', () => {
      expect(service.getCombinedModel(quickbetDataMock2.event.markets[0], {} as any)).toEqual({
        hasSP: false,
        hasSPLP: false,
        isUnnamedFavourite: false
      });
    });

    it('getCombinedModel negative', () => {
      quickbetDataMock.event.markets[0].isSpAvailable = false;
      quickbetDataMock.event.markets[0].isLpAvailable = true;
      expect(service.getCombinedModel(quickbetDataMock2.event.markets[0], null)).toEqual({
        hasSP: false,
        hasSPLP: false,
        isUnnamedFavourite: false
      });
    });
  });
});

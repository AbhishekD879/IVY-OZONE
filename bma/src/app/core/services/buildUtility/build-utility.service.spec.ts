import { BuildUtilityService } from './build-utility.service';
import { ISportEvent } from '../../models/sport-event.model';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('BuildUtilityService', () => {
  let service: BuildUtilityService;
  let filter;
  let time;
  let comments;
  let ssRequestHelper;
  let market;
  let scoreParserService;
  let sportEventHelperService: SportEventHelperService;
  let commentsValue;

  beforeEach(() => {
    market =  {
      cashoutAvail: 'true',
      correctPriceTypeCode: 'code',
      dispSortName: 'name',
      eachWayFactorNum: '2',
      eachWayFactorDen: '3',
      eachWayPlaces: '4',
      id: '12',
      isGpAvailable: true,
      isLpAvailable: true,
      isMarketBetInRun: true,
      isSpAvailable: true,
      liveServChannels: 'channel1',
      isEachWayAvailable: true,
      liveServChildrenChannels: 'channel2',
      marketsNames: 'market1',
      marketStatusCode: 'active',
      name: 'market1',
      nextScore: 15,
      outcomes: <any[]>[],
      periods: [],
      priceTypeCodes: '1',
      terms: 'terms',
      templateMarketId: 44,
      templateMarketName: 'no-name',
      viewType: 'init',
      label: 'label',
      isTopFinish: true,
      isToFinish: true,
      insuranceMarkets: true,
      isOther: true,
      isWO: true,
      displayOrder: '20',
      runnerNumber: '10',
      children: [{
        outcome: <any>{
          name: 'test-name',
          displayOrder: '10',
          runnerNumber: '10',
          racingFormEvent: {
            class: 'racing',
            refRecordId: '12'
          },
          racingFormOutcome: true,
          children: [
            {
              price: {
                handicapValueDec: true
              }
            }
          ]
        }
      }]
    };
    filter = {
      makeHandicapValue: jasmine.createSpy().and.returnValue('-new_name'),
      removeLineSymbol: jasmine.createSpy().and.returnValue('unpiped_cls'),
      clearEventName: jasmine.createSpy().and.returnValue('cleared_name'),
      getTimeFromName: jasmine.createSpy().and.returnValue('-new_name')
    };
    time = {
      getLocalHourMin: jasmine.createSpy().and.returnValue('10:00'),
      getCorrectDay: jasmine.createSpy(),
      getLocalHourMinInMilitary: jasmine.createSpy().and.returnValue('22:00'),
      getUTCDay: jasmine.createSpy('getUTCDay').and.returnValue('lorem'),
      getUTCDayValue: jasmine.createSpy('getUTCDayValue').and.returnValue('lorem')
    };
    comments = {
      testInitParse: jasmine.createSpy().and.callFake(comment => comment.toUpperCase()),
      testClockInitParse: jasmine.createSpy(),
      parseScoresFromName: jasmine.createSpy().and.returnValue('name'),
      footballInitParse: jasmine.createSpy()
    };
    commentsValue = [
      {
        eventPeriod: {
          children: [{ eventFact: { fact: 4, eventParticipantId: 1 }}, { eventFact: {  fact: 5, eventParticipantId: 2}},
            { eventPeriod: {
                periodIndex: 1,
                children: [{eventFact: {fact: 4, eventParticipantId: 1}}, { eventFact: { fact: 5, eventParticipantId: 2 }}]
              }
            }
          ]
        }
      },
      { eventParticipant: { id: 1, name: 'test1' } },
      { eventParticipant: { id: 2, name: 'test2' } },
    ];
    sportEventHelperService = new SportEventHelperService({} as any, {} as any, {} as any);
    ssRequestHelper = {
      getCommentsByEventsIds: jasmine.createSpy().and.returnValue(new Promise(resolve => resolve({
        SSResponse: {
          children: [
            {
              event: {
                children: commentsValue
              }
            }
          ]
        }
      })))
    };
    scoreParserService = {
      parseScores: jasmine.createSpy('parseScores'),
      getScoreType: jasmine.createSpy('getScoreType'),
    };
    service = new BuildUtilityService(filter, time, comments, ssRequestHelper, scoreParserService, sportEventHelperService);
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should build event model with comments for football', fakeAsync(() => {
    const football: any = [
      {
        originalName: 'name',
        id: '16',
        categoryName: 'Football',
        categoryCode: 'FOOTBALL'
      }
    ];
    spyOn(sportEventHelperService, 'isFootball').and.callThrough();
    service.buildEventWithScores(football);
    tick();
    expect(comments.footballInitParse).toHaveBeenCalledWith(commentsValue);
    expect(sportEventHelperService.isFootball).toBeTruthy();
    expect(ssRequestHelper.getCommentsByEventsIds).toHaveBeenCalledWith(jasmine.objectContaining({
      eventsIds: '16'
    }));
  }));

  describe('@addComments', () => {
    it('should add scores to comments and override name if sport has scoreType assigned in config', () => {
      const events = [{originalName: 'foo', categoryId: '16' }];
      const rawComments = {};
      const mockParserOutput = {
        home: { name: 'foo' },
        away: { name: 'bar' },
      };
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      scoreParserService.parseScores = jasmine.createSpy('parseScores')
        .and.returnValue(mockParserOutput);
      const expectedEvents = service['addComments'](events as ISportEvent[], rawComments);

      expect(scoreParserService.getScoreType).toHaveBeenCalledWith('16');
      expect(scoreParserService.parseScores).toHaveBeenCalledWith('foo', 'Simple');
      expect(expectedEvents[0].comments.teams).toEqual(mockParserOutput as any);
      expect(expectedEvents[0].name).toEqual('foo v bar');
    });

    it('should not add scores to comments if sport has no scoreType assigned in config', () => {
      const events = [{originalName: 'foo', categoryId: '16' }];
      const rawComments = {};
      scoreParserService.parseScores = jasmine.createSpy('parseScores')
        .and.returnValue('bar');
      const expectedEvents = service['addComments'](events as ISportEvent[], rawComments);

      expect(scoreParserService.getScoreType).toHaveBeenCalledWith('16');
      expect(scoreParserService.parseScores).not.toHaveBeenCalled();
      expect(expectedEvents[0].comments).toBeUndefined();
    });

    it('should not add scores to comments if parser fails', () => {
      const events = [{originalName: 'foo', categoryId: '16' }];
      const rawComments = {};
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      scoreParserService.parseScores = jasmine.createSpy('parseScores')
        .and.returnValue(null);
      const expectedEvents = service['addComments'](events as ISportEvent[], rawComments);

      expect(scoreParserService.getScoreType).toHaveBeenCalledWith('16');
      expect(scoreParserService.parseScores).toHaveBeenCalledWith('foo', 'Simple');
      expect(expectedEvents[0].comments).toBeUndefined();
    });

    it('should call tennisTransformFallback if scoreType iS SetsGamesPoints and set its output to comments', () => {
      const events = [{originalName: 'foo', categoryId: '16' }];
      const rawComments = {};
      const mockParserOutput = {
        home: { name: 'foo' },
        away: { name: 'bar' },
        type: 'SetsGamesPoints',
      };
      comments.tennisTransformFallback = jasmine.createSpy('tennisTransformFallback').and.returnValue('bar');
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('SetsGamesPoints');
      scoreParserService.parseScores.and.returnValue(mockParserOutput);
      const expectedEvents = service['addComments'](events as ISportEvent[], rawComments);

      expect(scoreParserService.getScoreType).toHaveBeenCalledWith('16');
      expect(scoreParserService.parseScores).toHaveBeenCalledWith('foo', 'SetsGamesPoints');
      expect(comments.tennisTransformFallback).toHaveBeenCalledWith(mockParserOutput);
      expect(expectedEvents[0].comments).toEqual('bar' as any);
      expect(expectedEvents[0].name).toEqual('foo v bar');
    });
  });

  it('should extend market model', () => {
    const marketEntity = {
      market: market
    };

    const extendedEntity = service.marketBuilder(marketEntity);
    expect(extendedEntity.displayOrder).toEqual(20);
    expect(extendedEntity.outcomes[0].name).toEqual('test-name-new_name');
    expect(extendedEntity.outcomes[0].prices.length).toEqual(1);
    expect(extendedEntity.outcomes[0].displayOrder).toEqual(10);
  });

  it('referenceEachWayTermsBuilder', () => {
    const marketEntity = {
      market:{
        children:[{
          referenceEachWayTerms:{
            id:'1',
            places:'4'
          }
        }]
      }
    } as any;
     service.referenceEachWayTermsBuilder(marketEntity);
     expect(marketEntity.market.referenceEachWayTerms.places).toEqual('4');
  });


  it('should extend event model', () => {
    const eventEntity: any = [{
      event: {
        typeFlagCodes: 'US UK',
        displayOrder: '10',
        rawIsOffCode: 'Y',
        name: 'originalName',
        children: []
      }
    }];
    expect(service.buildEvents(eventEntity)[0]).toEqual(jasmine.objectContaining({
      isUS: true,
      displayOrder: 10,
      eventIsLive: true,
      liveEventOrder: 0,
      className: 'unpiped_cls',
      name: 'cleared_name',
      originalName: 'originalName'
    }));
  });

  it('should build event with racing form', () => {
    const eventEntity: any = [{
      racingFormEvent: {
        class: 'racing',
        refRecordId: '12'
      },
      racingFormOutcome: true,
      event: {
        children: [
          {
            market: market
          }
        ]
      }
    }];

    expect(service.buildEventsWithRacingForm(eventEntity)[0].markets[0]).toEqual(<any>jasmine.objectContaining({
      runnerNumber: '10'
    }));
  });

  it('should build event with racing form outcome', () => {
    const event: any = [{
      "id": 24914169,
      "name": "Surrey Downs",
      "categoryId": "39",
      "markets": [
        {
          "id": "612479811",
          "eventId": "24914169",
          "outcomes": [
            {
              "id": "1971173985",
              "silkName": "4",
              "racerId": "24",
              "drawNumber": "4",
              "jockey": "Ian Sloan"
            },
            {
              "id": "1971173986",
              "silkName": "5",
              "racerId": "25",
              "drawNumber": "5",
              "jockey": "Jon Sloan"
            }
          ]
        }
      ]
    }];

    const racingFormOutcomeArray: any = [{
      racingFormOutcome: {
        "id": "24",
        "refRecordId": "1971173985",
        "draw": "4",
        "silkName": "4",
        "jockey": "Ian Sloan",
      }
    },
    {
      racingFormOutcome: {
        "id": "25",
        "refRecordId": "1971173986",
        "draw": "5",
        "silkName": "5",
        "trainer": "Jon Sloan",
      }
    }];
    expect(service.buildEventWithRacingFormOutcomes(event, racingFormOutcomeArray)[0].markets[0].outcomes[0]).toEqual(<any>jasmine.objectContaining({
      drawNumber: "4",
      id: "1971173985",
      jockey: "Ian Sloan",
      racerId: "24",
      silkName: "4"
    }));
  });

  it('should build event with racing form outcome with runner info', () => {
    const event: any = [{
      "id": 24914169,
      "name": "Surrey Downs",
      "categoryId": "39",
      "markets": [
        {
          "id": "612479811",
          "eventId": "24914169",
          "outcomes": [
            {
              "id": "1971173985",
              "silkName": "4",
              "racerId": "24",
              "drawNumber": "4",
              "jockey": "Ian Sloan"
            },
            {
              "id": "1971173986",
              "racerId": "25",
              "runnerNumber": "5",
              "drawNumber": "5",
              "jockey": "Jon Sloan"
            }
          ]
        }
      ]
    }];

    const racingFormOutcomeArray: any = [];
    expect(service.buildEventWithRacingFormOutcomes(event, racingFormOutcomeArray)[0].markets[0].outcomes[0]).toEqual(<any>jasmine.objectContaining({
      drawNumber: "4",
      id: "1971173985",
      jockey: "Ian Sloan",
      racerId: "24",
      silkName: "4"
    }));
  });
  it('should build pool model', () => {
    const poolModel = [
      {
        pool: {
          id: '10',
          url: '/',
          marketIds: '12, 11, 13',
          type: '1',
          children: [{id: 1}, {id: 2}]
        }
      },
      {
        pool: {
          id: '11',
          url: '/',
          type: '2',
          children: [{id: 3}, {id: 4}]
        }
      }
    ];
    const builtPoolModel = service.poolsBuilder(poolModel);

    expect(builtPoolModel[0].id).toEqual(10);
    expect(builtPoolModel[0].marketIds.length).toEqual(3);
    expect(builtPoolModel[0].guides.length).toEqual(2);
    expect(builtPoolModel[0].poolType).toEqual('1');
  });

  describe('buildEventsWithMarketCounts', () => {
    it('should build events with markets counts if childCount', () => {
      const eventEntities: any = [[
        { event: { id: 1, children: [] } },
        { event: { id: 2, children: [] } },
        { childCount: {
            count: '10',
            id: '12',
            refRecordId: '1'
          }},
        { childCount: {
            count: '200',
            id: '13',
            refRecordId: '2'
          }},
      ], undefined];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result[0].marketsCount).toEqual(10);
      expect(result[1].marketsCount).toEqual(200);
    });

    it('should build events with markets counts if aggregation', () => {
      const eventEntities: any = [[
        { event: { id: 1, children: [] } },
        { event: { id: 2, children: [] } }
      ], [
        { event: { id: 1, children: [] } },
        { event: { id: 2, children: [] } },
        { aggregation: {
            count: '15',
            id: '12',
            refRecordId: '1'
          }},
        { aggregation: {
            count: '150',
            id: '13',
            refRecordId: '2'
          }},
      ]];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result[0].marketsCount).toEqual(15);
      expect(result[1].marketsCount).toEqual(150);
    });

    it('should return empty array if there no events case1', () => {
      const eventEntities: any = [[1,2], []];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result).toEqual([]);
    });

    it('should return empty array if there no events case1', () => {
      const eventEntities: any = [[],[]];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result).toEqual([]);
    });

    it('should return empty array if there no events case2', () => {
      const eventEntities: any = [];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result).toEqual([]);
    });

    it('should return empty array if there no events case3', () => {
      const eventEntities: any = [[], undefined];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result).toEqual([]);
    });

    it('should return empty array if there no events case4', () => {
      const eventEntities: any = [undefined, []];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result).toEqual([]);
    });

    it('should return empty array if there no events case5', () => {
      const eventEntities: any = [undefined, undefined];
      const result = service.buildEventsWithMarketCounts(eventEntities);
      expect(result).toEqual([]);
    });
  });

  describe('buildCouponEventsWithMarketCounts', () => {
    it('should build events with markets counts if childCount', () => {
      const eventEntities: any = [
        { event: {
            id: 1,
            children: [
              { market: {
                  id: 22
                }
              },
              { childCount: {
                  count: '10',
                  id: '12',
                  refRecordId: '1'
                }
              }
            ]
          }
        }
      ];
      const result = service.buildCouponEventsWithMarketCounts(eventEntities);
      expect(result[0].marketsCount).toEqual(10);
    });

    it('should build events with markets counts if no childCount', () => {
      const eventEntities: any = [
        { event: {
            id: 1,
            children: [
              { market: {
                  id: 22
                }
              }
            ]
          }
        }
      ];
      const result = service.buildCouponEventsWithMarketCounts(eventEntities);
      expect(result[0].marketsCount).toBeUndefined();
    });
  });

  it('should build market counts model', () => {
    const eventEntities: any = [
      {
        count: '10',
        id: '12',
        refRecordId: 'test'
      },
      {
        count: '200',
        id: '13',
        refRecordId: 'test1'
      }
    ];
    expect(service.buildMarketCounts(eventEntities)).toEqual(jasmine.objectContaining({
      test: 10,
      test1: 200
    }));
  });

  it('should build market id\'s model', () => {
    const eventEntities: any = [
      {event: {id: 12, children: []}},
      {event: {id: 14, children: []}}
    ];
    expect(service.buildEventsIds(eventEntities)).toEqual([12, 14]);
  });

  it('should check handicap availability', () => {
    const outcome = market.children[0].outcome;
    outcome.name = undefined;
    expect((service as any).isHandicapAvailable(outcome)).toBeTruthy();
  });

  it('should check handicap availability', () => {
    const outcome = market.children[0].outcome;
    outcome.name = 'Tie';
    expect((service as any).isHandicapAvailable(outcome)).toBeFalsy();
    outcome.name = 'Home';
    expect((service as any).isHandicapAvailable(outcome)).toBeTruthy();
  });

  it('should properly change outcome name', () => {
    const outcome = market.children[0].outcome;
    outcome.name = 'Home';
    expect((service as any).createOutcomeName(outcome)).toEqual('Home-new_name');
    outcome.name = 'Tie';
    expect((service as any).createOutcomeName(outcome)).toEqual('Tie');
  });

  it('should build event model with comments and clock', () => {
    const data: any = {
      events: [
        {
          id: '10',
          categoryCode: 'test',
        },
        {
          id: '12',
          categoryCode: 'test1'
        }
      ],
      comments: {
        '10': 'comment',
      }
    };
    expect(service.buildEventsWithScoresAndClock(data)[0].comments).toEqual('COMMENT');
    expect(comments.testInitParse).toHaveBeenCalledWith('comment');
    expect(comments.testClockInitParse).toHaveBeenCalled();
  });

  it('should build event model with comments and clock', fakeAsync(() => {
    const voleyball: any = [
      {
        originalName: 'name',
        id: '10',
        categoryCode: 'VOLLEYBALL',
      }
    ];
    const badminton: any = [
      {
        originalName: 'name1',
        id: '11',
        categoryCode: 'BADMINTON',
      }
    ];
    service.buildEventWithScores(voleyball);
    expect(comments.parseScoresFromName).toHaveBeenCalledWith(voleyball[0].originalName);

    (service as any).buildEventWithScores(badminton).then((data: any) => {
      expect(data[0].comments).toBeDefined();
      expect(data[0].comments.teams.home.score).toEqual(4);
      expect(data[0].comments.teams.away.score).toEqual(5);
      expect(data[0].comments.teams.away.name).toEqual('unpiped_cls');
    });
    tick();
    expect(ssRequestHelper.getCommentsByEventsIds).toHaveBeenCalledWith(jasmine.objectContaining({
      eventsIds: '11'
    }));
  }));

  it('should build InPlay events with market count', () => {
    const data = {
      nowEvents: [{id: '1'}],
      outrightNowEvents: [{id: '2'}],
      outrightSpecificNowEvents: [{id: '3'}],
      laterEvents: [{id: '4'}],
      outrightLaterEvents: [{id: '1'}],
      outrightSpecificLaterEvents: [{id: '2'}],
      nonLiveServedEvents: [{id: '7'}],
      correction: 'cashout'
    };
    expect(service.buildInPlayEventsWithMarketsCount(data).length).toEqual(5);
  });

  it('should build events with external keys', () => {
    const elements = [
      {
        externalKeys: {
          externalKeyTypeCode: 'OBEvLinkNonTote',
          mappings: '1,3,EVENT,2,4',
          refRecordType: 'event',
        },
        event: {
          id: '1'
        },
      },
      {
        event: {
          id: '12'
        }
      }
    ];
    expect(service.buildEventsWithExternalKeys(elements).length).toEqual(1);
  });

  describe('@eventBuilder', () => {
    it('should create entity with local time', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'INTL_TOTE',
          startTime: '2018-12-01T05:00:00Z',
        }
      };
      const result = service.eventBuilder(eventEntity);
      expect(result.localTime).toEqual('-new_name');
    });

    it('should call getUTCDayValue for HR', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'HORSE_RACING',
          startTime: '2018-12-01T05:00:00Z',
          categoryId: '21',
          children: []
        }
      };
      service.eventBuilder(eventEntity);
      expect(time.getUTCDayValue).toHaveBeenCalled();
    });

    it('should call getUTCDay for GH', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'GREYHOUNDS',
          startTime: '2018-12-01T05:00:00Z',
          categoryId: '19',
          children: []
        }
      };
      service.eventBuilder(eventEntity);
      expect(time.getUTCDay).toHaveBeenCalled();
    });

    it('should call getCorrectDay for not GH/HR', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'FOOTBALL',
          startTime: '2018-12-01T05:00:00Z',
          children: []
        }
      };
      service.eventBuilder(eventEntity);
      expect(time.getCorrectDay).toHaveBeenCalled();
    });
    it('should set original name, if it doesnt exist initially', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'GREYHOUNDS',
          categoryId: '19',
          startTime: '2018-12-01T05:00:00Z',
          name: '13:45 Newcastle',
          children: []
        }
      };
      const response = service.eventBuilder(eventEntity);
      expect(time.getUTCDayValue).toHaveBeenCalled();
      expect(response.originalName).toBe('13:45 Newcastle');
    });

    it('should set original name, if it does exist initially', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'GREYHOUNDS',
          categoryId: '19',
          startTime: '2018-12-01T05:00:00Z',
          name: 'Newcastle',
          originalName: '13:45 Newcastle',
          children: []
        }
      };
      const response = service.eventBuilder(eventEntity);
      expect(time.getUTCDayValue).toHaveBeenCalled();
      expect(response.originalName).toBe('13:45 Newcastle');
    });
  });

  describe('@msEventBuilder', () => {
    it('should call getUTCDay', () => {
      const eventEntity: any = {
        event: {
          categoryId: '21',
          categoryCode: 'HORSE_RACING',
          startTime: '2018-12-01T05:00:00Z',
          children: []
        }
      };
      service.msEventBuilder(eventEntity.event);
      expect(time.getUTCDay).toHaveBeenCalled();
    });

    it('should call getCorrectDay', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'GREYHOUNDS',
          categoryId: '19',
          startTime: '2018-12-01T05:00:00Z',
          children: []
        }
      };
      service.msEventBuilder(eventEntity.event);
      expect(time.getUTCDayValue).toHaveBeenCalled();
    });

    it('should set original name, if it doesnt exist initially', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'GREYHOUNDS',
          categoryId: '19',
          startTime: '2018-12-01T05:00:00Z',
          name: '13:45 Newcastle',
          children: []
        }
      };
      const response = service.msEventBuilder(eventEntity.event);
      expect(time.getUTCDayValue).toHaveBeenCalled();
      expect(response.originalName).toBe('13:45 Newcastle');
    });

    it('should set original name, if it does exist initially', () => {
      const eventEntity: any = {
        event: {
          categoryCode: 'GREYHOUNDS',
          categoryId: '19',
          startTime: '2018-12-01T05:00:00Z',
          name: 'Newcastle',
          originalName: '13:45 Newcastle',
          children: []
        }
      };
      const response = service.msEventBuilder(eventEntity.event);
      expect(time.getUTCDayValue).toHaveBeenCalled();
      expect(response.originalName).toBe('13:45 Newcastle');
    });
  });

  it('setTrapNumbers', () => {
    const result = service['setTrapNumber'](<any>{runnerNumber: '1', name: 'Test (RES)', displayOrder: 2});
    expect(result.trapNumber).toBe(2);
    const result2 = service['setTrapNumber'](<any>{name: 'Test', displayOrder: 2});
    expect(result2.trapNumber).toBeUndefined();
  });

  describe('@getDayValue', () => {
    it('should verify case not equal to HR and GH', () => {
      const event = {
        event: {
          categoryCode: 'INTL_TOTE',
          startTime: 1550751407661
        }
      } as any;
      const result = service['getDayValue'](event);
      expect(result).not.toBeNull();
      expect(time.getCorrectDay).toHaveBeenCalled();
    });

    it('should verify for GH', () => {
      const event = {
        categoryCode: 'GREYHOUNDS',
        startTime: 1550751407661,
        categoryId: '19'
      } as any;
      const result = service['getDayValue'](event);
      expect(result).not.toBeNull();
      expect(time.getUTCDay).toHaveBeenCalled();
    });

    it('should verify for HR', () => {
      const event: any = {
        categoryCode: 'HORSE_RACING',
        startTime: 1550751407661,
        categoryId: '21'
      } as any;
      const result = service['getDayValue'](event);
      expect(result).not.toBeNull();
      expect(time.getUTCDayValue).toHaveBeenCalled();
    });
  });

  describe('getLocalTime', () => {
    let event;

    beforeEach(() => {
      event = {
        startTime: '2020-09-23T19:00:00Z',
        name: 'any',
        categoryCode: 'INTL_TOTE'
      } as any;
      filter.getTimeFromName.and.returnValue('');
    });

    it('time format HH:mm for TOTE', () => {
      expect(service.getLocalTime(event)).toBe('22:00');
    });

    it('time format HH:mm for isHHformat=true', () => {
      event.categoryCode = 'horseracing';
      expect(service.getLocalTime(event, true)).toBe('22:00');
    });

    it('time format HH:mm for isHHformat=true (Original Name exists)', () => {
      event.categoryCode = 'horseracing';
      event.originalName = 'any';
      expect(service.getLocalTime(event, true)).toBe('22:00');
    });
  });
});

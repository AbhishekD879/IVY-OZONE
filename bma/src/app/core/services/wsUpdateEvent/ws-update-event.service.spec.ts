import { pubSubApi } from '../communication/pubsub/pubsub-api.constant';
import { WsUpdateEventService } from './ws-update-event.service';
import { wsliveUpdate, eventMock } from './ws-update-event.service.mock';

describe('WsUpdateEventService', () => {
  let service: WsUpdateEventService;

  let commentsService;
  let cacheEventsService;
  let timeService;
  let fracToDecService;
  let pubSubService;
  let scoreParserService;
  let wsliveUpdateTmp, eventMockTmp;
  let sportEventHelperService;
  beforeEach(() => {
    wsliveUpdateTmp = JSON.parse(JSON.stringify(wsliveUpdate));
    eventMockTmp = JSON.parse(JSON.stringify(eventMock));

    commentsService = {
      footballUpdateExtend: jasmine.createSpy(),
    };
    cacheEventsService = {
      storedData: {
        index: {
          '7451432': {
            path: []
          }
        }
      }
    };
    timeService = {
      hideLiveUpdateClassTime: 0
    };

    fracToDecService = {
      getDecimal: jasmine.createSpy().and.returnValue(2.40)
    };
    pubSubService = {
      subscribe: (fileName, string, callBack) => {
        callBack({events: {}});
      },
      API: pubSubApi,
      publish: jasmine.createSpy(),
      publishSync: jasmine.createSpy()
    };
    scoreParserService = {
      getScoreType: jasmine.createSpy('getScoreType'),
    };
    sportEventHelperService = {
      isTennis: jasmine.createSpy('isTennis')
    };

    service = new WsUpdateEventService(
      commentsService,
      cacheEventsService,
      timeService,
      fracToDecService,
      pubSubService,
      scoreParserService,
      sportEventHelperService
    );
  });

  it('subscribe when is not inited', () => {
    spyOn<any>(pubSubService, 'subscribe').and.callThrough();
    spyOn<any>(service, 'eventUpdateHandler');
    service.isInited = false;
    service.subscribe();

    expect(pubSubService.subscribe).toHaveBeenCalledWith('wsUpdateEventService', 'WS_EVENT_UPDATE',
      jasmine.any(Function));
    expect(service['eventUpdateHandler']).toHaveBeenCalledTimes(1);
  });

  it('subscribe when is inited', () => {
    spyOn<any>(pubSubService, 'subscribe');
    service.isInited = true;
    service.subscribe();

    expect(pubSubService.subscribe).not.toHaveBeenCalled();
  });

  describe('applyUpdateByType', () => {
    const eventToUpdate = eventMock.eventMockDefault;
    const updateDetails = wsliveUpdate.mockPriceUpdate;

    it('case type is EVENT', () => {
      spyOn<any>(service, 'applyDelta');
      service['applyUpdateByType']('EVENT', {} as any, [eventToUpdate] as any, updateDetails as any);

      expect(service['applyDelta']).toHaveBeenCalledWith({}, eventToUpdate);
    });

    it('case type is SCBRD', () => {
      spyOn<any>(service, 'eventCommentsUpdate');
      service['applyUpdateByType']('SCBRD', {} as any, [eventToUpdate] as any, updateDetails as any);

      expect(service['eventCommentsUpdate']).toHaveBeenCalledWith({}, eventToUpdate as any);
    });

    it('case type is CLOCK', () => {
      const clockMock = {
        clock_seconds: '111',
        last_update: '2019-06-05 07:53:26',
        last_update_secs: (new Date().getTime() / 1000).toString(),
        offset_secs: '111',
        period_code: 'SECOND_HALF',
        period_index: '',
        start_time_secs: '1111',
        state: 'R'
      };

      spyOn<any>(service, 'eventClockUpdate').and.callThrough();

      eventToUpdate['clock'] = {
        refresh: jasmine.createSpy('refresh')
      };

      service['applyUpdateByType']('CLOCK', clockMock, [eventToUpdate] as any, updateDetails as any);

      expect(service['eventClockUpdate']).toHaveBeenCalledWith(clockMock, eventToUpdate as any);
      expect(eventToUpdate['clock'].refresh).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalled();
    });

    it('case type is SELCN', () => {
      spyOn<any>(service, 'updateMarketOrOutcome');
      service['applyUpdateByType']('SELCN', {} as any, [eventToUpdate] as any, updateDetails as any);

      expect(service['updateMarketOrOutcome']).toHaveBeenCalledWith({}, eventToUpdate as any, 'SELCN', updateDetails as any);
    });
  });

  describe('eventPriceUpdate', () => {

    it('should update prices', () => {
      spyOn<any>(service, 'getPriceChangeClassName');
      spyOn<any>(service, 'extendOutcome');
      const outcome = {prices: [{liveShowTimer: {type: 'className'}}]} as any;
      service['eventPriceUpdate']({}, outcome as any);

      expect(service['getPriceChangeClassName']).toHaveBeenCalledWith({}, outcome as any);
      expect(service['extendOutcome']).toHaveBeenCalledWith({}, outcome as any, 'className');
    });

    it('should change outcome status', () => {
      const outcome = {prices: [], outcomeStatusCode: ''};
      service['eventPriceUpdate']({priceNum: 1, priceDen: 2, status: 'status'}, outcome as any);

      expect(outcome.outcomeStatusCode).toEqual('status');
    });

    it('should update prices when there was no price', () => {
      spyOn<any>(service, 'getPriceChangeClassName');
      spyOn<any>(service, 'extendOutcome');
      const outcome = {prices: []};

      service['eventPriceUpdate']({priceNum: 1, priceDen: 2}, outcome as any);

      expect(service['getPriceChangeClassName']).not.toHaveBeenCalled();
      expect(service['extendOutcome']).toHaveBeenCalledWith({priceNum: 1, priceDen: 2}, outcome as any, '');
    });
  });

  describe('getPriceChangeClassName', () => {
    const outcome = {
      prices: [
        {
          liveShowTimer: {type: 'className'},
          priceDec: 7
        }
      ]
    } as any;

    it('should return blank line when status is S', () => {
      const delta = {status: 'S'} as any;

      expect(service['getPriceChangeClassName'](delta, outcome)).toEqual('');
    });

    it('should return bet-down when delta price is lower than price before', () => {
      const delta = {status: 'A', priceDec: 5} as any;

      expect(service['getPriceChangeClassName'](delta, outcome)).toEqual('bet-down');
    });

    it('should return bet-up when delta price is bigger than price before', () => {
      const delta = {status: 'A', priceDec: 8} as any;

      expect(service['getPriceChangeClassName'](delta, outcome)).toEqual('bet-up');
    });
  });

  describe('#eventCommentsUpdate', () => {
    it('should update event comments ', () => {
      service['eventCommentsUpdate']({}, {categoryCode: 'football', comments: {}} as any);

      expect(pubSubService.publish).toHaveBeenCalledWith('EVENT_SCORES_UPDATE',
        { event: { categoryCode: 'football', comments: {} } });
    });

    it('should not update when there are extender, but no comments', () => {
      service['eventCommentsUpdate']({}, {categoryCode: 'football'} as any);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should not update when there are no appropriate method', () => {
      service['eventCommentsUpdate']({}, {categoryCode: 'other', comments: {}}  as any);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should use updateSportScores when there is fallback score type', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      service['eventCommentsUpdate']({}, {categoryCode: 'other', comments: {}, categoryId: '1'}  as any);

      expect(scoreParserService.getScoreType).toHaveBeenCalledWith('1');
      expect(commentsService.updateSportScores).toHaveBeenCalledWith({}, {});
    });

    it('should use updateSportScores for Tennis event', () => {
      sportEventHelperService.isTennis.and.returnValue(true);
      const event = { id: 12, categoryCode: 'other', categoryId: '34' } as any;
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      service['eventCommentsUpdate']({}, event);

      expect(sportEventHelperService.isTennis).toHaveBeenCalled();
      expect(event).toEqual({ id: 12, categoryCode: 'other', comments: {
        teams: { player_1: { id: '12' }, player_2: { id: '12' } }
      }, categoryId: '34' });
    });

    it('should not update when there are extender, but no comments', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      service['eventCommentsUpdate']({}, {categoryCode: 'football'} as any);

      expect(pubSubService.publish).toHaveBeenCalled();
      expect(commentsService.updateSportScores).toHaveBeenCalledWith(
        { teams: { home: { eventId: undefined }, away: { eventId: undefined } }  },
        {}
      );
    });
  });

  it('it should update Event status code to S', () => {
    // event in cache with {eventStatusCode: 'A',}
    const eventToUpdate = eventMockTmp.eventMockDefault;
    const eventsListUpdate = [
      eventToUpdate
    ];

    service['updateEvents'](<any>eventsListUpdate, <any>wsliveUpdateTmp.mockEventS);
    expect(eventToUpdate.eventStatusCode).toBe('S');
  });

  it('it should update Event status code to A', () => {
    // event in cache with {eventStatusCode: 'S',}
    const eventToUpdate = eventMockTmp.eventMockSuspended;
    const eventsListUpdate = [eventToUpdate];

    service['updateEvents'](<any>eventsListUpdate, <any>wsliveUpdateTmp.mockEventA);

    // get updated status
    expect(eventToUpdate.eventStatusCode).toBe('A');
  });

  it('it should update market status code to S', () => {
    // event in cache with Active market
    const eventToUpdate = eventMockTmp.eventMockDefault;
    const eventsListUpdate = [eventToUpdate];

    service['updateEvents'](<any>eventsListUpdate, <any>wsliveUpdateTmp.mockMarketS);

    // get status from updated cache
    expect(eventToUpdate.markets[0].marketStatusCode).toBe('S');
  });

  it('it should update market status code to A', () => {
    // event in cache with suspended market
    const eventToUpdate = eventMockTmp.eventMockSuspended;
    const eventsListUpdate = [eventToUpdate];

    service['updateEvents'](<any>eventsListUpdate, <any>wsliveUpdateTmp.mockMarketA);

    // get status from updated cache
    expect(eventToUpdate.markets[0].marketStatusCode).toBe('A');
  });

  it('it should suspend outome in case price update with status S', () => {
    // event in cache with suspended market
    const eventToUpdate = eventMock.eventMockDefault;
    const eventsListUpdate = [eventToUpdate];

    service['updateEvents'](<any>eventsListUpdate, <any>wsliveUpdateTmp.mockPriceSuspend);

    // get status from updated cache
    expect(eventToUpdate.markets[0].outcomes[0].outcomeStatusCode).toBe('S');
  });

  it('it should change prices in outcome', () => {
    // event in cache with suspended market
    const eventToUpdate = eventMock.eventMockDefault;
    const eventsListUpdate = [eventToUpdate];

    service['updateEvents'](<any>eventsListUpdate, <any>wsliveUpdateTmp.mockPriceUpdate);

    // get prices from updated event
    const priceDen = Number(eventToUpdate.markets[0].outcomes[0].prices[0].priceDen);
    const priceNum = Number(eventToUpdate.markets[0].outcomes[0].prices[0].priceNum);

    expect(priceDen).toBe(9);
    expect(priceNum).toBe(1);
  });

  it(' should test deleteItemFromList method', () => {
    spyOn(service as any, 'deleteEvent');

    const eventToUpdate: any = eventMock.eventMockDefault;
    const eventsListUpdate: any[] = [eventToUpdate];
    const update = JSON.parse(JSON.stringify(wsliveUpdate.mockEventUndisplayed));
    update.type = 'EVENT';

    service['deleteItemFromList'](eventsListUpdate, update);
    expect(service['deleteEvent']).toHaveBeenCalledWith(eventToUpdate.id, eventsListUpdate, update.type);
  });

  it ('should test deleteSelection method', () => {
    spyOn(service as any, 'deleteEvent');

    const eventsListUpdate: any[] = [{
      id: '1111',
      markets: [
        {
          id: '33333',
          outcomes: [{
            id: '22222'
          }]
        }
      ]
    }];

    service['deleteSelection']('1111', '22222', '33333', eventsListUpdate);
    expect(service['deleteEvent']).toHaveBeenCalledWith('1111', eventsListUpdate, 'SELCN');
  });

  it ('should test deleteMarket method', () => {
    spyOn(service as any, 'deleteEvent');

    const eventsListUpdate: any[] = [{
      id: '1111',
      markets: [
        {
          id: '33333',
          outcomes: [{
            id: '22222'
          }]
        }
      ]
    }];

    service['deleteMarket']('1111', '33333', eventsListUpdate);
    expect(service['deleteEvent']).toHaveBeenCalledWith('1111', eventsListUpdate, 'EVMKT');
  });

  it('it should delete event from cashe', () => {
    cacheEventsService.storedData = {
      index: {
        '1': {
          'module1': {
            path: ['ribbonEvents', 'data', 'modules', 0, 'data', 0]
          },
          'module2': {
            path: ['ribbonEvents', 'data', 'modules', 1, 'data', 2]
          },
          'module': {
            path: ['otherPageModulesOfEvents', 'data', 'modules', 0, 'data', 0]
          }
        },
        '2': {
          'module1': {
            path: ['ribbonEvents', 'data', 'modules', 0, 'data', 1]
          },
          'module2': {
            path: ['ribbonEvents', 'data', 'modules', 1, 'data', 1]
          },
          'module4': {
            path: ['otherPageModulesOfEvents', 'data', 'modules', 1, 'data', 0]
          }
        },
        '3': {
          'module1': {
            path: ['ribbonEvents', 'data', 'modules', 0, 'data', 2]
          },
          'module2': {
            path: ['ribbonEvents', 'data', 'modules', 1, 'data', 0]
          },
          'module3': {
            path: ['otherPageModulesOfEvents', 'data', 'modules', 0, 'data', 1]
          },
          'module4': {
            path: ['otherPageModulesOfEvents', 'data', 'modules', 1, 'data', 1]
          }
        }
      },
      'ribbonEvents': {
        data: {
          modules: [
            {
              data: [{ id: 1}, { id: 2}, { id: 3}, {}]
            }, {
              data: [{ id: 3}, { id: 2}, { id: 1}]
            }
          ]
        }
      },
      'otherPageModulesOfEvents': {
        data: {
          modules: [
            {
              data: [{ id: 1}, { id: 3}]
            }, {
              data: [{ id: 2}, { id: 3}]
            }
          ]
        }
      }
    };
    const eventList = [{
      id: '1'
    }];

    service['deleteEvent']('1', eventList as any, 'EVENT');
    let resObj: any = {
      '2': {
        'module1': {
          path: ['ribbonEvents', 'data', 'modules', 0, 'data', 0]
        },
        'module2': {
          path: ['ribbonEvents', 'data', 'modules', 1, 'data', 1]
        },
        'module4': {
          path: ['otherPageModulesOfEvents', 'data', 'modules', 1, 'data', 0]
        }
      },
      '3': {
        'module1': {
          path: ['ribbonEvents', 'data', 'modules', 0, 'data', 1]
        },
        'module2': {
          path: ['ribbonEvents', 'data', 'modules', 1, 'data', 0]
        },
        'module3': {
          path: ['otherPageModulesOfEvents', 'data', 'modules', 0, 'data', 0]
        },
        'module4': {
          path: ['otherPageModulesOfEvents', 'data', 'modules', 1, 'data', 1]
        }
      }
    };
    expect(cacheEventsService.storedData.index).toEqual(resObj);

    service['deleteEvent']('2', eventList as any, 'EVENT');
    resObj = {
      '3': {
        'module1': {
          path: ['ribbonEvents', 'data', 'modules', 0, 'data', 0]
        },
        'module2': {
          path: ['ribbonEvents', 'data', 'modules', 1, 'data', 0]
        },
        'module3': {
          path: ['otherPageModulesOfEvents', 'data', 'modules', 0, 'data', 0]
        },
        'module4': {
          path: ['otherPageModulesOfEvents', 'data', 'modules', 1, 'data', 0]
        }
      }
    };
    expect(cacheEventsService.storedData.index).toEqual(resObj);
  });

  it('it should NOT delete event from cashe when we have duplicate events with different markets', () => {
    cacheEventsService.storedData = {
      index: {
        '3': {
          'module1': {
            path: ['ribbonEvents', 'data', 'modules', 0, 'data', 0]
          },
          'module2': {
            path: ['ribbonEvents', 'data', 'modules', 1, 'data', 0]
          }
        }
      },
      'ribbonEvents': {
        data: {
          modules: [
            {
              data: [{
                id: 3,
                markets: []
              }]
            }, {
              data: [{
                id: 3,
                markets: [{
                  id: 11111
                }]
              }]
            }
          ]
        }
      }
    };
    const eventList = [{
      id: '1'
    }];

    service['deleteEvent']('3', eventList as any, 'EVMKT');
    expect(cacheEventsService.storedData.index['3']['module1']).toBeUndefined();
    expect(cacheEventsService.storedData.ribbonEvents.data.modules[0].data.length).toEqual(0);
    expect(cacheEventsService.storedData.ribbonEvents.data.modules[1].data.length).toEqual(1);
  });

  it('it should NOT delete event from cashe when no event in cache', () => {
    cacheEventsService.storedData = {
      index: {
      },
      'ribbonEvents': {
        data: {
          modules: [
            {
              data: [{
                id: 3,
                markets: []
              }]
            }, {
              data: [{
                id: 3,
                markets: [{
                  id: 11111
                }]
              }]
            }
          ]
        }
      }
    };
    const eventList = [{
      id: '1'
    }];
    expect(cacheEventsService.storedData.index['3']).toBeUndefined();

    service['deleteEvent']('3', eventList as any, 'EVMKT');
    expect(cacheEventsService.storedData).toEqual({
      index: {
      },
      'ribbonEvents': {
        data: {
          modules: [
            {
              data: [{
                id: 3,
                markets: []
              }]
            }, {
              data: [{
                id: 3,
                markets: [{
                  id: 11111
                }]
              }]
            }
          ]
        }
      }
    });

    expect(pubSubService.publish.calls.allArgs()[0]).toEqual(
      [pubSubService.API.DELETE_EVENT_ON_LIVE_STREAM_MODULE, jasmine.any(Object)]
    );

    expect(pubSubService.publish.calls.allArgs()[1]).toEqual(
      [pubSubService.API.WS_EVENT_DELETE, jasmine.any(Array)]
    );
    expect(pubSubService.publish.calls.allArgs()[2]).toEqual(
      [pubSubService.API.DELETE_EVENT_FROM_CACHE, 3]
    );
  });

  describe('extendOutcome', () => {
    it('should extendOutcome with creating price object', () => {
      const outcome = {prices: []} as any;
      const expectedResult = {
        correctPriceType: 'LP',
        prices: [
          {
            priceType: 'LP',priceNum: 1,
            priceDen: 2,
            liveShowTimer: {type: ''}
          }
        ]
      };

      service['extendOutcome']({priceNum: 1, priceDen: 2}, outcome, '');

      expect(outcome).toEqual(expectedResult);
    });
  });

  describe('#deltaObject', () => {
    it('should run PRICE case, call getDecimal method and return proper delta with status="S"', () => {
      const updateItem = {
        type: 'PRICE',
        event: {
          market: {
            outcome: {
              outcomeId: 574650466,
              price: {
                lp_den: '998',
                lp_num: '1',
                status: 'S'
              },
            }
          }
        }
      } as any;
      fracToDecService.getDecimal = jasmine.createSpy().and.returnValue(1.001002);

      const result = service['deltaObject'](updateItem);

      expect(fracToDecService.getDecimal).toHaveBeenCalledWith('1', '998', 6);
      expect(result).toEqual({
        priceDec: 1.001002,
        priceDen: '998',
        priceNum: '1',
        status: 'S'
      } as any);
    });

    it('should run PRICE case, call getDecimal method and return proper delta with status=undefined', () => {
      const updateItem = {
        type: 'PRICE',
        event: {
          market: {
            outcome: {
              outcomeId: 574650466,
              price: {
                lp_den: '998',
                lp_num: '1'
              }
            }
          }
        }
      } as any;
      fracToDecService.getDecimal = jasmine.createSpy().and.returnValue(1.001002);

      const result = service['deltaObject'](updateItem);

      expect(fracToDecService.getDecimal).toHaveBeenCalledWith('1', '998', 6);
      expect(result).toEqual({
        priceDec: 1.001002,
        priceDen: '998',
        priceNum: '1',
        status: undefined
      } as any);
    });

    it('should run SCBRD case and return proper delta', () => {
      const updateItem = {
        type: 'SCBRD',
        event: {
          scoreboard: 'scoreboard'
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual('scoreboard' as any);
    });

    it('should run CLOCK case and return proper delta', () => {
      const updateItem = {
        type: 'CLOCK',
        event: {
          clock: 'clock'
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual('clock' as any);
    });

    it('should run EVMKT case and return delta with isDisplay=false', () => {
      const updateItem = {
        type: 'EVMKT',
        event: {
          market: {
            status: 'status',
            displayed: 'N'
          }
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        marketStatusCode: 'status',
        isDisplayed: false
      });
    });

    it('should run EVMKT case and return delta with isDisplayed=true', () => {
      const updateItem = {
        type: 'EVMKT',
        event: {
          market: {
            status: 'status',
            displayed: 'Y'
          }
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        marketStatusCode: 'status',
        isDisplayed: true
      });
    });

    it('should run EVENT case and return delta with isDisplayed=false, eventIsLive=true and resulted=true', () => {
      const updateItem = {
        type: 'EVENT',
        event: {
          eventId: 10241759,
          status: 'status',
          displayed: 'N',
          started: 'Y',
          race_stage: 'race_stage',
          result_conf: 'Y',
          market: {}
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        eventStatusCode: 'status',
        isDisplayed: false,
        eventIsLive: true,
        raceStage: 'race_stage',
        resulted: true
      });
    });

    it('should run EVENT case and return delta with isDisplayed=true, eventIsLive=false and resulted=false', () => {
      const updateItem = {
        type: 'EVENT',
        event: {
          eventId: 10241759,
          status: 'status',
          displayed: 'Y',
          started: 'Y',
          race_stage: 'race_stage',
          result_conf: 'N',
          market: {}
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        eventStatusCode: 'status',
        isDisplayed: true,
        eventIsLive: true,
        raceStage: 'race_stage',
        resulted: false
      });
    });

    it('should run SELCN case and return proper delta with isDisplayed=true', () => {
      const updateItem = {
        type: 'SELCN',
        event: {
          market: {
            outcome: {
              outcomeId: 574650466,
              status: 'status',
              displayed: 'Y'
            }
          }
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        outcomeStatusCode: 'status',
        isDisplayed: true,
      });
    });

    it('should run SELCN case and return proper delta with isDisplayed=false', () => {
      const updateItem = {
        type: 'SELCN',
        event: {
          market: {
            outcome: {
              outcomeId: 574650466,
              status: 'status',
              displayed: 'N'
            }
          }
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        outcomeStatusCode: 'status',
        isDisplayed: false,
      });
    });
  });

  describe('#getPriceChangeClassName', () => {
    it('should return empty ""', () => {
      const delta = {
        priceDec: 8,
        priceDen: 1,
        priceNum: 7,
        status: 'S'
      };
      const outcome = {
        prices: [{
          id: '13',
          priceType: 'LP',
          priceNum: 6,
          priceDen: 1,
          priceDec: 7
        }]
      } as any;

      const result = service['getPriceChangeClassName'](delta, outcome);

      expect(result).toEqual('');
    });

    it('should return bet-up', () => {
      const delta = {
        priceDec: 8,
        priceDen: 1,
        priceNum: 7,
        status: undefined
      };
      const outcome = {
        prices: [{
          id: '13',
          priceType: 'LP',
          priceNum: 6,
          priceDen: 1,
          priceDec: 7
        }]
      } as any;

      const result = service['getPriceChangeClassName'](delta, outcome);

      expect(result).toEqual('bet-up');
    });

    it('should return bet-down', () => {
      const delta = {
        priceDec: 1.12,
        priceDen: 8,
        priceNum: 1,
        status: undefined
      };
      const outcome = {
        prices: [{
          id: '13',
          priceType: 'LP',
          priceNum: 7,
          priceDen: 1,
          priceDec: 8
        }]
      } as any;

      const result = service['getPriceChangeClassName'](delta, outcome);

      expect(result).toEqual('bet-down');
    });
  });

  describe('applyDelta', () => {
    it(`should publish WS_EVENT_UPDATED`, () => {
      const eventToUpdate = { id: 1 } as any;

      service['applyDelta']({} as any, eventToUpdate);

      expect(pubSubService.publish).toHaveBeenCalledWith('WS_EVENT_UPDATED', eventToUpdate);
    });
  });
});

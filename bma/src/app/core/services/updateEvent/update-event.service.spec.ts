import { UpdateEventService } from './update-event.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf } from 'rxjs';

describe('UpdateEventService', () => {
  let service: UpdateEventService;
  let cacheEventsService;
  let commentsService;
  let timeService;
  let lStoSSDataStructureConverterService;
  let fracToDecService;
  let filtersService;
  let pubSubService;
  let windowRefService;
  let scoreParserService;
  let callbacks;
  let update;
  let siteServerEventToOutcomeService;
  let cmsService;
  let awsService;

  beforeEach(() => {
    update = {
      id: 10,
      type: 'sEVENT',
      channel: 'sSELCN',
      subject_type: 'sEVENT',
      channel_number: '8',
      subject_number: '1',
      payload: {
        ev_mkt_id: '11',
        lp_num: 1,
        is_off: 'Y',
        displayed: 'Y',
        status: true
      }
    };
    callbacks = {
      connect: {},
      pubsub: {},
      document: {}
    };
    cacheEventsService = {
      storeNewOutcomes: jasmine.createSpy('storeNewOutcomes'),
      storedData: {
        index: {
          '8': {
            testfav: {
              path: ['test', 'fav', 0],
              expire: 10,
              reference: {
                comments: {},
                markets: [
                  {
                    id: '11',
                    outcomes: [
                      {
                        id: '1',
                        name: 'test',
                        alphabetName: 't',
                        runnerNumber: 2,
                        prices: [{
                          priceDec: 10
                        }]
                      },
                      {
                        name: 'test',
                        id: '11',
                        prices: [{
                          priceDec: 30
                        }]
                      }
                    ]
                  }
                ],
                categoryCode: 'test'
              }
            }
          },
          '9': { eventsnextFour21data: { path: ['events', 'nextFour', '21', 'data', 0], expire: 22, reference: { id: 9 } } },
          '7': { nextRacesHomenextFour19data: { path: ['nextRacesHome', 'nextFour', '19', 'data', 0], expire: 33, reference: { id: 7 } } }
        },
        marketsIndex: {
          11: '11',
          13: '7',
        },
        outcomesIndex: ['1', '11'],
        events: { nextFour: { '21': { data: [ { id: 9 } ] } },
                  featured: {
                    '21': { data: [ { id: '8' } ] }
                  } },
        nextRacesHome: { nextFour: { '19': { data: [ { id: 7 } ] } } },
        test: {
          fav: [
            {
              id: 33,
              comments: {},
              markets: [
                {
                  id: '11',
                  outcomes: [
                    {
                      id: '1',
                      name: 'test',
                      alphabetName: 't',
                      runnerNumber: 2,
                      prices: [{
                        priceDec: 10
                      }]
                    },
                    {
                      name: 'test',
                      id: '11',
                      prices: [{
                        priceDec: 30
                      }]
                    }
                  ]
                }
              ],
              categoryCode: 'test'
            }
          ]
        }
      },
      storeNewMarketOrOutcome: jasmine.createSpy()
    };

    commentsService = {
      parseScoresFromName: jasmine.createSpy().and.returnValue('test'),
      sportUpdateExtend: jasmine.createSpy()
    };
    timeService = {};

    lStoSSDataStructureConverterService = {
      convertData: jasmine.createSpy()
    };
    fracToDecService = {
      getDecimal: jasmine.createSpy().and.returnValue(20)
    };
    filtersService = {
      makeHandicapValue: jasmine.createSpy()
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((file, method, cb) => {
        callbacks['pubsub'][method] = cb;
      }),
      publish: jasmine.createSpy(),
      publishSync: jasmine.createSpy(),
    };
    windowRefService = {
      document: {
        addEventListener: jasmine.createSpy().and.callFake((method, cb) => {
          callbacks['document'][method] = cb;
        })
      }
    };
    scoreParserService = {
      parseScores: jasmine.createSpy('parseScores').and.returnValue('parseScores'),
      getScoreType: jasmine.createSpy('getScoreType'),
    };
    siteServerEventToOutcomeService = {
      getEventToOutcomeForMarket: jasmine.createSpy().and.returnValue(observableOf([]))
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({}))
    };
    awsService = {
      addAction: jasmine.createSpy()
    };
    service = new UpdateEventService(
      cacheEventsService,
      commentsService,
      timeService,
      lStoSSDataStructureConverterService,
      fracToDecService,
      filtersService,
      pubSubService,
      windowRefService,
      scoreParserService,
      siteServerEventToOutcomeService,
      cmsService,
      awsService
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'updateEventFactory',
      pubSubService.API.LIVE_SERVE_MS_UPDATE,
      jasmine.any(Function)
    );
  });

  describe('updateStoredDataElement', () => {
    it('should update stored data element(sEVENT)', fakeAsync(() => {
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect(commentsService.parseScoresFromName).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SUSPENDED_EVENT, jasmine.any(Array));
    }));

    it('should update originalName when update type is sEVENT', fakeAsync(() => {
      spyOn(service as any, 'updateEventsObject');
      update.payload.names = { en: 'foo' };
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect((service as any).updateEventsObject).toHaveBeenCalledWith(
        {
          originalName: 'foo',
          eventStatusCode: true,
          isDisplayed: true,
          eventIsLive: false,
          raceStage: undefined,
          resulted: false,
          score: 'test',
        },
        jasmine.any(Object),
        jasmine.any(Function),
        'sEVENT'
      );
    }));

    it('should update Event and the originalName when update type is sEVENT with EventUpdate', fakeAsync(() => {
      spyOn(service as any, 'updateEventsObject').and.callThrough();
      update.payload.names = { en: 'foo' };
      update.payload.status = 'S';
      update.payload.fc_avail = 'N';
      update.payload.tc_avail = 'N';
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect((service as any).updateEventsObject).toHaveBeenCalledWith(
        {
          originalName: 'foo',
          eventStatusCode: 'S',
          isDisplayed: true,
          eventIsLive: false,
          raceStage: undefined,
          resulted: false,
          score: 'test',
          fcMktAvailable: 'N',
          tcMktAvailable: 'N'
        },
        jasmine.any(Object),
        jasmine.any(Function),
        'sEVENT'
      );

      expect(cacheEventsService.storedData.index['8'].testfav.reference.eventStatusCode).toEqual('S');
    }));

    it('should update scores from scoreParser if sport is Gaelic Football (category 53)', fakeAsync(() => {
      scoreParserService.getScoreType.and.returnValue('GAA');
      spyOn(service as any, 'updateEventsObject');
      cacheEventsService.storedData.index['bar'] = {
        currentMatchesdata: {
          reference: {
            categoryId: '53',
          }
        }
      };
      update.payload.names = { en: 'foo' };
      update.channel_number = 'bar';
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect(scoreParserService.parseScores).toHaveBeenCalledWith('foo', 'GAA');
      expect((service as any).updateEventsObject).toHaveBeenCalledWith(
        {
          originalName: 'foo',
          eventStatusCode: true,
          isDisplayed: true,
          eventIsLive: false,
          raceStage: undefined,
          resulted: false,
          score: 'parseScores',
        },
        jasmine.any(Object),
        jasmine.any(Function),
        'sEVENT'
      );
    }));

    it('should update stored data element(sSELCN)', fakeAsync(() => {
      update.subject_type = 'sSELCN';
      update.subject_number = 1;
      update.payload.displayed = 'N';
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect(fracToDecService.getDecimal).toHaveBeenCalled();
      expect(pubSubService.publishSync).toHaveBeenCalled();
    }));

    it('should update stored data element(sSCBRD)', fakeAsync(() => {
      update.subject_type = 'sSCBRD';
      update.subject_number = '11';
      update.payload.eventIsLive = true;
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.MOVE_EVENT_TO_INPLAY, jasmine.any(Object));
    }));

    it('should update stored data element(sMHCAP)', fakeAsync(() => {
      update.subject_number = '11';
      update.payload.raw_hcap = true;
      update.payload.hcap_values = {
        A: true,
        H: true
      };
      update.subject_type = 'sMHCAP';
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.OUTCOME_UPDATED, jasmine.any(Object));
    }));

    it('should update stored data element(sEVMKT)', fakeAsync(() => {
      update.subject_type = 'sEVMKT';
      update.payload.displayed = 'N';
      update.subject_number = 11;

      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();
      expect(pubSubService.publish).toHaveBeenCalledWith('DELETE_MARKET_FROM_CACHE', '11');
    }));

    it('should handle live market(sEVMKT)', fakeAsync(() => {
      update.subject_type = 'sEVMKT';
      callbacks.pubsub[pubSubService.API.LIVE_SERVE_MS_UPDATE](update);
      tick();
      expect(cacheEventsService.storeNewMarketOrOutcome).toHaveBeenCalled();
      expect(lStoSSDataStructureConverterService.convertData).toHaveBeenCalled();
    }));

    it('should handle live market(sSELCN)', fakeAsync(() => {
      update.subject_type = 'sSELCN';
      callbacks.pubsub[pubSubService.API.LIVE_SERVE_MS_UPDATE](update);
      tick();
      expect(fracToDecService.getDecimal).toHaveBeenCalled();
    }));

    it('should handle live market(sCLOCK)', fakeAsync(() => {
      update.subject_type = 'sCLOCK';
      update.payload.eventIsLive = true;
      callbacks.pubsub[pubSubService.API.LIVE_SERVE_MS_UPDATE](update);
      tick();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.MOVE_EVENT_TO_INPLAY, jasmine.any(Object));
    }));

    it('doc', fakeAsync(() => {
      const customEvent = {
        detail: {
          liveUpdate: [
            {
              msg_id: 10,
              channel: 'sPRICE',
              subject_type: 'sPRICE',
              subject_number: 2,
              channel_number: 2,
              payload: {
                ev_mkt_id: 1,
                lp_num: 2,
              }
            }
          ]
        },
      };
      cacheEventsService.storedData.index['2'] = {
        eventsnextFour21data: {
          reference: {
            categoryId: '19'
          }
        }
      };
      callbacks.document['LIVE_SERVE_UPDATE'](customEvent);
      tick();
      expect(fracToDecService.getDecimal).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_SERVE_UPDATE');
    }));

    it('should work when live update is not an array', fakeAsync(() => {
      spyOn(service as any, 'updateStoredDataElement').and.callThrough();
      const customEvent = {
        detail: {
          liveUpdate: {
            msg_id: 10,
            channel: 'sPRICE',
            subject_type: 'sPRICE',
            subject_number: 2,
            channel_number: 2,
            payload: {
              ev_mkt_id: 1,
              lp_num: 2,
            }
          }
        },
      };
      cacheEventsService.storedData.index['2'] = {
        eventsnextFour21data: {
          reference: {
            categoryId: '19'
          }
        }
      };
      callbacks.document['LIVE_SERVE_UPDATE'](customEvent);
      tick();
      expect(service['updateStoredDataElement']).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_SERVE_UPDATE');
    }));

    it('handleLiveMarket array of updates', fakeAsync(() => {
      spyOn(service as any, 'updateStoredDataElement').and.callThrough();
      spyOn(service as any, 'handleEDPLiveMarket').and.callThrough();
      const rawHcap = '-7.5';
      const hcapValues = {
        A: '+7.5',
        H: '-7.5'
      };
      const customEvent = {
        detail: {
          liveUpdate: [
            {
              msg_id: 10,
              channel: 'SEVENT',
              subject_type: 'sEVMKT',
              subject_number: 32,
              channel_number: 8,
              payload: {
                ev_mkt_id: 8,
                lp_num: 2,
                status: 'S',
                raw_hcap: rawHcap,
                hcap_values: hcapValues
              }
            }
          ]
        },
      };

      callbacks.document['LIVE_SERVE_UPDATE'](customEvent);
      tick();

      expect(service['updateStoredDataElement']).not.toHaveBeenCalled();
      expect(service['handleEDPLiveMarket']).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_SERVE_UPDATE');
    }));

    it('handleLiveMarket update', fakeAsync(() => {
      spyOn(service as any, 'updateStoredDataElement').and.callThrough();
      spyOn(service as any, 'handleEDPLiveMarket').and.callThrough();
      const rawHcap = '-7.5';
      const hcapValues = {
        A: '+7.5',
        H: '-7.5'
      };
      const customEvent = {
        detail: {
          liveUpdate: {
            msg_id: 10,
            channel: 'SEVENT',
            subject_type: 'sEVMKT',
            subject_number: 32,
            channel_number: 8,
            payload: {
              ev_mkt_id: 8,
              lp_num: 2,
              status: 'S',
              raw_hcap: rawHcap,
              hcap_values: hcapValues
            }
          }
        },
      };

      callbacks.document['LIVE_SERVE_UPDATE'](customEvent);
      tick();

      expect(service['updateStoredDataElement']).not.toHaveBeenCalled();
      expect(service['handleEDPLiveMarket']).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_SERVE_UPDATE');
    }));

    it('should update stored data element(sEVENT) because of is_off flag', fakeAsync(() => {
      cacheEventsService.storedData.index['8'].eventsnextFour21data = {
        path: ['events', 'nextFour', '21', 'data', 0],
        reference: {
          categoryId: '19'
        }
      };
      callbacks.pubsub.LIVE_SERVE_MS_UPDATE(update);
      tick();

      expect(pubSubService.publishSync.calls.allArgs()[0]).toEqual(
        [pubSubService.API.DELETE_EVENT_FROM_CACHE, 8]
      );
    }));

    it('should update stored data element when market suspension and handicap updates are together', fakeAsync(() => {
      spyOn(service as any, 'checkForNewMarketOutcomeFromLS').and.callThrough();
      const rawHcap = '-7.5';
      const hcapValues = {
        A: '+7.5',
        H: '-7.5'
      };
      const customEvent = {
        detail: {
          liveUpdate: [
            {
              msg_id: 10,
              channel: 'SEVENT',
              subject_type: 'sEVMKT',
              subject_number: 11,
              channel_number: 8,
              payload: {
                ev_mkt_id: 8,
                lp_num: 2,
                status: 'S',
                raw_hcap: rawHcap,
                hcap_values: hcapValues
              }
            }
          ]
        },
      };

      callbacks.document['LIVE_SERVE_UPDATE'](customEvent);
      tick();

      expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_SERVE_UPDATE');
      expect(service['checkForNewMarketOutcomeFromLS']).toHaveBeenCalledWith(customEvent.detail.liveUpdate[0] as any);
      expect(pubSubService.publishSync).toHaveBeenCalledWith(pubSubService.API.OUTCOME_UPDATED, jasmine.objectContaining({
        rawHandicapValue: rawHcap,
        marketStatusCode: 'S',
        isDisplayed: true
      }));
      expect(pubSubService.publishSync.calls.first().args[1].outcomes[0].prices[0]).toEqual(jasmine.objectContaining({
        handicapValueDec: hcapValues.H,
        rawHandicapValue: hcapValues.H
      }));
    }));
  });

  describe('updateOutcomeHandicap', () => {
    it(`should update 'handicapThreeWayType`, () => {
      spyOn(service as any, 'setOutcomeNameWithHandicapVal');
      const raw_hcap = '1.123';
      const marketStub = { outcomes: [{ id: 1 }, { id: 2 }, { id: 3 }] } as any;
      const payloadStub = { hcap_values: { H: raw_hcap, A: -raw_hcap, L: raw_hcap }, raw_hcap } as any;

      service['updateOutcomeHandicap'](marketStub, payloadStub);

      expect(marketStub.rawHandicapValue).toBe(payloadStub.raw_hcap);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(0))
        .toEqual([marketStub.outcomes[0], raw_hcap, raw_hcap]);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(1))
        .toEqual([marketStub.outcomes[1], raw_hcap, raw_hcap]);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(2))
        .toEqual([marketStub.outcomes[2], (-raw_hcap).toFixed(1), raw_hcap]);
    });

    it(`should update 'handicapTwoWayType`, () => {
      spyOn(service as any, 'setOutcomeNameWithHandicapVal');
      const raw_hcap = '1.123';
      const marketStub = { outcomes: [{ id: 1 }, { id: 2 }] } as any;
      const payloadStub = { hcap_values: { H: raw_hcap, A: -raw_hcap }, raw_hcap } as any;

      service['updateOutcomeHandicap'](marketStub, payloadStub);

      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(0))
        .toEqual([marketStub.outcomes[0], raw_hcap, raw_hcap]);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(1))
        .toEqual([marketStub.outcomes[1], (-raw_hcap).toFixed(1), raw_hcap]);
    });

    it(`should not update 'handicapTwoWayType when no outcomes`, () => {
      spyOn(service as any, 'setOutcomeNameWithHandicapVal');
      const raw_hcap = '1.123';
      const marketStub = { } as any;
      const payloadStub = { hcap_values: { H: raw_hcap, A: -raw_hcap }, raw_hcap } as any;

      service['updateOutcomeHandicap'](marketStub, payloadStub);

      expect(service['setOutcomeNameWithHandicapVal']).not.toHaveBeenCalled();
    });

    it('should update handicapThreeWayType when there is only one outcome in market', () => {
      spyOn(service as any, 'setOutcomeNameWithHandicapVal');
      const raw_hcap = '1.123';
      const marketStub = { outcomes: [{ id: 1 }] } as any;
      const payloadStub = { hcap_values: { H: raw_hcap, A: -raw_hcap, L: raw_hcap }, raw_hcap } as any;

      service['updateOutcomeHandicap'](marketStub, payloadStub);

      expect(marketStub.rawHandicapValue).toBe(payloadStub.raw_hcap);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(0))
        .toEqual([marketStub.outcomes[0], raw_hcap, raw_hcap]);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(1))
        .toEqual([marketStub.outcomes[1], raw_hcap, raw_hcap]);
    });

    it('should update handicapTwoWayType', () => {
      spyOn(service as any, 'setOutcomeNameWithHandicapVal');
      const raw_hcap = '1.123';
      const marketStub = { outcomes: [{ id: 1 }, { id: 2 }, { id: 3 }] } as any;
      const payloadStub = { hcap_values: { H: raw_hcap, A: -raw_hcap }, raw_hcap } as any;

      service['updateOutcomeHandicap'](marketStub, payloadStub);

      expect(marketStub.rawHandicapValue).toBe(payloadStub.raw_hcap);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(0))
        .toEqual([marketStub.outcomes[0], raw_hcap, raw_hcap]);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(1))
        .toEqual([marketStub.outcomes[1], (-raw_hcap).toFixed(1), raw_hcap]);
    });

    it('should update totalPointsType', () => {
      spyOn(service as any, 'setOutcomeNameWithHandicapVal');
      const raw_hcap = '1.123';
      const marketStub = { outcomes: [{ id: 1 }, { id: 2 }] } as any;
      const payloadStub = { hcap_values: { H: raw_hcap, B: -raw_hcap, L: raw_hcap, E: raw_hcap }, raw_hcap } as any;

      service['updateOutcomeHandicap'](marketStub, payloadStub);

      expect(marketStub.rawHandicapValue).toBe(payloadStub.raw_hcap);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(0))
        .toEqual([marketStub.outcomes[0], raw_hcap, raw_hcap]);
      expect(service['setOutcomeNameWithHandicapVal']['calls'].argsFor(1))
        .toEqual([marketStub.outcomes[1], raw_hcap, raw_hcap]);
    });

    it('should not call setOutcomeNameWithHandicapVal', () => {
      spyOn(service as any, 'setOutcomeNameWithHandicapVal');
      const raw_hcap = '1.123';
      const marketStub = { outcomes: [{ id: 1 }, { id: 2 }] } as any;
      const payloadStub = { hcap_values: { H: raw_hcap, B: -raw_hcap, L: raw_hcap }, raw_hcap } as any;

      service['updateOutcomeHandicap'](marketStub, payloadStub);

      expect(marketStub.rawHandicapValue).toBe(payloadStub.raw_hcap);
      expect(service['setOutcomeNameWithHandicapVal']).not.toHaveBeenCalled();
    });
  });

  describe('#deleteEvent', () => {
    it(`should delete event in his storage and from events index when NO persistentInCacheEventFound`, () => {
      const eventCountBeforeDelete = service.storedData.test.fav.length;
      service['deleteEvent']('7');

      expect(service.storedData.test.fav.length).toEqual(eventCountBeforeDelete);
      expect(service.storedData.index['7']).toBeUndefined();
    });

    it(`should NOT delete event in his storage and from events index when persistentInCacheEventFound`, () => {
      const eventCountBeforeDelete = service.storedData.test.fav.length;
      service.storedData.index['8'].testfav.reference.persistentInCache = true;
      service.storedData.test.fav[0].persistentInCache = true;

      service['deleteEvent']('8');

      expect(service.storedData.test.fav.length).toEqual(eventCountBeforeDelete);
      expect(service.storedData.index['8']).toBeDefined();
    });

    it(`pubSub.publish should be called with DELETE_EVENT_ON_LIVE_STREAM_MODULE`, () => {
      cacheEventsService.storedData.index['8'].testfav.path[0] = 'liveEventsStream';
      cacheEventsService.storedData.liveEventsStream = cacheEventsService.storedData.test;
      service['deleteEvent']('8');
      expect(pubSubService.publish).toHaveBeenCalledWith('DELETE_EVENT_ON_LIVE_STREAM_MODULE', jasmine.any(Object));
    });
  });

  describe('#isNextRacingEventIsOff', () => {
    it(`should allow to delete event when is_off is 'Y'`, () => {
      // @ts-ignore
      expect(service['isNextRacingEventIsOff'](service.storedData.index['7'], { payload: { is_off : 'Y' } })).toBeTruthy();
    });

    it(`should NOT allow to delete event when is_off is 'N'`, () => {
      // @ts-ignore
      expect(service['isNextRacingEventIsOff'](service.storedData.index['7'], { payload: { is_off : 'N' } })).toBeFalsy();
    });

    it(`should NOT allow to delete event when is_off property is not available`, () => {
      // @ts-ignore
      expect(service['isNextRacingEventIsOff'](service.storedData.index['7'], { payload: { } })).toBeFalsy();
    });

    it(`should NOT allow to delete event when no next races events in the cache`, () => {
      delete service.storedData.index['7'].eventsnextFour21data;
      delete service.storedData.index['7'].nextRacesHomenextFour19data;
      // @ts-ignore
      expect(service['isNextRacingEventIsOff'](service.storedData.index['7'], { })).toBeFalsy();
    });

    it(`should NOT allow to delete event when event is NOT found in the cache`, () => {
      // @ts-ignore
      expect(service['isNextRacingEventIsOff']([], { })).toBeFalsy();
      // @ts-ignore
      expect(service['isNextRacingEventIsOff'](undefined, { })).toBeFalsy();
    });
  });

  describe('#updateEventsObject', () => {
    let delta, upd;
    const fn = arg => arg, type = 'sEVENT';

    beforeEach(() => {
     delta = {
       isDisplayed: true,
       resulted: false
     };
     upd = {
        payload: { is_off: 'Y' },
        channel_number: 7,
        channel: 'sEVENT'
      };

      // @ts-ignore
      spyOn(service, 'deleteItemFromCacheByType');
    });

    it(`should updateMarketOrOutcome if channel equal SEVMKT `, () => {
      const updateObj = {
        channel_number: 13,
        channel: 'SEVMKT'
      } as any;
      const typeMKT = 'SEVMKT';
      spyOn(service as any, 'updateMarketOrOutcome');
      const eventForUpdate = service.storedData.index[7];

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(service['updateMarketOrOutcome']).toHaveBeenCalledWith(delta, eventForUpdate, typeMKT, updateObj, fn);
    });

    it(`should call SUSPEND_IHR_EVENT_OR_MRKT if market or event is suspended `, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'}
        }
      } as any;
      const typeMKT = 'sEVMKT';
      spyOn(service as any, 'updateMarketOrOutcome');
      const event = cacheEventsService.storedData.events.featured['21'].data[0];
      event.markets = [{id: 111, marketStatusCode: 'A'}];
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should call SUSPEND_IHR_EVENT_OR_MRKT with market=null`, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'}
        }
      } as any;
      const typeMKT = 'sEVMKT';
      spyOn(service as any, 'updateMarketOrOutcome');
      const event = cacheEventsService.storedData.events.featured['21'].data[0];
      event.markets = null;
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should call SUSPEND_IHR_EVENT_OR_MRKT with events=null`, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'}
        }
      } as any;
      const typeMKT = 'sEVMKT';
      spyOn(service as any, 'updateMarketOrOutcome');
      cacheEventsService.storedData.events = null;
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should call SUSPEND_IHR_EVENT_OR_MRKT with featured=null`, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'}
        }
      } as any;
      const typeMKT = 'sEVMKT';
      spyOn(service as any, 'updateMarketOrOutcome');
      cacheEventsService.storedData.events.featured['21'] = null;
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should call SUSPEND_IHR_EVENT_OR_MRKT with featured.data=null`, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'}
        }
      } as any;
      const typeMKT = 'sEVMKT';
      spyOn(service as any, 'updateMarketOrOutcome');
      cacheEventsService.storedData.events.featured['21'].data = null;
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should not call SUSPEND_IHR_EVENT_OR_MRKT with events=null`, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'},
          is_off: 'Y'
        }
      } as any;
      const typeMKT = 'sEVENT';
      spyOn(service as any, 'updateMarketOrOutcome');
      cacheEventsService.storedData.events = null;
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).not.toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should not call SUSPEND_IHR_EVENT_OR_MRKT with featured=null`, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'},
          is_off: 'Y'
        }
      } as any;
      const typeMKT = 'sEVENT';
      spyOn(service as any, 'updateMarketOrOutcome');
      cacheEventsService.storedData.events.featured['21'] = null;
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).not.toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should not call SUSPEND_IHR_EVENT_OR_MRKT with featured.data=null`, () => {
      const updateObj = {
        channel_number: '8',
        channel: 'sEVMKT',
        subject_number: 111,
        payload: {
          fc_avail: 'N',
          tc_avail: 'N',
          names: {en: 'Win or Each Way'},
          is_off: 'Y'
        }
      } as any;
      const typeMKT = 'sEVENT';
      spyOn(service as any, 'updateMarketOrOutcome');
      cacheEventsService.storedData.events.featured['21'].data = null;
      delta.marketStatusCode = 'S';

      service['updateEventsObject'](delta, updateObj, fn, typeMKT);

      expect(pubSubService.publish).not.toHaveBeenCalledWith('SUSPEND_IHR_EVENT_OR_MRKT', [updateObj.channel_number, delta]);
    });

    it(`should allow to delete event when isDisplayed: true and resulted: false
        and next races events exists in the cache and property is_off is 'Y'`, () => {
      // @ts-ignore
      service['updateEventsObject'](delta, upd, fn, type);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EVENT_SCORES_UPDATE, jasmine.any(Object));
      expect(service['deleteItemFromCacheByType']).toHaveBeenCalledWith(upd);
    });

    it(`should allow to delete event when isDisplayed: false`, () => {
      delta.isDisplayed = false;

      // @ts-ignore
      service['updateEventsObject'](delta, upd, fn, type);

      expect(service['deleteItemFromCacheByType']).toHaveBeenCalledWith(upd);
    });

    it(`should allow to delete event when isDisplayed: true and resulted: true`, () => {
      delta.resulted = true;

      // @ts-ignore
      service['updateEventsObject'](delta, upd, fn, type);

      expect(service['deleteItemFromCacheByType']).toHaveBeenCalledWith(upd);
    });

    it(`should NOT allow to delete event when no next races events in the cache`, () => {
      delete service.storedData.index['7'].eventsnextFour21data;
      delete service.storedData.index['7'].nextRacesHomenextFour19data;
      // @ts-ignore
      service['updateEventsObject'](delta, upd, fn, type);

      expect(service['deleteItemFromCacheByType']).not.toHaveBeenCalledWith(upd);
    });

    it(`should NOT allow to delete event when is_off is 'N'`, () => {
      upd.payload.is_off = 'N';
      // @ts-ignore
      service['updateEventsObject'](delta, upd, fn, type);

      expect(service['deleteItemFromCacheByType']).not.toHaveBeenCalledWith(upd);
    });

    it(`should NOT allow to delete event when is_off property is not available`, () => {
      upd.payload = {};
      // @ts-ignore
      service['updateEventsObject'](delta, upd, fn, type);

      expect(service['deleteItemFromCacheByType']).not.toHaveBeenCalledWith(upd);
    });
  });

  describe('eventPriceUpdate', function () {
    it('should add updated price if price array is empty (case when SP changed with LP)', () => {
      const delta = {
        priceDec: 1.3,
        priceDen: 4,
        priceNum: 5,
        status: undefined,
        isDisplayed: true,
        priceType: 'LP'
      };
      const outcome = { prices: [] } as any;
      service['eventPriceUpdate'](delta, outcome);
      expect(outcome.prices[0]).toEqual(delta);
      expect(outcome.correctPriceType).toEqual('LP');
    });
    it('should add updated price if price array isn`t defined (case when SP changed with LP)', () => {
      const delta = {
        priceDec: 1.3,
        priceDen: 4,
        priceNum: 5,
        status: undefined,
        isDisplayed: true,
        priceType: 'LP'
      };
      const outcome = {} as any;
      service['eventPriceUpdate'](delta, outcome);
      expect(outcome.prices[0]).toEqual(delta);
      expect(outcome.correctPriceType).toEqual('LP');
    });
    it('shouldn`t add price if update is not LP price added', () => {
      const delta = {
        status: 'A',
        isDisplayed: true
      };
      const outcome = {} as any;
      service['eventPriceUpdate'](delta, outcome);
      expect(outcome.prices.length).toEqual(0);
      expect(outcome.correctPriceType).not.toBeDefined();
    });
  });

  describe('updateMarketPriceType', () => {
    it('should set LP price type for market if only lP available', () => {
      const market = {} as any,
        payload = {
          lp_avail: 'Y'
        } as any;
      service['updateMarketPriceType'](market, payload);
      expect(market.isLpAvailable).toEqual(true);
      expect(market.isSpAvailable).toEqual(false);
      expect(market.priceTypeCodes).toEqual('LP,');
    });
    it('should set SP price type for market if only SP available', () => {
      const market = {} as any,
        payload = {
          sp_avail: 'Y'
        } as any;
      service['updateMarketPriceType'](market, payload);
      expect(market.isLpAvailable).toEqual(false);
      expect(market.isSpAvailable).toEqual(true);
      expect(market.priceTypeCodes).toEqual('SP,');
    });
    it('should set LP and SP price type for market if only lP available', () => {
      const market = {} as any,
        payload = {
          sp_avail: 'Y',
          lp_avail: 'Y'
        } as any;
      service['updateMarketPriceType'](market, payload);
      expect(market.isLpAvailable).toEqual(true);
      expect(market.isSpAvailable).toEqual(true);
      expect(market.priceTypeCodes).toEqual('LP,SP,');
    });
  });
  describe('updateMarketOrOutcome', () => {
    it('should call updateMarketPriceType', () => {
      const events = [{
        reference: {
          markets: [{
            id: '3'
          } as any]
        }
      }] as any;
      const liveUpdate = {
        subject_number: 3,
        payload: {
          sp_avail: 'Y',
          lp_avail: 'Y',
          ev_mkt_id: 3
        }
      } as any;
      service['updateMarketOrOutcome']({} as any, events as any, 'sEVMKT', liveUpdate, () => {});
      expect(events[0].reference.markets[0].isLpAvailable).toBeTruthy();
      expect(events[0].reference.markets[0].isSpAvailable).toBeTruthy();
      expect(events[0].reference.markets[0].priceTypeCodes).toEqual('LP,SP,');
    });
    it('should`t call updateMarketPriceType', () => {
      const events = [{
        reference: {
          markets: [{
            id: '3'
          } as any]
        }
      }] as any;
      const liveUpdate = {
        subject_number: 4,
        payload: {
          sp_avail: 'Y',
          lp_avail: 'Y',
          ev_mkt_id: 4
        }
      } as any;
      service['updateMarketOrOutcome']({} as any, events as any, 'sEVMKT', liveUpdate, () => {});
      expect(events[0].reference.markets[0].isLpAvailable).not.toBeDefined();
      expect(events[0].reference.markets[0].isSpAvailable).not.toBeDefined();
      expect(events[0].reference.markets[0].priceTypeCodes).not.toBeDefined();
    });
  });

  describe('getEventCategory', () => {
    it('should return empty string if event not provided', () => {
      expect(UpdateEventService['getEventCategory'](null)).toEqual('');
    });

    it('should return empty string if event no currentMatchesdata or eventdata', () => {
      expect(UpdateEventService['getEventCategory']({})).toEqual('');
    });

    it('should return empty string if event no reference in currentMatchesdata', () => {
      expect(UpdateEventService['getEventCategory']({
        currentMatchesdata: {}
      })).toEqual('');
    });

    it('should return empty string if event no categoryId in reference of currentMatchesdata', () => {
      expect(UpdateEventService['getEventCategory']({
        currentMatchesdata: {
          reference: {}
        }
      })).toEqual('');
    });

    it('should return categoryId if event has categoryId in reference of currentMatchesdata', () => {
      const categoryId = '14';

      expect(UpdateEventService['getEventCategory']({
        currentMatchesdata: {
          reference: {
            categoryId
          }
        }
      })).toEqual(categoryId);
    });

    it('should return empty string if event no reference in eventdata', () => {
      expect(UpdateEventService['getEventCategory']({
        eventdata: {}
      })).toEqual('');
    });

    it('should return empty string if event no categoryId in reference of eventdata', () => {
      expect(UpdateEventService['getEventCategory']({
        eventdata: {
          reference: {}
        }
      })).toEqual('');
    });

    it('should return categoryId if event has categoryId in reference of eventdata', () => {
      const categoryId = '14';

      expect(UpdateEventService['getEventCategory']({
        eventdata: {
          reference: {
            categoryId
          }
        }
      })).toEqual(categoryId);
    });
  });

  describe('deleteSelection', () => {
    beforeEach(() => {});
    it('should delete selection but not MARKET', () => {
      cacheEventsService.storedData = {
        outcomesIndex: {
          98682906: 612952,
          98682896: 612952
        },
        index: {
          612952: {
            eventdata: {
              path: ['event', 'data', 0],
              reference: {
                id: 612952,
                markets: [{
                  id: '27026352',
                  outcomes: [{
                    id: '98682906'
                  }, {
                    id: '98682896'
                  }]
                }]
              }
            }
          }
        }
      } as any;
      service.init();
      service['deleteSelection']('612952', '27026352', '98682906');

      expect(pubSubService.publish).toHaveBeenCalledTimes(2);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('DELETE_MARKET_FROM_CACHE', '27026352');
      expect(cacheEventsService.storedData.outcomesIndex).toEqual({ 98682896: 612952 });
    });

    it('should delete selection and market', () => {
      cacheEventsService.storedData = {
        outcomesIndex: {
          98682906: 612952
        },
        event: {
          data: []
        },
        index: {
          612952: {
            eventdata: {
              path: ['event', 'data', 0],
              reference: {
                id: 612952,
                markets: [{
                  id: '27026352',
                  groupedOutcomes: [{
                    id: '98682906'
                  }],
                  outcomes: [{
                    id: '98682906'
                  }]
                }]
              }
            }
          }
        }
      } as any;
      service.init();
      service['deleteSelection']('612952', '27026352', '98682906');

      expect(pubSubService.publish).toHaveBeenCalledTimes(3);
      expect(pubSubService.publish).toHaveBeenCalledWith('DELETE_MARKET_FROM_CACHE', '27026352');
      expect(cacheEventsService.storedData.outcomesIndex).toEqual({});
    });

    it('should delete selection for surfaceBet module', () => {
      cacheEventsService.storedData = {
        outcomesIndex: {
          98682906: 612952
        },
        surfaceBetEvents: {
          data: []
        },
        index: {
          612952: {
            surfaceBetEventsdata: {
              path: ['surfaceBetEvents', 'data', 0],
              reference: {
                id: 612952,
                markets: [{
                  id: '27026352',
                  outcomes: [{
                    id: '98682906'
                  }]
                }]
              }
            }
          }
        }
      } as any;
      service.init();
      service['deleteSelection']('612952', '27026352', '98682906');

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DELETE_SELECTION_FROMCACHE,
        { selectionId: '98682906', marketId: '27026352', eventId: '612952' });
      expect(pubSubService.publish).toHaveBeenCalledTimes(1);
      expect(cacheEventsService.storedData.outcomesIndex).toEqual({});
    });
  });

  describe('isSiteServerGetNewMarketAllowed', () => {
    it('should return false (not market update)', () => {
      expect(
        service['isSiteServerGetNewMarketAllowed']({ subject_type: 'sPRICE' } as any, {}, {})
      ).toBeFalsy();
    });

    it('should return false (disabled in config)', () => {
      service['siteServerLiveMarketsConfig'].enabled = false;
      expect(
        service['isSiteServerGetNewMarketAllowed']({ subject_type: 'sEVMKT' } as any, {}, {})
      ).toBeFalsy();
    });

    it('should return true (sportCategoriesIds empty)', () => {
      service['siteServerLiveMarketsConfig'].enabled = true;
      const storedData: any = {
        index: {
          '1': {
            eventdata: { reference: {} }
          }
        }
      };
      const updateData: any = { subject_type: 'sEVMKT', channel_number: '1' };
      expect(
        service['isSiteServerGetNewMarketAllowed'](updateData, { sportCategoriesIds: '' }, storedData)
      ).toBeTruthy();
    });

    it('should return true (category id found)', () => {
      service['siteServerLiveMarketsConfig'].enabled = true;
      const storedData: any = {
        index: {
          '1': {
            eventdata: { reference: { categoryId: '2' } }
          }
        }
      };
      const updateData: any = { subject_type: 'sEVMKT', channel_number: '1' };
      expect(
        service['isSiteServerGetNewMarketAllowed'](updateData, { sportCategoriesIds: '2' }, storedData)
      ).toBeTruthy();
    });

    it('should return false (category id not found)', () => {
      service['siteServerLiveMarketsConfig'].enabled = true;
      const storedData: any = {
        index: {
          '1': {
            eventdata: { reference: { categoryId: '3' } }
          }
        }
      };
      const updateData: any = { subject_type: 'sEVMKT', channel_number: '1' };
      expect(
        service['isSiteServerGetNewMarketAllowed'](updateData, { sportCategoriesIds: '2' }, storedData)
      ).toBeFalsy();
    });
  });

  describe('handleEDPLiveMarket', () => {
    it('not displayed', () => {
      service['handleEDPLiveMarket']({ payload: { displayed: 'N' } } as any);
      expect(cacheEventsService.storeNewMarketOrOutcome).not.toHaveBeenCalled();
    });

    it('no market link', () => {
      cacheEventsService.storeNewMarketOrOutcome.and.returnValue('');
      service['isSiteServerGetNewMarketAllowed'] = jasmine.createSpy('isSiteServerGetNewMarketAllowed');
      service['handleEDPLiveMarket']({ payload: { displayed: 'Y' } } as any);
      expect(service['isSiteServerGetNewMarketAllowed']).not.toHaveBeenCalled();
    });

    it('get new markets NOT allowed', () => {
      service['isSiteServerGetNewMarketAllowed'] = () => false;
      cacheEventsService.storeNewMarketOrOutcome.and.returnValue('link');
      service['handleEDPLiveMarket']({ payload: { displayed: 'Y' } } as any);
      expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_MARKET_FOR_EDP', 'link');
    });

    it('get new markets allowed (no market, no outcomes)', fakeAsync(() => {
      service['isSiteServerGetNewMarketAllowed'] = () => true;
      cacheEventsService.storeNewMarketOrOutcome.and.returnValue('link');
      service['handleEDPLiveMarket']({ payload: { displayed: 'Y' } } as any);
      tick();
      expect(siteServerEventToOutcomeService.getEventToOutcomeForMarket).toHaveBeenCalledTimes(1);
      expect(awsService.addAction).toHaveBeenCalledWith('EDPLiveMarketInfoAvailable', { ssMarketAvailable: false });
      expect(awsService.addAction).toHaveBeenCalledWith('EDPLiveMarketOutcomesInfoAvailable', { ssMarketOutcomesAvailable: false });
    }));

    it('get new markets allowed (market and outcomes exist)', fakeAsync(() => {
      service['isSiteServerGetNewMarketAllowed'] = () => true;
      const marketLink = {};
      cacheEventsService.storeNewMarketOrOutcome.and.returnValue(marketLink);
      siteServerEventToOutcomeService.getEventToOutcomeForMarket.and.returnValue(observableOf([{
        markets: [{ cashoutAvail: 'Y', outcomes: [{}] }]
      }]));
      service['handleEDPLiveMarket']({ payload: { displayed: 'Y' } } as any);
      tick();
      expect(siteServerEventToOutcomeService.getEventToOutcomeForMarket).toHaveBeenCalledTimes(1);
      // @ts-ignore
      expect(marketLink.cashoutAvail).toEqual('Y');
      expect(cacheEventsService.storeNewOutcomes).toHaveBeenCalledTimes(1);
      expect(pubSubService.publish).toHaveBeenCalledWith('LIVE_MARKET_FOR_EDP', marketLink);
      expect(awsService.addAction).toHaveBeenCalledWith('EDPLiveMarketInfoAvailable', { ssMarketAvailable: true });
      expect(awsService.addAction).toHaveBeenCalledWith('EDPLiveMarketOutcomesInfoAvailable', { ssMarketOutcomesAvailable: true });
    }));

    it('get new markets allowed (market exist and outcomes NOT exist)', fakeAsync(() => {
      service['isSiteServerGetNewMarketAllowed'] = () => true;
      const marketLink = {};
      cacheEventsService.storeNewMarketOrOutcome.and.returnValue(marketLink);
      siteServerEventToOutcomeService.getEventToOutcomeForMarket.and.returnValue(observableOf([{
        markets: [{}]
      }]));
      service['handleEDPLiveMarket']({ payload: { displayed: 'Y' } } as any);
      tick();
      expect(siteServerEventToOutcomeService.getEventToOutcomeForMarket).toHaveBeenCalledTimes(1);
      expect(awsService.addAction).toHaveBeenCalledWith('EDPLiveMarketInfoAvailable', { ssMarketAvailable: true });
      expect(awsService.addAction).toHaveBeenCalledWith('EDPLiveMarketOutcomesInfoAvailable', { ssMarketOutcomesAvailable: false });
    }));
  });

  describe('#clearLiveMarketsSubscriptions', () => {
    it('should call unsubscribe method for all subscriptions in siteServerLiveMarketsSubscriptions array', () => {
      const subscriber1 = { unsubscribe: jasmine.createSpy() } as any;
      const subscriber2 = { unsubscribe: jasmine.createSpy() } as any;
      service['siteServerLiveMarketsSubscriptions'].push(subscriber1);
      service['siteServerLiveMarketsSubscriptions'].push(subscriber2);

      service['clearLiveMarketsSubscriptions']();
      expect(subscriber1.unsubscribe).toHaveBeenCalled();
      expect(subscriber2.unsubscribe).toHaveBeenCalled();
      expect(service['siteServerLiveMarketsSubscriptions'].length).toEqual(0);
    });
  });

  describe('deleteMarket', () => {
    it('should call deleteEvent method', () => {
      service['deleteEvent'] = jasmine.createSpy('deleteEvent');
      service.storedData = {
        index: {
          '1111': [{
            reference: {
              markets: [
                {
                  id: '33333',
                  outcomes: [{
                    id: '22222'
                  }]
                }
              ]
            }
          }]
        },
        marketsIndex: {
          '33333': []
        }
      } as any;

      service['deleteMarket']('1111', '33333');
      expect(pubSubService.publish).toHaveBeenCalled();
      expect(service['deleteEvent']).toHaveBeenCalledWith('1111');
    });

    it('should NOT call deleteEvent method', () => {
      service['deleteEvent'] = jasmine.createSpy('deleteEvent');
      service.storedData = {
        index: {
          '1111': [{
            reference: {
              markets: [
                {
                  id: '99999',
                  outcomes: [{
                    id: '22222'
                  }]
                }
              ]
            }
          }]
        },
        marketsIndex: {
          '33333': []
        }
      } as any;

      service['deleteMarket']('1111', '33333');
      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(service['deleteEvent']).not.toHaveBeenCalled();
    });
  });

  describe('#deltaObject', () => {
    it('should run sPRICE case, call getDecimal method and return proper delta with status="S"', () => {
      const updateItem = {
        subject_type: 'sPRICE',
        payload: {
          lp_den: '998',
          lp_num: '1',
          status: 'S'
        }
      } as any;
      fracToDecService.getDecimal = jasmine.createSpy().and.returnValue(1.001002);

      const result = service['deltaObject'](updateItem);

      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(1, 998, 6);
      expect(result).toEqual({
        priceDec: 1.001002,
        priceDen: 998,
        priceNum: 1,
        status: 'S',
        isDisplayed: true,
        priceType: 'LP'
      } as any);
    });

    it('should run sPRICE case, call getDecimal method and return proper delta with status=undefined', () => {
      const updateItem = {
        subject_type: 'sPRICE',
        payload: {
          lp_den: '998',
          lp_num: '1'
        }
      } as any;
      fracToDecService.getDecimal = jasmine.createSpy().and.returnValue(1.001002);

      const result = service['deltaObject'](updateItem);

      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(1, 998, 6);
      expect(result).toEqual({
        priceDec: 1.001002,
        priceDen: 998,
        priceNum: 1,
        status: undefined,
        isDisplayed: true,
        priceType: 'LP'
      } as any);
    });

    it('should run sSCBRD case and return proper delta', () => {
      const updateItem = {
        subject_type: 'sSCBRD',
        payload: {
          lp_den: '998',
          lp_num: '1'
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        lp_den: '998',
        lp_num: '1',
        isDisplayed: true
      });
    });

    it('should run sCLOCK case and return proper delta', () => {
      const updateItem = {
        subject_type: 'sCLOCK',
        payload: {
          lp_den: '998',
          lp_num: '1'
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        lp_den: '998',
        lp_num: '1',
        isDisplayed: true
      });
    });

    it('should run sEVMKT case and return delta with isDisplay=false', () => {
      const updateItem = {
        subject_type: 'sEVMKT',
        payload: {
          status: 'status',
          displayed: 'N'
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        marketStatusCode: 'status',
        isDisplayed: false
      });
    });

    it('should run sEVMKT case and return delta with isDisplayed=true', () => {
      const updateItem = {
        subject_type: 'sEVMKT',
        payload: {
          status: 'status',
          displayed: 'Y'
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        marketStatusCode: 'status',
        isDisplayed: true
      });
    });

    it('should run sEVENT case and return delta with isDisplayed=true, eventIsLive=false and resulted=false', () => {
      const updateItem = {
        subject_type: 'sEVENT',
        payload: {
          status: 'status',
          displayed: 'Y',
          started: 'N',
          race_stage: 'race_stage',
          result_conf: 'N',
          names: {
            en: 'en'
          }
        }
      } as any;
      scoreParserService.getScoreType.and.returnValue('GAA');
      scoreParserService.parseScores.and.returnValue(true);

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        eventStatusCode: 'status',
        isDisplayed: true,
        eventIsLive: false,
        raceStage: 'race_stage',
        resulted: false,
        score: true,
        originalName: 'en'
      } as any);
    });

    it('should run sEVENT case and return delta with isDisplayed=false, eventIsLive=true and resulted=true', () => {
      const updateItem = {
        subject_type: 'sEVENT',
        payload: {
          status: 'status',
          displayed: 'N',
          started: 'Y',
          race_stage: 'race_stage',
          result_conf: 'Y',
          names: {
            en: 'en'
          }
        }
      } as any;
      scoreParserService.getScoreType.and.returnValue(false);
      scoreParserService.parseScores.and.returnValue('parseScores');

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        eventStatusCode: 'status',
        isDisplayed: false,
        eventIsLive: true,
        raceStage: 'race_stage',
        resulted: true,
        score: 'test',
        originalName: 'en'
      } as any);
    });

    it('should run sSELCN case and return proper delta with isDisplayed=true', () => {
      const updateItem = {
        subject_type: 'sSELCN',
        payload: {
          status: 'S',
          displayed: 'Y'
        }
      } as any;

      const result = service['deltaObject'](updateItem);

      expect(result).toEqual({
        status: 'S',
        isDisplayed: true
      });
    });

    it('should run sSELCN case and return proper delta with isDisplayed=false and with priceDelta added', () => {
      const updateItem = {
        subject_type: 'sSELCN',
        payload: {
          lp_den: '998',
          lp_num: '1',
          status: 'S',
          displayed: 'N'
        }
      } as any;
      fracToDecService.getDecimal = jasmine.createSpy().and.returnValue(1.001002);

      const result = service['deltaObject'](updateItem);

      expect(fracToDecService.getDecimal).toHaveBeenCalledWith(1, 998, 6);
      expect(result).toEqual({
        status: 'S',
        isDisplayed: false,
        priceDec: 1.001002,
        priceDen: 998,
        priceNum: 1
      } as any);
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
});

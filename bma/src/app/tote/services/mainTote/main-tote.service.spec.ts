import { ToteService } from './main-tote.service';
import environment from '@environment/oxygenEnvConfig';
import { TOTE_CONFIG } from '../../tote.constant';
import { fakeAsync, tick } from '@angular/core/testing';
import { Observable, of, throwError } from 'rxjs';
import Spy = jasmine.Spy;

describe('ToteService', () => {
  let service: ToteService;

  let timeService;
  let cacheEventsService;
  let templateService;
  let siteServerPoolService;
  let liveStreamService;
  let pubSubService;
  let channelService;
  let isPropertyAvailableService;
  let siteServerEventToOutcomeService;
  let siteServerService;
  let cmsService;
  let routingHelperService;

  const CMSconfig = {
    InternationalTotePool: {
      Enable_International_Totepools: true,
      Enable_International_Totepools_On_RaceCard: true
    }
  };

  beforeEach(() => {
    timeService = {
      getRacingTimeRangeForRequest: jasmine.createSpy().and.returnValue('some IRacingDateRange object'),
      apiDataCacheInterval: {},
      formatHours: jasmine.createSpy('formatHours').and.returnValue('')
    };

    cacheEventsService = {
      stored: jasmine.createSpy('stored').and.returnValue(true),
      async: jasmine.createSpy('async').and.returnValue(of(null)),
      store: jasmine.createSpy('store'),
      storedData: {}
    };

    templateService = {
      filterEventsWithoutMarketsAndOutcomes: jasmine.createSpy().and.returnValue([]),
      groupEventsByTypeName: jasmine.createSpy()
    };

    siteServerPoolService = {
      getPoolToPoolValue: jasmine.createSpy().and.returnValue(Promise.resolve(null)),
      getPoolsForClass: jasmine.createSpy('getPoolsForClass').and.returnValue(of([])),
      getPools: jasmine.createSpy('getPools').and.returnValue(of([])),
      getPoolsForEvent: jasmine.createSpy('getPoolsForEvent').and.returnValue(of([{}]))
    };

    liveStreamService = {
      addLiveStreamAvailability: jasmine.createSpy('addLiveStreamAvailability').and.returnValue(() => [])
    };

    pubSubService = {
      publish: jasmine.createSpy()
    };

    channelService = {
      getLSChannels: jasmine.createSpy()
    };

    isPropertyAvailableService = {
      isPropertyAvailable: jasmine.createSpy('isPropertyAvailable').and.returnValue(() => null)
    };

    siteServerEventToOutcomeService = {
      getEventToOutcomeForMarket: jasmine.createSpy('getEventToOutcomeForMarket').and.returnValue(of([]))
    };

    siteServerService = {
      getResultsByClasses: jasmine.createSpy('getResultsByClasses').and.returnValue(Promise.resolve(null)),
      getRawEventsByClasses: jasmine.createSpy('getRawEventsByClasses').and.returnValue(of([])),
      getEventByEventId: jasmine.createSpy('getEventByEventId').and.returnValue(of([]))
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(CMSconfig))
    };

    routingHelperService = {
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl').and.returnValue('url')
    };

    service = new ToteService(
      timeService,
      cacheEventsService,
      templateService,
      siteServerPoolService,
      liveStreamService,
      pubSubService,
      channelService,
      isPropertyAvailableService,
      siteServerEventToOutcomeService,
      siteServerService,
      cmsService,
      routingHelperService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['TOTE_CATEGORY_ID']).toBe(environment.TOTE_CATEGORY_ID);
    expect(service.liveStreamConfig).toEqual(jasmine.any(Object));
  });

  describe('cachedEvents', () => {
    it('get stored events', fakeAsync(() => {
      service.cachedEvents(null, '')().subscribe();
      tick();
      expect(cacheEventsService.async).toHaveBeenCalled();
    }));

    it('use loader function', fakeAsync(() => {
      cacheEventsService.stored.and.returnValue(null);
      const loaderFn = jasmine.createSpy('loaderFn').and.returnValue(of(null));
      service.cachedEvents(loaderFn, 'totes', 'categoryId', 'startTime')().subscribe();
      tick();
      expect(loaderFn).toHaveBeenCalled();
      expect(cacheEventsService.store).toHaveBeenCalledWith('totes', 'categoryId', 'startTime', null);
    }));
  });

  it('cachedEvents', () => {
    const result = service.cachedEvents(() => {}, 'test');
    expect(result).toEqual(jasmine.any(Function));
    result();
    expect(cacheEventsService.stored).toHaveBeenCalledWith('test');
    expect(cacheEventsService.async).toHaveBeenCalledWith(true, false);
  });

  it('subscribeEDPForUpdates', () => {
    const channel = ['sEVENT1', 'SEVENT1'];
    const event: any = { liveServChannels: 'sEVENT1,', liveServChildrenChannels: 'SEVENT1,' };
    channelService.getLSChannels.and.returnValue(channel);

    service.subscribeEDPForUpdates(event);

    expect(channelService.getLSChannels).toHaveBeenCalledWith(event);
    expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', { channel, module: 'edp' });
  });

  it('unSubscribeEDPForUpdates', () => {
    service.unSubscribeEDPForUpdates();
    expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'edp');
  });

  it('eventsByMeeting', () => {
    const events = [
      { typeName: 'a' },
      { typeName: 'a' },
      { typeName: 'b' },
      { typeName: 'b' },
      { typeName: 'b' }
    ];

    const result = service.eventsByMeeting(events as any);

    expect(result).toEqual(jasmine.any(Array));
    expect(result.length).toBe(2);
    expect(result[0].events.length).toBe(2);
    expect(result[1].events.length).toBe(3);
  });

  it('filterResultedMeetings', () => {
    const meetings = [
      {
        events: [{}]
      },
      {
        events: [{ isResulted: true }, {}]
      },
      {
        events: [{ isResulted: true }, { isResulted: true }]
      }
    ];
    const result = service.filterResultedMeetings(meetings as any);
    expect(result.length).toBe(2);
  });

  it('addLiveStreamAvailabilityToMeetings', () => {
    service.addLiveStreamAvailabilityToMeetings([{}] as any);
    expect(isPropertyAvailableService.isPropertyAvailable).toHaveBeenCalled();
  });

  it('addRaceNames', () => {
    const events = [
      { localTime: '2017-01-01', typeName: 'start' },
      { localTime: '2017-01-02', typeName: 'finish' }
    ];
    const result: any = service.addRaceNames(events as any);
    expect(result[0].raceName).toBe('2017-01-01 start');
    expect(result[1].raceName).toBe('2017-01-02 finish');
  });

  it('arrangeEvents', () => {
    service.eventsByMeeting = jasmine.createSpy().and.returnValue([]);
    service.filterResultedMeetings = jasmine.createSpy().and.returnValue([]);
    service.addLiveStreamAvailabilityToMeetings = jasmine.createSpy();

    const result = service.arrangeEvents([ { id: 1, isStarted: 'true' }, { id: 2, isStarted: 'false' } ]);

    expect(templateService.filterEventsWithoutMarketsAndOutcomes).toHaveBeenCalledWith(jasmine.any(Array));
    expect(service.eventsByMeeting).toHaveBeenCalledWith(jasmine.any(Array));
    expect(service.addLiveStreamAvailabilityToMeetings).toHaveBeenCalledWith(jasmine.any(Array));

    expect(result).toEqual({
      meetings: [],
      events: [{ id: 2, isStarted: 'false' }]
    });
  });

  it('poolsForMarket', () => {
    const pools = [
      { marketIds: [1, 2] },
      { marketIds: [3] }
    ];
    const result = service.poolsForMarket(2, pools);
    expect(result.length).toBe(1);
  });

  it('filterByPoolTypeOrder', () => {
    const pools = ['endless', 'space'];
    expect(service.filterByPoolTypeOrder(pools, 'endless').length).toBe(1);
    expect(service.filterByPoolTypeOrder(pools, 'borderless').length).toBe(0);
    // @ts-ignore
    expect(service.filterByPoolTypeOrder(pools, '')).toEqual(pools);
  });

  it('addNonRunners', () => {
    const events: any = [
      {
        markets: [
          {
            outcomes: [
              { name: 'N/R' },
              { name: 'Peter Pan' }
            ]
          }
        ]
      }
    ];
    expect(service.addNonRunners(events)).toBe(events);
    expect(events[0].markets[0].outcomes[0].nonRunner).toBeTruthy();
    expect(events[0].markets[0].outcomes[1].nonRunner).toBeFalsy();
  });

  it('addPoolsToEvents', () => {
    const poolsArray = [ { type: 'TR', marketIds: '1' }, { type: 'WN', marketIds: '1' }];
    const result:any = service.addPoolsToEvents( poolsArray, [{ markets: [{id: '1'}] }] );
    // @ts-ignore
    expect(result).toEqual([{
        markets: [{ id: '1' }],
        pools: [{ type: 'TR', marketIds: '1' }, { type: 'WN', marketIds: '1' }],
        defaultPoolType: 'WN',
        poolsTypesOrdered: ['WN', 'TR']
      }]);
  });

  it('setDefPoolType', () => {
    expect(service.setDefPoolType(['WN'])).toBe('WN');
    expect(service.setDefPoolType(['PL'])).toBe('PL');
    expect(service.setDefPoolType(['SH'])).toBe('SH');
    expect(service.setDefPoolType(['IE'])).toBe(undefined);
  });

  it('getGuidesData', () => {
    expect(service.getGuidesData('p1')).toEqual(jasmine.any(Promise));
    expect(siteServerPoolService.getPoolToPoolValue).toHaveBeenCalledWith('p1');
  });

  describe('getToteEvents', () => {
    it('with class ids', fakeAsync(() => {
      service.cachedEvents = (loader) => {
        loader().subscribe();
        return () => {};
      };
      service.getToteEvents('1,2,3');
      tick();
      expect(siteServerPoolService.getPoolsForClass).toHaveBeenCalled();
    }));

    it('without class ids', fakeAsync(() => {
      siteServerPoolService.getPools.and.returnValue( of([{ marketIds: [1] }]) );
      service.cachedEvents = (loader) => {
        loader().subscribe();
        return () => {};
      };
      service.getToteEvents('');
      tick();
      expect(siteServerPoolService.getPools).toHaveBeenCalled();
    }));

    it('error', fakeAsync(() => {
      service.cachedEvents = (loader) => {
        loader().subscribe({
          error: err => expect(err).toBe('error')
        });
        return () => {};
      };
      siteServerPoolService.getPoolsForClass.and.returnValue(throwError('error'));

      service.getToteEvents('1');
      tick();
    }));
  });

  it('setTimeRange if TOTE_CONFIG.eventsReqConfig.timeRange is NOT defined', () => {
    const oldValue = TOTE_CONFIG.eventsReqConfig.timeRange;
    TOTE_CONFIG.eventsReqConfig.timeRange = '';

    // @ts-ignore
    expect(service.setTimeRange()).toEqual({});

    TOTE_CONFIG.eventsReqConfig.timeRange = oldValue;
  });

  it('setTimeRange if TOTE_CONFIG.eventsReqConfig.timeRange is defined', () => {
    // @ts-ignore
    expect(service.setTimeRange()).toEqual('some IRacingDateRange object');
  });

  describe('getToteEvent', () => {
    it('no error', fakeAsync(() => {
      service.cachedEvents = (loader) => {
        loader({ eventsIds: [1] }).subscribe();
        return () => {};
      };

      service.getToteEvent('1');
      tick();

      expect(siteServerPoolService.getPoolsForEvent).toHaveBeenCalled();
      expect(siteServerEventToOutcomeService.getEventToOutcomeForMarket).toHaveBeenCalled();
      expect(liveStreamService.addLiveStreamAvailability).toHaveBeenCalled();
    }));

    it('error', fakeAsync(() => {
      service.cachedEvents = (loader) => {
        loader({ eventsIds: [1] }).subscribe({
          error: err => expect(err).toBe('error')
        });
        return () => {};
      };
      siteServerPoolService.getPoolsForEvent.and.returnValue(throwError('error'));

      service.getToteEvent('1');
      tick();
    }));
  });

  it('getEventsTabsDataByMeeting', () => {
    const meeting = { events: [{}] };
    const result = service.getEventsTabsDataByMeeting(meeting as any);
    expect(result).toEqual(jasmine.any(Array));
    expect(result.length).toBe(1);
    expect(result[0]).toEqual(jasmine.any(Object));
  });

  it('getEventsTabsDataByMeeting should set label from event localTime', () => {
    const meeting = { events: [ {localTime: '2:00'}, {localTime: '23:23'} ] };
    service.getEventsTabsDataByMeeting(meeting as any);
    expect(timeService.formatHours).toHaveBeenCalledTimes(meeting.events.length);
  });

  it('getPoolTabsData', () => {
    const data = { pools: [{}] };
    const result = service.getPoolTabsData(data as any);
    expect(result).toEqual(jasmine.any(Array));
    expect(result.length).toBe(1);
    expect(result[0]).toEqual(jasmine.any(Object));
  });

  it('prepareEventsObj', () => {
    const data = {};
    const result = service.prepareEventsObj(data);
    expect(templateService.groupEventsByTypeName).toHaveBeenCalledWith(data, true);
    expect(result).toEqual(jasmine.any(Object));
  });

  describe('resultsByClasses', () => {
    it('no error', () => {
      const data = {};
      expect(service.resultsByClasses(data)).toEqual(jasmine.any(Observable));
      expect(siteServerService.getResultsByClasses).toHaveBeenCalledWith(data);
    });

    it('error', fakeAsync(() => {
      siteServerService.getResultsByClasses.and.returnValue(throwError('error'));
      service.resultsByClasses({}).subscribe({
        error: err => expect(err).toBe('error')
      });
    }));
  });

  it('collapsedSummaries', () => {
    expect(service.collapsedSummaries()).toEqual(jasmine.any(Object));
  });

  it('getPoolStakes', () => {
    const event = {
      pools: [
        { poolType: 'WN' },
        { poolType: 'x' }
      ]
    };
    expect(service.getPoolStakes(event).poolType).toBe('WN');
    expect(service.getPoolStakes(event, 'x').poolType).toBe('x');

    expect(service.getPoolStakes(event, 'z')).toBeUndefined();
  });

  describe('@getToteLink', () => {

    beforeEach(() => {
      spyOn(service, 'getEventById').and.returnValue(of({} as any));
    });

    it('foolproof return', fakeAsync(() => {
      service.getToteLink(undefined, undefined, true).subscribe(url => {
        tick();
        expect(url).toBe('');
      });
    }));

    it('should check CMS config for int tote', fakeAsync(() => {
      service.getToteLink('12345', '54321', false).subscribe(url => {
        tick();
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
      });
    }));

    it('should not check CMS config for UK tote', fakeAsync(() => {
      service.getToteLink('12345', '54321', true).subscribe(url => {
        tick();
        expect(cmsService.getSystemConfig).not.toHaveBeenCalled();
      });
    }));

    it('should get ob event for UK', fakeAsync(() => {
      service.getToteLink('12345', '54321', true).subscribe(url => {
        tick();
        expect(service.getEventById).toHaveBeenCalledWith(12345);
      });
    }));

    it('should get ob event and edpUrl for International', fakeAsync(() => {
      service.getToteLink('12345', '54321', false).subscribe(url => {
        tick();
        expect(service.getEventById).toHaveBeenCalledWith(12345);
        expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith(jasmine.any(Object));
      });
    }));

    it('should not get ob event for International but return tote link if switcher is off', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        InternationalTotePool: {
          Enable_International_Totepools_On_RaceCard: false
        }
      }));
      service.getToteLink('12345', '54321', false).subscribe(url => {
        tick();
        expect(service.getEventById).not.toHaveBeenCalled();
        expect(routingHelperService.formResultedEdpUrl).not.toHaveBeenCalled();
        expect(url.includes('tote/event')).toBe(true);
      });
    }));

    // "ob event is not found" == old resulted event
    it('should return empty url if ob event is not found', fakeAsync(() => {
      (service.getEventById as Spy).and.returnValue(of(false));
      service.getToteLink('12345', '54321', false).subscribe(url => {
        tick();
        expect(url).toBe('');
      });
    }));

    it('should return empty url if switcher is off but tote id is unknown', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        InternationalTotePool: {
          Enable_International_Totepools_On_RaceCard: false
        }
      }));
      (service.getEventById as Spy).and.returnValue(of(false));
      service.getToteLink('12345', undefined, false).subscribe(url => {
        tick();
        expect(url).toBe('');
      });
    }));

    it('should open totepool tab for UK if event is not resulted yet', fakeAsync(() => {
      service.getToteLink('12345', '54321', true).subscribe(url => {
        tick();
        expect(url.includes('totepool')).toBe(true);
      });
    }));

    it('should not go to totepool tab for UK if event is resulted', fakeAsync(() => {
      (service.getEventById as Spy).and.returnValue(of({isResulted: true}));
      service.getToteLink('12345', '54321', true).subscribe(url => {
        tick();
        expect(url.includes('totepool')).toBe(false);
      });
    }));
  });

  it('getToteResults', fakeAsync(() => {
    service.prepareEventsObj = jasmine.createSpy('prepareEventsObj');
    service.getToteResults().subscribe();
    tick();
    expect(service.prepareEventsObj).toHaveBeenCalled();
  }));

  it('getRawToteEvents', () => {
    service.getRawToteEvents(1);
    expect(siteServerService.getRawEventsByClasses).toHaveBeenCalledWith({ classIds: [1], externalKeysEvent: true });
  });

  it('getEventById', () => {
    service.getEventById(1);
    expect(siteServerService.getEventByEventId).toHaveBeenCalledWith(1);
  });

  describe('#filterRacingGroup', () => {
    it('should return unchanged racing, if racing is null', () => {
      expect(service.filterToteGroup(null)).toBe(null);
    });
    it('should return unchanged racing, if racing is empty', () => {
      expect(service.filterToteGroup([]).length).toBe(0);
    });
    it('should return racing, if racing is not empty', () => {
      const today = new Date();
      const request = [{
        startTime: today.setDate(today.getDate() - 2)
      }, {
        startTime: today.setDate(today.getDate() + 2)
      }, {
        startTime: today
      }] as any;
      expect(service.filterToteGroup(request).length).toBeDefined()
    });
  });

});

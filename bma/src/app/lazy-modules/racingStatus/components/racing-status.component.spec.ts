import { RacingStatusComponent } from '@lazy-modules/racingStatus/components/racing-status.component';
import { of as observableOf } from 'rxjs';

describe('RacingStatusComponent', () => {
  const  mockData = {
    correctedDayValue: 'racing.sunday',
    liveServChannels: '123'
   } as any;

  let component: RacingStatusComponent;
  let localeService,
      liveServeHandleUpdatesService,
      windowRef,
      pubSubService,
      deviceService,
      cmsService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        EXTRA_PLACE_RACE_OFF: 'EXTRA_PLACE_RACE_OFF',
        SUSPEND_IHR_EVENT_OR_MRKT: 'SUSPEND_IHR_EVENT_OR_MRKT'
      }
    };
    deviceService = {isDesktop: false};
    liveServeHandleUpdatesService = {
      subscribe:jasmine.createSpy('subscribe').and.callFake((a, b)=> {
        b({
          type: 'sEVENT',
          payload: {
            started: 'Y',
            result_conf: 'Y',
            status: "A"
          }
        });
      })
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        HorseRacingBIR: {
          marketsEnabled: ['win or each Way']
        }
      }))
    };
    windowRef = {};
    component = new RacingStatusComponent(localeService, pubSubService, deviceService, cmsService, liveServeHandleUpdatesService, windowRef);
    component.event = {} as any;
  });

  describe('#ngOnInit', () => {
    it('should set "resulted" status', () => {
      component.event.isResulted = true;
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.result');
      expect(component.status.class).toBe('resulted');
    });

    it('should set "race-off" status', () => {
      component.event.isResulted = false;
      component.event.isLiveNowEvent = false;
      component.event.isStarted = true;
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.raceOff');
      expect(component.status.class).toBe('race-off');
    });

    it('should set "in-play" status', () => {
      component.event.isResulted = false;
      component.event.isStarted = false;
      component.isHrEdp = true;
      component.event.categoryId = '21';
      component.event.eventStatusCode = 'A';
      component.event.drilldownTagNames = 'EVFLAG_IHR';
      component.event.markets = [{marketStatusCode: 'A', name: 'Win or Each Way'} as any];
      component.event.rawIsOffCode = 'Y';
      component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(true);
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.inPlay');
    });

    it('should set "raceOff" status, NO rawIsOffCode & isStarted as true', () => {
      component.event.isResulted = false;
      component.event.isStarted = true;
      component.isHrEdp = true;
      component.event.categoryId = '21';
      component.event.eventStatusCode = 'A';
      component.event.drilldownTagNames = 'EVFLAG_IHR';
      component.event.markets = [{marketStatusCode: 'S', name: 'Win or Each Way'} as any];
      component.ngOnInit();
      expect(component.status.title).toBe('');
    });

    it('should set "raceOff" status', () => {
      component.event.isResulted = false;
      component.event.isStarted = true;
      component.isHrEdp = true;
      component.event.categoryId = '21';
      component.event.eventStatusCode = 'A';
      component.event.drilldownTagNames = 'EVFLAG_IHR';
      component.event.rawIsOffCode = 'Y';
      component.event.markets = [{marketStatusCode: 'S', name: 'Win or Each Way'} as any];
      component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(true);
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.raceOff');
    });

    it('should set "live" status', () => {
      component.event.isResulted = false;
      component.event.isLiveNowEvent = true;
      component.event.isStarted = true;
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.liveNow');
      expect(component.status.class).toBe('live');
    });

    it('should set "race-off" status when event.categoryName === Horse Racing', () => {
      component.event.categoryId = '21';
      component.event.isResulted = false;
      component.event.isStarted = true;
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.raceOff');
      expect(component.status.class).toBe('race-off');
    });

    it('EXTRA_PLACE_RACE_OFF subscription', () => {
      component.event = {
        id: 555,
        name: 'Leg event',
        markets: [],
        categoryCode: 'HORSE_RACING',
        isFinished: 'false',
      } as any;
      component.event.drilldownTagNames = 'EVFLAG_IHR',
      component.isHrEdp = true;
      component.isEventSelected = true;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.EXTRA_PLACE_RACE_OFF) {
          fn('555');
        }
      });
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.inPlay');
    });

    it('SUSPEND_IHR_EVENT_OR_MRKT subscription and title is raceOff', () => {
      component.event = {
        id: 555,
        name: 'Leg event',
        markets: [{marketStatusCode: 'S', name: 'Win or Each Way'}],
        categoryCode: 'HORSE_RACING',
        isFinished: 'false',
      } as any;
      component.event.drilldownTagNames = 'EVFLAG_IHR',
      component.isHrEdp = true;
      component.isEventSelected = true;
      component.isInplay = true;
      component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(true);
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT) {
          fn('555', {eventStatusCode: 'S', marketStatusCode: 'S', originalName: 'Win or Each Way'});
        }
      });
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.raceOff');
    });

    it('SUSPEND_IHR_EVENT_OR_MRKT subscription and title is raceOff - eventStatusCode as active', () => {
      component.event = {
        id: 555,
        name: 'Leg event',
        markets: [[{marketStatusCode: 'S', name: 'Win or Each Way'}]],
        categoryCode: 'HORSE_RACING',
        isFinished: 'false',
      } as any;
      component.event.drilldownTagNames = 'EVFLAG_IHR',
      component.isHrEdp = true;
      component.isEventSelected = true;
      component.isInplay = true;
      component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(true);
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT) {
          fn('555', {eventStatusCode: 'A', marketStatusCode: 'S', originalName: 'Win or Each Way'});
        }
      });
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.raceOff');
    });

    it('SUSPEND_IHR_EVENT_OR_MRKT subscription and title is inPlay', () => {
      component.event = {
        id: 555,
        name: 'Leg event',
        markets: [],
        categoryCode: 'HORSE_RACING',
        isFinished: 'false',
      } as any;
      component.event.drilldownTagNames = 'EVFLAG_IHR',
      component.isHrEdp = true;
      component.isEventSelected = true;
      component.isInplay = true;
      component['isBirMarketEnabled'] = jasmine.createSpy().and.returnValue(true);
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT) {
          fn('555', {eventStatusCode: 'A', marketStatusCode: 'A', originalName: 'Win or Each Way'});
        }
      });
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalledWith('racing.inPlay');
    });
  });
  describe('getBIRMarkets', () => {
    it('getBIRMarkets with cms config as null', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(null));
      component['getBIRMarkets']();
      expect(component['BIRMarketsEnabled']).toBeFalsy();
    });
    it('getBIRMarkets with actual values', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: {marketsEnabled: ['Win or Each Way']}}));
      component['getBIRMarkets']();
      expect(component['BIRMarketsEnabled']).toEqual(['Win or Each Way']);
    });
    it('getBIRMarkets with HorseRacingBIR as null', () => {
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: null}));
      component['getBIRMarkets']();
      expect(component['BIRMarketsEnabled']).toBeFalsy();
    });
  });
  describe('isBirMarketEnabled', () => {
    it('BIRMarketsEnabled', () => {
      component['BIRMarketsEnabled'] = ['Win or Each Way'];
      expect(component['isBirMarketEnabled']('Win or Each Way')).toBeTruthy();
    });
    it('isBirMarketEnabled with null input', () => {
      component['BIRMarketsEnabled'] = ['Win or Each Way'];
      expect(component['isBirMarketEnabled']()).toBeFalsy();
    });
    it('isBirMarketEnabled with BIRMarketsEnabled as null', () => {
      component['BIRMarketsEnabled'] = null;
      expect(component['isBirMarketEnabled']()).toBeFalsy();
    });
  });
  it('unsubscribe to be called in ngOnDestroy', () => {
    component.isPubsubSubscribed = true;
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });
  
  it('liveServeHandler for HR',() => {
    component.event  = mockData;
    component.isHrEdp = true;
    component.event.correctedDayValue='racing.today';
    component.liveServeSubscription = true;
    component.ngOnInit();
    expect(liveServeHandleUpdatesService.subscribe).toHaveBeenCalled();
  });

  it('liveServeHandler for GH',() => {
    component.event  = mockData;
    component.isHrEdp = false;
    component.event.correctedDay='sb.today';
    component.liveServeSubscription = true;
    component.ngOnInit();
    expect(liveServeHandleUpdatesService.subscribe).toHaveBeenCalled();
  });

  it('liveServeHandler',() => {
    component.event  = mockData;
    component.isHrEdp = false;
    component.event.correctedDay='racing.tomorrow';
    component.liveServeSubscription = false;
    component.ngOnInit();
    expect(liveServeHandleUpdatesService.subscribe).not.toHaveBeenCalled();
  });
});

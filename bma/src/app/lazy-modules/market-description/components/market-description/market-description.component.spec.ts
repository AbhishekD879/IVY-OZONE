import {
  MarketDescriptionComponent
 } from './market-description.component';

describe('MarketDescriptionComponent', () => {
  let component;
  let changeDetectorRef;
  let pubSubService;

  beforeEach(() => {
    pubSubService = {
      API: {
        HAS_MARKET_DESCRIPTION: 'HAS_MARKET_DESCRIPTION'
      },
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy().and.callFake((a, b, cb) => cb && cb()),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    component = new MarketDescriptionComponent(changeDetectorRef, pubSubService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should set marketDescription if it contains sorted markets (isHR and HR Category)', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: true,
          isGH: false
        }],
        categoryId: '21'
      } as any;
      component.selectedMarket = 'To Finish';
      component.ngOnInit();
      expect(component.marketData).toBeDefined();
      expect(component.isValidRaceEvent).toBeTruthy();
    });
    it('should set marketDescription if it contains sorted markets(isGH and GH Category)', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: true
        }],
        categoryId: '19'
      } as any;
      component.selectedMarket = 'To Finish';
      component.ngOnInit();
      expect(component.marketData).toBeDefined();
      expect(component.isValidRaceEvent).toBeTruthy();
    });
    it('should set marketDescription if it contains sorted markets (isHR and HR Category)', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false
        }],
        categoryId: '21'
      } as any;
      component.selectedMarket = 'To Finish';
      component.ngOnInit();
      expect(component.isValidRaceEvent).toBeFalsy();
    });
    it('should set marketDescription if it contains sorted markets(isGH and GH Category)', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false
        }],
        categoryId: '19'
      } as any;
      component.selectedMarket = 'To Finish';
      component.ngOnInit();
      expect(component.isValidRaceEvent).toBeFalsy();
    });
    it('should not set data if there are no sorted markets', () => {
      component.eventEntity = {
      } as any;
      component.ngOnInit();
      expect(component.marketData).toBeNull();
    });
    it('should call setBirDescription if birDescription is defined', () => {
      component['setBirDescription'] = jasmine.createSpy();
      component.selectedMarket = 'To Finish';
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false,
          birDescription: 'this in birdesc'
        }],
        categoryId: '19'
      } as any;
      component.ngOnInit();
      expect(component['setBirDescription']).toHaveBeenCalled();
    });
    it('should not call setBirDescription if birDescription is undefined', () => {
      component['setBirDescription'] = jasmine.createSpy();
      component.selectedMarket = 'To Finish';
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false,
        }],
        categoryId: '19'
      } as any;
      component.ngOnInit();
      expect(component['setBirDescription']).not.toHaveBeenCalled();
    });
  });
  describe('#ngOnChanges', () => {
    it('setMarketDescription should not be called', () => {
      const changes = {
      } as any;
      component['setMarketDescription'] = jasmine.createSpy();
      component.ngOnChanges(changes);

      expect(component['setMarketDescription']).not.toHaveBeenCalled();
    });

    it('setMarketDescription should be called', () => {
      const changes = {
        selectedMarket: 'Forecast'
      } as any;
      component['setMarketDescription'] = jasmine.createSpy();
      component.ngOnChanges(changes);

      expect(component['setMarketDescription']).toHaveBeenCalled();
    });
  });
  describe('#ngOndestroy', () => {
    it('pubsub.unsubscribe to have been called', () => {
      component.eventEntity ={id:123};
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith("market-description123");
    });
  });
  describe('#setBirDescription', () => {
    it('set all the flags true if satisfied', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false,
          birDescription: 'this in birdesc'
        }], drilldownTagNames: 'EVFLAG_IHR,EVFLAG', categoryId: '21', isStarted: true, eventIsLive: true, isResulted: false, id: 1
      }
      component.setBirDescription();
      expect(component.isEventBIR).toBeTrue();
      expect(component.isEventLive).toBeTrue();
      expect(component.isHrEvent).toBeTrue();
    });
    it('set flags flase if not satisfed', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false,
          birDescription: 'this in birdesc'
        }], drilldownTagNames: 'EVFLAG', categoryId: '20', isStarted: false, eventIsLive: false, isResulted: true, id: 1
      }
      component.setBirDescription();
      expect(component.isEventBIR).toBeFalse();
      expect(component.isEventLive).toBeFalse();
      expect(component.isHrEvent).toBeFalse();
    });
    it('should call pusub when race transists from prelive to live and make isEventLive if id matches ', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false,
          birDescription: 'this in birdesc'
        }], drilldownTagNames: 'EVFLAG_IHR,EVFLAG', categoryId: '21', isStarted: false, eventIsLive: false, isResulted: true
      }
      component.eventEntity.id = 1;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.EXTRA_PLACE_RACE_OFF) {
          fn(1);
        }
      });
      component.setBirDescription();
      expect(component.isEventLive).toBeTrue();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should not call pusub when race transists from prelive to live and make isEventLive if id not matches ', () => {
      component.eventEntity = {
        sortedMarkets: [{
          label: 'To Finish',
          isHR: false,
          isGH: false,
          birDescription: 'this in birdesc'
        }], drilldownTagNames: 'EVFLAG_IHR,EVFLAG', categoryId: '21', isStarted: false, eventIsLive: false, isResulted: true
      }
      component.eventEntity.id = 11;
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.EXTRA_PLACE_RACE_OFF) {
          fn('1');
        }
      });
      component.setBirDescription();
      expect(component.isEventLive).toBeFalse();
    });
  });
  describe('#showDescription', () => {
    it('should return true if condition statisfies', () => {
      component.marketData = { description: 'this is description' };
      component.isValidRaceEvent = true;
      component.isEventBIR = true;
      component.isEventLive = true;
      expect(component.showDescription()).toBeTrue();
    });
    it('should return true if condition statisfies#1', () => {
      component.marketData = { birDescription: 'this is bir description' };
      component.isValidRaceEvent = true;
      component.isEventBIR = true;
      component.isEventLive = false;
      component.isHrEvent = true;
      component.eventEntity = {rawIsOffCode: 'Y'};
      expect(component.showBIRDescription()).toBeTrue();
    });
    it('should return false if condition not statisfies', () => {
      component.isValidRaceEvent = false;
      component.isEventBIR = false;
      component.isEventLive = false;
      component.marketData = { description: 'this is description', birDescription: 'this is bir description' };
      expect(component.showDescription()).toBeFalse();
    });
    it('should return false if condition marketData is null', () => {
      component.isValidRaceEvent = false;
      component.isEventBIR = false;
      component.isEventLive = false;
      component.marketData = null;
      expect(component.showDescription()).toBeUndefined();
    });
  });
  describe('#showBirDescription', () => {
    it('should return true if condition statisfies', () => {
      component.marketData = { birDescription: 'this is bir description' };
      component.isValidRaceEvent = true;
      component.isEventBIR = true;
      component.isEventLive = true;
      component.isHrEvent = true;
      expect(component.showBIRDescription()).toBeTrue();
    });
    it('should return false if condition marketData is null', () => {
      component.marketData = null;
      component.isValidRaceEvent = true;
      component.isEventBIR = true;
      component.isEventLive = true;
      component.isHrEvent = true;
      expect(component.showBIRDescription()).toBeUndefined();
    });
    it('should return false if condition not statisfies', () => {
      component.isValidRaceEvent = false;
      component.isEventBIR = false;
      component.isEventLive = false;
      component.isHrEvent = false;
      component.marketData = { birDescription: 'this is bir description' }
      expect(component.showBIRDescription()).toBeFalse();
    });
  });
});

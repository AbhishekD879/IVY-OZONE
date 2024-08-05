import { InPlaySportTabComponent } from './in-play-sport-tab.component';

describe('#InPlaySportTabComponent', () => {
  let component: InPlaySportTabComponent;
  let inplayHelperService,
  inplayMainService,
  userService;

  beforeEach(() => {
    inplayHelperService = {
      subscribeForLiveUpdates: () => {},
      unsubscribeForLiveUpdates: () => {}
    };
    inplayMainService = {
      isCashoutAvailable: () => {}
    };
    userService = {};

    component = new InPlaySportTabComponent(inplayHelperService, inplayMainService, userService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('gtmDataLayer.eventAction should be equal live stream', () => {
    component.liveStreamTab = true;
    component.ngOnInit();

    expect(component.gtmDataLayer.eventAction).toBe('live stream');
  });

  it('gtmDataLayer.eventAction should be equal in-play', () => {
    component.liveStreamTab = false;
    component.ngOnInit();

    expect(component.gtmDataLayer.eventAction).toBe('in-play');
  });
  it('should call processInitialData if events data is 21', () => {
    component.eventsBySports = [{ events: [{ categoryId: '21' }] }] as any;
    spyOn(component as any, 'processInitialData');
    component.ngOnInit();
    expect(component['processInitialData']).toHaveBeenCalled();
  });
  it('should not call processInitialData if events data is not 21', () => {
    component.eventsBySports = [{ events: [{ categoryId: '20' }] }] as any;
    spyOn(component as any, 'processInitialData');
    component.ngOnInit();
    expect(component['processInitialData']).not.toHaveBeenCalled();
  });
  it('should not call processInitialData if eventsBySports is null', () => {
    component.eventsBySports = [null];
    spyOn(component as any, 'processInitialData');
    component.ngOnInit();
    expect(component['processInitialData']).not.toHaveBeenCalled();
  });
  it('should not call processInitialData if events is null', () => {
    component.eventsBySports = [{ events: [null] }] as any;
    spyOn(component as any, 'processInitialData');
    component.ngOnInit();
    expect(component['processInitialData']).not.toHaveBeenCalled();
  });
  describe('processInitialData', () => {
    it('should call setExpandedFlag', () => {
      component.eventsBySports = [{ events: [{ categoryId: '20' }] }] as any;
      spyOn(component as any, 'setExpandedFlag');
      component['processInitialData']();
      expect(component['setExpandedFlag']).toHaveBeenCalledWith(component.eventsBySports[0], 0);
    });
    it('should not call setExpandedFlag', () => {
      spyOn(component as any, 'setExpandedFlag');
      component['processInitialData']();
      expect(component['setExpandedFlag']).not.toHaveBeenCalled();
    });
  });
  describe('setExpandedFlag', () => {
    it('should set HREvents', () => {
      component.eventsBySports = [{ events: [{ startTime: '1:00', categoryId: '20' },{ startTime: '2:00', categoryId: '20' }] }] as any;
      component['setExpandedFlag'](component.eventsBySports[0], 0);
      expect(component.HREvents).toBeDefined();
      expect(component.HREvents.length).toEqual(2);
    });
  });
});

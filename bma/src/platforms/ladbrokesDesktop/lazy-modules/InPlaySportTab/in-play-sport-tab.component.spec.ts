import { InPlaySportTabComponent } from './in-play-sport-tab.component';

describe('#InPlaySportTabComponent', () => {
  let component: InPlaySportTabComponent;
  let userService;
  let inplayMainService;
  let inplayHelperService;

  beforeEach(() => {
    userService = {};
    inplayHelperService = {
      subscribeForLiveUpdates: jasmine.createSpy(),
      unsubscribeForLiveUpdates: jasmine.createSpy(),
    };

    inplayMainService = {
      isCashoutAvailable: jasmine.createSpy()
    };

    component = new InPlaySportTabComponent(
      inplayMainService,
      inplayHelperService,
      userService
    );
  });

  describe('@ngOnInit', () => {
    it('should set gtmDataLayer if it is in-play tab', () => {
      component.ngOnInit();
      expect(component.gtmDataLayer).toEqual({
        eventAction: 'in-play',
        eventLabel: 'more markets'
      });
    });

    it('should set gtmDataLayer if it is in-play tab', () => {
      component.liveStreamTab = true;
      component.ngOnInit();
      expect(component.gtmDataLayer).toEqual({
        eventAction: 'live stream',
        eventLabel: 'more markets'
      });
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
    it('should not call processInitialData if events data is not 21', () => {
      component.eventsBySports = [{ events: [{ categoryId: null }] }] as any;
      spyOn(component as any, 'processInitialData');
      component.ngOnInit();
      expect(component['processInitialData']).not.toHaveBeenCalled();
    });
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

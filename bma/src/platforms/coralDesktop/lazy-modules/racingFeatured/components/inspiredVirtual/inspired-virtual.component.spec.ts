import { DesktopInspiredVirtualComponent } from './inspired-virtual.component';
import { ISportEvent } from '@core/models/sport-event.model';

describe('DesktopInspiredVirtualComponent', () => {
  let component: DesktopInspiredVirtualComponent;
  let carouselService;
  let inspiredVirtualService;
  let router;
  let pubSubService;
  let storage;
  let virtualSharedService;
  let vEPService;

  beforeEach(() => {
    inspiredVirtualService = {
      config: {
        slidesLimit: 5
      },
      getGtmCommonObject: jasmine.createSpy().and.returnValue({
        eventCategory: 'horse racing',
        eventAction: 'virtual horse racing'
      }),
      getEvents: jasmine.createSpy().and.returnValue(Promise.resolve([])),
      virtualsGTMEventTracker: jasmine.createSpy(),
    };
    carouselService = {};
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      API: {
        PUSH_TO_GTM: 'PUSH_TO_GTM'
      }
    };

    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
    };

    virtualSharedService = {
      formVirtualTypeUrl: () => {},
      formVirtualEventUrl: () => {}
    };

    vEPService ={}

    component = new DesktopInspiredVirtualComponent(
      inspiredVirtualService,
      router,
      storage,
      carouselService,
      pubSubService,
      virtualSharedService,
      vEPService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('sendCollapseGTM', () => {
    it('should call sendGTM on first time collapse', () => {
      component.sportName = 'horseracing';
      component['sendGTM'] = jasmine.createSpy('sendGTM');
      component.isFirstTimeCollapsed = false;

      component.sendCollapseGTM();

      expect(component['sendGTM']).toHaveBeenCalledWith('collapse');
    });

    it('should change "isFirstTimeCollapsed" to be true, on first time collapse', () => {
      component.sportName = 'horseracing';
      component['sendGTM'] = jasmine.createSpy('sendGTM');
      component.isFirstTimeCollapsed = false;

      component.sendCollapseGTM();

      expect(component.isFirstTimeCollapsed).toBeTruthy();
    });

    it('should not call sendGTM if it was collapsed previously', () => {
      component.sportName = 'horseracing';
      component['sendGTM'] = jasmine.createSpy('sendGTM');
      component.isFirstTimeCollapsed = true;

      component.sendCollapseGTM();

      expect(component['sendGTM']).not.toHaveBeenCalled();
    });
  });

  describe('sendGTM', () => {
    it('should send GTM tracking', () => {
      const eventLabel = 'collapse';
      component.sportName = 'horseracing';
      component['sendGTM'](eventLabel);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
        eventCategory: 'horse racing',
        eventAction: 'virtual horse racing',
        eventLabel: eventLabel
      }]);
    });
  });

  describe('goToLiveEvent', () => {

    it('should test goToLiveEvent when isVirtualHomePage is true', () => {
      const event = { classId: '123'} as ISportEvent;
      component.isVirtualHomePage = true;
      component.goToLiveEvent(event);
      expect(inspiredVirtualService.virtualsGTMEventTracker).toHaveBeenCalled();
      expect(router.navigateByUrl).toHaveBeenCalled();
    });

    it('should test goToLiveEvent', () => {
      component.sportName = 'horseracing';
      const event = { classId: '123'} as ISportEvent;
      component.goToLiveEvent(event);
      expect(router.navigateByUrl).toHaveBeenCalled();
    });

    it('should test goToLiveEvent when event is undefined', () => {
      component.sportName = 'horseracing';
      component.goToLiveEvent( undefined);
      expect(router.navigateByUrl).toHaveBeenCalledWith('virtual-sports/sports');
    });
  });
});

import { InplayHRHeaderComponent } from "./inplay-hr-header.component";

describe('InplayHRHeaderComponent', () => {
  let component: InplayHRHeaderComponent;
  let routingHelperService;
  let router;
  let eventService;
  let localeService;
  
  beforeEach(() => {

    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    eventService = {
      isLiveStreamAvailable: jasmine.createSpy('isLiveStreamAvailable').and.returnValue({
        liveStreamAvailable: true
      })
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('More')
    };
    component = new InplayHRHeaderComponent(
      routingHelperService,
      router,
      eventService,
      localeService
    );
  });
  describe('#ngOnInit', () => {
    it('should assign seeAllText', () => {
      localeService.getString = jasmine.createSpy('getString').and.returnValue('seeAllText');
      component.ngOnInit();
      expect(component['seeAllText']).toEqual('seeAllText');
    });
    it('should assign watchText', () => {
      localeService.getString = jasmine.createSpy('getString').and.returnValue('watchText');
      component.ngOnInit();
      expect(component['watchText']).toEqual('watchText');
    });
    it('should assign hrHeaderClasses', () => {
      spyOn(component,'setHeaderClass')
      component.ngOnInit();
      expect(component.setHeaderClass).toHaveBeenCalled();
    });
  });
  describe('#isStreamLabelShown', () => {
    it('should assign isLiveStreamAvailable', () => {
      const result = component.isStreamLabelShown(({ name: 'event' } as any));
      expect(eventService.isLiveStreamAvailable).toHaveBeenCalledWith({ name: 'event' });
      expect(result).toEqual(true);
    });
  });
  describe('#formEdpUrl', () => {
    it('should call routingHelperService.formEdpUrl', () => {
      component.formEdpUrl({ name: 'event' } as any);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ name: 'event' });
    });
    it('should form Edp url', () => {
      const result = component.formEdpUrl({ name: 'event' } as any);
      expect(result).toEqual('url');
    });
  });
  describe('trackEvent', () => {
    it('should call formEdpUrl and router.navigateByUrl', () => {
      spyOn(component, 'formEdpUrl')
      component.trackEvent({ name: 'event' } as any);
      expect(component.formEdpUrl).toHaveBeenCalledWith({ name: 'event' } as any);
      expect(router.navigateByUrl).toHaveBeenCalled();
    });
  });
  describe('setHeaderClass', () => {
    it('should return css classes', () => {
      component.showRaceDetails = true;
      const result = component.setHeaderClass();
      expect(result).toEqual({'header-details': !component.showRaceDetails,
      'header-race-details': component.showRaceDetails})
    });
  });
  describe('handleEvent', () => {
    it('should call stopPropagation', () => {
      const event: any = {
        stopPropagation: jasmine.createSpy()
      };
      component.handleEvent(event);
      expect(event.stopPropagation).toHaveBeenCalled();
    });
  });
});


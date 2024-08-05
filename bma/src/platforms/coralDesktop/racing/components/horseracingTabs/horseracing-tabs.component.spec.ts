import { DesktopHorseracingTabsComponent  } from './horseracing-tabs.component';

describe('DesktopHorseracingTabsComponent ', () => {
  let component;
  let cmsService;
  let router;
  let routingHelperService;
  let eventService, vEPService;

  beforeEach(() => {
    cmsService = {};
    router = {};
    routingHelperService = {};
    eventService = {};
    vEPService = {};
    
    component = new DesktopHorseracingTabsComponent(router, routingHelperService, eventService, cmsService, vEPService);
  });

  describe('onFeaturedEvents', () => {
    it('fetchCardId', () => {
      component.fetchCardId = jasmine.createSpy();
      component.onFeaturedEvents({output: 'fetchCardId', value: {id: '1'}});
      expect(component.fetchCardId).toHaveBeenCalled();
    });

    it('featuredLoaded', () => {
      component.handleFeaturedLoaded = jasmine.createSpy();
      component.onFeaturedEvents({output: 'featuredLoaded', value: 5});
      expect(component.handleFeaturedLoaded).toHaveBeenCalledWith(5);
    });
  });
});

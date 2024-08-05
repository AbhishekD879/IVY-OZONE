import { of as observableOf } from 'rxjs';

import { DesktopGreyhoundsTabsComponent } from '@ladbrokesDesktop/racing/components/greyhoundsTabs/greyhounds-tabs.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('DesktopGreyhoundsTabsComponent', () => {
  let component: DesktopGreyhoundsTabsComponent;
  let router;
  let filterService;
  let racingGaService;
  let routingHelperService;
  let eventService;
  let cmsService;
  let pubSubService;
  let gtm, vEPService,
  sessionStorageService, deviceService;

  const mockCmsConfig = {
    racing: true
  };

  beforeEach(() => {
    router = jasmine.createSpyObj('router', ['navigateByUrl']);
    filterService = jasmine.createSpyObj('filterService', ['orderBy', 'date']);
    racingGaService = jasmine.createSpyObj('racingGaService', ['trackModule', 'reset']);
    routingHelperService = jasmine.createSpyObj('routingHelperService', ['formSportUrl', 'formEdpUrl']);
    eventService = jasmine.createSpyObj('eventService', ['isAnyCashoutAvailable']);
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(mockCmsConfig))
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    sessionStorageService = {
      set: jasmine.createSpy('set')
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    deviceService= { isDesktop : true };
    vEPService = {
      targetTab: {subscribe : (cb) => cb()},
      lastBannerEnabled: {subscribe : (cb) => cb()},
      accorditionNumber: {subscribe : (cb) => cb()},
    };
    component = new DesktopGreyhoundsTabsComponent(
      router,
      filterService,
      racingGaService,
      routingHelperService,
      eventService,
      pubSubService,
      cmsService,
      gtm,
      sessionStorageService,
      deviceService, 
      vEPService
    );
  });

  it('should store CMS config', () => {
    expect(component.sysConfig).toEqual(mockCmsConfig);
  });

  it('should call ngOnInint', () => {
    component.isEventOverlay = true;
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }];
    
    const parentNgOnInit = spyOn(DesktopGreyhoundsTabsComponent.prototype['__proto__'], 'ngOnInit');
    component.ngOnInit();
    expect(parentNgOnInit).toHaveBeenCalled();
    expect(gtm.push).not.toHaveBeenCalled();
  });

  it('should filter time', () => {
    const time = 'Mon Feb 25 2019 16:00:44 GMT+0200';
    const format = 'mm-dd-YY';

    component.filteredTime(time, format);
    expect(filterService.date).toHaveBeenCalledWith(time, format);
  });

  it('should forma EDP url', () => {
    const eventEntity: any = {
      name: 'test event'
    };

    component.formEdpUrl(eventEntity);
    expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(eventEntity);
  });

  it('should filter events by type name and check for cashout availability', () => {
    const typeName = 'Ukraine Persha Liga - Kostolomy';
    const events: any = [{
      id: 1,
      typeName
    }, {
      id: 2,
      typeName: 'Championship'
    }, {
      id: 3,
      typeName
    }, {
      id: 4
    }];

    component.checkCacheOut(events, typeName);
    expect(eventService.isAnyCashoutAvailable).toHaveBeenCalledWith([events[0], events[2]], [{ cashoutAvail: 'Y' }]);
  });
  
  it('should call overlayContentHandler', () => {
    const eventEntity: any = {
      name: 'test event'
    };
    component.filter = 'uk-races';

    component.overlayContentHandler(eventEntity);
    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('should call toggleByMeetingAccordion expand', () => {
    component.isEventOverlay = true;
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }];
    component.toggleByMeetingAccordion(1,'UK races' );
    expect(gtm.push).toHaveBeenCalled();
  });

  it('should call toggleByMeetingAccordion collapse', () => {
    component.isEventOverlay = true;
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }];
    component.toggleByMeetingAccordion(0,'UK races' );
    expect(gtm.push).toHaveBeenCalled();
  });

  it('should call toggleByMeetingAccordion events tab', () => {
    component.isEventOverlay = true;
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }];
    component.toggleByMeetingAccordion(0,'Events' );
    expect(gtm.push).toHaveBeenCalled();
  });

  it('should call toggleByMeetingAccordion isEventOverlay false', () => {
    component.isEventOverlay = false;
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }];
    component.toggleByMeetingAccordion(0,'UK races' );
    expect(gtm.push).toHaveBeenCalled();
  });

  it('should get changes listened', () => {
    component.isEventOverlay = false;
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }];
    component.display = 'future';
    component.filterInitData = jasmine.createSpy('filterInitData');
    component.toggleByMeetingAccordion = jasmine.createSpy('toggleByMeetingAccordion');
    component.ngOnChanges({
      filter: { currentValue: 'by-meeting'},
      viewByFilters: ['someFilter']
    } as any);

    expect(component.isExpanded).toBeTrue();
    expect(component.filterInitData).toHaveBeenCalled();
    expect(component.toggleByMeetingAccordion).toHaveBeenCalled();
  });
});

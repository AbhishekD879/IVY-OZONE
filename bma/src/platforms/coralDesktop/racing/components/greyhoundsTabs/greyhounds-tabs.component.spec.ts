import { of as observableOf } from 'rxjs';
import { DesktopGreyhoundsTabsComponent } from '@coralDesktop/racing/components/greyhoundsTabs/greyhounds-tabs.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('DesktopGreyhoundsTabsComponent', () => {
  let component: DesktopGreyhoundsTabsComponent;
  let router;
  let filterService;
  let racingGaService;
  let routingHelperService;
  let eventService;
  let cmsService;
  let pubSubService, gtm, vEPService;
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
    gtm = {
      push: jasmine.createSpy('push')
    };
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
      vEPService
    );
  });

  it('should store CMS config', () => {
    expect(component.sysConfig).toEqual(mockCmsConfig);
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

  it('#showTodayTomorrowNoEvents should indicate when display no events label', () => {
    component.racing = {} as any;
    component.responseError = true;
    expect(component.showTodayTomorrowNoEvents).toBeFalsy();

    component.responseError = false;
    component.filter = 'next-races';
    expect(component.showTodayTomorrowNoEvents).toBeFalsy();

    component.filter = 'by-meeting';
    component.racing.groupedRacing = [];
    expect(component.showTodayTomorrowNoEvents).toBeTruthy();

    component.filter = 'by-meeting';
    component.racing.groupedRacing = [{} as any];
    expect(component.showTodayTomorrowNoEvents).toBeFalsy();

    component.filter = 'by-time';
    component.racing.events = [];
    expect(component.showTodayTomorrowNoEvents).toBeTruthy();

    component.filter = 'by-time';
    component.racing.events = [{} as any];
    expect(component.showTodayTomorrowNoEvents).toBeFalsy();
  });

});

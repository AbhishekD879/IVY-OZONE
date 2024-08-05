import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { HorseracingTabsComponent } from '@racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';

import { ISystemConfig } from '@core/services/cms/models/system-config';

describe('HorseTabsComponent', () => {
  let component: HorseracingTabsComponent;

  let router, routingHelperService, eventService, cmsService, vEPService;

  const sysConfig: ISystemConfig = {
    InternationalTotePool: {
      Enable_International_Totepools: true
    },
    NextRacesToggle: {
      nextRacesComponentEnabled: true,
      nextRacesTabEnabled: true
    },
    VirtualSports: {
      'virtual-horse-racing': true
    },
    defaultAntepostTab: {
    }
  };

  beforeEach(() => {
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      url: 'url1'
    };

    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl').and.returnValue(observableOf('url'))
    };
    eventService = {
      isAnyCashoutAvailable: jasmine.createSpy()
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(sysConfig))
    };
    vEPService = {
      targetTab: {subscribe : (cb) => cb()},
      lastBannerEnabled: {subscribe : (cb) => cb()},
      accorditionNumber: {subscribe : (cb) => cb()},
    };

    component = new HorseracingTabsComponent(router, routingHelperService, eventService, cmsService, vEPService);
  });

  it('should create HorseracingTabsComponent instance', () => {
    expect(component).toBeTruthy();
  });

  describe('@ngOnInit', () => {
    it('should isExtraPlaceAvailable = false and offersAndFeaturedRacesTitle = undefined', () => {
      const sysConfigModified = Object.assign({}, sysConfig);
      sysConfigModified['featuredRaces'] = {
        enabled: false,
        title: 'featuredRaces'
      };
      component.cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig')
        .and.returnValue(observableOf(sysConfigModified));

      component.ngOnInit();

      expect(component['isExtraPlaceAvailable']).toBeFalsy();
      expect(component['offersAndFeaturedRacesTitle']).toBeUndefined();
    });

    it('should isExtraPlaceAvailable = true and offersAndFeaturedRacesTitle = "featuredRaces"', () => {
      const sysConfigModified = Object.assign({}, sysConfig);
      sysConfigModified['featuredRaces'] = {
        enabled: true,
        title: 'featuredRaces'
      };
      component.cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig')
        .and.returnValue(observableOf(sysConfigModified));

      component.ngOnInit();

      expect(component['isExtraPlaceAvailable']).toBeTruthy();
      expect(component['offersAndFeaturedRacesTitle']).toEqual(sysConfigModified.featuredRaces.title);
    });

    it('ngOnInit', () => {
      component.ngOnInit();

      component.switchers.forEach(switcher => {
        switcher.onClick();
      });

      expect(routingHelperService.formSportUrl).toHaveBeenCalledTimes(2);
    });

    it('defaultAntepostTab should be "SomeTab"', () => {
      sysConfig.defaultAntepostTab.tabName = 'SomeTab';
      component.ngOnInit();
      expect(component.defaultAntepostTab).toBe('SomeTab');
    });

    it('defaultAntepostTab should be undefined, if not configured in cms', () => {
      sysConfig.defaultAntepostTab = {};
      component.ngOnInit();
      expect(component.defaultAntepostTab).toBeUndefined();
    });

    it('nextRacesComponentEnabled should be true by default', () => {
      component.ngOnInit();
      expect(component.nextRacesComponentEnabled).toBeTruthy();
    });

    it('nextRacesComponentEnabled should be false, its turned off in cms', () => {
      sysConfig.NextRacesToggle.nextRacesComponentEnabled = false;
      component.ngOnInit();
      expect(component.nextRacesComponentEnabled).toBeFalsy();
    });
   });

  it('#trackByFlag, should return a value', () => {
    const value = {
      flag: 'flag'
    };

    expect(component.trackByFlag(1, value)).toEqual(value.flag);
  });

  describe('handleFeaturedLoaded', () => {
    it('should set handleFeaturedLoaded prop to true', () => {
      expect(component.featuredLoaded).toBeFalsy();
      component.handleFeaturedLoaded();
      expect(component.featuredLoaded).toBeTruthy();
    });
  });

  describe('handleNextRacesLoaded', () => {
    it('should set nextRacesLoaded prop to true', () => {
      expect(component.nextRacesLoaded).toBeFalsy();
      component.handleNextRacesLoaded();
      expect(component.nextRacesLoaded).toBeTruthy();
    });
  });

  describe('displayNextRaces', () => {
    it('should return false in case of error', () => {
      component['responseError'] = 'error' as any;
      expect(component.displayNextRaces).toBeFalsy();
    });

    it('should return false in case if tab is not featured', () => {
      component['responseError'] = undefined as any;
      component['display'] = 'home-tab' as any;
      expect(component.displayNextRaces).toBeFalsy();
    });

    it('should return false in case if feat is disabled', () => {
      component['responseError'] = undefined as any;
      component['display'] = 'featured' as any;
      component['nextRacesComponentEnabled'] = false;
      expect(component.displayNextRaces).toBeFalsy();
    });

    it('should return false in case if no error and tab is featured and feat is enabled', () => {
      component['responseError'] = undefined as any;
      component['display'] = 'featured' as any;
      component['nextRacesComponentEnabled'] = true;
      expect(component.displayNextRaces).toBeTruthy();
    });
  });

  it('@checkCacheOut, should check filter and isAnyCashoutAvailable', () => {
    const events = [{
        typeName: 'typeName'
      }, {
        typeName: ''
      }] as any,
      typeName = 'typeName',
      cashoutParam = [{ cashoutAvail: 'Y' }];

    component.checkCacheOut(events, typeName);

    expect(component['eventService'].isAnyCashoutAvailable).toHaveBeenCalledWith([events[0]], cashoutParam);
  });

  describe('#goToFilter', () => {
    beforeEach(() => {
      component.racingPath = 'racingPath';
      component.display = 'display';
    });
    it('should call goToFilter', fakeAsync(() => {
      component.goToFilter('filter');
      tick(100);

      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
      expect(routingHelperService.formSportUrl).toHaveBeenCalledWith('racingPath', 'display/filter');
    }));

    it('should call goToFilter when url equal with router.url', fakeAsync(() => {
      routingHelperService.formSportUrl.and.returnValue(observableOf('url1'));
      component.goToFilter('filter');
      tick(1000);

      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(routingHelperService.formSportUrl).toHaveBeenCalledWith('racingPath', 'display/filter');
    }));
  });

  describe('@showNoEvents', () => {
    const display = 'yourcall';
    let responseError, racing;

    beforeEach(() => {
      responseError = undefined;
      racing = [];
    });

    it('should return true - has no events', () => {
      expect(component.showNoEvents(display, responseError, racing)).toBeTruthy();
    });

    it('should return true - has events', () => {
      racing = {
        events: [],
        length: 1
      };

      expect(component.showNoEvents(display, responseError, racing)).toBeTruthy();
    });

    it('should return false', () => {
        responseError = {};

      expect(component.showNoEvents(display, responseError, racing)).toBeFalsy();
    });
  });

  describe('onFeaturedEvents', () => {
    it('nextRacesLoaded', () => {
      component.onFeaturedEvents({output: 'nextRacesLoaded', value: {id: '1'}});
      expect(component.nextRacesLoaded).toBe(true);
    });

    it('featuredLoaded', () => {
      const param = {output: 'featuredLoaded', value: {id: '1'}} as any;
      component.onFeaturedEvents(param);
      expect(component.featuredLoaded).toBe(true);
      expect(component.racing).toEqual({id: '1'});
    });
  });
});

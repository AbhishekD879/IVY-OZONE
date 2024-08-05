import { Observable, of as observableOf, Subject } from 'rxjs';

import environment from '@environment/oxygenEnvConfig';
import { MaintenanceService } from './maintenance.service';
import { NavigationEnd, NavigationStart } from '@angular/router';

describe('MaintenanceService', () => {
  let service: MaintenanceService;

  let windowRefService;
  let cmsService;
  let http;
  let pubSubService;
  let router;

  const endDate: Date = new Date();
  endDate.setDate(endDate.getDate() + 1);
  const startDate: Date = new Date();
  startDate.setDate(endDate.getDate() - 1);
  const maintenancePath = '/under-maintenance';
  const maintenancePage = {
    validityPeriodEnd: endDate.toString(),
    validityPeriodStart: startDate.toString()
  };

  beforeEach(() => {
    windowRefService = {
      nativeWindow: jasmine.createSpyObj(['setTimeout'])
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({maintenancePage: {enabled: true}})),
      getMaintenancePage: jasmine.createSpy('getMaintenancePage').and.returnValue(observableOf([maintenancePage])),
    };
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf({
        body: {
          SSResponse: {
            children: [{
              healthCheck: {
                status: 'OK'
              }
            }]
          }
        }
      }))
    };
    router = {
      events: new Subject(),
      url: '/sport/football',
      navigate: jasmine.createSpy()
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        MAINTENANCE_PAGE_DATA_CHANGED: 'MAINTENANCE_PAGE_DATA_CHANGED'
      }
    };

    service = new MaintenanceService(
      windowRefService,
      cmsService,
      pubSubService,
      http,
      router
    );
  });

  describe('constructor', () => {

    it('should be defined', () => {
      expect(service).toBeDefined();
    });

    describe('firstNavigationStartsCheck', () => {
      let isCmsMaintenanceEnabledSpy;

      beforeEach(() => {
        isCmsMaintenanceEnabledSpy = spyOn(service, 'isCmsMaintenanceEnabled').and.returnValue(observableOf(true));
        spyOn(service, 'runMaintenanceCheck');
      });

      it('should subscribe and wait for routing events', () => {
        expect(isCmsMaintenanceEnabledSpy).not.toHaveBeenCalled();
        expect(service.runMaintenanceCheck).not.toHaveBeenCalled();
      });

      it('should filter non-end events', () => {
        router.events.next(new NavigationStart(1, ''));

        expect(service.runMaintenanceCheck).not.toHaveBeenCalled();
      });

      it('should run maintenance check (maintenance page)', () => {
        router.url = maintenancePath;
        router.events.next(new NavigationEnd(1, '', ''));

        expect(isCmsMaintenanceEnabledSpy).not.toHaveBeenCalled();
        expect(service.runMaintenanceCheck).toHaveBeenCalledWith(false);
      });

      it('should run maintenance check (edp page, maintenance OFF)', () => {
        isCmsMaintenanceEnabledSpy.and.returnValue(observableOf(false));
        router.events.next(new NavigationEnd(1, '', ''));

        expect(isCmsMaintenanceEnabledSpy).toHaveBeenCalled();
        expect(service.runMaintenanceCheck).toHaveBeenCalledWith(false);
      });

      it('should run maintenance check (edp page, maintenance ON)', () => {
        router.events.next(new NavigationEnd(1, '', ''));

        expect(isCmsMaintenanceEnabledSpy).toHaveBeenCalled();
        expect(service.runMaintenanceCheck).toHaveBeenCalledWith(true);
      });
    });
  });

  describe('isCmsMaintenanceEnabled', () => {

    it('should request cms service with no cache', () => {
      const request = service.isCmsMaintenanceEnabled();

      expect(request).toEqual(jasmine.any(Observable));

      request.subscribe(() => {
        expect(cmsService.getSystemConfig).toHaveBeenCalledWith();
      });
    });

    it(`should check that maintenance is set as 'enabled'`, () => {
      service.isCmsMaintenanceEnabled().subscribe(enabled => {
        expect(enabled).toBe(true);
      });

      cmsService.getSystemConfig.and.returnValue(observableOf({maintenancePage: {enabled: false}}));
      service.isCmsMaintenanceEnabled().subscribe(enabled => {
        expect(enabled).toBe(false);
      });

      cmsService.getSystemConfig.and.returnValue(observableOf({maintenancePage: {}}));
      service.isCmsMaintenanceEnabled().subscribe(enabled => {
        expect(enabled).toBe(false);
      });

      cmsService.getSystemConfig.and.returnValue(observableOf({}));
      service.isCmsMaintenanceEnabled().subscribe(enabled => {
        expect(enabled).toBe(false);
      });
    });
  });

  describe('runMaintenanceCheck', () => {

    beforeEach(() => {
      expect(service['isCmsDataActual']).toBe(true);

      spyOn(service, 'checkForMaintenance').and.returnValue(observableOf({} as any));
      spyOn(service, 'runMaintenanceStatusPoll');
    });

    it('should call maintenance check now and run poll', () => {
      service.runMaintenanceCheck(true);

      expect(service.checkForMaintenance).toHaveBeenCalled();
      expect(service.runMaintenanceStatusPoll).toHaveBeenCalled();
    });

    it('should call maintenance via run poll only', () => {
      service.runMaintenanceCheck(false);

      expect(service.checkForMaintenance).not.toHaveBeenCalled();
      expect(service.runMaintenanceStatusPoll).toHaveBeenCalled();
    });

    it('should mark cms data as not actual', () => {
      service.runMaintenanceCheck(true);

      expect(service['isCmsDataActual']).toBe(false);
    });
  });

  describe('runMaintenanceStatusPoll', () => {

    it('should set timeout with given delay', () => {
      service.runMaintenanceStatusPoll();

      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 60000);
    });

    it('should call maintenance check and run poll again', () => {
      let breakLoop = false;
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => {
        if (!breakLoop && cb) {
          breakLoop = true;
          cb();
        }
      });
      spyOn(service, 'checkForMaintenance').and.returnValue(observableOf({} as any));
      spyOn(service, 'runMaintenanceStatusPoll').and.callThrough();

      service.runMaintenanceStatusPoll();

      expect(service.checkForMaintenance).toHaveBeenCalled();
      expect(service.runMaintenanceStatusPoll).toHaveBeenCalled();
    });
  });

  describe('checkForMaintenance', () => {
    let getActiveMaintenancePageSpy;

    beforeEach(() => {
      getActiveMaintenancePageSpy = spyOn(service, 'getActiveMaintenancePage').and.returnValue(observableOf({} as any));
    });

    it('should redirect to maintenance', () => {
      service.checkForMaintenance().subscribe(() => {
        expect(getActiveMaintenancePageSpy).toHaveBeenCalled();
        expect(router.navigate).toHaveBeenCalledTimes(1);
        expect(router.navigate).toHaveBeenCalledWith([maintenancePath]);
      });
    });

    it('should make no actions (active)', () => {
      router.url = maintenancePath;

      service.checkForMaintenance().subscribe(() => {
        expect(getActiveMaintenancePageSpy).toHaveBeenCalled();
        expect(router.navigate).not.toHaveBeenCalled();
      });
    });

    it('should make no actions (inactive)', () => {
      getActiveMaintenancePageSpy.and.returnValue(observableOf(null));

      service.checkForMaintenance().subscribe(() => {
        expect(getActiveMaintenancePageSpy).toHaveBeenCalled();
        expect(router.navigate).not.toHaveBeenCalled();
      });
    });

    it('should redirect to home', () => {
      router.url = maintenancePath;
      getActiveMaintenancePageSpy.and.returnValue(observableOf(null));

      service.checkForMaintenance().subscribe(() => {
        expect(getActiveMaintenancePageSpy).toHaveBeenCalled();
        expect(router.navigate).toHaveBeenCalledTimes(1);
        expect(router.navigate).toHaveBeenCalledWith(['/']);
      });
    });

    it('should call reload method', () => {
      router.url = maintenancePath;
      service.reload = jasmine.createSpy('reload');
      service.checkForMaintenance().subscribe(() => {
        expect(service.reload).toHaveBeenCalled();
      });
    });
  });

  describe('#reload', () => {
    beforeEach(() => {
    });
    it('should reload page if maintenance is active but config was changed', () => {
      const activeMaintenancePage = <any>{ url: 'url' };
      service['activeMaintenancePage'] = <any>{ url: 'url1' };

      service.reload(activeMaintenancePage);
      expect(service['activeMaintenancePage']).toEqual(activeMaintenancePage);
      expect(pubSubService.publish).toHaveBeenCalledWith('MAINTENANCE_PAGE_DATA_CHANGED', activeMaintenancePage);
    });
    it('should not reload page if maintenance is active and config was not changed', () => {
      const activeMaintenancePage = <any>{ url: 'url' };
      service['activeMaintenancePage'] = <any>{ url: 'url' };

      service.reload(activeMaintenancePage);
      expect(service['activeMaintenancePage']).toEqual(activeMaintenancePage);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  describe('getMaintenanceIfActive', () => {
    let isCmsMaintenanceEnabledSpy;
    let getActiveMaintenancePageSpy;

    beforeEach(() => {
      isCmsMaintenanceEnabledSpy = spyOn(service, 'isCmsMaintenanceEnabled').and.returnValue(observableOf(true));
      getActiveMaintenancePageSpy = spyOn(service, 'getActiveMaintenancePage').and.returnValue(observableOf({} as any));
    });

    it('should return page', () => {
      service.getMaintenanceIfActive().subscribe((page: any) => {
        expect(isCmsMaintenanceEnabledSpy).toHaveBeenCalled();
        expect(getActiveMaintenancePageSpy).toHaveBeenCalled();
        expect(page).toEqual({});
      });
    });

    it('should still return page (cms data says not enabled, but is not actual)', () => {
      isCmsMaintenanceEnabledSpy.and.returnValue(observableOf(false));
      service['isCmsDataActual'] = false;

      service.getMaintenanceIfActive().subscribe((page: any) => {
        expect(isCmsMaintenanceEnabledSpy).toHaveBeenCalled();
        expect(getActiveMaintenancePageSpy).toHaveBeenCalled();
        expect(page).toEqual({});
      });
    });

    it('should return null (no active page)', () => {
      getActiveMaintenancePageSpy.and.returnValue(observableOf(null));

      service.getMaintenanceIfActive().subscribe((page: any) => {
        expect(isCmsMaintenanceEnabledSpy).toHaveBeenCalled();
        expect(getActiveMaintenancePageSpy).toHaveBeenCalled();
        expect(page).toBe(null);
      });
    });

    it('should return null (actual cms data says not enabled)', () => {
      isCmsMaintenanceEnabledSpy.and.returnValue(observableOf(false));

      service.getMaintenanceIfActive().subscribe((page: any) => {
        expect(isCmsMaintenanceEnabledSpy).toHaveBeenCalled();
        expect(getActiveMaintenancePageSpy).not.toHaveBeenCalled();
        expect(page).toBe(null);
      });
    });
  });

  describe('getActiveMaintenancePage', () => {

    it('should use cache', () => {
      service['maintenancePageData$'] = observableOf({} as any);

      service.getActiveMaintenancePage().subscribe((page: any) => {
        expect(page).toEqual({});
        expect(cmsService.getMaintenancePage).not.toHaveBeenCalled();
      });
    });

    it('should create cms stream cache', () => {
      expect(service['maintenancePageData$']).not.toBeDefined();

      service.getActiveMaintenancePage();

      expect(cmsService.getMaintenancePage).toHaveBeenCalled();
      expect(service['maintenancePageData$']).toEqual(jasmine.any(Observable));
    });

    it('should clean stream cache with timeout', () => {
      // @ts-ignore my freak solution
      // eslint-disable-next-line
      windowRefService.nativeWindow.setTimeout.run = function me() { me.cb && me.cb(); };
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => {
        cb && (windowRefService.nativeWindow.setTimeout.run.cb = cb);
      });

      service.getActiveMaintenancePage().subscribe(() => {
        expect(service['maintenancePageData$']).toEqual(jasmine.any(Observable));
        expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 5000);

        windowRefService.nativeWindow.setTimeout.run();
        expect(service['maintenancePageData$']).toBeDefined();
        expect(service['maintenancePageData$']).toBeFalsy();
      });
    });

    it('should request cms and return active page data', () => {
      service.getActiveMaintenancePage().subscribe((page: any) => {
        expect(cmsService.getMaintenancePage).toHaveBeenCalled();
        expect(page).toEqual(maintenancePage);
      });
    });

    it('should return null if no pages in response', () => {
      cmsService.getMaintenancePage.and.returnValue(observableOf([]));

      service.getActiveMaintenancePage().subscribe((page: any) => {
        expect(cmsService.getMaintenancePage).toHaveBeenCalled();
        expect(page).toBe(null);
      });
    });

    it('should return null if end date of first page is in past', () => {
      cmsService.getMaintenancePage.and.returnValue(observableOf([
        {
          validityPeriodEnd: startDate.toString(),
          validityPeriodStart: startDate.toString()
        }
      ]));

      service.getActiveMaintenancePage().subscribe((page: any) => {
        expect(cmsService.getMaintenancePage).toHaveBeenCalled();
        expect(page).toBe(null);
      });
    });

    it('should return null if start date of first page is in future', () => {
      cmsService.getMaintenancePage.and.returnValue(observableOf([
        {
          validityPeriodEnd: endDate.toString(),
          validityPeriodStart: endDate.toString()
        }
      ]));

      service.getActiveMaintenancePage().subscribe((page: any) => {
        expect(cmsService.getMaintenancePage).toHaveBeenCalled();
        expect(page).toBe(null);
      });
    });
  });

  describe('siteServerHealthCheck', () => {
    it('forceRequest: false', (done) => {
      service.siteServerHealthCheck().subscribe((res) => {
        expect(res).toEqual('No HealthCheck for non maintenance page');
        done();
      });
    });
    it('forceRequest: true', (done) => {
      service.siteServerHealthCheck(true).subscribe((res) => {
        expect(res).toEqual('OK');
        expect(http.get).toHaveBeenCalledTimes(1);
        expect(http.get).toHaveBeenCalledWith(`${environment.SITESERVER_COMMON_ENDPOINT}/HealthCheck`, jasmine.anything());
        done();
      });
    });
  });
});

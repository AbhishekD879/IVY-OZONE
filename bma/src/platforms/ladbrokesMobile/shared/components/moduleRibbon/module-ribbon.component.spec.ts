import { LadbrokesModuleRibbonComponent } from './module-ribbon.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

describe('LadbrokesModuleRibbonComponent', () => {
  let moduleRibbonComponent,
    location,
    ribbonService,
    user,
    pubSubService,
    router,
    sessionService,
    cmsService,
    germanSupportService,
    sessionStorageService,device, bonusSuppressionService,segmentEventManagerService;

  const navPoints = [{
    homeTabs: ['/home/eventhub/2', '/home/featured']
  }, {
    homeTabs: ['/home/eventhub/2', '/home/other']
  }, {
    homeTabs: []
  }] as any;

  beforeEach(() => {
    location = {
      isCurrentPathEqualTo: jasmine.createSpy('isCurrentPathEqualTo'),
      path: jasmine.createSpy('path')
    };
    ribbonService = {
      moduleList: [{ directiveName: 'NextRaces' }, { directiveName: 'Enhanced Multiples' }],
      removeTab: jasmine.createSpy('removeTab'),
      isPrivateMarketsTab: jasmine.createSpy('isPrivateMarketsTab'),
      getPrivateMarketTab: jasmine.createSpy('getPrivateMarketTab').and.returnValue(of([
        { directiveName: 'NextRaces' }, { directiveName: 'Enhanced Multiples' }
      ]))
    };
    user = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    };
    pubSubService = {
      API: {
        SESSION_LOGOUT: 'SESSION_LOGOUT',
        HIDE_PRIVATE_MARKETS_TAB: 'HIDE_PRIVATE_MARKETS_TAB'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy()
    };
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue({
          unsubscribe: jasmine.createSpy()
        })
      },
      navigate: jasmine.createSpy('navigate'),
      url: '/'
    };
    sessionService = {
      whenUserSession: jasmine.createSpy('whenUserSession')
    };

    cmsService = {
      getNavigationPoints: jasmine.createSpy('getNavigationPoints').and.returnValue(of(navPoints)),
      getFirstBetDetails: jasmine.createSpy('getFirstBetDetails').and.returnValue(of({
        brand:'bma',
        months:1
      })),
      getCMSRGYconfigData: jasmine.createSpy('getCMSRGYconfigData').and.returnValue(of({}))
    };

    germanSupportService = {
      toggleItemsList: jasmine.createSpy('toggleItemsList')
    };

    sessionStorageService={
      get: jasmine.createSpy('get').and.callFake(
        n => {
          if(n === 'firstBetTutorial') { return {user:'test'}} 
          else if(n === 'initialTabLoaded')  {return {id:1}}
          else if(n === 'firstBetTutorialAvailable'){ return false}
      }),
      remove: jasmine.createSpy('remove'),
      set: jasmine.createSpy('set')
    }
    device = { requestPlatform : 'mobile'};
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    };
    moduleRibbonComponent = new LadbrokesModuleRibbonComponent(
      location, ribbonService, user, pubSubService, router, sessionService, cmsService, germanSupportService
      ,device,sessionStorageService, bonusSuppressionService,segmentEventManagerService);
    moduleRibbonComponent.moduleRibbon = null;

  });

  describe('@ngOnInit', () => {
    it('should filter moduleList items and remove next races for not logged in user', fakeAsync(() => {
      cmsService.getNavigationPoints.and.returnValue(of([]));
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent['filterModulesBasedOnRgyellow'] = jasmine.createSpy('filterModulesBasedOnRgyellow');
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
      sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));
      moduleRibbonComponent.ngOnInit();
      moduleRibbonComponent['filterModulesBasedOnRgyellow']();
      tick();

      expect(germanSupportService.toggleItemsList)
        .toHaveBeenCalledWith([{ directiveName: 'NextRaces' }, { directiveName: 'Enhanced Multiples' }], 'filterNextRaces');
    }));

    it('ngOnInit success', fakeAsync(() => {
      moduleRibbonComponent.user = {
        status: true,
        sportBalance:2,
        username: 'test1'
      };
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
      location.isCurrentPathEqualTo.and.callFake(param => param === '/home/next-races');
      moduleRibbonComponent['filterModulesBasedOnRgyellow'] = jasmine.createSpy('filterModulesBasedOnRgyellow');
      ribbonService.isPrivateMarketsTab.and.returnValue(false);

      sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));

      moduleRibbonComponent.ngOnInit();
      tick();

      expect(germanSupportService.toggleItemsList)
        .toHaveBeenCalledWith([{ directiveName: 'NextRaces' }, { directiveName: 'Enhanced Multiples' }], 'filterNextRaces');
    }));

    it('should NOT filter moduleList items and remove next races when redirect to Private Markets page is needed', fakeAsync(() => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
      location.isCurrentPathEqualTo.and.callFake(param => param === '/');
      ribbonService.isPrivateMarketsTab.and.returnValue(true);

      sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));

      moduleRibbonComponent.ngOnInit();
      tick();

      expect(germanSupportService.toggleItemsList).not
        .toHaveBeenCalledWith([{ directiveName: 'NextRaces' }, { directiveName: 'Enhanced Multiples' }], 'filterNextRaces');
    }));

    it('should NOT filter moduleList items and remove next races when redirect to Home page is needed', fakeAsync(() => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent.location.path = jasmine.createSpy('path').and.returnValue('/');
      location.isCurrentPathEqualTo.and.callFake(param => param === '/home/private-markets');
      ribbonService.isPrivateMarketsTab.and.returnValue(false);

      sessionService.whenUserSession = jasmine.createSpy('sessionService.whenSession').and.returnValue(of({}));

      moduleRibbonComponent.ngOnInit();
      tick();

      expect(germanSupportService.toggleItemsList).not
        .toHaveBeenCalledWith([{ directiveName: 'NextRaces' }, { directiveName: 'Enhanced Multiples' }], 'filterNextRaces');
    }));
  });

  describe('addPrivateMarketTab', () => {
    it('should set privateMarketTabCreated to true, call ribbonService.getPrivateMarketTab, fill moduleList and call setLocation',
    fakeAsync(() => {
      moduleRibbonComponent['privateMarketTabCreated'] = false;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['setLocation'] = jasmine.createSpy('setLocation');
      moduleRibbonComponent['filterNextRaces'] = jasmine.createSpy('filterNextRaces');
      moduleRibbonComponent['isRedirectNeeded'] = jasmine.createSpy('isRedirectNeeded').and.returnValue(false);
      ribbonService.getPrivateMarketTab.and.returnValue(of([1]));
      moduleRibbonComponent.user.status = true;

      moduleRibbonComponent['addPrivateMarketTab']();
      tick();

      expect(moduleRibbonComponent['privateMarketTabCreated']).toBe(true);
      expect(moduleRibbonComponent['setLocation']).toHaveBeenCalled();
      expect(moduleRibbonComponent['filterNextRaces']).toHaveBeenCalled();
      expect(moduleRibbonComponent.moduleList).toEqual([1]);
    }));

    it('should set privateMarketTabCreated to false when getPrivateMarketTab promise fails', fakeAsync(() => {
      moduleRibbonComponent['privateMarketTabCreated'] = false;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['setLocation'] = jasmine.createSpy('setLocation');
      ribbonService.getPrivateMarketTab.and.returnValue(throwError(''));
      moduleRibbonComponent.user.status = true;

      moduleRibbonComponent['addPrivateMarketTab']();
      tick();

      expect(moduleRibbonComponent['privateMarketTabCreated']).toBe(false);
      expect(moduleRibbonComponent['setLocation']).not.toHaveBeenCalled();
      expect(moduleRibbonComponent.moduleList).toEqual(undefined);
    }));

    it('should NOT call filterNextRaces', fakeAsync(() => {
      moduleRibbonComponent['privateMarketTabCreated'] = false;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['setLocation'] = jasmine.createSpy('setLocation');
      moduleRibbonComponent['isRedirectNeeded'] = jasmine.createSpy('isRedirectNeeded').and.returnValue(true);
      moduleRibbonComponent['filterNextRaces'] = jasmine.createSpy('filterNextRaces');
      ribbonService.getPrivateMarketTab.and.returnValue(of([1]));
      moduleRibbonComponent.user.status = true;

      moduleRibbonComponent['addPrivateMarketTab']();
      tick();

      expect(moduleRibbonComponent['privateMarketTabCreated']).toBe(true);
      expect(moduleRibbonComponent['setLocation']).toHaveBeenCalled();
      expect(moduleRibbonComponent['filterNextRaces']).not.toHaveBeenCalled();
      expect(moduleRibbonComponent.moduleList).toEqual([1]);
    }));

    it('should NOT go into if statement body if user is not defined', () => {
      moduleRibbonComponent.user = null;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['privateMarketTabCreated'] = false;

      moduleRibbonComponent['addPrivateMarketTab']();

      expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
    });

    it('should NOT go into if statement body if isOnPrivateMarketTab returns true', () => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(true);
      moduleRibbonComponent['privateMarketTabCreated'] = false;

      moduleRibbonComponent['addPrivateMarketTab']();

      expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
    });

    it('should NOT go into if statement body if privateMarketTabCreated is set to true', () => {
      moduleRibbonComponent.user.status = true;
      moduleRibbonComponent['isOnPrivateMarketTab'] = jasmine.createSpy('isOnPrivateMarketTab').and.returnValue(false);
      moduleRibbonComponent['privateMarketTabCreated'] = true;

      moduleRibbonComponent['addPrivateMarketTab']();

      expect(ribbonService.getPrivateMarketTab).not.toHaveBeenCalled();
    });
  });
});

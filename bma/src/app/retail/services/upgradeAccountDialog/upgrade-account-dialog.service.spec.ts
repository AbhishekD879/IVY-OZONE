import { of as observableOf, Observable } from 'rxjs';
import { fakeAsync } from '@angular/core/testing';
import { UpgradeAccountDialogService } from '@platform/retail/services/upgradeAccountDialog/upgrade-account-dialog.service';

describe('UpgradeAccountDialogService', () => {
  let service: UpgradeAccountDialogService,
    storageService,
    dialogService,
    userService,
    gtmService,
    router,
    routingStateService,
    dynamicComponentLoader,
    deviceService,
    cmsService;

  beforeEach(() => {
    storageService = {
      setCookie: jasmine.createSpy('setCookie'),
      getCookie: jasmine.createSpy('getCookie').and.returnValue('true')
    };

    dialogService = {
      params: {},
      ids: { upgradeAccountDialog: 'upgradeAccountDialog' },
      openDialog: jasmine.createSpy('openDialog').and.callFake((a, b, c, params, e) => {
        params.upgrade();
        params.cancel();
      }),
      closeDialog: jasmine.createSpy('closeDialog'),
      closeDialogs: jasmine.createSpy('closeDialogs')
    } as any;

    userService = {
      isInShopUser: jasmine.createSpy('isInShopUser'),
      isRouletteJourney: jasmine.createSpy('isRouletteJourney').and.returnValue(false)
    };

    gtmService = {
      push: jasmine.createSpy('push'),
      formatErrorMessage: jasmine.createSpy().and.returnValue('')
    } as any;

    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe')
      },
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    } as any;

    routingStateService = jasmine.createSpyObj('RoutingStateService', ['getPreviousSegment']);

    dynamicComponentLoader = {
      loadModule: jasmine.createSpy('loadModule').and.returnValue(Promise.resolve({
        componentFactoryResolver: {
          resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(jasmine.anything())
        }
      }))
    } as any;

    deviceService = {
      isMobile: true
    } as any;

    cmsService = jasmine.createSpyObj('CmsService', ['getSystemConfig']);

    service = new UpgradeAccountDialogService(
      dialogService,
      gtmService,
      storageService,
      userService,
      router,
      routingStateService,
      dynamicComponentLoader,
      deviceService,
      cmsService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#showUpgradeDialog', () => {
    let trackEventData, dialogUpgradeAction, dialogCancelAction, observer;

    beforeEach(() => {
      trackEventData = service['trackEventData'];
      dialogUpgradeAction = service['dialogUpgradeAction'];
      dialogCancelAction = service['dialogCancelAction'];
      observer = { next: jasmine.createSpy(), complete: jasmine.createSpy() };
    });

    it('call showUpgradeDialog for in-show user without native', fakeAsync(() => {
      service['isAvailableForUser'] = jasmine.createSpy('isAvailableForUser').and.returnValue(observableOf(true));
      const result = service.showUpgradeDialog(false);
      result.subscribe();
      expect(service['isAvailableForUser']).toHaveBeenCalled();
      expect(result).toEqual(jasmine.any(Observable));
    }));

    it('showUpgradeDialog and isAvailableForUser returns false', () => {
      const errorHandler = jasmine.createSpy('errorHandler');
      const successHandler = jasmine.createSpy('successHandler');
      const completeHandler = jasmine.createSpy('completeHandler');
      service['isAvailableForUser'] = jasmine.createSpy('isAvailableForUser').and.returnValue(observableOf(false));
      service.showUpgradeDialog().subscribe(successHandler, errorHandler, completeHandler);
      expect(successHandler).toHaveBeenCalled();
      expect(errorHandler).not.toHaveBeenCalled();
      expect(completeHandler).toHaveBeenCalled();
    });

    describe('decorateMenuAction', () => {
      it('should decorate menu item', () => {
        userService.isInShopUser.and.returnValue(true);
        const menuItem: any = { targetUri: 'deposit' };
        service.decorateMenuAction(menuItem);
        expect(menuItem.action).toBeDefined();
        menuItem.action();
      });

      it('should not decorate menu item', () => {
        const menuItem: any = {};
        service.decorateMenuAction(menuItem);
        expect(menuItem.action).not.toBeDefined();
      });
    });

    it('isAvailableForUser', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({
        Connect: {
          upgrade: true
        }
      }));
      userService.isInShopUser.and.returnValue(true);
      const result = service['isAvailableForUser']();
      result.subscribe();
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(userService.isInShopUser).toHaveBeenCalled();
      expect(result).toEqual(jasmine.any(Observable));
    });

    it('dialogUpgradeAction', () => {
      const trackData = Object.assign({}, trackEventData, { eventLabel: 'yes - upgrade Account' });

      dialogUpgradeAction.call(service, observer);
      expect(gtmService.push).toHaveBeenCalledWith(trackData.event, trackData);
      expect(observer.next).toHaveBeenCalledWith({ redirectUri: 'retail-registration' });
      expect(observer.complete).toHaveBeenCalled();
    });

    it('dialogCancelAction', () => {
      const trackData = Object.assign({}, trackEventData, { eventLabel: 'no thanks' }),
        value = false; // or true

      dialogCancelAction.call(service, observer, value);
      expect(gtmService.push).toHaveBeenCalledWith(trackData.event, trackData);
      expect(observer.next).toHaveBeenCalledWith({ cancelled: value });
      expect(observer.complete).toHaveBeenCalled();
    });
  });
});

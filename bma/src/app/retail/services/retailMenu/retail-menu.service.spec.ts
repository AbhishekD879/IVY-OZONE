import { forkJoin, Observable, of } from 'rxjs';

import { RetailMenuService } from '@retailModule/services/retailMenu/retail-menu.service';
import { UserService } from '@core/services/user/user.service';
import { IRetailConfig } from '@app/core/services/cms/models/system-config';
import { IRetailMenu } from '@app/core/services/cms/models/menu/retail-menu.model';
import { IVerticalMenu } from '@app/core/services/cms/models/menu/vertical-menu.model';

describe('RetailMenuService', () => {
  let service: RetailMenuService,
    cmsService,
    userService,
    pubSubService,
    betFilterParamsService,
    router;

  const fakeRetailMenuItem = {
    linkTitle: 'title', linkSubtitle: 'subtitle', hidden: false, targetUri: '/retail-registration'
  };

  beforeEach(() => {
    userService = jasmine.createSpyObj<UserService>('UserService', ['getRetailCard', 'isInShopUser']);
    pubSubService = {
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT',
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };
    betFilterParamsService = jasmine.createSpyObj('BetFilterParamsService', ['chooseMode']);
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        Connect: {
          menu: {}
        }})),
      getRetailMenu: jasmine.createSpy('getRetailMenu').and.returnValue(of([fakeRetailMenuItem])),
    };
    router = {
      config: []
    };

    service = new RetailMenuService(cmsService, userService, pubSubService, betFilterParamsService, router);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('subscribe', () => {
    pubSubService.subscribe.and.callFake((a, b, cb) => cb());
    service['updateRetailMenuItems'] = jasmine.createSpy('updateRetailMenuItems');

    service.subscribe();

    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'userLoginOnConnectMenu',
      [pubSubService.API.SUCCESSFUL_LOGIN, pubSubService.API.SESSION_LOGOUT],
      jasmine.any(Function));
    expect(service['updateRetailMenuItems']).toHaveBeenCalled();
  });

  describe('createRetailMenuItems', () => {
    it('should for call cmsService.getSystemConfig and cmsService.getRetailMenu', () => {
      service['createRetailMenuItems']();

      expect(service['cmsService'].getSystemConfig).toHaveBeenCalled();
      expect(service['cmsService'].getRetailMenu).toHaveBeenCalled();
    });

    it('should define systemConfig.Connect', () => {
      forkJoin([
        service['cmsService'].getSystemConfig()
      ])
        .subscribe(([systemConfig]) => {
          expect(systemConfig.Connect && systemConfig.Connect.menu).toBeTruthy();
        });
    });

    it('should map retail menu items', () => {
      service['assignMenuAction'] = jasmine.createSpy('assignMenuAction');

      service['createRetailMenuItems']();

      expect(service['assignMenuAction']).toHaveBeenCalled();
    });

    it('should call retailMenuItems.next', () => {
      service.retailMenuItems = jasmine.createSpyObj('retailMenuItems', ['next']);

      service['createRetailMenuItems']();

      expect(service.retailMenuItems.next).toHaveBeenCalled();
    });

    it('should not call retailMenuItems.next', () => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      service.retailMenuItems = jasmine.createSpyObj('retailMenuItems', ['next']);

      service['createRetailMenuItems']();

      expect(service.retailMenuItems.next).not.toHaveBeenCalled();
    });
  });

  describe('updateRetailMenuItems', () => {
    it('should call cmsService.getSystemConfig', () => {
      service['isMenuItemAvailable'] = jasmine.createSpy('isMenuItemAvailable');
      service['redirectInShopUser'] = jasmine.createSpy('redirectInShopUser');
      spyOnProperty(service.retailMenuItems, 'value').and.returnValue([fakeRetailMenuItem]);

      service['updateRetailMenuItems']();

      expect(service['cmsService'].getSystemConfig).toHaveBeenCalled();
      expect(service['isMenuItemAvailable']).toHaveBeenCalled();
      expect(service['redirectInShopUser']).toHaveBeenCalled();
    });
  });

  describe('redirectInShopUser', () => {
    it('when connectCard IS defined and user clicked on upgrade menu item', () => {
      userService.getRetailCard.and.returnValue({});
      const targetUri = 'retail-upgrade';
      const returnUrl = service['redirectInShopUser'](targetUri);

      expect(returnUrl).toEqual('/retail-registration');
    });

    it('when connectCard IS NOT defined or user didn\'t click on upgrade menu item', () => {
      userService.getRetailCard.and.returnValue(null);
      const targetUri = jasmine.any(String);
      const returnUrl = service['redirectInShopUser'](targetUri.jasmineToString());

      expect(returnUrl).toEqual(jasmine.any(String));
    });
  });

  describe('isMenuItemAvailable', () => {
    it('should return true if uri include "upgrade" or "registration"', () => {
      const menuItemUri = 'upgrade';
      const retailConfig = {
        upgrade: true
      } as IRetailConfig;

      userService.isInShopUser.and.returnValue(true);

      const result = service['isMenuItemAvailable'](menuItemUri, retailConfig);

      expect(result).toBeTruthy();
    });

    describe('else-statement', () => {
      let menuItemUri, retailConfig;
      beforeEach(() => {
        userService.isInShopUser.and.returnValue(false);
        menuItemUri = '/bet-tracker';
        retailConfig = {
          shopBetTracker: true,
          shopBetHistory: true,
          shopLocator: true,
          upgrade: true
        } as IRetailConfig;
        spyOn(router.config, 'find').and.callThrough();
      });

      it('should return true if path in the data', () => {
        const config = {
          path: '',
          children: [
            {
              path: 'bet-tracker',
              data: {
                feature: 'shopBetTracker'
              }
            }
          ]
        };
        router.config.push(config);

        const result = service['isMenuItemAvailable'](menuItemUri, retailConfig);

        expect(router.config.find).toHaveBeenCalledWith(jasmine.any(Function));
        expect(result).toBeTruthy();
      });

      it('should return false when config contains only path without data prop', () => {
        const config = {
          path: '',
          children: [
            {
              path: 'bet-tracker',
            }
          ]
        };
        router.config.push(config);

        const result = service['isMenuItemAvailable'](menuItemUri, retailConfig);

        expect(router.config.find).toHaveBeenCalledWith(jasmine.any(Function));
        expect(result).toBeFalsy();
      });

      it('should return true when config contains path and feature in the data prop', () => {
        const config = {
          path: '',
          children: [{
            data: {
              path: 'bet-tracker',
              feature: 'shopBetTracker'
            }
          }]
        };
        router.config.push(config);

        const result = service['isMenuItemAvailable'](menuItemUri, retailConfig);

        expect(router.config.find).toHaveBeenCalledWith(jasmine.any(Function));
        expect(result).toBeTruthy();
      });

      it('should return false when config contains only feature in the data prop', () => {
        const config = {
          path: '',
          children: [{
            data: {
              feature: 'shopBetTracker'
            }
          }]
        };
        router.config.push(config);

        const result = service['isMenuItemAvailable'](menuItemUri, retailConfig);

        expect(router.config.find).toHaveBeenCalledWith(jasmine.any(Function));
        expect(result).toBeFalsy();
      });

      it('should return false when config is empty', () => {
        const config = {
          path: '',
          children: []
        };
        router.config.push(config);

        const result = service['isMenuItemAvailable'](menuItemUri, retailConfig);

        expect(router.config.find).toHaveBeenCalledWith(jasmine.any(Function));
        expect(result).toBeFalsy();
      });
    });
  });

  describe('assignMenuAction', () => {
    beforeEach(() => {
      service['betFilterMenuItemAction'] = jasmine.createSpy('betFilterMenuItemAction');
      service['commonMenuItemAction'] = jasmine.createSpy('commonMenuItemAction');
    });

    it('should assign betFilterMenuItemAction func for bet-filter menu item', () => {
      const menuItem = {
        targetUri: 'bet-filter'
      } as Partial<IRetailMenu & IVerticalMenu>;

      const result = service['assignMenuAction'](menuItem);

      expect(result.action).toEqual(jasmine.any(Function));

      result.action();

      expect(service['betFilterMenuItemAction']).toHaveBeenCalled();
      expect(service['commonMenuItemAction']).not.toHaveBeenCalled();
    });

    it('should assign commonMenuItemAction func for none bet-filter menu item', () => {
      const menuItem = {
        targetUri: 'bla-bla-bla',
        upgradePopup: true
      } as Partial<IRetailMenu & IVerticalMenu>;

      const result = service['assignMenuAction'](menuItem);

      expect(menuItem.upgradePopup).toBeTruthy();
      expect(result.action).toEqual(jasmine.any(Function));

      result.action();

      expect(service['commonMenuItemAction']).toHaveBeenCalled();
      expect(service['betFilterMenuItemAction']).not.toHaveBeenCalled();
    });
  });

  describe('betFilterMenuItemAction', () => {
    beforeEach(() => {
      betFilterParamsService.chooseMode.and.returnValue(of(null));
    });

    it('should call betFilterParamsService.chooseMode', () => {
      const result = service['betFilterMenuItemAction']();

      result.subscribe();

      expect(result).toEqual(jasmine.any(Observable));
      expect(betFilterParamsService.chooseMode).toHaveBeenCalled();
    });
  });

  it('commonMenuItemAction', () => {
    const result = service['commonMenuItemAction']();

    result.subscribe();
    expect(result).toEqual(jasmine.any(Observable));
  });

  it('updateRetailMenuItems', () => {
    cmsService.getSystemConfig.and.returnValue(of());
    service['updateRetailMenuItems']();

    expect(cmsService.getSystemConfig).toHaveBeenCalled();
  });
});

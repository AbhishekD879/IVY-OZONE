import { UpgradeAccountDialogService } from '@ladbrokesMobile/retail/services/upgradeAccountDialog/upgrade-account-dialog.service';
// eslint-disable-next-line max-len
import { of as observableOf, Observable } from 'rxjs';

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
      getCookie: jasmine.createSpy('getCookie')
    };

    dialogService = {};
    userService = {
      isMultiChannelUser: jasmine.createSpy('isMultiChannelUser'),
      status: true,
    };

    gtmService = {};
    router = {};
    routingStateService = {};
    dynamicComponentLoader = {};
    deviceService = {};
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
    expect(service['modulePath']).toEqual('@retail-lazy-load/retail.module#RetailModule');
  });

  it('isAvailableForUser', () => {
    cmsService.getSystemConfig.and.returnValue(observableOf({
      Connect: {
        upgrade: true
      }
    }));
    userService.isMultiChannelUser.and.returnValue(false);
    const result = service['isAvailableForUser']();
    result.subscribe();
    expect(cmsService.getSystemConfig).toHaveBeenCalled();
    expect(userService.isMultiChannelUser).toHaveBeenCalled();
    expect(result).toEqual(jasmine.any(Observable));
  });
});

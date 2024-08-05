import { RetailPageComponent as OxygenRetailPageComponent } from '@app/retail/components/retailPage/retail-page.component';
import { RetailPageComponent } from '@ladbrokesMobile/retail/components/retailPage/retail-page.component';
import { UPGRADE_ACCOUNT_DIALOG } from '@ladbrokesMobile/retail/constants/retail.constant';
import { of as observableOf, throwError } from 'rxjs';

describe('RetailPageComponent', () => {
  let component: RetailPageComponent;
  let userService, pubSubService, localeService, cmsService, domSanitizer, navigationService, dialogService,
    componentFactoryResolver, betFilterParamsService, gtmService, gridGtmData, changeDetectorRef, windowRef;

  beforeEach(() => {
    spyOn(OxygenRetailPageComponent.prototype, 'ngOnInit').and.callFake(() => { });
    userService = jasmine.createSpyObj('UserService', ['isInShopUser', 'isRetailUser', 'isMultiChannelUser', 'status']);
    localeService = {
      getLocale: jasmine.createSpy('getLocale').and.returnValue('en-US')
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig'),
      getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue(observableOf({}))
    };
    pubSubService = {
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT',
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    navigationService = {
      goToCashierDeposit: jasmine.createSpy()
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
    };
    betFilterParamsService = {
      betFilterParams: {}
    };
    spyOn(console, 'warn');
    gridGtmData = {
      event: 'trackEvent',
      eventCategory: 'Grid',
      eventAction: 'Menu',
      eventLabel: 'Activate Card'
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    windowRef = {
      nativeWindow: {
        location: {
          pathname: 'testPath'
        }
      }
    };
    component = new RetailPageComponent(
      userService,
      localeService,
      cmsService,
      domSanitizer,
      pubSubService,
      navigationService,
      dialogService,
      componentFactoryResolver,
      betFilterParamsService,
      gtmService,
      changeDetectorRef,
      windowRef
    );
  });

  it('ngOnInit', () => {
    component['configUpgradeButton'] = jasmine.createSpy('configUpgradeButton');
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'userLoginOnHub', [
      pubSubService.API.SUCCESSFUL_LOGIN,
      pubSubService.API.SESSION_LOGOUT],
      jasmine.any(Function));
    expect(component['configUpgradeButton']).toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('userLoginOnHub');
  });

  it('should send GTM', () => {
    component.trackUpgradeNavigation('Activate Card');
    expect(gtmService.push).toHaveBeenCalledWith(gridGtmData.event, gridGtmData);
  });

  describe('configUpgradeButton', () => {
    beforeEach(() => {
      component['getUpgradeButtonStaticBlock'] = jasmine.createSpy('getUpgradeButtonStaticBlock');
    });

    it('should show upgrade button', () => {
      userService.isMultiChannelUser.and.returnValue(false);
      userService.status.and.returnValue(true);
      cmsService.getSystemConfig.and.returnValue(observableOf({ Connect: { upgrade: true } }));
      component['configUpgradeButton']();
      expect(component['showUpgradeButton']).toBeTruthy();
    });

    it('should hide upgrade button', () => {
      userService.isMultiChannelUser.and.returnValue(true);
      userService.status.and.returnValue(true);
      cmsService.getSystemConfig.and.returnValue(observableOf({ Connect: { upgrade: false } }));
      component['configUpgradeButton']();
      expect(component['showUpgradeButton']).toBeFalsy();
    });

    it('for inShopUser', () => {
      userService.isInShopUser.and.returnValue(true);
      cmsService.getSystemConfig.and.returnValue(observableOf({ Connect: { upgrade: true } }));
      component['configUpgradeButton']();
      expect(component['getUpgradeButtonStaticBlock']).toHaveBeenCalledWith(UPGRADE_ACCOUNT_DIALOG.inshopUpgrade.dialogButton);
    });

    it('for online users', () => {
      userService.isInShopUser.and.returnValue(false);
      userService.isRetailUser.and.returnValue(false);
      cmsService.getSystemConfig.and.returnValue(observableOf({ Connect: { upgrade: true } }));
      component['configUpgradeButton']();
      expect(component['getUpgradeButtonStaticBlock']).toHaveBeenCalledWith(UPGRADE_ACCOUNT_DIALOG.onlineUpgrade.dialogButton);
    });
  });

  describe('getUpgradeButtonStaticBlock', () => {
    it('should call cmsService.getStaticBlock', () => {
      component['getUpgradeButtonStaticBlock']('inshop-upgrade-dialog-button');

      expect(cmsService.getStaticBlock).toHaveBeenCalledWith(
        'inshop-upgrade-dialog-button',
        'en-US'.toLocaleLowerCase());
    });

    it('should call domSanitizer.bypassSecurityTrustHtml', () => {
      const cmsContent = {
        htmlMarkup: '<b>test</b>'
      };
      cmsService.getStaticBlock.and.returnValue(observableOf(cmsContent));

      component['getUpgradeButtonStaticBlock']('inshop-upgrade-dialog-button');

      expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith(cmsContent.htmlMarkup);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should warn about error', () => {
      cmsService.getStaticBlock.and.returnValue(throwError({ error: 'Error message!' }));

      component['getUpgradeButtonStaticBlock']('inshop-upgrade-dialog-button');

      expect(console.warn).toHaveBeenCalledWith(jasmine.any(String), jasmine.any(Object));
    });
  });
});

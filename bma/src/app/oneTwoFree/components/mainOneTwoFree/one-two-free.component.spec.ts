import { of as observableOf, of, throwError } from 'rxjs';

import { ONE_TWO_FREE_EVENTS } from '@app/oneTwoFree/components/mainOneTwoFree/one-two-free.constants';
import { OneTwoFreeComponent } from './one-two-free.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('OneTwoFreeComponent', () => {
  let addToBetslipService;
  let asyncScriptLoader;
  let pubSubService;
  let component: OneTwoFreeComponent;
  let cmsService;
  let router;
  let staticContentData;
  let userService;
  let routingState;
  let windowRef;
  let localeService;
  let deviceService;
  let otfIosToggleData;
  let awsService;
  let domToolsService;
  let bonusSuppression,storageService;

  let serviceClosureService;

  const BODY_CLASS: string = 'menu-opened';
  const cmsIOSToggleData = {
    text: 'To play 1-2-Free on this device, please visit {{URL}} to play the game',
    iosAppOff: true,
    url: 'https://ladbrokes.com',
    urlText: 'ladbrokes.come',
    closeCtaText: 'ertwertwertwet',
    proceedCtaText: 'Go to'
  };

  beforeEach(() => {
    asyncScriptLoader = {
      loadJsFile: jasmine.createSpy().and.returnValue(observableOf(null)),
      loadCssFile: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    addToBetslipService = {
      addToBetSlip: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    awsService = {
      addAction: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    localeService = {
      getString: jasmine.createSpy().and.returnValue('No content provided')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    storageService = {
      set:jasmine.createSpy('set')
  };

    deviceService = {
      isMobile: true
    };

    routingState = {
      getPreviousUrl: jasmine.createSpy().and.returnValue('/1-2-free')
    };

    router =  {
      navigate: jasmine.createSpy()
    };

    domToolsService = {
      addClass: jasmine.createSpy('domToolsService.addClass'),
      removeClass: jasmine.createSpy('domToolsService.removeClass')
    };

    serviceClosureService = {
      userServiceClosureOrPlayBreakCheck: jasmine.createSpy('userServiceClosureOrPlayBreakCheck'),
      userServiceClosureOrPlayBreak: jasmine.createSpy('userServiceClosureOrPlayBreak'),
    }

    windowRef = {
      document: {
        body: {},
        dispatchEvent: jasmine.createSpy(),
        addEventListener: jasmine.createSpy(),
        removeEventListener: jasmine.createSpy()
      },
      nativeWindow: {
        location: {
          pathname: '/1-2-free'
        },
        CustomEvent: () => {},
        Event: {
          prototype: null
        }
      }
    };

    userService = {
      status: false,
      username: 'bla',
      bppToken:'awtyuipoiuygfhjkvcvb',
      isInShopUser: () => {
        return false;
      },
    };
    
    staticContentData = [{
      pageName: 'Splash page',
      title: '',
      pageText1: '<p>Win $50 in cash ABSOLUTELY FREE! TEST</p>',
      pageText2: '',
      pageText3: '',
      pageText4: '',
      pageText5: '',
      ctaText1: 'PLAY NOW',
      ctaText2: 'CANCEL'
    }];
    
    otfIosToggleData  = {
      url: 'url',
      text: 'text',
      urlText: 'urlText',
      closeCtaText: 'ok',
      proceedCtaText: 'go to',
      iosAppOff: true
    };
    
    cmsService = {
      getOTFStaticContent: jasmine.createSpy().and.returnValue(observableOf(staticContentData)),
      getOTFIosToggle: jasmine.createSpy().and.returnValue(observableOf(otfIosToggleData)),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };
    
    bonusSuppression = {
      checkIfYellowFlagDisabled : jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true),
      navigateAwayForRGYellowCustomer : jasmine.createSpy('navigateAwayForRGYellowCustomer')
    }

    component = new OneTwoFreeComponent(
      windowRef as any,
      asyncScriptLoader as any,
      router as any,
      pubSubService as any,
      cmsService as any,
      addToBetslipService as any,
      userService as any,
      deviceService as any,
      routingState as any,
      localeService as any,
      awsService as any,
      domToolsService as any,
      bonusSuppression as any,
      serviceClosureService as any,
      storageService as any
    );

    component['checkIsIOSApp'] = () => true;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call openLoginPopUp onInit component', () => {
    const mockCheckIsIOSApp = spyOn(component, 'checkIsIOSApp' as any);
    const expectedCMSContent = '<p>Win $50 in cash ABSOLUTELY FREE! TEST</p>';

    component.ngOnInit();
    expect(cmsService.getOTFStaticContent).toHaveBeenCalledTimes(1);
    expect(component.splashContent).toEqual(expectedCMSContent);
    expect(mockCheckIsIOSApp).toHaveBeenCalledTimes(1);
  });

  it('should call awsService logger on onInit component', () => {
    cmsService.getOTFStaticContent = jasmine.createSpy().and.returnValue(throwError({status: '500'}));

    component.ngOnInit();
    expect(awsService.addAction)
      .toHaveBeenCalledWith('1-2-free=>Get_OTFLoginStaticContent_Error', Object({ error: Object({ status: '500' }) }));
  });

  it('should call awsService logger with default message on onInit component', () => {
    cmsService.getOTFStaticContent = jasmine.createSpy().and.returnValue(throwError(null));

    component.ngOnInit();
    expect(awsService.addAction)
      .toHaveBeenCalledWith('1-2-free=>Get_OTFLoginStaticContent_Error', Object({ error: 'no error data' }));
  });

  it('should not update `splashContent` ', () => {
    cmsService.getOTFStaticContent = jasmine.createSpy().and.returnValue(observableOf(null));

    component.ngOnInit();
    expect(component.splashContent).toEqual('No content provided');
  });

  it('should subscribe to Login/Sign in events', () => {
    component['openLoginPopUp']();

    expect(pubSubService.publish).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'OneTwoFree', ['SUCCESSFUL_LOGIN', 'SESSION_LOGIN'], jasmine.any(Function));
  });

  it('should call `initOneTwoFree` method on Login/Sign In success', () => {
    spyOn(component, 'initOneTwoFree' as any);
    bonusSuppression.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false);
    let methodCb = () => {};
    pubSubService.subscribe.and.callFake((name, method, cb) => { methodCb = cb; });
    component['openLoginPopUp']();
    methodCb();

    expect(component['initOneTwoFree']).toHaveBeenCalledTimes(1);
  });

  it('should call `initOneTwoFree` method on Login/Sign In success', () => {
    spyOn(component, 'initOneTwoFree' as any);
    let methodCb = () => {};
    pubSubService.subscribe.and.callFake((name, method, cb) => { methodCb = cb; });
    component['userService'].isInShopUser = () => true;
    component['openLoginPopUp']();
    methodCb();

    expect(component['initOneTwoFree']).not.toHaveBeenCalled();
    expect(component['isInShopUser']).toBeTruthy();
  });

  it('should call initOneTwoFree onInit component', () => {
    component['checkIsIOSApp'] = () => false;
    Object.defineProperty(component['userService'], 'status', { get: () => true });

    spyOn(component, 'initOneTwoFree' as any);
    component.ngOnInit();

    expect(component['initOneTwoFree']).toHaveBeenCalledTimes(1);
  });

  it('should NOT call initOneTwoFree onInit component but set isInShopUser = true', () => {
    component['checkIsIOSApp'] = () => false;
    component['userService'].isInShopUser = () => true;
    Object.defineProperty(component['userService'], 'status', { get: () => true });

    spyOn(component, 'initOneTwoFree' as any);
    component.ngOnInit();

    expect(component['initOneTwoFree']).not.toHaveBeenCalled();
    expect(component['isInShopUser']).toBeTruthy();
  });

  it('should call bootstrapOneTwoFree after initOneTwoFree was called', () => {
    spyOn(component, 'bootstrapOneTwoFree' as any);
    spyOn(component, 'ie11CustomEventPolyfill' as any);
    component['initOneTwoFree']();
    expect(component.isGuest).toEqual(false);
    expect(component['ie11CustomEventPolyfill']).toHaveBeenCalledTimes(0);
    expect(component['bootstrapOneTwoFree']).toHaveBeenCalledTimes(1);
  });

  it('should call dispatch BOOTSTRAP event', () => {
    const mockParams = new CustomEvent(ONE_TWO_FREE_EVENTS.BOOTSTRAP_ONE_TWO_FREE,
      { detail: Object.assign({}, { username: 'bla' })});
    component['bootstrapOneTwoFree']();
    expect(windowRef.document.dispatchEvent).toHaveBeenCalledWith(mockParams);
  });

  it('should navigate to home page is bundle loading failed', () => {
    asyncScriptLoader.loadJsFile =  jasmine.createSpy();

    component['bootstrapOneTwoFree']();

    expect(awsService.addAction).toHaveBeenCalledTimes(1);
    expect(router.navigate).toHaveBeenCalled();
  });

  it('should navigate to home page is bundle loading failed with default error', () => {
    asyncScriptLoader.loadJsFile = jasmine.createSpy().and.returnValue(throwError(null));
    asyncScriptLoader.loadCssFile = jasmine.createSpy();

    component['bootstrapOneTwoFree']();

    expect(awsService.addAction).toHaveBeenCalledWith('1-2-free=>Loading_OTF_Resources_Error', Object({ error: 'no error data' }));
    expect(router.navigate).toHaveBeenCalled();
  });

  it('should call removeEventListener onDestroy component', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe)
      .toHaveBeenCalledWith('OneTwoFree');
    expect(windowRef.document.removeEventListener)
      .toHaveBeenCalledWith(ONE_TWO_FREE_EVENTS.DESTROY_ONE_TWO_FREE, component['destroyOneTwoFree']);
  });

  it('should call addToBetslip with custom event & callBacks & publish and redirect home', () => {
    const mockEvent = new CustomEvent(ONE_TWO_FREE_EVENTS.ADD_TO_BETSLIP,
      { detail: Object.assign({}, { predictions: ['123123', '234234'], isMobile: true })});

    const { predictions } = mockEvent.detail;
    component['addToBetslip'](mockEvent);

    expect(component['addToBetslipService'].addToBetSlip).toHaveBeenCalledWith(predictions.join(','), true, true, true);
  });

  it('should call addToBetslip with custom event, fail, and log Aws', () => {
    addToBetslipService.addToBetSlip = jasmine.createSpy().and.returnValue(throwError({status: '500'}));

    const mockEvent = new CustomEvent(ONE_TWO_FREE_EVENTS.ADD_TO_BETSLIP,
      { detail: Object.assign({}, { predictions: ['123123', '234234'], isMobile: true }) });

    component['addToBetslip'](mockEvent);

    expect(awsService.addAction)
      .toHaveBeenCalledWith('1-2-free=>Add_To_BetSlip_Error', Object({ error: Object({ status: '500' }) }));
  });

  it('should call addToBetslip with custom event, fail, and log Aws with default err name', () => {
    addToBetslipService.addToBetSlip = jasmine.createSpy().and.returnValue(throwError(null));

    const mockEvent = new CustomEvent(ONE_TWO_FREE_EVENTS.ADD_TO_BETSLIP,
      { detail: Object.assign({}, { predictions: ['123123', '234234'], isMobile: true })});

    component['addToBetslip'](mockEvent);

    expect(awsService.addAction)
      .toHaveBeenCalledWith('1-2-free=>Add_To_BetSlip_Error', Object({ error: 'no error data' }));
  });

  it('should call addToBetslip with custom event & callBacks & publish and not redirect home', () => {
    const mockEvent = new CustomEvent(ONE_TWO_FREE_EVENTS.ADD_TO_BETSLIP,
      { detail: Object.assign({}, { predictions: ['123123', '234234'], isMobile: false })});
    const { predictions } = mockEvent.detail;
    component['addToBetslip'](mockEvent);

    expect(component['addToBetslipService'].addToBetSlip).toHaveBeenCalledWith(predictions.join(','), true, true, false);
  });

  it('should redirect user if `goToBetting` called', () => {
    component['goToBetting']();
    expect(router.navigate).toHaveBeenCalledWith(['sport', 'football', 'matches']);
  });

  it('should redirect user to `Root` if `destroyOneTwoFree` called', () => {
    component['destroyOneTwoFree']();
    expect(router.navigate).toHaveBeenCalledWith(['/']);
  });

  it('should redirect user to `Previous Page` if `destroyOneTwoFree` called', () => {
    routingState.getPreviousUrl = jasmine.createSpy().and.returnValue('/test');

    component['destroyOneTwoFree']();
    expect(router.navigate).toHaveBeenCalledWith(['/test']);
  });

  it('should redirect to previous location, NOT root', () => {
    routingState.getPreviousUrl = jasmine.createSpy().and.returnValue('/1-2-free');

    component['destroyOneTwoFree']();
    expect(router.navigate).toHaveBeenCalledWith(['/']);
  });

  describe('should show IOS redirect dialog', () => {
    it('should show iosToggle dialog',  () => {
      expect(component.showIOSDialog).toEqual(false);
      component['checkIsIOSApp'] = () => true;

      (cmsService.getOTFIosToggle as jasmine.Spy).and.returnValue(observableOf(cmsIOSToggleData));
      component.ngOnInit();

      expect(component.showIOSDialog).toEqual(true);
      expect(component.dialogContent.btnPrimary.cssClass).toEqual('iosDialogBtn-primary');
    });

    it('should log Aws error',  () => {
      component['checkIsIOSApp'] = () => true;
      (cmsService.getOTFIosToggle as jasmine.Spy).and.returnValue(throwError(null));
      component.ngOnInit();

      expect(awsService.addAction)
        .toHaveBeenCalledWith('1-2-free=>Get_IosToggleData_Error', Object({ error: 'no error data' }));
    });

    it('should show iosToggle dialog without primary button',  () => {
      cmsIOSToggleData.url =  null;
      cmsIOSToggleData.proceedCtaText = 'some text';

      expect(component.showIOSDialog).toEqual(false);
      component['checkIsIOSApp'] = () => true;

      (cmsService.getOTFIosToggle as jasmine.Spy).and.returnValue(observableOf(cmsIOSToggleData));
      component.ngOnInit();

      expect(component.dialogContent.btnPrimary.cssClass).toEqual('hidden');
    });

    it('should not open iosToggle dialog when isIos=false', fakeAsync(() => {
      const mockIosCmsToggleDialog = spyOn(component, 'buildIosCmsToggleDialog' as any);
      component['checkIsIOSApp'] = () => false;
      component.ngOnInit();

      expect(mockIosCmsToggleDialog).not.toHaveBeenCalled();
      tick();
    }));

    it('should not open iosToggle dialog when iosAppOff=false', fakeAsync(() => {
      otfIosToggleData.iosAppOff = false;
      cmsService.getOTFIosToggle = jasmine.createSpy().and.returnValue(observableOf(otfIosToggleData));

      component['checkIsIOSApp'] = () => true;
      const mockIosCmsToggleDialog = spyOn(component, 'buildIosCmsToggleDialog' as any);
      component.ngOnInit();

      cmsService.getOTFIosToggle()
        .subscribe(item => {
          expect(item.iosAppOff).toBeFalsy();
        });
      expect(mockIosCmsToggleDialog).not.toHaveBeenCalled();
      tick();
    }));

    it('should NOT open iosToggle dialog when iosAppOff=false in array like data', () => {
      const customOtfIosToggleData = [{
        ...otfIosToggleData,
        iosAppOff: false
      }];
      cmsService.getOTFIosToggle = jasmine.createSpy().and.returnValue(observableOf(customOtfIosToggleData));

      component['checkIsIOSApp'] = () => true;
      const mockIosCmsToggleDialog = spyOn(component, 'buildIosCmsToggleDialog' as any);
      component.ngOnInit();

      cmsService.getOTFIosToggle()
        .subscribe(item => {
          expect(item[0].iosAppOff).toBeFalsy();
        });

      expect(mockIosCmsToggleDialog).not.toHaveBeenCalled();
    });

    it('should open iosToggle dialog when iosAppOff=true in array like data', fakeAsync(() => {
      const customOtfIosToggleData = [{
        ...otfIosToggleData,
        iosAppOff: true
      }];
      cmsService.getOTFIosToggle = jasmine.createSpy().and.returnValue(observableOf(customOtfIosToggleData));

      component['checkIsIOSApp'] = () => true;
      const mockIosCmsToggleDialog = spyOn(component, 'buildIosCmsToggleDialog' as any);
      component.ngOnInit();

      cmsService.getOTFIosToggle()
        .subscribe(item => {
          expect(item[0].iosAppOff).not.toBeFalsy();
        });
      expect(mockIosCmsToggleDialog).toHaveBeenCalledWith(
        Object({ url: 'url', text: 'text', urlText: 'urlText', closeCtaText: 'ok', proceedCtaText: 'go to', iosAppOff: true }));
      tick();
    }));

    it('should NOT open iosToggle dialog when iosAppOff=false in object like data', fakeAsync(() => {
      const customOtfIosToggleData = {
        ...otfIosToggleData,
        iosAppOff: false
      };
      cmsService.getOTFIosToggle = jasmine.createSpy().and.returnValue(observableOf(customOtfIosToggleData));

      component['checkIsIOSApp'] = () => true;
      const mockIosCmsToggleDialog = spyOn(component, 'buildIosCmsToggleDialog' as any);
      component.ngOnInit();

      cmsService.getOTFIosToggle()
        .subscribe(item => {
          expect(item.iosAppOff).toBeFalsy();
        });
      expect(mockIosCmsToggleDialog).not.toHaveBeenCalled();
      tick();
    }));

    it('should open iosToggle dialog when iosAppOff=true in object like data', fakeAsync(() => {
      otfIosToggleData.iosAppOff = true;
      cmsService.getOTFIosToggle = jasmine.createSpy().and.returnValue(observableOf(otfIosToggleData));

      component['checkIsIOSApp'] = () => true;
      const mockIosCmsToggleDialog = spyOn(component, 'buildIosCmsToggleDialog' as any);
      component.ngOnInit();

      cmsService.getOTFIosToggle()
        .subscribe(item => {
          expect(item.iosAppOff).not.toBeFalsy();
        });
      expect(mockIosCmsToggleDialog).toHaveBeenCalledWith(
        Object({ url: 'url', text: 'text', urlText: 'urlText', closeCtaText: 'ok', proceedCtaText: 'go to', iosAppOff: true }));
      tick();
    }));
  });

  it('should check user platform iPhone', () => {
    (<any>navigator)['__defineGetter__']('userAgent', () => {
      return 'iPhone';
    });

    component.ngOnInit();

    cmsService.getOTFIosToggle()
      .subscribe(item => {
        expect(item).toBeDefined();
      });

    (cmsService.getOTFIosToggle as jasmine.Spy).and.returnValue(observableOf(cmsIOSToggleData));

    expect(component.showIOSDialog).toEqual(true);
  });

  it('should check user platform Ipad', () => {
    (<any>navigator)['__defineGetter__']('userAgent', () => {
      return 'iPAD';
    });

    component.ngOnInit();

    cmsService.getOTFIosToggle()
      .subscribe(item => {
        expect(item).toBeDefined();
      });

    (cmsService.getOTFIosToggle as jasmine.Spy).and.returnValue(observableOf(cmsIOSToggleData));

    expect(component.showIOSDialog).toEqual(true);
  });

  it('should check user platform Ipad and Safari', () => {
    const customDeviceService = {
      ...deviceService,
      isIos: jasmine.createSpy().and.returnValue(true),
      isSafari: jasmine.createSpy().and.returnValue(true)
    };

    const customComponent = new OneTwoFreeComponent(
      windowRef as any,
      asyncScriptLoader as any,
      router as any,
      pubSubService as any,
      cmsService as any,
      addToBetslipService as any,
      userService as any,
      customDeviceService as any,
      routingState as any,
      localeService as any,
      awsService as any,
      domToolsService as any,
      bonusSuppression as any,
      serviceClosureService as any,
      storageService as any
    );
    expect(customComponent.showIOSDialog).toEqual(false);
    customComponent.ngOnInit();

    cmsService.getOTFIosToggle()
      .subscribe(item => {
        expect(item).toBeDefined();
      });

    (cmsService.getOTFIosToggle as jasmine.Spy).and.returnValue(observableOf(cmsIOSToggleData));

    expect(customComponent.showIOSDialog).toEqual(false);
  });

  it('should check user platform Iphone and NOT Safari', () => {
    const customDeviceService = {
      ...deviceService,
      isIos: jasmine.createSpy().and.returnValue(true),
      isSafari: jasmine.createSpy().and.returnValue(false)
    };

    const customComponent = new OneTwoFreeComponent(
      windowRef as any,
      asyncScriptLoader as any,
      router as any,
      pubSubService as any,
      cmsService as any,
      addToBetslipService as any,
      userService as any,
      customDeviceService as any,
      routingState as any,
      localeService as any,
      awsService as any,
      domToolsService as any,
      bonusSuppression as any,
      serviceClosureService as any,
      storageService as any
    );
    expect(customComponent.showIOSDialog).toEqual(false);
    customComponent.ngOnInit();

    cmsService.getOTFIosToggle()
      .subscribe(item => {
        expect(item).toBeDefined();
      });

    (cmsService.getOTFIosToggle as jasmine.Spy).and.returnValue(observableOf(cmsIOSToggleData));

    expect(customComponent.showIOSDialog).toEqual(false);
  });

  it('should check user platform if not Iphone/Ipad', fakeAsync(() => {
    otfIosToggleData.iosAppOff = false;
    cmsService.getOTFIosToggle = jasmine.createSpy().and.returnValue(observableOf(otfIosToggleData));

    (<any>navigator)['__defineGetter__']('userAgent', () => {
      return 'Safari';
    });

    const mockIosCmsToggleDialog = spyOn(component, 'buildIosCmsToggleDialog' as any);
    component.ngOnInit();

    cmsService.getOTFIosToggle()
      .subscribe(item => {
        expect(item.iosAppOff).toBeFalsy();
      });
    expect(mockIosCmsToggleDialog).not.toHaveBeenCalled();
    tick();
  }));

  describe('Testing handleIOSDialogBtn method', () => {
    it('should redirect to root', () => {
      component.handleIOSDialogBtn();
      expect(domToolsService.removeClass).toHaveBeenCalledWith({}, BODY_CLASS);
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should redirect to previous page', () => {
      routingState.getPreviousUrl = jasmine.createSpy().and.returnValue('/test');

      component.handleIOSDialogBtn();
      expect(domToolsService.removeClass).toHaveBeenCalledWith({}, BODY_CLASS);
      expect(windowRef.document.body).toEqual({});
      expect(router.navigate).toHaveBeenCalledWith(['/test']);
    });
  });

  describe('Test `showSplashLogin` method', () => {
    beforeEach(() => {
      userService.isInShopUser =  () => false;
      userService.status = false;
    });

    it('should return true if Guest', () => {
      expect(component['showSplashLogin']()).toEqual(true);
    });

    it('should return false if NOT Guest', () => {
      userService.status = true;

      component['checkIsIOSApp'] = () => false;
      component.ngOnInit();

      expect(component['showSplashLogin']()).toEqual(false);
    });
  });

  it('should call ie11 polyfill method', () => {
    windowRef.nativeWindow.CustomEvent = null;

    expect(windowRef.nativeWindow.CustomEvent).toEqual(null);
    component['bootstrapOneTwoFree']();
    const event = new component['windowRef'].nativeWindow.CustomEvent('hello');
    const event2 = new component['windowRef'].nativeWindow.CustomEvent('hello', { detail: { foo: 'bar' } });
    expect(windowRef.nativeWindow.CustomEvent).toBeDefined();
    expect(event.detail).toEqual(null);
    expect(event.bubbles).toEqual(false);
    expect(event2.detail).toEqual({ foo: 'bar' });
  });

  it('should call sendAwsRequest', () => {
    const mockEvent = new CustomEvent(ONE_TWO_FREE_EVENTS.OTF_NEW_RELIC,
      { detail: Object.assign({}, { data: 'OTF_NEW_RELIC', err: { message: 'error' } })});

    component['sendAwsRequest'](mockEvent);

    expect(awsService.addAction)
      .toHaveBeenCalledWith('1-2-free=>OTF_NEW_RELIC', Object({ error: 'error' }));
  });

  it('should call sendAwsRequest with default name', () => {
    const mockEvent = new CustomEvent(ONE_TWO_FREE_EVENTS.OTF_NEW_RELIC,
      { detail: Object.assign({}, { data: null, err: null })});

    component['sendAwsRequest'](mockEvent);

    expect(awsService.addAction)
      .toHaveBeenCalledWith('1-2-free=>app error', Object({ error: 'no error data' }));
  });

  it('should call sendAwsRequest with dispatchEvent', () => {
    const mockParams = new CustomEvent(ONE_TWO_FREE_EVENTS.F2P_ACTIVATE,
      { detail: {F2P : serviceClosureService.userServiceClosureOrPlayBreakCheck() &&
     serviceClosureService.userServiceClosureOrPlayBreak}});

    component['F2PSuspension']();
    expect(windowRef.document.dispatchEvent).toHaveBeenCalledWith(mockParams);    
  });

  it('should not update showBackButton if there is no delay', () => {
    asyncScriptLoader.loadJsFile =  jasmine.createSpy();

    component['bootstrapOneTwoFree']();

    expect(component.showBackButton).toBeFalse();
  });

  describe('updateOtfSegmentStorage', () => {
    it('should set otfsegment data', () => {
      storageService.get = jasmine.createSpy('get').and.returnValue({ user: 'username1', 'segment': false });
      component['updateOtfSegmentStorage']()
      expect(storageService.set).toHaveBeenCalledTimes(1);
    })
  })
});

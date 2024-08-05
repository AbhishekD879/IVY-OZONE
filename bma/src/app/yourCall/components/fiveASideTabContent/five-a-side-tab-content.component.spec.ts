import { FiveASideTabContentComponent } from './five-a-side-tab-content.component';
import { of, throwError } from 'rxjs';

describe('#FiveASideTabContentComponent', () => {
  let component;
  let cmsService;
  let domSanitizer;
  let router;
  let routingHelperService;
  let activatedRoute;
  let fiveASideBet;
  let gtmService;
  let fiveASideService;
  let windowRefService;
  let domToolsService;
  let deviceService;
  let pubSubService;

  beforeEach(() => {
    cmsService = {
      getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue(of({
        htmlMarkup: '<HTML>'
      }))
    };
    domSanitizer = {
      sanitize: jasmine.createSpy('sanitize').and.returnValue('<HTML>'),
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('<HTML>')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('event/12345')
    };
    activatedRoute = {
      snapshot: {
        children: []
      }
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((s, c, func) => {
        func(false);
      }),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    fiveASideBet = {};
    gtmService = {
      push: jasmine.createSpy('push'),
    };
    fiveASideService = {
      showView: jasmine.createSpy('showView'),
      hideView: jasmine.createSpy('hideView'),
    };
    windowRefService = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener')
      }
    };
    domToolsService = {
      scrollPageTop: jasmine.createSpy('scrollPageTop')
    };
    deviceService = {
      isTablet: true,
      isIos: true
    };

    component = new FiveASideTabContentComponent(
      cmsService,
      domSanitizer,
      router,
      routingHelperService,
      activatedRoute,
      fiveASideBet,
      fiveASideService,
      gtmService,
      windowRefService,
      domToolsService,
      deviceService,
      pubSubService
      );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.isLoaded).toEqual(false);
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit', () => {
      windowRefService.nativeWindow.addEventListener.and.returnValue(() => {});
      expect(component.isLoaded).toEqual(false);
      component.ngOnInit();

      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('five-a-side-launcher');
      expect(domSanitizer.sanitize).toHaveBeenCalledWith(0, '<HTML>');
      expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith('<HTML>');
      expect(component.staticBlockContent).toEqual('<HTML>');

      expect(component.showPitch).toEqual(false);
      expect(component.isLoaded).toEqual(true);
      expect(component.focusOutListener).toBeDefined();
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it('should call ngOnInit with reloadState', () => {
      expect(component.isLoaded).toEqual(false);
      component.ngOnInit();

      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('five-a-side-launcher');
      expect(cmsService.getStaticBlock).toHaveBeenCalledTimes(1);

      expect(component.showPitch).toEqual(false);
      expect(component.isLoaded).toEqual(true);
    });

    it('should call ngOnInit error form cms', () => {
      cmsService.getStaticBlock.and.returnValue(throwError(''));
      expect(component.isLoaded).toEqual(false);
      component.ngOnInit();

      expect(cmsService.getStaticBlock).toHaveBeenCalledWith('five-a-side-launcher');

      expect(component.showPitch).toEqual(false);
      expect(component.isLoaded).toEqual(true);
      expect(component.cmsDown).toEqual(true);
    });

    it('should call ngOnInit and open pithc view', () => {
      activatedRoute.snapshot.children = [{
        paramMap: {
          get: jasmine.createSpy('get').and.returnValue('pitch')
        }
      }];
      pubSubService.subscribe = jasmine.createSpy('subscribe');
      component.ngOnInit();

      expect(component.showPitch).toEqual(true);
    });
  });

  describe('#ngOnDestroy', () => {
    it('should call ngOnDestroy method', () => {
      component.focusOutListener = jasmine.createSpy('focusOutListener').and.returnValue(() => {});
      component.ngOnDestroy();
      expect(component.focusOutListener).toHaveBeenCalled();
      expect(fiveASideService.hideView).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });

    it('should Not call focusOutListener method', () => {
      component.ngOnDestroy();

      expect(component.focusOutListener).not.toBeDefined();
    });
  });

  describe('#onClick', () => {
    it('should navigate to pitch view when click on build class', () => {
      component.eventEntity = {};
      component.onClick({
        preventDefault: () => {},
        target: {
          className: 'build'
        }
      } as any);

      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({});
      expect(router.navigate).toHaveBeenCalledWith(['/event/12345/5-a-side/pitch']);
      expect(component.showPitch).toEqual(true);
      expect(gtmService.push).toHaveBeenCalled();
    });

    it('should not navigate to pitch view not target', () => {
      component.eventEntity = {};
      component.onClick({
        preventDefault: () => {},
      } as any, null);

      expect(routingHelperService.formEdpUrl).not.toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
      expect(component.showPitch).toEqual(false);
    });

    it('should not navigate to pitch view wrong target', () => {
      component.eventEntity = {};
      component.onClick({
        preventDefault: () => {},
      } as any, {
        className: ''
      });

      expect(routingHelperService.formEdpUrl).not.toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
      expect(component.showPitch).toEqual(false);
    });

    it('#should track open pitch view', () => {
      component.eventEntity = {};
      component.onClick({
        preventDefault: () => {
        }, target: {
          className: 'build'
        }
      } as any);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({});
      expect(router.navigate).toHaveBeenCalledWith(['/event/12345/5-a-side/pitch']);
      expect(component.showPitch).toEqual(true);
      expect(gtmService.push).toHaveBeenCalled();
    });
  });

  describe('#reloadState', () => {
    it('should reload State', () => {
      component['getStaticBlock'] = jasmine.createSpy();
      component.reloadState();

      expect(component.isLoaded).toEqual(false);
      expect(component.cmsDown).toEqual(false);
      expect(component['getStaticBlock']).toHaveBeenCalled();
    });
  });

  describe('onCloseIosKeyboardListener', () => {
    it('should not add focusout listener if device is not iOS', () => {
      deviceService.isIos = false;

      component['onCloseIosKeyboardListener']();

      expect(component.focusOutListener).not.toBeDefined();
      expect(windowRefService.nativeWindow.addEventListener).not.toHaveBeenCalled();
    });

    it('should not add focusout listener if device is not tablet but iOS', () => {
      deviceService.isIos = true;
      deviceService.isTablet = false;

      component['onCloseIosKeyboardListener']();

      expect(component.focusOutListener).not.toBeDefined();
      expect(windowRefService.nativeWindow.addEventListener).not.toHaveBeenCalled();
    });

    it('should add focusout listener if device is not tablet but iOS and scroll top', () => {
      windowRefService.nativeWindow.addEventListener.and.callFake((event, handler) => {
        handler && handler();
      });

      component['onCloseIosKeyboardListener']();

      expect(windowRefService.nativeWindow.addEventListener).toHaveBeenCalledWith('focusout', jasmine.any(Function));
      expect(domToolsService.scrollPageTop).toHaveBeenCalledWith(0);
    });
  });
});

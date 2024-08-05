import { BsNotificationComponent } from './bs-notification.component';

describe('BsNotificationComponent', () => {
  let component: BsNotificationComponent;
  let router;
  let deviceService;
  let windowRef;
  let domTools;
  let domSanitizer;
  let elementRef;
  let changeDetection;
  const changes = {
    bsMessage: {
      currentValue: 'success'
    }
  } as any;
  const event = {
    target: {
      dataset: {
        routerlink: 'test link'
      }
    }
  } as any;

  beforeEach(() => {
    router = jasmine.createSpyObj('router', ['navigateByUrl']);
    deviceService = { isMobile: true };
    domSanitizer = {
      sanitize: () => 'safeString',
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml').and.returnValue('sanitized')
    };
    domTools = {
      getOffset: jasmine.createSpy().and.callFake(param => {
        return { top: 30 };
      })
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake(cb => {
          cb();
        }),
        clearTimeout: jasmine.createSpy('clearTimeout'),
        innerHeight: 1
      },
      document: {
        querySelector: jasmine.createSpy()
      }
    };
    elementRef = {
      nativeElement: {
        focus: jasmine.createSpy('focus'),
        style: {
          display: 'static'
        }
      }
    };
    changeDetection = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
  });

  function createComponent() {
    component = new BsNotificationComponent(deviceService, windowRef, domTools, domSanitizer, router, elementRef,changeDetection);
    component.bsPosition = 'top';
    component.bsType = 'success';
    component['notifyTimeout'] = 1;
  }

  it('should create BsNotificationComponent instance', () => {
    createComponent();
    component.ngOnInit();
    expect(component['element'].focus).toHaveBeenCalledTimes(1);
    expect(component.cssClass).toEqual('top success');
  });

  it('should clear notify timeout on destroy', () => {
    const notifyTimeout = 10;

    createComponent();
    component['notifyTimeout'] = notifyTimeout;
    component.ngOnDestroy();

    expect(windowRef.nativeWindow.clearTimeout).toHaveBeenCalled();
  });

  describe('onChanges', () => {
    it('should set bs message onChanges', () => {
      createComponent();
      component.bsNoScroll = false;
      component.ngOnChanges(changes);
      expect(component['domSanitizer'].bypassSecurityTrustHtml).toHaveBeenCalledWith('success');
    });

    it('should not set bs message onChanges if some props are not available', () => {
      createComponent();
      component.bsNoScroll = true;
      component.bsType = 'default';
      changes.bsMessage.currentValue = undefined;
      component.ngOnChanges(changes);
      expect(component['message']).toEqual('');
      expect(component.cssClass).toEqual('top default');
    });

    it('should set bs message onChanges', () => {
      createComponent();
      component.bsNoScroll = true;
      component.bsType = 'test';
      changes.bsMessage.currentValue = 'test';
      component.ngOnChanges(changes);
      expect(component['domSanitizer'].bypassSecurityTrustHtml).toHaveBeenCalledWith('test');
    });

    it('should not set bs message onChanges if !isMessageChanged', () => {
      createComponent();
      component.ngOnChanges({ bsMessage: null });
      expect(component['domSanitizer'].bypassSecurityTrustHtml).not.toHaveBeenCalledWith(null);
    });
  });

  describe('checkRedirect', () => {
    it('should navigate by existed url', () => {
      createComponent();
      component.checkRedirect(event);
      expect(router.navigateByUrl).toHaveBeenCalledWith('test link');
    });

    it('should not navigate if there is no url', () => {
      event.target.dataset.routerlink = '';
      createComponent();
      component.checkRedirect(event);
      expect(component['router'].navigateByUrl).not.toHaveBeenCalled();
    });
  });

  describe('hideNotification', () => {
    it('should hide notification', () => {
      createComponent();
      component.bsIsClosable = true;
      component.hideNotification();
      expect(component.bsMessage).toBeUndefined();
      expect(component.message).toBeUndefined();
      expect(component['element'].style.display).toEqual('none');
    });

    it('should not hide notification', () => {
      createComponent();
      component.bsIsClosable = false;
      component.hideNotification();
      expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
    });
  });

  describe('scrollToNotification', () => {
    it('should scroll to notification if there is error div', () => {
      mockCalls(1);
      createComponent();
      component.scrollToNotification();
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('.bs-notification.danger, .bs-notification.success');
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('.is-visible');
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('.bs-selections-wrapper');
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('.sidebar-menu-header');
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('.single-stake');
    });

    it('should set scroll pos is inner height >= panelOffset', () => {
      mockCalls(100);
      createComponent();
      component.scrollToNotification();
      expect(domTools.getOffset).toHaveBeenCalledWith({ clientHeight: 20 });
    });

    it('should not scroll to notification', () => {
      windowRef.document = {
        querySelector: jasmine.createSpy().and.callFake(param => {
          if (param === 'input:focus') {
            return {};
          }
        })
      };
      createComponent();
      component.scrollToNotification();
      expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
    });

    it('should scroll if platform is desktop', () => {
      windowRef.nativeWindow = {
        setTimeout: jasmine.createSpy().and.callFake(cb => cb())
      };
      windowRef.document = {
        querySelector: jasmine.createSpy().and.callFake(sel => {
          return [
            '.bs-notification.danger, .bs-notification.success',
            '.bs-selections-wrapper',
            '.bs-selections-wrapper.scrollable-content'
          ].includes(sel) ? {} : null;
        })
      };
      createComponent();
      deviceService.isMobile = false;
      deviceService.isDesktop = true;
      component.scrollToNotification();
      expect(domTools.getOffset).toHaveBeenCalledTimes(4);
    });
  });

  function mockCalls(height) {
    windowRef = {
      document: {
        querySelector: jasmine.createSpy().and.callFake(param => {
          switch (param) {
          case 'input:focus':
            return null;
          case '.bs-notification.danger, .bs-notification.success':
            return { clientHeight: 20 };
          case '.bs-selections-wrapper.scrollable-content':
            return { scrollTop: 10 };
          case '.is-visible':
            return { test: 'isVisible' };
          case '.bs-selections-wrapper':
            return { test: 'scrollDiv' };
          case '.sidebar-menu-header':
            return { clientHeight: 2 };
          case '.single-stake':
            return { clientHeight: 3 };
          case '.scrollable-content':
            return { scrollTop: 20 };
          }
        })
      },
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake(cb => {
          cb();
        }),
        innerHeight: height
      }
    };
    domTools = {
      getOffset: jasmine.createSpy().and.callFake(param => {
        return { top: 30 };
      })
    };
  }
});

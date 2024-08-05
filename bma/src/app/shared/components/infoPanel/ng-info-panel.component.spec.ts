import { ElementRef } from '@angular/core';
import { fakeAsync } from '@angular/core/testing';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { NgInfoPanelComponent } from '@shared/components/infoPanel/ng-info-panel.component';

describe('NgInfoPanelComponent', () => {
  let component: NgInfoPanelComponent;
  let rendererService;
  let elementRef;
  let windowRef;
  let router;
  let domSanitizer;

  const document = {};

  beforeEach(() => {
    rendererService = {
      renderer: {
        listen: jasmine.createSpy()
      }
    };
    elementRef = {
      nativeElement: {
        getBoundingClientRect: jasmine.createSpy(),
        querySelectorAll: jasmine.createSpy().and.returnValue([])
      }
    };
    windowRef = {
      document: {
        querySelectorAll: jasmine.createSpy().and.returnValue([])
      }
    };
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy().and.callFake(message => message)
    };
    component = new NgInfoPanelComponent(
      document,
      windowRef as WindowRefService,
      elementRef as ElementRef,
      {} as DomToolsService,
      rendererService,
      domSanitizer,
      router,
      {} as DeviceService
    );

    spyOn<any>(component, 'getMessageElem').and.callThrough();
    spyOn<any>(component, 'makeAutoScroll');
    spyOn<any>(component, 'removeWatchingEventListeners');
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should bind events listeners after show InfoPanel', () => {
    spyOn<any>(component, 'addWatchingEventListeners');
    component.showInfoPanel('test');

    expect(component['addWatchingEventListeners']).toHaveBeenCalled();
  });

  it('should not init panel if no message provided', () => {
    spyOn(component, 'initInfoPanel');
    component.message = '';
    component.ngOnInit();

    expect(component.initInfoPanel).not.toHaveBeenCalled();
  });

  it('should init panel if message provided', () => {
    spyOn(component, 'initInfoPanel');
    component.message = 'MessageMock';
    component.ngOnInit();

    expect(component.initInfoPanel).toHaveBeenCalled();
  });

  it('should unbind events listeners on component destroy', () => {
    component.ngOnInit();
    component.ngOnDestroy();
    expect(component['removeWatchingEventListeners']).toHaveBeenCalled();
  });

  it('should unbind events listeners if panel hides', () => {
    component.ngOnInit();
    component.hideInfoPanel();
    expect(component['removeWatchingEventListeners']).toHaveBeenCalled();
  });

  it('should not unsubscribe if never subscribed', () => {
    component.ngOnInit();
    component.hideInfoPanel();
  });

  it('should set isPanelShown false', () => {
    component.ngOnInit();
    component.isPanelShown = true;
    component.hideInfoPanel();
    expect(component.isPanelShown).toBeFalsy();
  });

  it('should set isPanelShown false if no message', () => {
    component.message = '';
    component.ngOnInit();
    component.isPanelShown = true;
    component.showInfoPanel();
    expect(component.isPanelShown).toBeFalsy();
  });

  it('should test Changes', () => {
    spyOn(component, 'initInfoPanel');

    component.ngOnChanges({});
    expect(component.initInfoPanel).not.toHaveBeenCalled();
  });

  it('should test Changes', () => {
    spyOn(component, 'initInfoPanel');
    const messageChanges: any = {
      message: {}
    };

    component.ngOnChanges(messageChanges);

    expect(component.initInfoPanel).not.toHaveBeenCalled();
  });

  it('should test Changes', () => {
    spyOn(component, 'initInfoPanel');

    const messageChanges: any = {
      message: {
        firstChange: true,
        currentValue: 'initial message'
      }
    };

    component.ngOnChanges(messageChanges);

    expect(component.initInfoPanel).not.toHaveBeenCalled();
  });

  it('should test Changes', () => {
    spyOn(component, 'initInfoPanel');

    const messageChanges: any = {
      message: {
        firstChange: false,
        currentValue: null
      }
    };

    component.ngOnChanges(messageChanges);

    expect(component.initInfoPanel).not.toHaveBeenCalled();
  });

  it('should test Changes', () => {
    spyOn(component, 'initInfoPanel');

    const messageChanges: any = {
      message: {
        firstChange: false,
        currentValue: 'Message Mock'
      }
    };

    component.ngOnChanges(messageChanges);

    expect(component.initInfoPanel).toHaveBeenCalled();
  });

  describe('InfoPanel', () => {
    beforeEach(() => {
      component.ngOnInit();
      spyOn<any>(component, 'hideInfoPanel');
      spyOn<any>(component, 'showInfoPanel');
    });
    it('should call hideInfoPanel', () => {
      component.initInfoPanel();
      expect(component['hideInfoPanel']).toHaveBeenCalled();
    });
    it('should call showInfoPanel', () => {
      component.message = 'Test';
      component.initInfoPanel();
      expect(component['showInfoPanel']).toHaveBeenCalled();
    });
  });

  describe('showInfoPanel', () => {
    const message = 'href="someLink"';
    beforeEach(() => {
      component.ngOnInit();
      component.isPanelShown = false;
    });
    it('should set isPanelShown true when dynamic showing', () => {
      component.showInfoPanel(message);
      expect(component.isPanelShown).toBeTruthy();
      expect(component.infoMsg).toEqual('data-routerlink="someLink"');
    });
    it('should set isPanelShown true', () => {
      component.message = message;
      component.showInfoPanel();
      expect(component.isPanelShown).toBeTruthy();
      expect(component.infoMsg).toEqual('data-routerlink="someLink"');
    });
    it('should set component message and type when they are set', () => {
      const msg = 'ffs', type = 'warning';
      component.showInfoPanel(msg, type);
      expect(component.message).toEqual(msg);
      expect(component.type).toEqual(type);
    });
    it('should NOT set component message and type', () => {
      component.message = 'wtf';
      component.type = 'warning';
      component.showInfoPanel();
      expect(component.message).toEqual('wtf');
      expect(component.type).toEqual('warning');
    });
  });

  it('watchClick handler should not try to hide already hidden panel', fakeAsync((done: DoneFn) => {
    spyOn(component, 'hideInfoPanel');
    component.isPanelShown = false;
    component['watchClick'](new MouseEvent('click'));

    expect(component.hideInfoPanel).not.toHaveBeenCalled();
  }));

  it('watchClick handler should not hide panel on scroll (mobile)', () => {
    spyOn(component, 'hideInfoPanel');
    component.touchMoved = false;
    component['watchClick'](new MouseEvent('touchend'));

    expect(component.hideInfoPanel).not.toHaveBeenCalled();
  });

  it('watchClick handler should not hide panel if redirectUrl is not defined', () => {
    spyOn(component, 'hideInfoPanel');
    component.touchMoved = false;
    component.isPanelShown = true;
    component.noHideMessage = false;
    component['watchClick']({
      target: {
        tagName: 'someTag',
        dataset: {}
      }
    } as any);

    expect(component.hideInfoPanel).not.toHaveBeenCalled();
  });


  describe('addWatchingEventListeners', () => {
    it('should add eventListener for device', () => {
      component.noHide = false;
      component['deviceService'].isDesktop = true;
      component['addWatchingEventListeners']();

      expect(component['removeWatchingEventListeners']).toHaveBeenCalled();
      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'click', jasmine.any(Function));
    });

    it('should add eventListeners for mobile', () => {
      component.noHide = false;
      component['deviceService'].isDesktop = false;
      component['addWatchingEventListeners']();

      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'touchend', jasmine.any(Function));
      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'touchstart', jasmine.any(Function));
      expect(rendererService.renderer.listen).toHaveBeenCalledWith({}, 'touchmove', jasmine.any(Function));
    });
  });

  it('onTouchStart', () => {
    component.touchMoved = true;
    component['onTouchStart']();

    expect(component.touchMoved).toEqual(false);
  });

  it('onTouchMove', () => {
    component.touchMoved = false;
    component['onTouchMove']();

    expect(component.touchMoved).toEqual(true);
  });

  describe('get ngInfoPanelWithArrowClass', () => {
    it('should set css class for infoPanel with arrow top', () => {
      component['withArrowTop'] = true;
      component['withArrowBottom'] = false;
      component['noBgColor'] = false;
      expect(component['ngInfoPanelWithArrowClass']).toEqual(' arrow-panel top');
    });

    it('should set css class for infoPanel with arrow bottom', () => {
      component['withArrowTop'] = false;
      component['withArrowBottom'] = true;
      component['noBgColor'] = false;
      expect(component[ 'ngInfoPanelWithArrowClass' ]).toEqual(' arrow-panel bottom');
    });

    it('should set css class for infoPanel with arrow top', () => {
      component['withArrowTop'] = false;
      component['withArrowBottom'] = false;
      component['noBgColor'] = true;
      expect(component['ngInfoPanelWithArrowClass']).toEqual(' no-bg-color');
    });
  });

  describe('get ngInfoPanelClass', () => {
    it('should set css class for infoPanel without arrow', () => {
      component['align'] = 'center';
      expect(component['ngInfoPanelClass']).toEqual('center');
    });

    it('should set css class for infoPanel without arrow for quick deposit on betslip', () => {
      component['quickDepositPanel'] = true;
      expect(component['ngInfoPanelClass']).toEqual('undefined quick-deposit-info');
    });
  });

  describe('#checkRedirect', () => {
    it('should redirect if routerlink param is present', () => {
      const event = {
        target: {
          dataset: {
            routerlink: 'someLink'
          }
        }
      } as any;
      component['checkRedirect'](event);
      expect(router.navigateByUrl).toHaveBeenCalledWith('someLink');
    });
  });

  describe('#watchClick', () => {
    it('should not hide info panel', fakeAsync(() => {
      component['hideInfoPanel'] = jasmine.createSpy();
      component['watchClick']({} as any);
      expect(component['hideInfoPanel']).not.toHaveBeenCalled();
    }));
  });

  describe('#getMessageElem', () => {
    it('should replace href to data-routerlink', () => {
      component['getMessageElem']('href="123"');
      expect(domSanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith('data-routerlink="123"');
    });
  });
});

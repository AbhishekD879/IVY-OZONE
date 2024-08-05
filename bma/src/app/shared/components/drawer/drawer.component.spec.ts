import { DrawerComponent } from './drawer.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';

describe('DrawerComponent', () => {
  let windowRefService;
  let domToolsService;
  let deviceService;
  let changeDetectorRef;
  let pubSubService;
  let component: DrawerComponent;
  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout')
      },
      document: {}
    };
    domToolsService = {
      toggleClass: jasmine.createSpy('toggleClass'),
      getPageScrollTop: jasmine.createSpy('getPageScrollTop'),
      scrollPageTop: jasmine.createSpy('scrollPageTop')
    };
    deviceService = {};
    changeDetectorRef = {
      markForCheck: () => {}
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi,
      subscribe: jasmine.createSpy('publish')
    };

    component = new DrawerComponent(
      windowRefService,
      domToolsService,
      deviceService,
      changeDetectorRef,
      pubSubService
    );
  });

  it('ngOnInit', () => {
    component.showDrawer = jasmine.createSpy();

    component.show = false;
    component.ngOnInit();

    component.show = true;
    component.ngOnInit();

    expect(component.showDrawer).toHaveBeenCalledTimes(1);
  });

  it('ngOnChanges', () => {
    component.showDrawer = jasmine.createSpy();
    component.hideDrawer = jasmine.createSpy();
    component.contentClass = 'five-a-side pitch';

    component.ngOnChanges({} as any);

    component.show = false;
    component.ngOnChanges({ 'show': {} } as any);

    component.show = true;
    component.ngOnChanges({ 'show': {} } as any);

    expect(component.showDrawer).toHaveBeenCalledTimes(1);
    expect(component.hideDrawer).toHaveBeenCalledTimes(1);
  });

  it('ngOnDestroy', () => {
    component['toggleBodyClass'] = jasmine.createSpy();
    component.ngOnDestroy();
    expect(component['toggleBodyClass']).toHaveBeenCalledWith(false);
  });

  it('ngOnDestroy shouldn`t call toggleBodyClass method in removeBodyClassOnClose param is false', () => {
    component['toggleBodyClass'] = jasmine.createSpy();
    component.removeBodyClassOnClose = false;
    component.ngOnDestroy();
    expect(component['toggleBodyClass']).not.toHaveBeenCalled();
  });

  it('showDrawer', () => {
    const markForCheckSpy = spyOn(changeDetectorRef, 'markForCheck');
    component['saveScrollPosition'] = jasmine.createSpy();
    component['toggleBodyClass'] = jasmine.createSpy();
    component.shown.next = jasmine.createSpy();
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());

    component.visible = true;
    component.showDrawer();

    component.visible = false;
    component.showDrawer();

    expect(component['saveScrollPosition']).toHaveBeenCalledTimes(1);
    expect(component['toggleBodyClass']).toHaveBeenCalledTimes(1);
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledTimes(2);
    expect(component.shown.next).toHaveBeenCalledTimes(1);
    expect(markForCheckSpy).toHaveBeenCalled();
  });

  it('hideDrawer', () => {
    const markForCheckSpy = spyOn(changeDetectorRef, 'markForCheck');
    component['restoreScrollPosition'] = jasmine.createSpy();
    component['toggleBodyClass'] = jasmine.createSpy();
    component.hidden.next = jasmine.createSpy();
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());

    component.visible = true;
    component.hideDrawer();

    component.visible = false;
    component.hideDrawer();

    expect(component['toggleBodyClass']).toHaveBeenCalledTimes(1);
    expect(component['restoreScrollPosition']).toHaveBeenCalledTimes(1);
    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledTimes(1);
    expect(component.hidden.next).toHaveBeenCalledTimes(1);
    expect(markForCheckSpy).toHaveBeenCalled();
  });

  it('hideDrawer shouldn`t call toggleBodyClass method in removeBodyClassOnClose param is false', () => {
    spyOn(changeDetectorRef, 'markForCheck');
    component['restoreScrollPosition'] = jasmine.createSpy();
    component['toggleBodyClass'] = jasmine.createSpy();
    component.hidden.next = jasmine.createSpy();
    windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());
    component.removeBodyClassOnClose = false;

    component.visible = false;
    component.hideDrawer();

    expect(component['toggleBodyClass']).not.toHaveBeenCalled();
  });

  it('overlayClick', () => {
    component.hide.next = jasmine.createSpy();
    component.overlayClick();
    expect(component.hide.next).toHaveBeenCalledTimes(1);
  });

  it('closeClick', () => {
    component.hide.next = jasmine.createSpy();
    component.closeClick();
    expect(component.hide.next).toHaveBeenCalledTimes(1);
  });

  it('escPress', () => {
    component.hide.next = jasmine.createSpy();
    component.escPress();
    expect(component.hide.next).toHaveBeenCalledTimes(1);
  });

  describe('toggleBodyClass', () => {
    it('should not change body class if component is relative to parent', () => {
      component.relativeToParent = true;

      component['toggleBodyClass'](true);

      expect(domToolsService.toggleClass).not.toHaveBeenCalled();
    });

    it('should set body class as "drawer-visible" on non touch device', () => {
      deviceService.isTouch = false;

      component['toggleBodyClass'](true);

      expect(domToolsService.toggleClass).toHaveBeenCalledWith(
        windowRefService.document.body, 'drawer-visible', true
      );
    });

    it('should set body class as "drawer-visible-touch" on touch device', () => {
      deviceService.isTouch = true;
      component['toggleBodyClass'](false);
      expect(domToolsService.toggleClass).toHaveBeenCalledWith(
        windowRefService.document.body, 'drawer-visible-touch', false
      );
    });
  });



  it('saveScrollPosition', () => {
    deviceService.isTouch = true;
    component['saveScrollPosition']();

    deviceService.isTouch = false;
    component['saveScrollPosition']();

    expect(domToolsService.getPageScrollTop).toHaveBeenCalledTimes(1);
  });

  it('restoreScrollPosition', () => {
    deviceService.isTouch = true;
    component['restoreScrollPosition']();

    deviceService.isTouch = false;
    component['restoreScrollPosition']();

    expect(domToolsService.scrollPageTop).toHaveBeenCalledTimes(1);
  });

  it('ngOnChanges - should call publish if contentClass has verdict-nw', () => {
    component.showDrawer = jasmine.createSpy();
    component.hideDrawer = jasmine.createSpy();
    component.show = true;
    component.contentClass = 'verdict-nw';
    component.ngOnChanges({ 'show': {} } as any);

    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('ngOnChanges - should not publish if contentClass has no verdict-nw', () => {
    component.showDrawer = jasmine.createSpy();
    component.hideDrawer = jasmine.createSpy();
    component.show = true;
    component.contentClass = 'edit';
    component.ngOnChanges({ 'show': {} } as any);

    expect(pubSubService.publish).not.toHaveBeenCalled();
  });

  it('ngOnChanges - should not publish if contentClass is null', () => {
    component.showDrawer = jasmine.createSpy();
    component.hideDrawer = jasmine.createSpy();
    component.show = true;
    component.contentClass = null;
    component.ngOnChanges({ 'show': {} } as any);

    expect(pubSubService.publish).not.toHaveBeenCalled();
  });

  it('ngOnChanges show false- should call publish if contentClass is non verdict-nw', () => {
    component.showDrawer = jasmine.createSpy();
    component.hideDrawer = jasmine.createSpy();
    component.show = false;
    component.contentClass = 'verdict-nw';
    component.ngOnChanges({ 'show': {} } as any);

    expect(pubSubService.publish).toHaveBeenCalled();
  });

  it('ngOnChanges show false- should call publish if contentClass is non verdict-nw', () => {
    component.showDrawer = jasmine.createSpy();
    component.hideDrawer = jasmine.createSpy();
    component.show = false;
    component.contentClass = 'edit';
    component.ngOnChanges({ 'show': {} } as any);

    expect(pubSubService.publish).not.toHaveBeenCalled();
  });

  it('ngOnChanges show false- should call publish if contentClass is null', () => {
    component.showDrawer = jasmine.createSpy();
    component.hideDrawer = jasmine.createSpy();
    component.show = false;
    component.contentClass = null;
    component.ngOnChanges({ 'show': {} } as any);

    expect(pubSubService.publish).not.toHaveBeenCalled();
  });

  describe('#isCoralMobile on ngOnInit', () => {
    it('should set to isCoralMobile to true when brand and platform matches', () => {
      environment.brand = 'bma'; environment.CURRENT_PLATFORM = 'mobile';
      component.ngOnInit();
      expect(component.isCoralMobile).toBeTruthy();
    });
    it('should set to isCoralMobile to false when platform is desktop', () => {
      environment.brand = 'bma'; environment.CURRENT_PLATFORM = 'desktop';
      component.ngOnInit();
      expect(component.isCoralMobile).toBeFalsy();
    });
    it('should set to isCoralMobile to false when brand is ladbrokes', () => {
      environment.brand = 'ladbrokes'; environment.CURRENT_PLATFORM = 'desktop';
      component.ngOnInit();
      expect(component.isCoralMobile).toBeFalsy();
    });
  });
});

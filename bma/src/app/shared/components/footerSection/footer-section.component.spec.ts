import { FooterSectionComponent } from '@shared/components/footerSection/footer-section.component';

describe('FooterSectionComponent', () => {
  const title = 'footerSection';

  let component: FooterSectionComponent;
  let windowRefService;
  let commandService;
  let pubSubService;
  let filtersService;
  let deviceService;
  let changeDetectorRef;

  beforeEach(() => {
    windowRefService = {
      document: {
        body: {},
        querySelector: jasmine.createSpy('querySelector').and.returnValue({})
      },
      nativeWindow: {
        clearInterval: jasmine.createSpy('clearInterval'),
        setInterval: jasmine.createSpy('setInterval').and.callFake((fn: Function) => fn())
      }
    };
    commandService = {
      register: jasmine.createSpy('register').and.callFake((a, cb) => cb(true)),
      API: {
        TOGGLE_FOOTER_MENU: 'TOGGLE_FOOTER_MENU',
        SHOW_HIDE_FOOTER_MENU: 'SHOW_HIDE_FOOTER_MENU'
      }
    };
    pubSubService = {
      API: {
        TOGGLE_MOBILE_HEADER_FOOTER: 'TOGGLE_MOBILE_HEADER_FOOTER',
        LOGIN_COUNTER_UPDATE: 'LOGIN_COUNTER_UPDATE',
        SESSION_LOGOUT: 'SESSION_LOGOUT',
        SESSION_LOGIN: 'SESSION_LOGIN',
        QUICK_SWITCHER_ACTIVE: 'QUICK_SWITCHER_ACTIVE'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb(1)),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy()
    };
    filtersService = {
      date: jasmine.createSpy()
    };
    deviceService = {
      isMobile: true
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy(),
    };
    component = new FooterSectionComponent(
      filtersService,
      windowRefService,
      commandService,
      pubSubService,
      deviceService,
      changeDetectorRef
    );
  });


  it('toggleFooterVisibility', () => {
    expect(component.showFooter).toBe(true);
    component['toggleFooterVisibility'](false);
    expect(component.showFooter).toBe(false);
    expect(component['changeDetectorRef'].detectChanges).toHaveBeenCalled();
  });

  it('toogleFooterMenu', () => {
    expect(component.showFooterMenu).toBe(true);
    component['toogleFooterMenu'](false);
    expect(component.showFooterMenu).toBe(false);
    expect(component['changeDetectorRef'].detectChanges).toHaveBeenCalled();
  });

  it('handleSessionEnd', () => {
    expect(component.clock.visible).toBe(false);
    component['handleSessionEnd']();
    expect(component.clock.visible).toBe(false);
    expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
  });

  describe('updateSessionCounter', () => {
    beforeEach(() => {
      component['formatSessionTimeValue'] = jasmine.createSpy('formatSessionTimeValue');
    });

    it('#session-timer exist', () => {
      component['updateSessionCounter'](3600);
      expect(component['formatSessionTimeValue']).toHaveBeenCalledWith(3600);
    });

    it('#session-timer does not exist', () => {
      windowRefService.document.querySelector.and.returnValue(null);
      component['updateSessionCounter'](3600);
      expect(component['formatSessionTimeValue']).not.toHaveBeenCalled();
    });
  });

  it('formatSessionTimeValue', () => {
    expect(component['formatSessionTimeValue'](86400)).toBe('1 day 00:00');
    expect(component['formatSessionTimeValue'](10411200)).toBe('120 days 12:00:00');
    expect(component['formatSessionTimeValue'](0)).toBe('00:00');
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(commandService.register).toHaveBeenCalledWith(commandService.API.TOGGLE_FOOTER_MENU, jasmine.any(Function));
    expect(commandService.register).toHaveBeenCalledWith(commandService.API.SHOW_HIDE_FOOTER_MENU, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.QUICK_SWITCHER_ACTIVE, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(title, pubSubService.API.LOGIN_COUNTER_UPDATE, jasmine.any(Function));
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
        title, [pubSubService.API.SESSION_LOGOUT, pubSubService.API.SESSION_LOGIN], jasmine.any(Function)
    );
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
  });
});

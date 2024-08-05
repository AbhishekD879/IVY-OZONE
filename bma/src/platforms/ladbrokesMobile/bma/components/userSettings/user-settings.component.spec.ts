import { of } from 'rxjs';
import { LadbrokesUserSettingsComponent } from './user-settings.component';

describe('LadbrokesUserSettingsComponent', () => {
  let userService;
  let nativeBridgeService;
  let pubSubService;
  let deviceService;
  let cmsService;
  let sessionService;
  let router;
  let component: LadbrokesUserSettingsComponent;
  let gtmService;
  let locale;
  let arcUserService;
  let upms;

  beforeEach(() => {
    userService = {
      oddsFormat: 'frac',
      set: jasmine.createSpy(),
      setTouchIdLogin: jasmine.createSpy(),
      getTouchIdLogin: jasmine.createSpy(),
      quickBetNotification: true,
      timeline: true
    };
    nativeBridgeService = {
      sendReport: jasmine.createSpy(),
      touchIDSettingsUpdate: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        TIMELINE_SETTINGS_CHANGE: 'TIMELINE_SETTINGS_CHANGE'
      }
    };
    deviceService = {
      osName: '',
      isWrapper: true,
      isAndroid: false
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({})),
      getFeatureConfig: jasmine.createSpy().and.returnValue(of({}))
    };
    sessionService = {
      whenSession: jasmine.createSpy().and.returnValue(of(null))
    };
    router = {
      navigate: jasmine.createSpy()
    };
    gtmService = {
      push: jasmine.createSpy('gtm')
    };
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('coral pulse')
    };
    arcUserService = {
      quickbet: true
    };
    component = new LadbrokesUserSettingsComponent(
      userService,
      nativeBridgeService,
      pubSubService,
      deviceService,
      cmsService,
      sessionService,
      router,
      gtmService,
      locale,
      arcUserService,
      upms
    );
  });


  it('setSetting', () => {
    component['deviceService'].osName = 'Android';

    component.config = {
      quickBet: { EnableQuickBet: true },
      NativeConfig: { visibleDiagnosticsButton: ['android'] },
      FeatureToggle: { Timeline: null }
    } as any;
    spyOn(component, 'checkArcUser');
    component.setSetting();

    expect(component.oddsFormat).toBe(userService.oddsFormat);
    expect(userService.getTouchIdLogin).toHaveBeenCalled();
    expect(component.allowQuickBetNotifications).toBeTruthy();

    expect(component.timelineObj).toEqual({
      status: userService.timeline
    });

    expect(component.switchers).toEqual([{
      name: 'bma.userSettingsOddsFormatFrac',
      onClick: jasmine.any(Function),
      viewByFilters: 'frac'
    }, {
      name: 'bma.userSettingsOddsFormatDec',
      onClick: jasmine.any(Function),
      viewByFilters: 'dec'
    }]);
  });

  it('setSetting (wrapper)', () => {
    component['deviceService'].isWrapper = true;
    component['deviceService'].isAndroid = true;
    component['deviceService'].isMobile = true;
    component['deviceService'].osName = 'Android';
    component['nativeBridgeService'] = { touchIDConfigured: true } as any;
    component.config = {
      quickBet: {},
      NativeConfig: { visibleDiagnosticsButton: ['android'] },
      FeatureToggle: { Timeline: {} }
    } as any;
    spyOn(component, 'checkArcUser');
    component.setSetting();

    expect(component.oddsFormat).toBe(userService.oddsFormat);
    expect(userService.getTouchIdLogin).toHaveBeenCalled();
    expect(component.allowQuickBetNotifications).toBeFalsy();

    expect(component.switchers).toEqual([{
      name: 'bma.userSettingsOddsFormatFrac',
      onClick: jasmine.any(Function),
      viewByFilters: 'frac'
    }, {
      name: 'bma.userSettingsOddsFormatDec',
      onClick: jasmine.any(Function),
      viewByFilters: 'dec'
    }]);

    expect(component.isAndroid).toBeTruthy();
    expect(component.touchIDConfiguredShow).toBeTruthy();
    expect(component.showDiagnostics).toBeTruthy();
  });

  it('setTouchIdLogin', () => {
    const value = 'enabled';
    component.setTouchIdLogin(value);
    expect(component.touchIdLogin).toBe(value);
    expect(userService.setTouchIdLogin).toHaveBeenCalledWith(value);
    expect(nativeBridgeService.touchIDSettingsUpdate).toHaveBeenCalledWith(true);
  });

  it('setTouchIdLoginLad', () => {
    const value = true;
    component.setTouchIdLoginLad(value);
    expect(component.touchIdLoginLad).toBe(value);
    expect(userService.setTouchIdLogin).toHaveBeenCalledWith(value ? 'enabled' : 'disabled');
    expect(nativeBridgeService.touchIDSettingsUpdate).toHaveBeenCalledWith(value);
  });

  it('changeQuickBetSetting', () => {
    component.changeQuickBetSetting(true);
    expect(userService.set).toHaveBeenCalledWith({ quickBetNotification: true });
  });

  it('sendReport', () => {
    component.sendReport();
    expect(nativeBridgeService.sendReport).toHaveBeenCalled();
  });
});

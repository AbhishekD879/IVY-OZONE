import { throwError, of, of as observableOf } from 'rxjs';
import { UserSettingsComponent } from './user-settings.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('#UserSettingsComponent', () => {
  let userService;
  let nativeBridgeService;
  let pubSubService;
  let deviceService;
  let cmsService;
  let sessionService;
  let router;
  let gtmService;
  let locale;
  let arcUserService;
  let upms;
  let component: UserSettingsComponent;

  const config = {};

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
        SET_ODDS_FORMAT: 'SET_ODDS_FORMAT',
        TIMELINE_SETTINGS_CHANGE: 'TIMELINE_SETTINGS_CHANGE'
      }
    };
    deviceService = {
      osName: '',
      isWrapper: true,
      isAndroid: true,
      isTablet: false,
      isDesktop: false,
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of(config)),
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
    upms = {
      setOddsPreference: jasmine.createSpy('setOddsPreference').and.returnValue(observableOf({preferences:{oddPreference:'frac'}}))
    }

    component = new UserSettingsComponent(
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

  it('isTabletOrDesktop', () => {
    expect(component.isTabletOrDesktop).toBeFalsy();

    deviceService.isTablet = true;
    component = new UserSettingsComponent(
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
    expect(component.isTabletOrDesktop).toBeTruthy();

    deviceService.isTablet = false;
    deviceService.isDesktop = true;
    component = new UserSettingsComponent(
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
    expect(component.isTabletOrDesktop).toBeTruthy();
  });

  it('#ngOnInit ', fakeAsync(() => {
      component.setSetting = jasmine.createSpy('setSetting');
      component.hideSpinner = jasmine.createSpy('hideSpinner');

      sessionService.whenSession.and.returnValue(Promise.resolve(true));


      component.ngOnInit();
      tick();
      expect(cmsService.getSystemConfig).toHaveBeenCalledWith(true);
      expect(cmsService.getFeatureConfig).toHaveBeenCalledWith('NativeConfig', false, true);
      expect(component.setSetting).toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();
    })
  );

  it('ngOnInit (logged out)', () => {
    sessionService.whenSession.and.returnValue(throwError(null));

    component.ngOnInit();

    expect(sessionService.whenSession).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalledWith(['/']);
  });

  it('setSetting', () => {
    component['deviceService'].osName = 'Android';
    component.config = {
      quickBet: {EnableQuickBet: true},
      NativeConfig: { visibleDiagnosticsButton: ['android'] }
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

  it(`should call setOddFormat on switchers onClick`, () => {
    spyOn(component as any, 'setOddsFormat');
    component.config = {
      quickBet: {EnableQuickBet: true},
      NativeConfig: {visibleDiagnosticsButton: ['android']}
    } as any;

    component['setSetting']();
    component['switchers'][0].onClick();
    component['switchers'][1].onClick();
    expect(component['setOddsFormat']).toHaveBeenCalledTimes(2);
  });

  it('setSetting (wrapper)', () => {
    component['deviceService'].isWrapper = true;
    component['deviceService'].isAndroid = true;
    component['deviceService'].osName = 'Android';
    component['nativeBridgeService'] = {touchIDConfigured: true} as any;
    component.config = {
      quickBet: {},
      NativeConfig: {visibleDiagnosticsButton: ['android']}
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

  it('setOddsFormat', () => {
    const value = 'frac';
    component.setOddsFormat(value);
    expect(component.oddsFormat).toBe(value);
    expect(userService.set).toHaveBeenCalledWith({oddsFormat: value});
    expect(pubSubService.publish).toHaveBeenCalledWith('SET_ODDS_FORMAT', value);
  });
  it('setOddsFormat with oddsFormat and settingValue equal', () => {
    const value = 'frac';
    component.oddsFormat = 'frac';
    expect(component.setOddsFormat(value)).toBeUndefined();
  });
  
  it('setTouchIdLogin', () => {
    const value = 'enabled';
    component.setTouchIdLogin(value);
    expect(component.touchIdLogin).toBe(value);
    expect(userService.setTouchIdLogin).toHaveBeenCalledWith(value);
    expect(nativeBridgeService.touchIDSettingsUpdate).toHaveBeenCalledWith(true);
  });

  it('changeQuickBetSetting', () => {
    component.changeQuickBetSetting(true);
    expect(userService.set).toHaveBeenCalledWith({quickBetNotification: true});
  });

  it('sendReport', () => {
    component.sendReport();
    expect(nativeBridgeService.sendReport).toHaveBeenCalled();
  });

  it('changeTimelineSetting', () => {
    component.changeTimelineSetting(true);

    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventAction : 'betting settings',
      eventCategory : 'coral pulse',
      eventLabel: 'toggle on'
    });
    expect(userService.set).toHaveBeenCalledWith({ timeline: true });
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.TIMELINE_SETTINGS_CHANGE);
  });

  it('changeTimelineSetting false', () => {
    component.changeTimelineSetting(false);

    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventAction : 'betting settings',
      eventCategory : 'coral pulse',
      eventLabel: 'toggle off'
    });
    expect(userService.set).toHaveBeenCalledWith({ timeline: false });
  });
  describe('checkArcUser', () => {
    it('should not allow quickbet', () => {
      arcUserService.quickbet = true;
      component['checkArcUser']();
      expect(component.quickBetNotificationObj).toEqual({
        status: false
      });
    })
    it('should allow quickbet', () => {
      arcUserService.quickbet = false;
      component['checkArcUser']();
      expect(component.quickBetNotificationObj).toEqual({
        status: userService.quickBetNotification
      });
    })
  });
});

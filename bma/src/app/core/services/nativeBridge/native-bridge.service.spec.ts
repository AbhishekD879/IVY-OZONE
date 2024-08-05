import { NavigationEnd } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';
import * as _ from 'underscore';

import { ReplaySubject, Subject, of } from 'rxjs';
import { NativeBridgeService } from './native-bridge.service';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('NativeBridgeService', () => {
  let service: NativeBridgeService;
  let command;
  let document;
  let documentCbMap;
  let windowRef;
  let pubsub;
  let user;
  let router;
  let deviceService;

  beforeEach(() => {
    command = {
      API: commandApi,
      execute: jasmine.createSpy(),
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve())
    };
    documentCbMap = {};
    document = document = {
      __listenersList: {} as { [key: string]: Function [] },
      addEventListener: jasmine.createSpy('addEventListener').and.callFake((eventName: string, callback: any) => {
        document.__listenersList[eventName] = document.__listenersList[eventName] || [];
        document.__listenersList[eventName].push(callback);
        documentCbMap[eventName] = callback;
      }),
      dispatchEvent: (event: CustomEvent) => {
        const listenerCallbacks = document.__listenersList ? document.__listenersList[event.type] : [];
        if (listenerCallbacks) {
          listenerCallbacks.forEach((callback) => {
            callback(event);
          });
        }
      },
      createElement: jasmine.createSpy().and.returnValue(window.document.createElement('iframe')),
      body: {
        appendChild: jasmine.createSpy(),
        removeChild: jasmine.createSpy()
      }
    };
    deviceService = {
      isIos: true
    };
    windowRef = {
      document: {},
      nativeWindow: {
        document: {},
        NativeBridge: {
          betSlipCloseAnimationDuration: 100,
          touchIDConfigured: true,
          betSelections: [{}],
          favourites: [{}, {}],
          creferer: true,
          profileid: 10,
          eventStartTime: '10:10',
          playerStatus: true,
          showUserBalanceValue: true,
          isNativePage: true,
          pushNotificationsEnabled: true,
          isRemovingGamingEnabled: true,
          login: jasmine.createSpy(),
          loginSalesForce: jasmine.createSpy(),
          loginWithTouchID: jasmine.createSpy(),
          openNativeLoginDialog: jasmine.createSpy(),
          touchIDLoginFailed: jasmine.createSpy(),
          onFingerPrintLoginFailed: jasmine.createSpy(),
          touchIDSettingsUpdate: jasmine.createSpy(),
          syncPlayerBetSlip: jasmine.createSpy(),
          logout: jasmine.createSpy(),
          deposit: jasmine.createSpy(),
          accaNotificationChanged: jasmine.createSpy(),
          showVideoStreamV2: jasmine.createSpy(),
          pauseVideo: jasmine.createSpy(),
          registrationStarted: jasmine.createSpy(),
          registrationFinished: jasmine.createSpy(),
          registrationFinishedSalesForce: jasmine.createSpy(),
          passwordChanged: jasmine.createSpy(),
          onEventAlertsClick: jasmine.createSpy(),
          showFootballAlerts: jasmine.createSpy(), // TODO: Reverted changes from BMA-37049.
          // Will be removed after new approach implementation.
          onCloseBetSlip: jasmine.createSpy(),
          onOpenBetSlip: jasmine.createSpy(),
          onGaming: jasmine.createSpy(),
          onCloseLoginDialog: jasmine.createSpy(),
          getBuildVersion: jasmine.createSpy(),
          betPlaceSuccessful: jasmine.createSpy(),
          onOpenPopup: jasmine.createSpy(),
          onClosePopup: jasmine.createSpy(),
          onLoginPopupsEnd: jasmine.createSpy(),
          onFeaturedTabClicked: jasmine.createSpy(),
          onCookieBannerClosed: jasmine.createSpy(),
          onRightMenuClick: jasmine.createSpy(),
          onFreeBetUpdated: jasmine.createSpy(),
          onFreeBetUpdatedV2: jasmine.createSpy(),
          onBalanceChanged: jasmine.createSpy(),
          showErrorForNative: jasmine.createSpy(),
          eventPageLoaded: jasmine.createSpy(),
          footballEventPageLoaded: jasmine.createSpy(), // TODO: Reverted changes from BMA-37049.
          // Will be removed after new approach implementation.
          pageLoaded: jasmine.createSpy(),
          onUrlChanged: jasmine.createSpy(),
          wrapperSendDiagnostics: jasmine.createSpy(),
          loginSessionToken: jasmine.createSpy(),
          loginError: jasmine.createSpy(),
          onSessionLimitChanged: jasmine.createSpy(),
          showUserBalance: jasmine.createSpy(),
          arePrivateMarketsAvailable: jasmine.createSpy(),
          syncFavourites: jasmine.createSpy(),
          showPolicyBanner: jasmine.createSpy(),
          onEventDetailsStreamAvailable: jasmine.createSpy(),
          checkConnect: jasmine.createSpy(),
          checkGrid: jasmine.createSpy(),
          onVirtualsSelected: jasmine.createSpy(),
          onUserAction: jasmine.createSpy(),
          onActivateWinAlerts: jasmine.createSpy(),
          showNotificationSettings: jasmine.createSpy(),
          hideSplashScreen: jasmine.createSpy(),
          syncBetSlip: jasmine.createSpy(),
          onOddsSettingsChanged: jasmine.createSpy(),
          goToPage: jasmine.createSpy(),
          onVideoPlayerExpanded: jasmine.createSpy('onVideoPlayerExpanded'),
          onMatchAlertsClick: jasmine.createSpy(),
          multipleEventPageLoaded: jasmine.createSpy(),
          winAlertsStatus: jasmine.createSpy(),
          disableWinAlertsStatus: jasmine.createSpy(),
          onClearCache: jasmine.createSpy(),
          networkIndicatorEnabled: jasmine.createSpy('networkIndicatorEnabled'),
          isWrapperSubject: new ReplaySubject(),
          displayInLandscapeMode: jasmine.createSpy(),
          shareContentOnSocialMediaGroups: jasmine.createSpy()
        },
        setTimeout: jasmine.createSpy().and.callFake(callback => {
          callback && callback();
        }),
        clearTimeout: jasmine.createSpy(),
        navigator: {
          userAgent: 'android'
        },
        location: {
          href: 'url',
        }
      }
    };
    pubsub = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      publish: jasmine.createSpy('publish')
    };
    user = {
      showBalance: false,
      setTouchIdLogin: jasmine.createSpy(),
      sessionToken: '3fwerasgv4234123dgsfdg',
      status: true
    };
    router = {
      events: new Subject()
    };

    spyOn(console, 'warn');
    service = new NativeBridgeService(command, document, windowRef, pubsub, user, router, deviceService);
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should init', () => {
    service.init();
    expect(pubsub.subscribe).toHaveBeenCalledWith('nativeBridgeFactory', 'SET_ODDS_FORMAT', jasmine.any(Function));
    expect(pubsub.subscribe).toHaveBeenCalledWith('nativeBridgeFactory', pubsub.API.SYNC_BETSLIP_TO_NATIVE, jasmine.any(Function));
    expect(pubsub.subscribe).toHaveBeenCalledWith('nativeBridgeFactory', 'USER_BALANCE_SHOW', jasmine.any(Function));
    expect(pubsub.subscribe).toHaveBeenCalledWith('nativeBridgeFactory', pubsub.API.SYNC_FAVOURITES_TO_NATIVE, jasmine.any(Function));
    expect(command.executeAsync).toHaveBeenCalledWith(command.API.BETSLIP_READY);
  });

  describe('when streamAndBetPlaced event occurs, should call pubsub BETS_COUNTER_PLACEBET', () => {
    beforeEach(() => {
      service.init();
    });

    it('should add event listeners to the document', () => {
      expect(document.addEventListener.calls.allArgs()).toEqual([
        ['CURRENT_WATCH_LIVE_STATE_CHANGED', jasmine.any(Function)],
        ['syncBetSlip', jasmine.any(Function)],
        ['CHANGE_BET_SLIP_SLIDE_STATE', jasmine.any(Function)],
        ['syncFavourites', jasmine.any(Function)],
        ['openPromotionWithType', jasmine.any(Function)],
        ['showOptInSplashScreen', jasmine.any(Function)],
        ['showMarketingPreferencePage', jasmine.any(Function)],
        ['ADD_TO_QUICKBET', jasmine.any(Function)],
        ['virtualSportSelected', jasmine.any(Function)],
        ['streamAndBetPlaced', jasmine.any(Function)],
        ['onCookieBannerAccept', jasmine.any(Function)],
        ['onCheckConnectReceived', jasmine.any(Function)],
        ['onCheckGridReceived', jasmine.any(Function)],
        ['onOrientationChanged', jasmine.any(Function)],
        ['TOUCH_ID_CHANGED', jasmine.any(Function)],
        ['videoPlayerCollapsed', jasmine.any(Function)],
        ['updateBalance', jasmine.any(Function)],
        ['onBuildVersionReceived', jasmine.any(Function)],
        ['onBetSharingCompleted', jasmine.any(Function)]
      ]);
    });
    describe('with 0', () => {
      it('when no event detail is available ', () => {
        documentCbMap['streamAndBetPlaced']({});
      });
      it('when no placedBetsCount data is available ', () => {
        documentCbMap['streamAndBetPlaced']({ detail: {} });
      });
      afterEach(() => {
        expect(pubsub.publish).toHaveBeenCalledWith('BETS_COUNTER_PLACEBET', 0);
      });
    });
    it('with placedBetsCount value, when this information is available', () => {
      documentCbMap['streamAndBetPlaced']({ detail: { placedBetsCount: 3 }});
      expect(pubsub.publish).toHaveBeenCalledWith('BETS_COUNTER_PLACEBET', 3);
    });
  });
  it('when videoPlayerCollapsed event occurs, should call pubsub IS_NATIVE_VIDEO_STICKED', () => {
    service.init();
    documentCbMap['videoPlayerCollapsed']({ detail: { state: true }});
    expect(pubsub.publish).toHaveBeenCalledWith('IS_NATIVE_VIDEO_STICKED', false);
  });

  it('when onBetSharingCompleted event occurs, should call pubsub BET_SHARING_COMPLETED', () => {
    const data = "test"
    service.init();
    documentCbMap['onBetSharingCompleted'](data);
    expect(pubsub.publish).toHaveBeenCalledWith('BET_SHARING_COMPLETED', data);
  });

  it('when updateBalance event occurs, should call pubsub IMPLICIT_BALANCE_REFRESH', () => {
    service.init();
    documentCbMap['updateBalance']();
    expect(pubsub.publish).toHaveBeenCalledWith('IMPLICIT_BALANCE_REFRESH');
  });

  describe('addEventListener', () => {
    it('CURRENT_WATCH_LIVE_STATE_CHANGED', () => {
      service.init();
      const event = new CustomEvent('CURRENT_WATCH_LIVE_STATE_CHANGED', {detail: {settingValue: true}});
      document.dispatchEvent(event);
      expect(service.playerStatus).toBeTruthy();
    });

    it('syncBetSlip', () => {
      service.init();
      service['syncBetSlipFromNative'] = jasmine.createSpy();
      const event = new CustomEvent('syncBetSlip');
      document.dispatchEvent(event);
      expect(service['syncBetSlipFromNative']).toHaveBeenCalled();
    });

    it('CHANGE_BET_SLIP_SLIDE_STATE', () => {
      service.init();
      service['openSlideOutBetSlip'] = jasmine.createSpy();
      const event = new CustomEvent('CHANGE_BET_SLIP_SLIDE_STATE');
      document.dispatchEvent(event);
      expect(service['openSlideOutBetSlip']).toHaveBeenCalled();
    });

    it('syncFavourites', () => {
      service.init();
      service['syncFavouritesFromNative'] = jasmine.createSpy();
      const event = new CustomEvent('syncFavourites');
      document.dispatchEvent(event);
      expect(service['syncFavouritesFromNative']).toHaveBeenCalled();
    });

    it('openPromotionWithType', () => {
      service.init();
      const event = new CustomEvent('openPromotionWithType', {detail: {settingValue: true}});
      document.dispatchEvent(event);
      const args = command.executeAsync.calls.allArgs();
      expect(command.executeAsync).toHaveBeenCalledTimes(2);
      expect(args.length).toEqual(2);
      expect(args[0]).toEqual([command.API.BETSLIP_READY]);
      expect(args[1]).toEqual([command.API.PROMOTIONS_SHOW_OVERLAY, Array(event.detail.settingValue), 'defaultResult']);
    });

    it('showOptInSplashScreen', () => {
      service.init();
      service['showOptInSplashScreen'] = jasmine.createSpy();
      const event = new CustomEvent('showOptInSplashScreen');
      document.dispatchEvent(event);
      expect(service['showOptInSplashScreen']).toHaveBeenCalled();
    });

    it('showMarketingPreferencePage', () => {
      service.init();
      service['showMarketingPreferencePage'] = jasmine.createSpy();
      const event = new CustomEvent('showMarketingPreferencePage');
      document.dispatchEvent(event);
      expect(service['showMarketingPreferencePage']).toHaveBeenCalled();
    });

    it('ADD_TO_QUICKBET', () => {
      service.init();
      service['showOptInSplashScreen'] = jasmine.createSpy();
      const event = new CustomEvent('ADD_TO_QUICKBET', {detail: {selectionId: 1}});
      document.dispatchEvent(event);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.SYNC_NATIVE_QUICKBET_SELECTION, 1);
    });

    it('virtualSportSelected', () => {
      service.init();
      service['showOptInSplashScreen'] = jasmine.createSpy();
      const event = new CustomEvent('virtualSportSelected', {detail: 'test'});
      document.dispatchEvent(event);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.VIRTUAL_ORIENTATION_CHANGED, 'test');
    });

    it('onCheckConnectReceived', () => {
      service.init();
      const event = new CustomEvent('onCheckConnectReceived', {detail: 'test'});
      document.dispatchEvent(event);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.CHECK_RETAIL_NATIVE, 'test');
    });

    it('onCheckGridReceived', () => {
      service.init();
      const event = new CustomEvent('onCheckGridReceived', {detail: 'test'});
      document.dispatchEvent(event);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.CHECK_RETAIL_NATIVE, 'test');
    });

    it('onOrientationChanged', () => {
      service.init();
      const event = new CustomEvent('onOrientationChanged', {detail: 'test'});
      document.dispatchEvent(event);
      expect(pubsub.publish).toHaveBeenCalledWith(pubsub.API.ORIENTATION_CHANGED, 'test');
    });

    it('TOUCH_ID_CHANGED', () => {
      const data = {
        detail: {
          settingValue: 'test'
        }
      };
      service.init();
      const event = new CustomEvent('TOUCH_ID_CHANGED', data);
      document.dispatchEvent(event);
      expect(user.setTouchIdLogin).toHaveBeenCalledWith(data.detail.settingValue);
    });
  });

  it('should hide splash screen', () => {
    pubsub.subscribe.and.callFake((name, api, cb) => {
      cb({});
    });
    spyOn(_, 'isFunction').and.returnValue(true);
    service['hideSplashScreen'] = jasmine.createSpy();
    service.init();
    expect(pubsub.subscribe).toHaveBeenCalledWith(
      'nativeBridgeFactory', pubsub.API.APP_IS_LOADED, jasmine.any(Function));
    expect(service['hideSplashScreen']).toHaveBeenCalled();
  });

  it('sholud call onOddsSettingsChanged', () => {
    pubsub.subscribe.and.callFake((subscriber, key, fn) => fn('frac'));
    spyOn<any>(service, 'onOddsSettingsChanged');
    service.init();
    expect(pubsub.subscribe).toHaveBeenCalledWith(
      'nativeBridgeFactory', 'SET_ODDS_FORMAT', jasmine.any(Function));
    expect(service['onOddsSettingsChanged']).toHaveBeenCalled();
  });

  it('sholud call syncBetSlipToNative', () => {
    const callbacks = {};

    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    spyOn<any>(service, 'syncBetSlipToNative');
    service.init();
    callbacks['SYNC_BETSLIP_TO_NATIVE']();
    expect(service['syncBetSlipToNative']).toHaveBeenCalled();
  });

  it('sholud call showUserBalance', () => {
    const callbacks = {};

    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    spyOn<any>(service, 'showUserBalance');
    service.init();
    callbacks['USER_BALANCE_SHOW']();
    expect(service['showUserBalance']).toHaveBeenCalled();
  });

  it('sholud call syncFavouritesToNative', () => {
    const callbacks = {};

    pubsub.subscribe.and.callFake((subscriber, key, fn) => {
      callbacks[key] = fn;
    });
    spyOn<any>(service, 'syncFavouritesToNative');
    service.init();
    callbacks['SYNC_FAVOURITES_TO_NATIVE']();
    expect(service['syncFavouritesToNative']).toHaveBeenCalled();
  });

  it('should change url', fakeAsync(() => {
    service.init();
    service.onUrlChanged = jasmine.createSpy();
    router.events.next(new NavigationEnd(1, 'url', 'urlAfterRedirects'));
    tick(501);
    expect(service.onUrlChanged).toHaveBeenCalled();
  }));

  it('displayInLandscapeMode', () => {
    service.isWrapper = true;
    spyOn(_, 'isFunction').and.returnValue(true);
    service['displayInLandscapeMode']();
    expect(windowRef.nativeWindow.NativeBridge.displayInLandscapeMode).toHaveBeenCalled();
  });

  describe('get/set bridge values', () => {
    beforeEach(() => {
      service.init();
    });

    it('should get isWrapperStream', () => {
      const streamWrapper = of(true);
      service['isWrapperSubject'].asObservable = jasmine.createSpy().and.returnValue(streamWrapper);
      expect(service.isWrapperStream).toBe(streamWrapper);
      expect(service['isWrapperSubject'].asObservable).toHaveBeenCalled();
    });

    it('should get duration for close betslip sidebar animation', () => {
      expect(service.betSlipCloseAnimationDuration).toBe(100);
    });

    it('touchIDConfigured should be true if touchIDConfigured === "true"', () => {
      windowRef.nativeWindow.NativeBridge.touchIDConfigured = 'true';
      expect(service.touchIDConfigured).toBe(true);
    });

    it('touchIDConfigured should be true if touchIDConfigured === true', () => {
      windowRef.nativeWindow.NativeBridge.touchIDConfigured = true;
      expect(service.touchIDConfigured).toBe(true);
    });

    it('touchIDConfigured should be false if touchIDConfigured === "false"', () => {
      windowRef.nativeWindow.NativeBridge.touchIDConfigured = 'false';
      expect(service.touchIDConfigured).toBe(false);
    });

    it('touchIDConfigured should be false if not wrapper', () => {
      service.isWrapper = false;
      expect(service.touchIDConfigured).toBe(false);
    });

    it('should get bet selections', () => {
      expect(service.betSelections.length).toBe(1);
    });

    it('should get favourites', () => {
      expect(service.favourites.length).toBe(2);
    });

    it('should get NativeBridge creferer value', () => {
      expect(service.creferer).toBe(true);
    });

    it('should get profile id', () => {
      expect(service.profileid).toBe(10);
    });

    it('should get event start time', () => {
      expect(service.eventStartTime).toBe('10:10');
    });

    it('should set event start time', () => {
      service.eventStartTime = '11:00';
      expect(service.eventStartTime).toBe('11:00');
    });

    it('should get player status', () => {
      expect(service.playerStatus).toBe(true);
    });

    it('should set player status', () => {
      service.playerStatus = false;
      expect(service.playerStatus).toBe(false);
    });

    it('should get isNativePage value', () => {
      expect(service.isNativePage).toBe(true);
    });

    it('should get isMobengaWrapper value', () => {
      expect(service.isMobengaWrapper).toBe(undefined);
      service['windowRef'] = <any>{
        document: {
          Native: true
        },
        nativeWindow: {}
      };
      expect(service.isMobengaWrapper).toBeTruthy();
    });

    it('should get openNativeLoginDialog value', () => {
      expect(service.isLoginDialog()).toBe(true);
    });

    it('should get pushNotificationsEnabled value', () => {
      expect(service.pushNotificationsEnabled).toBe(true);
    });

    it('should trigger login failed method', () => {
      service.touchIDLoginFailedIfExist({ code: '404', msg: 'error' });
      expect(windowRef.nativeWindow.NativeBridge.touchIDLoginFailed).toHaveBeenCalled();
      expect(windowRef.nativeWindow.NativeBridge.onFingerPrintLoginFailed).toHaveBeenCalled();
    });

    it('should trigger touch id settings update method', () => {
      service.touchIDSettingsUpdate(true);
      expect(windowRef.nativeWindow.NativeBridge.touchIDSettingsUpdate).toHaveBeenCalled();
    });

    it('should sync player betslip', () => {
      service.syncPlayerBetSlip(10);
      expect(windowRef.nativeWindow.NativeBridge.syncPlayerBetSlip).toHaveBeenCalled();
    });

    it('should call NativeBridge accaNotificationChanged method', () => {
      service.accaNotificationChanged({});
      expect(windowRef.nativeWindow.NativeBridge.accaNotificationChanged).toHaveBeenCalled();
    });

    describe('tdpeh - should get native bridge AppsFlyer property', () => {
      it('tdpeh - exist', () => {
        service.isWrapper = true;
        service['bridge'] = { tdpeh: '23' };
        expect(service.tdpeh).toBe('23');
      });
      it('tdpeh - not exist', () => {
        service.isWrapper = true;
        service['bridge'] = { };
        expect(service.tdpeh).toBe(null);
      });
      it('tdpeh - exist but it is not a Wrapper', () => {
        service.isWrapper = false;
        service['bridge'] = { tdpeh: '23' };
        expect(service.tdpeh).toBe(null);
      });
    });

    describe('should logout', () => {
      it('is wrapper and has functions', () => {
        service.logout();
        expect(windowRef.nativeWindow.NativeBridge.logout).toHaveBeenCalled();
        expect(windowRef.nativeWindow.NativeBridge.showUserBalance).toHaveBeenCalledWith(true);
      });

      it('is not wrapper', () => {
        service.isWrapper = false;
        service.logout();
        expect(windowRef.nativeWindow.NativeBridge.logout).not.toHaveBeenCalled();
        expect(windowRef.nativeWindow.NativeBridge.showUserBalance).not.toHaveBeenCalledWith(true);
      });

      it('is wrapper but no functions', () => {
        service.isWrapper = true;
        spyOn(_, 'isFunction').and.returnValue(false);
        service.logout();
        expect(windowRef.nativeWindow.NativeBridge.logout).not.toHaveBeenCalled();
        expect(windowRef.nativeWindow.NativeBridge.showUserBalance).not.toHaveBeenCalledWith(true);
      });
    });

    it('should set deposit if method exists', () => {
      service.depositIfExist('USD', 10);
      expect(windowRef.nativeWindow.NativeBridge.deposit).toHaveBeenCalled();
    });

    it('should show video for android wrapper < v6.4 ', () => {
      service.showVideoIfExist('/', 10, 'test', '');
      expect(windowRef.nativeWindow.NativeBridge.showVideoStreamV2).toHaveBeenCalledWith('/', 10, 'test');
    });

    it('should show video and provider', () => {
      service['bridge'].id = '123';
      service.showVideoIfExist('/', 10, 'test', 'provider');
      expect(windowRef.nativeWindow.NativeBridge.showVideoStreamV2).toHaveBeenCalledWith('/', 10, 'test', 'provider');
    });

    it('should show video', () => {
      service.isWrapper = true;
      windowRef.nativeWindow.NativeBridge.showVideoStreamV2 = undefined;
      windowRef.nativeWindow.NativeBridge.showVideoStream = jasmine.createSpy();
      service.showVideoIfExist('/', 10, 'test', '');
      expect(windowRef.nativeWindow.NativeBridge.showVideoStream).toHaveBeenCalledWith('/');
    });

    it('should pause video', () => {
      service.hideVideoStream();
      expect(windowRef.nativeWindow.NativeBridge.pauseVideo).toHaveBeenCalled();
    });

    it('should get video support status', () => {
      expect(service.supportsVideo()).toBeTruthy();
    });

    it('should call registrationStarted method if exists', () => {
      service.registrationStartedIfExist();
      expect(windowRef.nativeWindow.NativeBridge.registrationStarted).toHaveBeenCalled();
    });

    it('should call registrationFinished method if exists', () => {
      service.registrationFinishedIfExist('10', 'pass');
      expect(windowRef.nativeWindow.NativeBridge.registrationFinished).toHaveBeenCalledWith('10', 'pass');
    });

    it('should call registrationFinished method if exists with default params', () => {
      service.registrationFinishedIfExist();
      expect(windowRef.nativeWindow.NativeBridge.registrationFinished).toHaveBeenCalledWith('', '');
    });

    it('should call registrationFinished method if exists', () => {
      service.isWrapper = true;
      spyOn(_, 'isFunction').and.returnValue(true);
      windowRef.nativeWindow.NativeBridge.touchIDConfigured = false;
      service.registrationFinishedIfExist('10', 'pass');
      expect(windowRef.nativeWindow.NativeBridge.registrationFinished).toHaveBeenCalledWith('10');
    });

    it('#registrationFinishedSalesForce', () => {
      service.isWrapper = true;
      spyOn(_, 'isFunction').and.returnValue(true);
      service.registrationFinishedSalesForce('42');
      expect(windowRef.nativeWindow.NativeBridge.registrationFinishedSalesForce).toHaveBeenCalledWith('42');
    });

    it('#registrationFinishedSalesForce should call with empty string as default param', () => {
      service.isWrapper = true;
      spyOn(_, 'isFunction').and.returnValue(true);
      service.registrationFinishedSalesForce();
      expect(windowRef.nativeWindow.NativeBridge.registrationFinishedSalesForce).toHaveBeenCalledWith('');
    });

    it('should not call registrationFinishedSalesForce if it is not wrapper', () => {
      service.isWrapper = false;
      service.registrationFinishedSalesForce('42');
      expect(windowRef.nativeWindow.NativeBridge.registrationFinishedSalesForce).not.toHaveBeenCalledWith();
    });

    it('should not call registrationFinishedSalesForce if no such method', () => {
      service.isWrapper = true;
      spyOn(_, 'isFunction').and.returnValue(false);
      service.registrationFinishedSalesForce('42');
      expect(windowRef.nativeWindow.NativeBridge.registrationFinishedSalesForce).not.toHaveBeenCalledWith();
    });

    it('should call passwordChanged method if exists', () => {
      service.passwordChangedIfExist('pass', 'user');
      expect(windowRef.nativeWindow.NativeBridge.passwordChanged).toHaveBeenCalled();
    });

    it('should check football alerts status', () => {
      expect(service.hasOnEventAlertsClick()).toBeTruthy();

      // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
      expect(service.hasShowFootballAlerts()).toBeTruthy();
      // TODO END
    });

    it('should show football alerts', () => {
      service.onEventAlertsClick('id', 'football', '15', 'EVFLAG_FE,EVFLAG_PVM,EVFLAG_NE,EVFLAG_BL,', 'cashout');
      expect(windowRef.nativeWindow.NativeBridge.onEventAlertsClick).toHaveBeenCalledWith('id', 'football', '15', 'Perform');
      expect(windowRef.nativeWindow.NativeBridge.onMatchAlertsClick).toHaveBeenCalledWith(JSON.stringify({location: 'cashout'}));

      // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
      service.showFootballAlerts();
      expect(windowRef.nativeWindow.NativeBridge.showFootballAlerts).toHaveBeenCalled();
      // TODO END
    });

    it('should trigger close betslip', () => {
      service.onCloseBetSlip();
      expect(windowRef.nativeWindow.NativeBridge.onCloseBetSlip).toHaveBeenCalled();
    });

    it('should trigger open betslip', () => {
      service.onOpenBetSlip();
      expect(windowRef.nativeWindow.NativeBridge.onOpenBetSlip).toHaveBeenCalled();
    });

    it('should trigger open gaming', () => {
      service.onGaming();
      expect(windowRef.nativeWindow.NativeBridge.onGaming).toHaveBeenCalled();
    });

    it('should not trigger open gaming when isWrapper equals false', () => {
      service.isWrapper = false;
      service.onGaming();
      expect(windowRef.nativeWindow.NativeBridge.onGaming).not.toHaveBeenCalled();
    });

    it('should trigger login dialog close', () => {
      service.onCloseLoginDialog();
      expect(windowRef.nativeWindow.NativeBridge.onCloseLoginDialog).toHaveBeenCalled();
    });

    it('should trigger dialog open', () => {
      service.onOpenPopup('test');
      expect(windowRef.nativeWindow.NativeBridge.onOpenPopup).toHaveBeenCalled();
    });

    it('should trigger dialog open', () => {
      service.onClosePopup('test');
      expect(windowRef.nativeWindow.NativeBridge.onClosePopup).toHaveBeenCalled();
    });

    it('should get isNativePage value', () => {
      expect(service.getNativePageOpened()).toBe(true);
    });

    it('should check if wrapper supports onFeaturedTabClicked function', () => {
      expect(service.hasOnFeaturedTabClicked()).toBe(true);
    });

    it('should trigger login popup end', () => {
      service.onLoginPopupsEnd();
      expect(windowRef.nativeWindow.NativeBridge.onLoginPopupsEnd).toHaveBeenCalled();
    });

    it('should trigger right menu click', () => {
      service.onRightMenuClick();
      expect(windowRef.nativeWindow.NativeBridge.onRightMenuClick).toHaveBeenCalled();
    });

    it('should trigger cookie banner close', () => {
      service.onCookieBannerClosed();
      expect(windowRef.nativeWindow.NativeBridge.onCookieBannerClosed).toHaveBeenCalled();
    });

    it('should trigger free bet update v2', () => {
      service.isWrapper = true;
      windowRef.nativeWindow.NativeBridge.onFreeBetUpdatedV2 = jasmine.createSpy();
      spyOn(_, 'isFunction').and.returnValue(true);
      service.onFreeBetUpdated(false, []);
      expect(windowRef.nativeWindow.NativeBridge.onFreeBetUpdatedV2).toHaveBeenCalled();
    });

    it('should trigger free bet update', () => {
      service.isWrapper = true;
      windowRef.nativeWindow.NativeBridge.onFreeBetUpdatedV2 = undefined;
      service.onFreeBetUpdated(false, []);
      expect(windowRef.nativeWindow.NativeBridge.onFreeBetUpdated).toHaveBeenCalled();
    });

    it('should check private markets availability', () => {
      service.arePrivateMarketsAvailable(false);
      expect(windowRef.nativeWindow.NativeBridge.arePrivateMarketsAvailable).toHaveBeenCalled();
    });

    it('should trigger balance change', () => {
      service.onBalanceChanged({ amount: '20' });
      expect(windowRef.nativeWindow.NativeBridge.onBalanceChanged).toHaveBeenCalled();
    });

    it('should show error for native', () => {
      service.showErrorForNative('error');
      expect(windowRef.nativeWindow.NativeBridge.showErrorForNative).toHaveBeenCalled();
    });

    describe('pageLoaded', () => {
      it('should trigger page loaded status', () => {
        service.pageLoaded();
        expect(windowRef.nativeWindow.NativeBridge.pageLoaded).toHaveBeenCalledWith('3fwerasgv4234123dgsfdg');
      });

      it('should include sessionToken into pageLoaded function call if system is Ios', () => {
        (service as any).deviceService.isIos = true;
        service.pageLoaded();
        expect(windowRef.nativeWindow.NativeBridge.pageLoaded).toHaveBeenCalledWith('3fwerasgv4234123dgsfdg');
        service.pageLoaded();
        expect(windowRef.nativeWindow.NativeBridge.pageLoaded).toHaveBeenCalledWith('3fwerasgv4234123dgsfdg');
      });

      it('should not include sessionToken into pageLoaded function call if system is not Ios', () => {
        (service as any).deviceService.isIos = false;
        service.pageLoaded();
        expect(windowRef.nativeWindow.NativeBridge.pageLoaded).toHaveBeenCalledWith();
        service.pageLoaded();
        expect(windowRef.nativeWindow.NativeBridge.pageLoaded).toHaveBeenCalledWith();
      });

      it('should not trigger page loaded status', () => {
        service['bridge'].pageLoaded = undefined;
        service.pageLoaded();
        expect(windowRef.nativeWindow.NativeBridge.pageLoaded).toBeUndefined();
        expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
      });

      it('should call page loaded without delay', () => {
        service.pageLoaded();
        expect(windowRef.nativeWindow.setTimeout).not.toHaveBeenCalled();
        expect(windowRef.nativeWindow.NativeBridge.pageLoaded).toHaveBeenCalled();
      });
    });

    it('should trigger football page loaded status', () => {
      service.eventPageLoaded('id', 'football');
      expect(windowRef.nativeWindow.NativeBridge.eventPageLoaded).toHaveBeenCalled();
      // TODO: Reverted changes from BMA-37049. Will be removed after new approach implementation.
      service.footballEventPageLoaded();
      expect(windowRef.nativeWindow.NativeBridge.footballEventPageLoaded).toHaveBeenCalled();
      // TODO END
    });

    it('should trigger url changed', () => {
      service.onUrlChanged('/');
      expect(windowRef.nativeWindow.NativeBridge.onUrlChanged).toHaveBeenCalled();
    });

    it('should check if wrapper supports Diagnostics function', () => {
      expect(service.isDiagnostics()).toBeTruthy();
    });

    it('should send report', () => {
      service.sendReport();
      expect(windowRef.nativeWindow.NativeBridge.wrapperSendDiagnostics).toHaveBeenCalled();
    });

    it('should pass session token to native bridge', () => {
      const token = {
        username: 'user',
        sessionToken: 'fwefefv',
        isFromBetSlip: false,
        password: 'qwerty'
      };

      service.loginSessionToken(token);
      expect(windowRef.nativeWindow.NativeBridge.loginSessionToken).toHaveBeenCalledWith(JSON.stringify(token));
    });

    it('should send report', () => {
      service.loginError('error');
      expect(windowRef.nativeWindow.NativeBridge.loginError).toHaveBeenCalled();
    });

    it('should trigger session limit', () => {
      service.onSessionLimitChanged(100);
      expect(windowRef.nativeWindow.NativeBridge.onSessionLimitChanged).toHaveBeenCalled();
    });

    it('should show user balance', () => {
      service.showUserBalance(100);
      expect(windowRef.nativeWindow.NativeBridge.showUserBalance).toHaveBeenCalled();
    });

    it('should show user balance', () => {
      service.syncFavouritesToNative([]);
      expect(windowRef.nativeWindow.NativeBridge.syncFavourites).toHaveBeenCalled();
    });

    it('should sync favourites with native', () => {
      service.syncFavouritesFromNative();
      expect(command.execute).toHaveBeenCalled();
    });

    it('should show policy banner', () => {
      service.showPolicyBanner('test');
      expect(windowRef.nativeWindow.NativeBridge.showPolicyBanner).toHaveBeenCalled();
    });

    it('should check stream availability', () => {
      const event = {
        categoryId: 10,
        classId: 1,
        typeId: 2,
        eventId: 12
      };
      service.onEventDetailsStreamAvailable(event);
      expect(windowRef.nativeWindow.NativeBridge.onEventDetailsStreamAvailable).toHaveBeenCalled();
    });

    it('should check stream availability', () => {
      user.status = false;
      const event = {
        categoryId: 10,
        classId: 1,
        typeId: 2,
        eventId: 12
      };
      service.onEventDetailsStreamAvailable(event);
      expect(windowRef.nativeWindow.NativeBridge.onEventDetailsStreamAvailable).not.toHaveBeenCalled();
    });

    it('should check if connect native app was used previously', () => {
      service.checkConnect();
      expect(windowRef.nativeWindow.NativeBridge.checkConnect).toHaveBeenCalled();
    });

    describe('checkGRID to check native app', () => {
      it('should trigger open checkGrid', () => {
        service.checkGrid();
        expect(windowRef.nativeWindow.NativeBridge.checkGrid).toHaveBeenCalled();
      });

      it('should not trigger open checkGrid when isWrapper equals false', () => {
        service.isWrapper = false;
        service.checkGrid();
        expect(windowRef.nativeWindow.NativeBridge.checkGrid).not.toHaveBeenCalled();
      });
    });
  });

  describe('getMobileOperatingSystem', () => {
    it('should get mobile operating system', () => {
      expect(service.getMobileOperatingSystem()).toBe('android');
    });

    it('should get mobile operating system (ios)', () => {
      windowRef.nativeWindow.navigator.userAgent = 'user agent Macintosh';
      expect(service.getMobileOperatingSystem()).toBe('ios');
    });

    it('should get mobile operating system (mac os)', () => {
      windowRef.nativeWindow.navigator.userAgent = 'user agent Macintosh';
      service.isWrapper = false;
      expect(service.getMobileOperatingSystem()).toBe('unknown');
    });
  });

  it('should get mobile operating system, iOS', () => {
    windowRef.nativeWindow.navigator.userAgent = 'iPhone';
    service.getMobileOperatingSystem();
    expect(service.getMobileOperatingSystem()).toBe('ios');
  });

  it('should get mobile operating system, windows', () => {
    windowRef.nativeWindow.navigator.userAgent = 'windows phone';
    service.getMobileOperatingSystem();
    expect(service.getMobileOperatingSystem()).toBe('wp');
  });

  it('should not get mobile operating system', () => {
    windowRef.nativeWindow.navigator.userAgent = 'test';
    service.getMobileOperatingSystem();
    expect(service.getMobileOperatingSystem()).toBe('unknown');
  });

  it('should login', () => {
    service.loginIfExist('10', 'pass');
    expect(windowRef.nativeWindow.NativeBridge.login).toHaveBeenCalledWith('10', 'pass');
  });

  it('should call loginIfExist with only playerCode parameter', () => {
    service.isWrapper = true;
    spyOn(_, 'isFunction').and.returnValue(true);
    windowRef.nativeWindow.NativeBridge.touchIDConfigured = false;
    service.loginIfExist('10', 'pass');
    expect(windowRef.nativeWindow.NativeBridge.login).toHaveBeenCalledWith('10');
  });

  it('#loginSalesForce', () => {
    service.isWrapper = true;
    spyOn(_, 'isFunction').and.returnValue(true);
    service.loginSalesForce('42');
    expect(windowRef.nativeWindow.NativeBridge.loginSalesForce).toHaveBeenCalledWith('42');
  });

  it('should not call loginSalesForce if it is not wrapper', () => {
    service.isWrapper = false;
    service.loginSalesForce('42');
    expect(windowRef.nativeWindow.NativeBridge.loginSalesForce).not.toHaveBeenCalledWith();
  });

  it('should not call loginSalesForce if no such method', () => {
    service.isWrapper = true;
    spyOn(_, 'isFunction').and.returnValue(false);
    service.loginSalesForce('42');
    expect(windowRef.nativeWindow.NativeBridge.loginSalesForce).not.toHaveBeenCalledWith();
  });

  it('should login with touch id', () => {
    service.loginWithTouchID(false, '', false);
    expect(windowRef.nativeWindow.NativeBridge.loginWithTouchID).toHaveBeenCalledWith(false, '', false);
  });

  it('should open login dialog', () => {
    service.openLoginDialog(['']);
    expect(windowRef.nativeWindow.NativeBridge.openNativeLoginDialog).toHaveBeenCalled();
  });

  it('should create mobenga iframe', () => {
    service.createMobengaIframe();
    expect(document.body.appendChild).toHaveBeenCalled();
  });

  it('should trigger feature tab click', () => {
    service.onFeaturedTabClicked();
    expect(windowRef.nativeWindow.NativeBridge.onFeaturedTabClicked).toHaveBeenCalled();
  });

  it('should trigger onUserAction tracker with JSON-string passed', () => {
    service.appSeeTrackAction({ action: 'name', data: { key: 'value' } });
    expect(windowRef.nativeWindow.NativeBridge.onUserAction).toHaveBeenCalledWith('{"action":"name","data":{"key":"value"}}');
  });

  it('should call onActivateWinAlerts method', () => {
    service.onActivateWinAlerts('123', ['111']);
    expect(windowRef.nativeWindow.NativeBridge.onActivateWinAlerts).toHaveBeenCalledWith('123', ['111']);
  });

  it('should not call onActivateWinAlerts method', () => {
    service.isWrapper = false;
    service.onActivateWinAlerts('123', ['111']);
    expect(windowRef.nativeWindow.NativeBridge.onActivateWinAlerts).not.toHaveBeenCalled();
  });

  it('should call showNotificationSettings method', () => {
    service.showNotificationSettings();
    expect(windowRef.nativeWindow.NativeBridge.showNotificationSettings).toHaveBeenCalled();
  });

  it('should not call showNotificationSettings method', () => {
    service.isWrapper = false;
    service.showNotificationSettings();
    expect(windowRef.nativeWindow.NativeBridge.showNotificationSettings).not.toHaveBeenCalled();
  });
  it('should open slideout betslip', fakeAsync(() => {
    const event: any = {
      detail: {
        isOpen: true
      }
    };
    service.openSlideOutBetSlip(event);
    tick();
    expect(pubsub.publish).toHaveBeenCalledWith('show-slide-out-betslip', true);
  }));

  it('should call onVirtualsSelected native bridge method', () => {
    const testEventId = '101';
    const testSportId = '102';
    service.onVirtualsSelected(testSportId, testEventId);
    expect(windowRef.nativeWindow.NativeBridge.onVirtualsSelected).toHaveBeenCalledWith(testSportId, testEventId);
  });

  it('should get isRemovingGamingEnabled value', () => {
    expect(service.isRemovingGamingEnabled).toBe(true);
  });

  describe('handleNativeVideoPlayer', () => {
    let element;
    beforeEach(() => {
      element = {
        offsetTop: 100,
        offsetParent: {
          offsetTop: 10,
          offsetParent: {
            offsetTop: 1,
            offsetParent: null
          }
        }
      } as any;
    });
    describe('should do nothing', () => {
      it('when is not wrapper', () => {
        service.isWrapper = false;
      });
      it('when no element provided', () => {
        element = null;
      });
      it('when onVideoPlayerExpanded is not supported', () => {
        (service as any).bridge = {};
      });
      afterEach(() => {
        service.handleNativeVideoPlayer(element);
        expect(windowRef.nativeWindow.NativeBridge.onVideoPlayerExpanded).not.toHaveBeenCalled();
      });
    });
    it('should get element global offset', () => {
      service.handleNativeVideoPlayer(element);
      expect(windowRef.nativeWindow.NativeBridge.onVideoPlayerExpanded).toHaveBeenCalledWith(111);
    });
  });

  describe('handleNativeVideoPlaceholder', () => {
    let element;
    beforeEach(() => {
      element = { style: {} };
      windowRef.nativeWindow.NativeBridge.nativeVideoPlayerHeight = 123;
    });
    it('if no element should do nothing', () => {
      service.handleNativeVideoPlaceholder(true, null);
    });
    it('should show placeholder', () => {
      service.handleNativeVideoPlaceholder(true, element);
      expect(element.style.height).toEqual('123px');
    });
    it('should hide placeholder', () => {
      service.handleNativeVideoPlaceholder(false, element);
      expect(element.style.height).toEqual('0px');
    });
  });

  it('showOptInSplashScreen', () => {
    service['showOptInSplashScreen']();
    const param = [{ visibility: true, type: 'optIn' }];
    expect(console.warn).toHaveBeenCalled();
    expect(command.execute).toHaveBeenCalledWith(command.API.OPT_IN_SPLASH_UPDATE_STATE, param);
  });

  it('showMarketingPreferencePage', () => {
    service['showMarketingPreferencePage']();
    expect(console.warn).toHaveBeenCalled();
    expect(command.execute).toHaveBeenCalledWith(command.API.OPT_IN_INACTIVE_USER);
  });

  it('hideSplashScreen', () => {
    service.isWrapper = true;
    spyOn(_, 'isFunction').and.returnValue(true);
    service['hideSplashScreen']();
    expect(windowRef.nativeWindow.NativeBridge.hideSplashScreen).toHaveBeenCalled();
  });

  it('syncBetSlipToNative', () => {
    service.isWrapper = true;
    spyOn(_, 'isFunction').and.returnValue(true);
    const outcomes: Array<string> = ['test'];
    service['syncBetSlipToNative'](outcomes);
    expect(windowRef.nativeWindow.NativeBridge.syncBetSlip).toHaveBeenCalledWith(JSON.stringify(outcomes));
  });

  it('onOddsSettingsChanged', () => {
    service.isWrapper = true;
    spyOn(_, 'isFunction').and.returnValue(true);
    const settingValue: any = {};
    service['onOddsSettingsChanged'](settingValue);
    expect(windowRef.nativeWindow.NativeBridge.onOddsSettingsChanged).toHaveBeenCalledWith(settingValue);
  });

  it('when BuildVersion event occurs, should call pubsub APP_BUILD_VERSION', () => {
    service.init();
    const response = { detail: { versionValue: '6' } };
    documentCbMap['onBuildVersionReceived'](response);
    expect(pubsub.publish).toHaveBeenCalledWith('APP_BUILD_VERSION', response.detail.versionValue);
  });

  describe('BuildVersion', () => {
    it('should trigger when isWrapper true device is iOS', () => {
      service.isWrapper = true;
      deviceService.isIos = true;
      service.getBuildVersion();
      expect(windowRef.nativeWindow.NativeBridge.getBuildVersion).toHaveBeenCalled();
    });
    it('should not trigger when isWrapper false device is iOS', () => {
      service.isWrapper = false;
      deviceService.isIos = true;
      service.getBuildVersion();
      expect(windowRef.nativeWindow.NativeBridge.getBuildVersion).not.toHaveBeenCalled();
    });
    it('should not trigger when isWrapper false device is not iOS', () => {
      service.isWrapper = false;
      deviceService.isIos = false;
      service.getBuildVersion();
      expect(windowRef.nativeWindow.NativeBridge.getBuildVersion).not.toHaveBeenCalled();
    });
  });

  describe('#betPlaceSuccessful', () => {
    it('should call betPlaceSuccessful', () => {
      service.isWrapper = true;
      service.betPlaceSuccessful('123', 'Football', 'Single');
      expect(windowRef.nativeWindow.NativeBridge.betPlaceSuccessful).toHaveBeenCalled();
    });
  });

  describe('#multipleEventPageLoaded', () => {
    it('should call multipleEventPageLoaded - native app', () => {
      service.isWrapper = true;
      const eventIds = ['123', '234'],
      categoryName = 'Football';
      service.multipleEventPageLoaded(eventIds, categoryName);
      expect(windowRef.nativeWindow.NativeBridge.multipleEventPageLoaded).toHaveBeenCalledWith(JSON.stringify({eventIds, categoryName}));
    });

    it('should call multipleEventPageLoaded - not native app', () => {
      service.isWrapper = false;
      const eventIds = ['123', '234'],
      categoryName = 'Football';
      service.multipleEventPageLoaded(eventIds, categoryName);
      expect(windowRef.nativeWindow.NativeBridge.multipleEventPageLoaded).not.toHaveBeenCalled();
    });
  });

  describe('#winAlertsStatus', () => {
    it('should call winAlertsStatus - native app', () => {
      service.isWrapper = true;
      service.winAlertsStatus();
      expect(windowRef.nativeWindow.NativeBridge.winAlertsStatus).toHaveBeenCalled();
    });

    it('should call winAlertsStatus - not native app', () => {
      service.isWrapper = false;
      service.winAlertsStatus();
      expect(windowRef.nativeWindow.NativeBridge.winAlertsStatus).not.toHaveBeenCalled();
    });
  });

  describe('#disableWinAlertsStatus', () => {
    it('should call disableWinAlertsStatus - native app', () => {
      service.isWrapper = true;
      service.disableWinAlertsStatus('123');
      expect(windowRef.nativeWindow.NativeBridge.disableWinAlertsStatus).toHaveBeenCalled();
    });

    it('should call disableWinAlertsStatus - not native app', () => {
      service.isWrapper = false;
      service.disableWinAlertsStatus('123');
      expect(windowRef.nativeWindow.NativeBridge.disableWinAlertsStatus).not.toHaveBeenCalled();
    });
  });

  describe('#onClearCache', () => {
    it('should call onClearCache - native app', () => {
      service.isWrapper = true;
      service.onClearCache();
      expect(windowRef.nativeWindow.NativeBridge.onClearCache).toHaveBeenCalled();
    });

    it('should call onClearCache - not native app', () => {
      service.isWrapper = false;
      service.onClearCache();
      expect(windowRef.nativeWindow.NativeBridge.onClearCache).not.toHaveBeenCalled();
    });
  });

  describe('#networkIndicatorEnabled', () => {
    it('should call networkIndicatorEnabled', () => {
      service.isWrapper = true;
      service.networkIndicatorEnabled(true);
      expect(windowRef.nativeWindow.NativeBridge.networkIndicatorEnabled).toHaveBeenCalled();
    });
    it('should not call networkIndicatorEnabled', () => {
      service.isWrapper = false;
      service.networkIndicatorEnabled(true);
      expect(windowRef.nativeWindow.NativeBridge.networkIndicatorEnabled).not.toHaveBeenCalled();
    });
  });

  describe('shareContentOnSocialMediaGroups', () => {
    it('should call shareContentOnSocialMediaGroups', () => {
      service.isWrapper = true;
      service.shareContentOnSocialMediaGroups(true);
      expect(windowRef.nativeWindow.NativeBridge.shareContentOnSocialMediaGroups).toHaveBeenCalled();
    })
    it('should not call shareContentOnSocialMediaGroups', () => {
      service.isWrapper = false;
      service.shareContentOnSocialMediaGroups(true);
      expect(windowRef.nativeWindow.NativeBridge.shareContentOnSocialMediaGroups).not.toHaveBeenCalled();
    })
  })
});

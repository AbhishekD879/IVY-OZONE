import { of, Subject, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { EventVideoStreamComponent } from './event-video-stream.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { DialogService } from '@core/services/dialogService/dialog.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IStreamProvidersResponse, } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { IStreamReplayUrls } from '@lazy-modules/eventVideoStream/services/iGameMedia/i-gameMedia.model';

describe('EventVideoStreamComponent', () => {
  let component: EventVideoStreamComponent;
  let deviceService;
  let gtmService;
  let eventEntity;
  let pubsubService;
  let eventVideoStreamProvider;
  let localeService;
  let nativeBridgeService;
  let iGameMediaService;
  let sessionService;
  let liveStreamService;
  let userService;
  let windowRefService;
  let watchRulesService;
  let changeDetectorRef;
  let dialogService;
  let componentFactoryResolver;
  let cms;

  beforeEach(() => {
    nativeBridgeService = {
      supportsVideo: jasmine.createSpy('supportsVideo'),
      playerStatus: false,
      showErrorForNative: jasmine.createSpy('showErrorForNative'),
      hideVideoStream: jasmine.createSpy('hideVideoStream')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('localeString')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve())
    };
    deviceService = {
      isDesktop: true,
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true),
      performProviderIsMobile: jasmine.createSpy('performProviderIsMobile'),
      isWrapper: false
    };
    liveStreamService = {
      prioritizeStream: jasmine.createSpy('prioritizeStream')
    };
    iGameMediaService = {
      getStreamsForEvent: jasmine.createSpy('getStreamsForEvent').and.returnValue(of({
        stream: 'some/url'
      } as IStreamProvidersResponse)),
      getHRReplayStreamUrls: jasmine.createSpy('getHRReplayStreamUrls').and.returnValue(of({
        provider: "ATR",
        streamInfo: {
          bitrateLevel: "Adaptive",
          streamUrl:'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8#t=550,600'
    
        },
        status: "SUCCESS",
        closingStage:true,
        startTime:100,
        endTime:300,
        message: "Streaming error / authentication failed / VOD not available"
      } as IStreamReplayUrls))
    };
    eventVideoStreamProvider = {
      playListener: new Subject<void>(),
      showHideStreamListener: new Subject<boolean>(),
      isStreamBetAvailable:  jasmine.createSpy('isStreamBetAvailable').and.returnValue(true),
      getStreamBetCmsConfig:  jasmine.createSpy('getStreamBetCmsConfig').and.returnValue(of({
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      }))
    };
    pubsubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    userService = {
      status: false
    };
    windowRefService = {
      document: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener')
      }
    };
    eventEntity = {
      id: 1234,
      streamProviders: {}
    } as ISportEvent;
    watchRulesService = {
      shouldShowCSBIframe: jasmine.createSpy('shouldShowCSBIframe'),
      isInactiveUser: jasmine.createSpy('isInactiveUser').and.returnValue(false)
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog'),
      closeDialog: jasmine.createSpy('closeDialog')
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue({ name: 'VideoStreamErrorDialogComponent'})
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy()
    };

    createComponent();
  });

  function createComponent() {
    component = new EventVideoStreamComponent(userService, nativeBridgeService, localeService, gtmService,
      sessionService, deviceService, liveStreamService, iGameMediaService, eventVideoStreamProvider, pubsubService,
      windowRefService, watchRulesService, changeDetectorRef, dialogService, componentFactoryResolver, cms
    );

    component.eventEntity = eventEntity;
  }

  it('should create component', () => {
    expect(component).toBeTruthy();
    expect(component.isDesktop).toBeTruthy();
    expect(component.providerInfoAvailable).toBeFalsy();
  });

  it('should set isDesktop property', () => {
    deviceService.isDesktop = false;
    createComponent();

    expect(component.isDesktop).toBeFalsy();
  });

  it('should call playStream method if its Wrapper and playerStatus is false', () => {
    nativeBridgeService.playerStatus = false;
    deviceService.isWrapper = true;
    spyOn(component, 'playStream');
    expect(component).toBeTruthy();

    component['eventVideoStreamProvider'].playListener.subscribe(() => {
      expect(component.playStream).toHaveBeenCalled();
    });
  });

  it('should handle reload stream event', fakeAsync(() => {
    component.showPlayer = true;

    eventVideoStreamProvider.playListener.subscribe(() => {
      expect(component.showPlayer).toBeFalsy();
    });
    component['handleReloadStream']();
    tick();
  }));

  it('should handle reload stream event(show video stream)', fakeAsync(() => {
    component.showPlayer = true;
    component['showStream'] = false;

    component['handleReloadStream']();
    expect(component.showPlayer).toBeFalsy();
    expect(component['showStream']).toBeFalsy();
  }));

  describe('parseCssClasses', () => {
    it('should set default values for cssClassesForStreams', () => {
      component['parseCssClasses']();

      expect(component['iGameMediaCssClasses']).toEqual('');
      expect(component['videoStreamProvidersCssClasses']).toEqual('');
    });

    it('should parse passed inputs for cssClassesForStreams', () => {
      const cssClassesForStreams = {
        iGameMedia: 'hide-desktop',
        otherProviders: 'show-all'
      };

      component.cssClassesForStreams = cssClassesForStreams;
      component['parseCssClasses']();

      expect(component['iGameMediaCssClasses']).toEqual(cssClassesForStreams.iGameMedia);
      expect(component['videoStreamProvidersCssClasses']).toEqual(cssClassesForStreams.otherProviders);
    });
  });

  describe('hideStream', () => {
    it('should handle other streaming provider', fakeAsync(() => {
      component.showPlayer = true;

      eventVideoStreamProvider.showHideStreamListener.subscribe((value) => {
        expect(value).toBeFalsy();
      });
      component['hideStream']();
      tick();
      expect(component['providerInfoAvailable']).toBeFalsy();
    }));
  });

  describe('getUserLoggedOutMessage', () => {
    it('should return error message for anonymous user', () => {
      userService.status = false;
      expect(component['getUserLoggedOutMessage']()).toEqual('onlyLoginRequired');
    });

    it('should return error message for logged in user', () => {
      userService.status = true;
      expect(component['getUserLoggedOutMessage']()).toEqual('');
    });
  });

  describe('getProviderInfo', () => {
    let providerInfo;
    let successHandler;
    let errorHandler;

    beforeEach(() => {
      eventEntity = {
        id: 1234
      } as ISportEvent;
      providerInfo = {
        stream: 'stream/url'
      } as IStreamProvidersResponse;
      successHandler = jasmine.createSpy('successHandler');
      errorHandler = jasmine.createSpy('errorHandler');

      component.eventEntity = eventEntity;
    });

    it('should return cached stream if there is "stream" property', fakeAsync(() => {
      component.streamCache.set(eventEntity.id, providerInfo);

      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(jasmine.objectContaining(providerInfo));
      expect(sessionService.whenProxySession).not.toHaveBeenCalled();
    }));

    it('should remove stream from cache if it has not valid info and handle session reject', fakeAsync(() => {
      sessionService.whenProxySession.and.callFake(() => Promise.reject('some error'));
      providerInfo.stream = null;
      component.streamCache.set(eventEntity.id, providerInfo);

      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      tick();

      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith('streamIsNotAvailable');
      expect(component.streamCache.get(eventEntity.id)).toBeFalsy();
    }));

    it('should handle case when the device is not online', fakeAsync(() => {
      deviceService.isOnline.and.returnValue(false);
      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalledWith('serverError');
      expect(component.streamCache.get(eventEntity.id)).toBeFalsy();
      expect(sessionService.whenProxySession).not.toHaveBeenCalled();
    }));

    it('should handle case when session rejection when the device is not online', fakeAsync(() => {
      sessionService.whenProxySession.and.callFake(() => Promise.reject('error'));

      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      deviceService.isOnline.and.returnValue(false);
      tick();

      expect(errorHandler).toHaveBeenCalledWith('serverError');
      expect(component.streamCache.get(eventEntity.id)).toBeFalsy();
    }));

    it('should handle case when device is offline after session complete', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());

      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      deviceService.isOnline.and.returnValue(false);
      tick();

      expect(errorHandler).toHaveBeenCalledWith('serverError');
      expect(iGameMediaService.getStreamsForEvent).not.toHaveBeenCalled();
    }));

    it('should handle case when user becomes logged out after session promise resolve', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = false;

      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalledWith('streamIsNotAvailable');
      expect(iGameMediaService.getStreamsForEvent).not.toHaveBeenCalled();
    }));

    it('should handle error of iGameMediaService.getStreamsForEvent', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      iGameMediaService.getStreamsForEvent.and.returnValue(throwError('error'));

      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalledWith('streamIsNotAvailable');
      expect(iGameMediaService.getStreamsForEvent).toHaveBeenCalledWith(eventEntity);
    }));

    it('should handle success of iGameMediaService.getStreamsForEvent and cache providerInfo', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));

      component['getProviderInfo']().subscribe(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(providerInfo);
      expect(component.streamCache.get(eventEntity.id)).toEqual(providerInfo);
    }));
  });

  describe('showHideStream', () => {
    it('should return null if there is cached error', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'provider name',
        priorityProviderCode: 'provider code'
      } as IStreamProvidersResponse;
      const successHandler = jasmine.createSpy('successHandler');

      component.streamCache.set(eventEntity.id, { error: 'some error' } as IStreamProvidersResponse);

      component['showHideStream'](providerInfo).subscribe(successHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(null);
      expect(liveStreamService.prioritizeStream).not.toHaveBeenCalled();
    }));

    it('should return provider info', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'provider name',
        priorityProviderCode: 'provider code'
      } as IStreamProvidersResponse;
      const successHandler = jasmine.createSpy('successHandler');

      component.streamCache.set(eventEntity.id, { error: '' } as IStreamProvidersResponse);

      component['showHideStream'](providerInfo).subscribe(successHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith(providerInfo);
      expect(liveStreamService.prioritizeStream).toHaveBeenCalledWith(component.eventEntity, providerInfo);
      expect(component['providerInfoAvailable']).toBeTruthy(); // should be set after prioritizeStream !!!
      expect(component.providerInfo).toEqual(providerInfo);
    }));
  });

  describe('parseErrorMessage', () => {
    it('should return an empty string if no error is stored', () => {
      expect(component['parseErrorMessage']()).toEqual('');
      expect(localeService.getString).not.toHaveBeenCalled();
    });

    it('should parseErrorMessage correctly', () => {
      component['ERROR_MESSAGES'].onlyLoginRequired = true;

      component['parseErrorMessage']();
      expect(localeService.getString).toHaveBeenCalledWith('sb.onlyLoginRequired');
    });
  });

  describe('showErrorMessage', () => {
    it('set default error type if not mapped key passed', () => {
      const errorMessageType = 'someNewType';
      const translation = 'service error';

      localeService.getString.and.returnValue(translation);
      component['isDesktop'] = true;
      component.showErrorMessage(errorMessageType);

      expect(component['ERROR_MESSAGES'].servicesCrashed).toBeTruthy();
      expect(component.errorMessage).toEqual(translation);
      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
      expect(dialogService.openDialog).not.toHaveBeenCalled();
    });

    it('set default error type if not mapped key passed on mobile', () => {
      const errorMessageType = 'someNewType';
      const translation = 'service error';

      localeService.getString.and.returnValue(translation);
      component['isDesktop'] = false;
      component.showErrorMessage(errorMessageType);

      expect(component['ERROR_MESSAGES'].servicesCrashed).toBeTruthy();
      expect(component.errorMessage).toEqual(translation);
      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        DialogService.API.videoStreamError, { name: 'VideoStreamErrorDialogComponent'}, true, {
          errorMsg: translation,
          eventEntity,
          isInactivePopup: false
        }
      );
    });

    it('should reset new error key', () => {
      const errorMessageType = 'usageLimitsBreached';

      component['ERROR_MESSAGES'].servicesCrashed = true;
      component.showErrorMessage(errorMessageType);

      expect(component['ERROR_MESSAGES'].servicesCrashed).toBeFalsy();
      expect(component['ERROR_MESSAGES'].usageLimitsBreached).toBeTruthy();
      expect(localeService.getString).toHaveBeenCalledWith('sb.usageLimitsBreached');
    });

    it('should reset same error key that is visible', () => {
      const errorMessageType = 'servicesCrashed';

      component['ERROR_MESSAGES'].servicesCrashed = true;
      component.showErrorMessage(errorMessageType);

      expect(component['ERROR_MESSAGES'].servicesCrashed).toBeTruthy();
      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
    });
  });

  describe('onPlayLiveStreamError', () => {
    const reason = 'some error';
    beforeEach(() => {
      spyOn(component as any, 'onError');
    });

    it('should emit play stream error output', fakeAsync(() => {
      const streamErrorListener = jasmine.createSpy('streamErrorListener');

      component.playStreamError.subscribe(streamErrorListener);
      component['showStream'] = true;
      component.onPlayLiveStreamError(reason);
      tick();

      expect(streamErrorListener).toHaveBeenCalledWith(reason);
      expect(component['showStream']).toBeFalsy();
    }));

    it(`should run onError if showCSBIframe`, () => {
      component.showCSBIframe = true;

      component.onPlayLiveStreamError(reason);

      expect(component['onError']).toHaveBeenCalledWith(reason);
    });

    it(`should Not run onError if showCSBIframe`, () => {
      component.showCSBIframe = false;

      component.onPlayLiveStreamError(reason);

      expect(component['onError']).not.toHaveBeenCalled();
    });
  });

  describe('unsubscribeOfWrapperListeners', () => {
    it(`should removeEventListener if isWrapper`, () => {
      deviceService.isWrapper = true;

      component['unsubscribeOfWrapperListeners']();

      expect(windowRefService.document.removeEventListener).toHaveBeenCalledWith('CURRENT_WATCH_LIVE_STATE_CHANGED', jasmine.any(Function));
    });

    it(`should Not removeEventListener if isWrapper equal false`, () => {
      deviceService.isWrapper = false;

      component['unsubscribeOfWrapperListeners']();

      expect(windowRefService.document.removeEventListener).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe for pubusb events', () => {
      component['ERROR_MESSAGES'].serverError = false;
      component.ngOnDestroy();

      expect(pubsubService.unsubscribe).toHaveBeenCalledWith('EventVideoStreamComponent');
      expect(dialogService.closeDialog).not.toHaveBeenCalled();
    });

    it('should close pop-up with server error', () => {
      component['ERROR_MESSAGES'].serverError = true;
      component.ngOnDestroy();

      expect(dialogService.closeDialog).toHaveBeenCalledWith(DialogService.API.videoStreamError);
    });

    it('should unsubscribe for action listener', () => {
      component['actionSubscriber'] = eventVideoStreamProvider.playListener.subscribe();

      spyOn(component['actionSubscriber'], 'unsubscribe').and.callThrough();
      component.ngOnDestroy();

      expect(component['actionSubscriber'].unsubscribe).toHaveBeenCalled();
    });

    it('should not remove event listener if it is not wrapper', () => {
      component.ngOnDestroy();
      expect(windowRefService.document.removeEventListener).not.toHaveBeenCalled();
      expect(pubsubService.unsubscribe).toHaveBeenCalledWith('EventVideoStreamComponent');
    });

    it('should add listener for native player', () => {
      deviceService.isWrapper = true;

      component.ngOnDestroy();

      expect(windowRefService.document.removeEventListener).toHaveBeenCalledWith('CURRENT_WATCH_LIVE_STATE_CHANGED', jasmine.any(Function));
    });

    it('should unsubscribe from system config subscription', () => {
      component['systemConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;

      component.ngOnDestroy();

      expect(component['systemConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('showError', () => {
    beforeEach(() => {
      component.showPlayer = true;
      component['showStream'] = true;
      eventEntity.isFinished = false;
    });

    it('should show default error reason', () => {
      component['showError'](null);

      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
      expect(component['ERROR_MESSAGES'].servicesCrashed).toBeTruthy();
      expect(component.showPlayer).toBeFalsy();
      expect(component['showStream']).toBeFalsy();
    });

    it('should strack error event with gtm', () => {
      const translation = 'some message';

      localeService.getString.and.returnValue(translation);
      component['showError'](null);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'Livestream',
        eventAction: 'error',
        liveStreamError: translation
      }));
    });

    it('should handle eventFinished error', () => {
      const reason = 'eventFinished';

      component['ERROR_MESSAGES'].servicesCrashed = true;
      component['showError'](reason);

      expect(component.eventEntity.isFinished).toBeTruthy();
      expect(localeService.getString).toHaveBeenCalledWith(`sb.${reason}`);
      expect(component['ERROR_MESSAGES'][reason]).toBeTruthy();
    });

    it('should handle native notification', () => {
      nativeBridgeService.supportsVideo.and.returnValue(true);
      component['showError'](null);

      expect(nativeBridgeService.showErrorForNative).toHaveBeenCalledWith('servicesCrashed');
    });

    it('should show web error even it is wrapper but user gets inactive qualification error', () => {
      nativeBridgeService.supportsVideo.and.returnValue(true);
      watchRulesService.isInactiveUser.and.returnValue(true);
      component['showError']('deniedByInactiveWatchRules');

      expect(nativeBridgeService.showErrorForNative).not.toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith(`sb.deniedByInactiveWatchRules`);
    });
  });

  describe('onError', () => {
    let streamErrorListener;

    beforeEach(() => {
      streamErrorListener = jasmine.createSpy('streamErrorListener');
      component.playStreamError.subscribe(streamErrorListener);
    });

    it('should emit default error reason', fakeAsync(() => {
      component['onError'](null);
      tick();

      expect(streamErrorListener).toHaveBeenCalledWith('servicesCrashed');
    }));

    it('should check if there is stored stream for eventFinished reason', fakeAsync(() => {
      const reason = 'eventFinished';

      component['onError'](reason);
      tick();

      expect(streamErrorListener).toHaveBeenCalledWith(reason);
    }));

    it('should set error to stored stream for usageLimitsBreached reason', fakeAsync(() => {
      const reason = 'usageLimitsBreached';
      const providerInfo = {
        error: ''
      } as IStreamProvidersResponse;

      component['streamCache'].set(eventEntity.id, providerInfo);
      component['onError'](reason);
      tick();

      expect(streamErrorListener).toHaveBeenCalledWith(reason);
      expect(providerInfo.error).toEqual(reason);
    }));
  });

  describe('playStream', () => {
    let streamErrorListener;
    let showHideStreamListener;

    beforeEach(() => {
      streamErrorListener = jasmine.createSpy('streamErrorListener');
      showHideStreamListener = jasmine.createSpy('showHideStreamListener');

      eventVideoStreamProvider.showHideStreamListener.subscribe(showHideStreamListener);
      component.playStreamError.subscribe(streamErrorListener);
      component.showPlayer = true;
      component['showStream'] = true;
      component['isReplayVideo'] = false;
      component['hideAllErrorMessage'] = jasmine.createSpy('hideAllErrorMessage');
    });

    it('should hanlde case of anonymous user', fakeAsync(() => {
      userService.status = false;

      component.playStream();
      tick();

      expect(component.showPlayer).toBeFalsy();
      expect(component['showStream']).toBeFalsy();
      expect(streamErrorListener).toHaveBeenCalledWith('onlyLoginRequired');
      expect(showHideStreamListener).not.toHaveBeenCalled();
    }));

    it('should catch error of getProviderInfo', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      iGameMediaService.getStreamsForEvent.and.returnValue(throwError('error'));

      component.playStream();
      tick();

      expect(component.showPlayer).toBeFalsy();
      expect(component['showStream']).toBeFalsy();
      expect(streamErrorListener).toHaveBeenCalledWith('streamIsNotAvailable');
      expect(showHideStreamListener).not.toHaveBeenCalled();
    }));

    it('should handle case when stored stream has error', fakeAsync(() => {
      const reason = 'usageLimitsBreached';
      const providerInfo = {
        stream: 'stream/url',
        error: reason
      } as IStreamProvidersResponse;

      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));

      component.playStream();
      tick();

      expect(component.showPlayer).toBeFalsy();
      expect(component['showStream']).toBeFalsy();
      expect(streamErrorListener).toHaveBeenCalledWith('servicesCrashed');
      expect(showHideStreamListener).not.toHaveBeenCalled();
    }));

    it('should handle success case when player was not shown', fakeAsync(() => {
      const providerInfo = {
        stream: 'stream/url'
      } as IStreamProvidersResponse;

      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      component.showPlayer = false;
      iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));

      component.playStream();
      tick();

      expect(component.showPlayer).toBeTruthy();
      expect(component['showStream']).toBeTruthy();
      expect(streamErrorListener).not.toHaveBeenCalled();
      expect(showHideStreamListener).not.toHaveBeenCalled();
    }));

    it('should define showCSBIframe and unsubscribeOfWrapperListeners', fakeAsync(() => {
      component.showCSBIframe = false;
      const providerInfo = {
        stream: 'stream/url'
      } as IStreamProvidersResponse;

      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      eventEntity.streamProviders.iGameMedia = false;
      iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));

      spyOn(component as any, 'unsubscribeOfWrapperListeners');
      watchRulesService.shouldShowCSBIframe.and.returnValue(true);

      component.playStream();
      tick();

      expect(component.showCSBIframe).toBeTruthy();
      expect(component['unsubscribeOfWrapperListeners']).toHaveBeenCalled();
    }));

    it('should Not unsubscribeOfWrapperListeners if showCSBIframe equal false', fakeAsync(() => {
      spyOn(component as any, 'unsubscribeOfWrapperListeners');
      watchRulesService.shouldShowCSBIframe.and.returnValue(false);

      component.playStream();
      tick();

      expect(component.showCSBIframe).toBeFalsy();
      expect(component['unsubscribeOfWrapperListeners']).not.toHaveBeenCalled();
    }));

    it('should handle success case when player was shown for desktop device and not IMG and not showCSBIframe',
      fakeAsync(() => {
        const providerInfo = {
          stream: 'stream/url'
        } as IStreamProvidersResponse;

        sessionService.whenProxySession.and.returnValue(Promise.resolve());
        userService.status = true;
        deviceService.isDesktop = false;
        eventEntity.streamProviders.iGameMedia = true;
        iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));
        watchRulesService.shouldShowCSBIframe.and.returnValue(true);

        component.playStream();
        tick();

        expect(showHideStreamListener).not.toHaveBeenCalledWith(true);
      }));

      it('should define performConfig', fakeAsync(() => {
        const meta = {
          partnerId: '1',
          seed: '123asd'
        } as any;

        spyOn(console, 'warn');
        component['eventEntity'].id = 1;
        component['streamCache'].set(1, { meta } as any);
        sessionService.whenProxySession.and.returnValue(Promise.resolve());
        userService.status = true;
        eventEntity.streamProviders.iGameMedia = false;
        iGameMediaService.getStreamsForEvent.and.returnValue(of({ meta }));
        watchRulesService.shouldShowCSBIframe.and.returnValue(false);

        component.playStream();
        tick();

        expect(component.performConfig).toEqual(meta);
        expect(console.warn).not.toHaveBeenCalled();
      }));

      it('should define performConfig', fakeAsync(() => {
        const meta = { } as any;

        spyOn(console, 'warn');
        component['eventEntity'].id = 1;
        component['streamCache'].set(1, { meta } as any);
        sessionService.whenProxySession.and.returnValue(Promise.resolve());
        userService.status = true;
        eventEntity.streamProviders.iGameMedia = false;
        iGameMediaService.getStreamsForEvent.and.returnValue(of({ meta }));
        watchRulesService.shouldShowCSBIframe.and.returnValue(false);

        component.playStream();
        tick();

        expect(component.performConfig).toEqual(meta);
        expect(console.warn).not.toHaveBeenCalled();
      }));

      it('should console.warn if Not performConfig', fakeAsync(() => {
        spyOn(console, 'warn');
        component['eventEntity'].id = 1;
        component['streamCache'].set(1, { } as any);
        sessionService.whenProxySession.and.returnValue(Promise.resolve());
        userService.status = true;
        eventEntity.streamProviders.iGameMedia = false;
        iGameMediaService.getStreamsForEvent.and.returnValue(of({ }));
        watchRulesService.shouldShowCSBIframe.and.returnValue(false);

        component.playStream();
        tick();

        expect(console.warn).toHaveBeenCalledWith(jasmine.any(String));
      }));

      it('should console.warn if Not performConfig', fakeAsync(() => {
        const meta = null as any;

        spyOn(console, 'warn');
        component['eventEntity'].id = 1;
        component['streamCache'].set(1, { meta } as any);
        sessionService.whenProxySession.and.returnValue(Promise.resolve());
        userService.status = true;
        eventEntity.streamProviders.iGameMedia = false;
        iGameMediaService.getStreamsForEvent.and.returnValue(of({ meta }));
        watchRulesService.shouldShowCSBIframe.and.returnValue(false);

        component.playStream();
        tick();

        expect(console.warn).toHaveBeenCalledWith(jasmine.any(String));
      }));

      afterEach(() => {
        expect(component['hideAllErrorMessage']).toHaveBeenCalled();
      });
  });

  describe('playReplayStream', () => {
    let streamErrorListener;
    let showHideStreamListener;
    beforeEach(() => {
      streamErrorListener = jasmine.createSpy('streamErrorListener');
      showHideStreamListener = jasmine.createSpy('showHideStreamListener');
      component['hideAllErrorMessage'] = jasmine.createSpy('hideAllErrorMessage');

      eventVideoStreamProvider.showHideStreamListener.subscribe(showHideStreamListener);
      component.playStreamError.subscribe(streamErrorListener);
      component.showPlayer = true;
      component['showStream'] = true;
      component['isReplayVideo'] = true;
     
    });
    it('should hanlde case of anonymous user', fakeAsync(() => {
      userService.status = false;
      component.playReplayStream();
      tick();
      expect(component.showPlayer).toBeFalsy();
      expect(component['showStream']).toBeFalsy();
      expect(streamErrorListener).toHaveBeenCalledWith('onlyLoginRequired');
      expect(showHideStreamListener).not.toHaveBeenCalled();      
    }));

    it('getHRReplayUrls success', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      component.playReplayStream();
    }));
    afterEach(() => {
      expect(component['hideAllErrorMessage']).toHaveBeenCalled();
    });
  });
  describe('getHRReplayUrls', () => {
    it('getHRReplayUrls null rsponse', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      const errorMessage = 'servicesCrashed';
      const streamingUrlresp = null;
      iGameMediaService.getHRReplayStreamUrls.and.returnValue(of(streamingUrlresp));
      component.getHRReplayUrls();
      tick();
    }));
    it('should catch error of getHRReplayUrls', fakeAsync(() => {
      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      userService.status = true;
      component['isDesktop'] = false;
      const streamingUrlresp = {
        provider: "ATR",
        streamInfo: {
          bitrateLevel: "Adaptive",
          streamUrl: 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8#t=550,600'

        },
        status: "ERROR",
        closingStage: 550,
        message: "Streaming error / authentication failed / VOD not available"
      }
      component.showCSBIframeReplay = false;
      iGameMediaService.getHRReplayStreamUrls.and.returnValue(of(streamingUrlresp));
    
      component['getHRReplayUrls']();
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        DialogService.API.videoStreamError, { name: 'VideoStreamErrorDialogComponent'}, true, {
          errorMsg:streamingUrlresp.message ,
          eventEntity,
          isInactivePopup: false
                }
      );
    }));
  });

  describe('hideAllErrorMessage', () => {
    it('should reset all error types', () => {
      component.ERROR_MESSAGES.eventFinished = true;
      component.ERROR_MESSAGES.geoBlocked = true;
      component.errorMessage = 'geoBlocked';

      component['hideAllErrorMessage']();

      expect(component.ERROR_MESSAGES.eventFinished).toBeFalsy();
      expect(component.ERROR_MESSAGES.geoBlocked).toBeFalsy();
      expect(component.errorMessage).toEqual('');
    });
  });

  describe('handlePlayingStream', () => {
    let streamErrorListener;
    let showHideStreamListener;

    beforeEach(() => {
      streamErrorListener = jasmine.createSpy('streamErrorListener');
      showHideStreamListener = jasmine.createSpy('showHideStreamListener');

      eventVideoStreamProvider.showHideStreamListener.subscribe(showHideStreamListener);
      component.playStreamError.subscribe(streamErrorListener);
    });

    describe('should set showPlayer status from native', () => {
      beforeEach(() => {
        component.showPlayer = false;
        component['showStream'] = false;
        deviceService.isWrapper = true;
        nativeBridgeService.playerStatus = true;
        component['isReplayVideo']=false;

      });
      it('and hide stream', fakeAsync(() => {
        component['handlePlayingStream']();
        tick();
        expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
      }));
      

      it('and not terminate non-playing native video', fakeAsync(() => {
        nativeBridgeService.playerStatus = false;
        component['handlePlayingStream']();
        tick();
        expect(nativeBridgeService.hideVideoStream).not.toHaveBeenCalled();
      }));

      it('and not terminate native video if providerInfoAvailable', fakeAsync(() => {
        component.providerInfoAvailable = true;
        nativeBridgeService.playerStatus = true;
        component['handlePlayingStream']();
        tick();
        expect(nativeBridgeService.hideVideoStream).not.toHaveBeenCalled();
      }));
      afterEach(() => {
        expect(component.showPlayer).toBeFalsy();
        expect(component.providerInfoAvailable).toBeFalsy();
        expect(showHideStreamListener).toHaveBeenCalledWith(false);
      });
    });

    it('should not change showPlayer if showCSBIframe equal true', fakeAsync(() => {
      component.showPlayer = false;
      component.showCSBIframe = true;
      component['showStream'] = false;
      deviceService.isWrapper = true;
      component['handlePlayingStream']();
      tick();

      expect(component.showPlayer).toBeFalsy();
    }));
    it('isReplayVideo', fakeAsync(() => {
      userService.status = true;
      deviceService.isDesktop = false;
      component.showPlayer = false;
      component['showStream'] = true;
      component['isReplayVideo'] = true;
      component['handlePlayingStream']();
      tick();
    }));
    it('should play stream', fakeAsync(() => {
      const providerInfo = {
        stream: 'stream/url'
      } as IStreamProvidersResponse;

      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));
      userService.status = true;
      deviceService.isDesktop = false;
      component.showPlayer = false;
      component['showStream'] = true;

      component['handlePlayingStream']();
      tick();

      expect(component.showPlayer).toBeTruthy();
      expect(streamErrorListener).not.toHaveBeenCalled();
      expect(showHideStreamListener).not.toHaveBeenCalled();
    }));

    it('should play stream once', fakeAsync(() => {
      const providerInfo = {
        stream: 'stream/url'
      } as IStreamProvidersResponse;

      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));
      userService.status = true;
      component['showStream'] = true;

      component['handlePlayingStream']();
      component['handleUserAuth']();
      expect(sessionService.whenProxySession).toHaveBeenCalledTimes(1);
    }));
  });

  describe('toggleStream', () => {
    let showHideStreamListener;

    beforeEach(() => {
      showHideStreamListener = jasmine.createSpy('showHideStreamListener');
      eventVideoStreamProvider.showHideStreamListener.subscribe(showHideStreamListener);
    });

    it('should change stream shown property and hide stream', fakeAsync(() => {
      component['showStream'] = true;

      component['toggleStream']();
      tick();

      expect(component['showStream']).toBeFalsy();
      expect(showHideStreamListener).toHaveBeenCalledWith(false);
    }));
  });

  describe('handleUserAuth', () => {
    let showHideStreamListener;

    beforeEach(() => {
      showHideStreamListener = jasmine.createSpy('showHideStreamListener');

      eventVideoStreamProvider.showHideStreamListener.subscribe(showHideStreamListener);
    });

    it('should handle case for session login event', fakeAsync(() => {
      deviceService.isDesktop = false;
      userService.status = true;
      createComponent();
      component.showPlayer = true;
      component['showStream'] = true;
      component['ERROR_MESSAGES'].onlyLoginRequired = true;
      component.errorMessage = 'login required';

      component['handleUserAuth']();
      tick();

      expect(component.showPlayer).toBeFalsy();
      expect(component['showStream']).toBeFalsy();
      expect(component.errorMessage).toEqual('');
      expect(component['ERROR_MESSAGES'].onlyLoginRequired).toBeFalsy();
      expect(showHideStreamListener).toHaveBeenCalledWith(false);
    }));

    it('should handle case for session login event and show player if it is desktop', fakeAsync(() => {
      deviceService.isDesktop = true;
      userService.status = true;
      createComponent();
      component.showPlayer = true;
      component['showStream'] = true;
      component['ERROR_MESSAGES'].onlyLoginRequired = true;
      component.errorMessage = 'login required';

      component['handleUserAuth']();
      tick();

      expect(component.showPlayer).toBeTruthy();
      expect(component['showStream']).toBeTruthy();
      expect(component.errorMessage).toEqual('');
      expect(component['ERROR_MESSAGES'].onlyLoginRequired).toBeFalsy();
      expect(iGameMediaService.getStreamsForEvent).toHaveBeenCalled();
    }));

    it('should handle case for session logout event when player was shown', fakeAsync(() => {
      const errorMessage = 'service crashed';

      component.showPlayer = true;
      component['showStream'] = true;
      component['ERROR_MESSAGES'].servicesCrashed = true;
      localeService.getString.and.returnValue(errorMessage);

      userService.status = false;
      component['handleUserAuth']();
      tick();

      expect(component.showPlayer).toBeFalsy();
      expect(component['showStream']).toBeFalsy();
      expect(component.errorMessage).toEqual(errorMessage);
      expect(showHideStreamListener).toHaveBeenCalledWith(false);
    }));
  });

  describe('ngOnInit', () => {
    let showHideStreamListener;

    beforeEach(() => {
      showHideStreamListener = jasmine.createSpy('showHideStreamListener');
      eventVideoStreamProvider.showHideStreamListener.subscribe(showHideStreamListener);
    });

    it('should susbscribe for pubsub events and parse css classes', () => {
      const cssClassesForStreams = {
        iGameMedia: 'hide-desktop',
        otherProviders: 'show-all'
      };

      component.cssClassesForStreams = cssClassesForStreams;
      component.ngOnInit();

      expect(pubsubService.subscribe).toHaveBeenCalledWith('EventVideoStreamComponent',
        [pubsubService.API.SUCCESSFUL_LOGIN, pubsubService.API.SESSION_LOGOUT], component['handleUserAuth']);
      expect(component['iGameMediaCssClasses']).toEqual(cssClassesForStreams.iGameMedia);
      expect(component['videoStreamProvidersCssClasses']).toEqual(cssClassesForStreams.otherProviders);
    });

    it('should subscribe to playListener', fakeAsync(() => {
      component['showStream'] = true;

      component.ngOnInit();
      eventVideoStreamProvider.playListener.next();
      tick();

      expect(component['showStream']).toBeFalsy();
      expect(showHideStreamListener).toHaveBeenCalledWith(false);
    }));

    it('should preload stream', fakeAsync(() => {
      const providerInfo = {
        stream: 'stream/url'
      } as IStreamProvidersResponse;

      sessionService.whenProxySession.and.returnValue(Promise.resolve());
      iGameMediaService.getStreamsForEvent.and.returnValue(of(providerInfo));
      userService.status = true;

      component.preloadStream = true;
      component.ngOnInit();
      tick();

      expect(component.showPlayer).toBeTruthy();
      expect(showHideStreamListener).not.toHaveBeenCalled();
    }));

    it('should not add listener for native player', () => {
      component.ngOnInit();
      expect(windowRefService.document.addEventListener).not.toHaveBeenCalled();
    });

    it('should add listener for native player', () => {
      deviceService.isWrapper = true;

      component.ngOnInit();

      expect(windowRefService.document.addEventListener).toHaveBeenCalledWith('CURRENT_WATCH_LIVE_STATE_CHANGED', jasmine.any(Function));
    });
  });

  describe('@setStreamShowFlag', () => {
    it('should reset flags when native wrapper\'s player in closing', () => {
      component.showPlayer = true;
      (component as any).showStream = true;
      spyOn(component['playStreamError'], 'emit');

      component['setStreamShowFlag']({ detail: { settingValue: false } as any });
      expect(component['showStream']).toBeFalsy();
      expect(component['showPlayer']).toBeFalsy();
      expect(component['playStreamError'].emit).toHaveBeenCalled();
    });
    it('should not reset flags when native wrapper\'s player is opening closing', () => {
      component.showPlayer = false;
      (component as any).showStream = false;
      spyOn(component['playStreamError'], 'emit');

      component['setStreamShowFlag']({ detail: { settingValue: true } as any });
      expect(component['showStream']).toBeTruthy();
      expect(component['showPlayer']).toBeTruthy();
      expect(component['playStreamError'].emit).not.toHaveBeenCalled();
    });
  });

  describe('isStreamBetAvailable', () => {
    it('should call the isStreamBetAvailable', () => {      
      component.eventEntity = {categoryId: '21'} as any;
      component.providerInfo = {
        priorityProviderName:'ATR'
      } as any;
      component.isMyBets = false; 
      component['isMobile'] = true; 
      component.providerInfoAvailable = true;     
      component['streamBetCmsConfig'] = {
        enabled: true,
        sportIds: ['16', '21'],
        streamProviders: ['ATR']        
      };
      expect(component.isStreamBetAvailable()).toBeTruthy();
    });
  });

  describe('ngOnChanges', () => {
    beforeEach(() => {
      spyOn(component as any, 'handleReloadStream');
      component.isOnInitDone = true;
    });

    it('should call the handleReloadStream', () => {
      component.ngOnChanges({eventEntity: true} as any);
      expect(component['handleReloadStream']).toHaveBeenCalled();
    });

    it('should not call the handleReloadStream', () => {
      component.ngOnChanges({eventEntity: false} as any);
      expect(component['handleReloadStream']).not.toHaveBeenCalled();
    });
  });
});

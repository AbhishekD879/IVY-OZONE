import { fakeAsync, tick } from '@angular/core/testing';
import { of as observableOf, Subject, throwError, from as observableFrom } from 'rxjs';

import {
  VideoStreamProvidersComponent
} from '@lazy-modules/eventVideoStream/components/videoStreamProviders/video-stream-providers.component';

import { DialogService } from '@core/services/dialogService/dialog.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IPerformGroupConfig, IStreamProvidersResponse } from '@lazy-modules/eventVideoStream/models/video-stream.model';

describe('VideoStreamProvidersComponent', () => {
  let component: VideoStreamProvidersComponent;
  let windowRefService;
  let streamTrackingService;
  let elementRef;
  let deviceService;
  let gtmService;
  let eventEntity;
  let commandService;
  let loadVideoJsService;
  let eventVideoStreamProvider;
  let localeService;
  let cmsService;
  let nativeBridgeService;
  let rendererService;
  let sessionService;
  let liveStreamService;
  let racingStreamService;
  let imgService;
  let watchRulesService;
  let atTheRacesService;
  let userService;
  let domSanitizer;
  let performGroupService;
  let mockHtml5VideoTag;
  let desktopPlayerMock;
  let successHandler;
  let errorHandler;
  let cmsConfigs;
  let convivaService;
  let dialogService;
  let componentFactoryResolver;
  let activatedRoute;
  let videoStreamData

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.returnValue(Math.random()),
        clearTimeout: jasmine.createSpy('clearTimeout').and.returnValue(null),
        videojs: jasmine.createSpy('videojs')
      },
      document: {
        getElementById: jasmine.createSpy('getElementById')
      }
    }; activatedRoute = {
      snapshot: {
        params: {}
      }
    };
    loadVideoJsService = {
      loadScripts: jasmine.createSpy('loadScripts').and.returnValue(observableOf({}))
    };
    streamTrackingService = {
      setTrackingForPlayer: jasmine.createSpy('setTrackingForPlayer'),
      addIdToTrackedList: jasmine.createSpy('addIdToTrackedList'),
      checkIdForDuplicates: jasmine.createSpy('checkIdForDuplicates')
    };
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({})
      }
    };
    deviceService = {
      isDesktop: true,
      isMobile:false,
      performProviderIsMobile: jasmine.createSpy('performProviderIsMobile').and.callFake(v => v)
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    commandService = {
      register: jasmine.createSpy('register'),
      unregister: jasmine.createSpy('unregister'),
      API: {
        GET_LIVE_STREAM_STATUS: 'GET_LIVE_STREAM_STATUS'
      }
    };
    eventVideoStreamProvider = {
      playListener: new Subject<void>(),
      showHideStreamListener: new Subject<boolean>(),
      playSuccessErrorListener: new Subject<boolean>()
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('localeString')
    };
    nativeBridgeService = {
      supportsVideo: jasmine.createSpy('supportsVideo'),
      playerStatus: false,
      showErrorForNative: jasmine.createSpy('showErrorForNative'),
      hideVideoStream: jasmine.createSpy('hideVideoStream'),
      showVideoIfExist: jasmine.createSpy('showVideoIfExist')
    };
    eventEntity = {
      id: 111,
      typeId: '11',
      categoryId: '1',
      categoryCode: 'FOOTBALL',
      streamProviders: {
        ATR: false,
        RPGTV: false,
        RacingUK: false,
        IMG: false,
        Perform: false
      }
    } as ISportEvent;
    videoStreamData={
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
    };
    performGroupService = {
      isEventStarted: jasmine.createSpy('isEventStarted').and.returnValue(false),
      performGroupId: jasmine.createSpy('performGroupId').and.returnValue(observableOf(true)),
      getVideoUrl: jasmine.createSpy('getVideoUrl').and.callFake(v => observableOf(v)),
      getElementWidth: jasmine.createSpy('isEventStarted')
    };
    domSanitizer = {
      bypassSecurityTrustUrl: jasmine.createSpy('bypassSecurityTrustUrl').and.callFake((v) => v)
    };
    userService = {};
    atTheRacesService = {
      isEventStarted: jasmine.createSpy('isEventStarted').and.returnValue(false),
      setConfigParams: jasmine.createSpy('setConfigParams'),
      getVideoUrl: jasmine.createSpy('getVideoUrl').and.callFake(v => observableOf(v))
    };
    watchRulesService = {
      canWatchEvent: jasmine.createSpy('canWatchEvent').and.returnValue(observableOf(true)),
      canWatchPerformStream: jasmine.createSpy('canWatchPerformStream').and.returnValue(observableOf(true)),
      isInactiveUser: jasmine.createSpy('isInactiveUser').and.returnValue(false)
    };
    imgService = {
      isEventStarted: jasmine.createSpy('isEventStarted').and.returnValue(false),
      getVideoUrl: jasmine.createSpy('getVideoUrl').and.callFake(v => observableOf(v)),
      setConfigParams: jasmine.createSpy('setConfigParams')
    };
    racingStreamService = {
      isEventStarted: jasmine.createSpy('isEventStarted').and.returnValue(false),
      getVideoUrl: jasmine.createSpy('getVideoUrl').and.callFake(v => observableOf(v))
    };
    sessionService = {};
    liveStreamService = {
      checkIfRacingEvent: jasmine.createSpy('checkIfRacingEvent').and.returnValue(false)
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(Math.random())
      }
    };
    convivaService = {
      preload: jasmine.createSpy('preload'),
      initVideoAnalytics: jasmine.createSpy('initVideoAnalytics'),
      release: jasmine.createSpy('release'),
      initVideoJsAnalytics: jasmine.createSpy('initVideoJsAnalytics'),
      setConfig: jasmine.createSpy('setConfig'),
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy().and.returnValue({ name: 'VideoStreamErrorDialogComponent'})
    };
    mockHtml5VideoTag = {
      pause: jasmine.createSpy('pauseHtml5'),
      removeEventListener: jasmine.createSpy('removeEventListener'),
      addEventListener: jasmine.createSpy('addEventListener'),
      play: jasmine.createSpy('playHtml5'),
      currentTime: jasmine.createSpy('currentTime'),
      classList: { remove: jasmine.createSpy('remove') }
      };
    desktopPlayerMock = {
     tech : jasmine.createSpy('tech').and.returnValue({
      on: jasmine.createSpy('on')
     }),
      reset: jasmine.createSpy('reset'),
      errorDisplay: {
        opened_: true
      },
      error: jasmine.createSpy('error'),
      dispose: jasmine.createSpy('dispose'),
      src: jasmine.createSpy('src'),
      ready: jasmine.createSpy('ready'),
      play: jasmine.createSpy('play'),
      on: jasmine.createSpy('play'),
      currentTime:jasmine.createSpy('currentTime'),
      playsinline: jasmine.createSpy('playsinline'),
      classList: { remove: jasmine.createSpy('remove') }
    };
    cmsConfigs = {
      imgStreamingConfig: {
        operatorId: 1,
        IMGSecret: 'secret'
      },
      performConfig: {
        id: '123'
      },
      atTheRacesConfig: {
        PartnerCode: 1,
        Secret: 'secret'
      },
      Conviva: {
        enabled: true
      }
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        performGroup: cmsConfigs.performConfig,
        IMGStreaming: cmsConfigs.imgStreamingConfig,
        AtTheRaces: cmsConfigs.atTheRacesConfig,
        Conviva: cmsConfigs.Conviva
      }))
    };

    successHandler = jasmine.createSpy('success');
    errorHandler = jasmine.createSpy('errorHandler');

    component = new VideoStreamProvidersComponent(performGroupService, domSanitizer, elementRef, userService, windowRefService,
      cmsService, commandService, atTheRacesService, watchRulesService, imgService, racingStreamService,
      nativeBridgeService, localeService, loadVideoJsService, streamTrackingService, gtmService,
      sessionService, deviceService, liveStreamService, eventVideoStreamProvider, rendererService, convivaService,
      dialogService, componentFactoryResolver,activatedRoute
    );

    component.eventEntity = eventEntity;
    component.videoStreamData = videoStreamData;
    component.streamCache = new Map();
    component.streamUniqueId = "rtmpe-hls";
    component.isReplayVideo = false;
    component['html5VideoTag'] = mockHtml5VideoTag;
    component['performConfig'] = {
      partnerId: '2',
      seed: '123asd'
    } as any;
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should call playStream method if its Wrapper and playerStatus is false', () => {
    nativeBridgeService.playerStatus = false;
    deviceService.isWrapper = true;
    deviceService.isMobile = true;
    spyOn(component, 'playStream');
    expect(component).toBeTruthy();

    component['eventVideoStreamProvider'].playListener.subscribe(() => {
      expect(component.playStream).toHaveBeenCalled();
    });
  });

  it('should init video player', () => {
    component.playStream();
    component.streamUniqueId = 'rtmpe-hls';
    expect(elementRef.nativeElement.querySelector).toHaveBeenCalledWith('#rtmpe-hls');
    expect(windowRefService.nativeWindow.videojs).toHaveBeenCalled();
  });

  it('should showErrorMessage', () => {
    component.ERROR_MESSAGES.loginRequired = true;
    component['deviceService'].isDesktop = false;
    component['deviceService'].isMobile = true;
    component.showErrorMessage('eventNotStarted');

    expect(component.ERROR_MESSAGES.loginRequired).toBeFalsy();
    expect(component.ERROR_MESSAGES.eventNotStarted).toBeTruthy();

    component.desktopPlayer = desktopPlayerMock;
    component['deviceService'].isDesktop = true;
    component['deviceService'].isMobile = false;
    component.showErrorMessage('onlyLoginRequired');

    expect(localeService.getString).toHaveBeenCalledWith('sb.onlyLoginRequired');
    expect(component.desktopPlayer.errorDisplay.opened_).toBeFalsy();
    expect(component.desktopPlayer.error).toHaveBeenCalledWith('localeString');
  });

  it('getVideoType should return "application/x-mpegURL"', () => {
    expect(component['getVideoType']('url')).toEqual('application/x-mpegURL');
  });

  describe('showError', () => {
    beforeEach(() => {
      component.showPlayer = true;
      eventEntity.isFinished = false;
    });

    it('should show default error reason', () => {
      component['showError'](null);

      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
      expect(component['ERROR_MESSAGES'].servicesCrashed).toBeTruthy();
      expect(component.showPlayer).toBeFalsy();
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
      watchRulesService.isInactiveUser.and.returnValue(false);
      nativeBridgeService.supportsVideo.and.returnValue(true);
      component['showError'](null);

      expect(nativeBridgeService.showErrorForNative).toHaveBeenCalledWith('servicesCrashed');
    });

    it('should show web error even it is wrapper but user gets inactive qualification error', () => {
      nativeBridgeService.supportsVideo.and.returnValue(true);
      watchRulesService.isInactiveUser.and.returnValue(true);
      component['showError']('deniedByInactiveWatchRules');

      expect(component.isInactiveUserError).toBeTruthy();
      expect(nativeBridgeService.showErrorForNative).not.toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith(`sb.deniedByInactiveWatchRules`);
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
        DialogService.API.videoStreamError, { name: 'VideoStreamErrorDialogComponent' }, true, {
          errorMsg: translation,
          eventEntity,
          isInactivePopup: false,
          isReplay: false
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

  describe('onError', () => {
    let streamErrorListener;

    beforeEach(() => {
      streamErrorListener = jasmine.createSpy('streamErrorListener');
      component.playStreamError.subscribe(streamErrorListener);
      component.showVideoPlayer = true;
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
      expect(component.showVideoPlayer).toBeFalsy();
    }));
  });

  describe('hideStream', () => {
    let playSuccessErrorListener;

    beforeEach(() => {
      playSuccessErrorListener = jasmine.createSpy('playSuccessErrorListener');
      eventVideoStreamProvider.playSuccessErrorListener.subscribe(playSuccessErrorListener);

      component.showPlayer = true;
      component['streamActive'] = true;
    });

    it('should handle not desktop mode', fakeAsync(() => {
      component['hideStream']();
      tick();

      expect(playSuccessErrorListener).toHaveBeenCalledWith(false);
      expect(mockHtml5VideoTag.pause).toHaveBeenCalled();
      expect(component.showPlayer).toBeFalsy();
      expect(component['streamActive']).toBeFalsy();
    }));

    it('should handle not desktop mode but wrapper mode', fakeAsync(() => {
      deviceService.isWrapper = true;
      deviceService.isMobile = true;

      component['hideStream']();
      tick();

      expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
      expect(playSuccessErrorListener).toHaveBeenCalledWith(false);
      expect(mockHtml5VideoTag.pause).not.toHaveBeenCalled();
      expect(component.showPlayer).toBeFalsy();
      expect(component['streamActive']).toBeFalsy();
    }));

    it('should handle desktop mode without desktop player', fakeAsync(() => {
      deviceService.isDesktop = true;
      component['hideStream']();
      tick();

      expect(nativeBridgeService.hideVideoStream).toHaveBeenCalled();
      expect(playSuccessErrorListener).toHaveBeenCalledWith(false);
      expect(mockHtml5VideoTag.pause).toHaveBeenCalled();
    }));

    it('should handle desktop mode with desktop player', fakeAsync(() => {
      deviceService.isDesktop = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['hideStream']();
      tick();

      expect(playSuccessErrorListener).toHaveBeenCalledWith(false);
      expect(mockHtml5VideoTag.pause).not.toHaveBeenCalled();
      expect(desktopPlayerMock.reset).toHaveBeenCalledWith();
    }));
  });

  describe('setPlayerSize', () => {
    it('should calculate frame width based on elementWidth', () => {
      const elementWidth = 100;
      performGroupService.getElementWidth.and.returnValue(elementWidth);
      const parentNode = { tag: 'div' };

      elementRef.nativeElement.parentNode = parentNode;
      component['setPlayerSize']();

      expect(component.frameWidth).toEqual(elementWidth);
      expect(component.frameHeight).toEqual(56);
    });

    it('should calculate frame width based on stored frameWidth', () => {
      const parentNode = { tag: 'div' };

      component.frameWidth = 200;

      elementRef.nativeElement.parentNode = parentNode;
      component['setPlayerSize']();

      expect(component.frameWidth).toEqual(200);
      expect(component.frameHeight).toEqual(112);
    });
  });

  describe('pushToDataLayer', () => {
    it('should push event data to gtm datalayer', () => {
      component['pushToDataLayer']();

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'streaming',
        eventAction: 'click',
        eventLabel: 'watch video stream',
        sportID: eventEntity.categoryId,
        typeID: eventEntity.typeId,
        eventId: eventEntity.id
      }));
    });
  });

  describe('getStreamId', () => {
    it('should not set streamId if passed providerInfo is not valid', () => {
      component['getStreamId'](null);
      expect(component['streamID']).toBeFalsy();

      component['getStreamId']({} as IStreamProvidersResponse);
      expect(component['streamID']).toBeFalsy();

      component['getStreamId']({listOfMediaProviders: []} as IStreamProvidersResponse);
      expect(component['streamID']).toBeFalsy();
    });

    it('should not set streamId if passed providerInfo does not have matched childrens', () => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: []
        }, {
          name: 'Perform',
          children: null
        }]
      } as IStreamProvidersResponse;

      component['getStreamId'](providerInfo);
      expect(component['streamID']).toBeFalsy();

      providerInfo.listOfMediaProviders[1].children = [];
      expect(component['streamID']).toBeFalsy();

      providerInfo.listOfMediaProviders[1].children = [{
        media: null
      }];
      expect(component['streamID']).toBeFalsy();
    });

    it('should set streamId as null if accessProperty is "0"', () => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: []
        }, {
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'imgEventId:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['getStreamId'](providerInfo);
      expect(component['streamID']).toBeNull();
    });

    it('should set streamId if accessProperty is not "0"', () => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: []
        }, {
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['getStreamId'](providerInfo);
      expect(component['streamID']).toEqual(',1231223:');
    });
  });

  describe('checkCanWatch', () => {
    beforeEach(() => {
      component['streamID'] = '1234';
      component['streamActive'] = true;
    });

    it('should reset streamActive flag and return true if watchRulesService was triggered before', fakeAsync(() => {
      component['canWatchEvent'] = true;

      component['checkCanWatch']().subscribe(successHandler, errorHandler);
      tick();

      expect(component['streamID']).toBeNull();
      expect(component['streamActive']).toBeFalsy();
      expect(component['canWatchEvent']).toBeTruthy();
      expect(successHandler).toHaveBeenCalledWith(true);
    }));

    it('should handle success check of watchRuleService', fakeAsync(() => {
      component['canWatchEvent'] = false;

      component['checkCanWatch']().subscribe(successHandler, errorHandler);
      tick();

      expect(component['streamID']).toBeNull();
      expect(component['streamActive']).toBeFalsy();
      expect(component['canWatchEvent']).toBeTruthy();
      expect(successHandler).toHaveBeenCalled();
    }));

    it('should handle error check of watchRuleService', fakeAsync(() => {
      component['canWatchEvent'] = false;
      watchRulesService.canWatchEvent.and.returnValue(throwError(''));

      component['checkCanWatch']().subscribe(successHandler, errorHandler);
      tick();

      expect(component['streamID']).toBeNull();
      expect(component['streamActive']).toBeFalsy();
      expect(component['canWatchEvent']).toBeFalsy();
      expect(errorHandler).toHaveBeenCalled();
    }));
  });

  describe('getStreamNotStartedMessage', () => {
    it('should handle not matched stream provider', (() => {
      component.eventEntity.streamProviders.iGameMedia = true;

      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);

      expect(successHandler).toHaveBeenCalledWith('');
    }));

    it('should handle Perform provider', () => {
      component.eventEntity.streamProviders.Perform = true;
      performGroupService.isEventStarted.and.returnValue(true);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);

      expect(successHandler).toHaveBeenCalledWith('');

      performGroupService.isEventStarted.and.returnValue(false);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);

      expect(errorHandler).toHaveBeenCalledWith('eventNotStarted');
    });

    it('should handle IMG provider', () => {
      component.eventEntity.streamProviders.IMG = true;
      imgService.isEventStarted.and.returnValue(true);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);

      expect(successHandler).toHaveBeenCalledWith('');

      imgService.isEventStarted.and.returnValue(false);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);

      expect(errorHandler).toHaveBeenCalledWith('eventNotStarted');
    });

    it('should handle RacingUK provider', () => {
      component.eventEntity.streamProviders.RacingUK = true;
      racingStreamService.isEventStarted.and.returnValue(true);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);
      expect(successHandler).toHaveBeenCalledWith('');

      racingStreamService.isEventStarted.and.returnValue(false);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);
      expect(errorHandler).toHaveBeenCalledWith('eventNotStarted');
    });

    it('should handle RPGTV provider', () => {
      component.eventEntity.streamProviders.RPGTV = true;
      racingStreamService.isEventStarted.and.returnValue(true);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);
      expect(successHandler).toHaveBeenCalledWith('');

      racingStreamService.isEventStarted.and.returnValue(false);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);
      expect(errorHandler).toHaveBeenCalledWith('eventNotStarted');
    });

    it('should handle ATR provider', () => {
      component.eventEntity.streamProviders.ATR = true;
      atTheRacesService.isEventStarted.and.returnValue(true);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);
      expect(successHandler).toHaveBeenCalledWith('');

      atTheRacesService.isEventStarted.and.returnValue(false);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);
      expect(errorHandler).toHaveBeenCalledWith('eventNotStarted');
    });
  });

  describe('getStreamUnavailableMessage', () => {
    it('should handle servicesCrashed case', () => {
      component.eventEntity.startTime = '2018-06-30T16:57:00Z';

      expect(component['getStreamUnavailableMessage']()).toEqual('servicesCrashed');
    });

    it('should handle eventFinished case', () => {
      component.eventEntity.startTime = '2018-06-30T16:57:00Z';
      component.eventEntity.isFinished = true;
      component.eventEntity.streamProviders.ATR = true;

      expect(component['getStreamUnavailableMessage']()).toEqual('eventFinished');
    });

    it('should handle default case', () => {
      component.eventEntity.startTime = '2018-06-30T16:57:00Z';
      component.eventEntity.isFinished = false;
      component.eventEntity.streamProviders.ATR = true;

      expect(component['getStreamUnavailableMessage']()).toEqual('');
    });
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
      expect(component.isInactiveUserError).toBeFalsy();
    });
  });

  describe('autoPlayStream', () => {
    it('should not change property of showVideoPlayer if device is not desktop', () => {
      component['showVideoPlayer'] = true;
      component['isDesktop'] = false;

      component['autoPlayStream']();

      expect(component['showVideoPlayer']).toBeTruthy();
    });

    it('should load scripts and do not perform autoPlay', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;

      component['autoPlayStream']();
      tick();

      expect(loadVideoJsService.loadScripts).toHaveBeenCalled();
      expect(component['videJsTimeout']).not.toBeDefined();
      expect(component['showVideoPlayer']).toBeFalsy();
    }));

    it('should load scripts and do perform autoPlay', fakeAsync(() => {
      component.autoPlay = true;
      component['isDesktop'] = true;
      component['isReplayVideo'] = false;
      component['autoPlayStream']();
      tick();

      expect(loadVideoJsService.loadScripts).toHaveBeenCalled();
      expect(component['showVideoPlayer']).toBeFalsy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(component['playStream']);
    }));
    it('should load scripts and do perform watchreplay', fakeAsync(() => {
      component.autoPlay = true;
      component['isDesktop'] = true;
      component['isReplayVideo'] = true;

      component['autoPlayStream']();
      tick();

      expect(loadVideoJsService.loadScripts).toHaveBeenCalled();
      expect(component['showVideoPlayer']).toBeFalsy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(component['ReplayStream']);
    }));
  });

  describe('handlePlayerError', () => {
    it('should not track error for desktop device type', () => {
      component['isDesktop'] = true;
      liveStreamService.checkIfRacingEvent.and.returnValue(true);

      component['handlePlayerError']();

      expect(gtmService.push).not.toHaveBeenCalled();
      expect(component['trackErrors'].length).toEqual(0);
    });

    it('should not track duplicated errors', () => {
      component['isDesktop'] = false;
      liveStreamService.checkIfRacingEvent.and.returnValue(false);
      component['trackErrors'].push('servicesCrashed');

      component['handlePlayerError']();

      expect(gtmService.push).not.toHaveBeenCalled();
      expect(component['trackErrors'].length).toEqual(1);
    });

    it('should track unique error for racing and non desktop', () => {
      component['isDesktop'] = false;
      liveStreamService.checkIfRacingEvent.and.returnValue(true);
      component['trackErrors'].push('servicesCrashed');
      component.ERROR_MESSAGES.geoBlocked = true;

      component['handlePlayerError']();

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'Livestream',
        eventAction: 'error'
      }));
      expect(localeService.getString).toHaveBeenCalledWith('sb.geoBlocked');
      expect(component['trackErrors'].length).toEqual(2);
    });
  });

  describe('resizeView', () => {
    it('should set timeout property', () => {
      component['resizeTimeFrame'] = 500;
      component['resizeView']();

      expect(windowRefService.nativeWindow.clearTimeout).not.toHaveBeenCalled();
      expect(component['resizeTimeout']).toEqual(jasmine.any(Number));
    });

    it('should clear timeout before storing new one set timeout property', () => {
      component['resizeTimeFrame'] = 500;
      component['resizeView']();
      component['resizeView']();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(jasmine.any(Number));
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(component['setPlayerSize'],
        500);
    });
  });

  describe('contextMenuListener', () => {
    it('should call prevent default method of event object', () => {
      const pointerEvent = {
        preventDefault: jasmine.createSpy('preventDefault')
      };
      component['contextMenuListener'](pointerEvent as any);
      expect(pointerEvent.preventDefault).toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe for command events', () => {
      component['videJsTimeout'] = 1234;
      component.ngOnDestroy();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(component['videJsTimeout']);
      expect(commandService.unregister).toHaveBeenCalledWith(commandService.API.GET_LIVE_STREAM_STATUS);
      expect(mockHtml5VideoTag.removeEventListener).toHaveBeenCalled();
    });

    it('should unsubscribe for action listener', () => {
      component['actionSubscriber'] = eventVideoStreamProvider.playListener.subscribe();

      spyOn(component['actionSubscriber'], 'unsubscribe').and.callThrough();
      component.ngOnDestroy();

      expect(component['actionSubscriber'].unsubscribe).toHaveBeenCalled();
      expect(mockHtml5VideoTag.removeEventListener).toHaveBeenCalled();
    });

    it('should unsubscribe for stream flow listener', () => {
      component['streamFlowSubscriber'] = watchRulesService.canWatchEvent().subscribe();

      spyOn(component['streamFlowSubscriber'], 'unsubscribe').and.callThrough();
      component.ngOnDestroy();

      expect(component['streamFlowSubscriber'].unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe for resize listener', () => {
      const resizeListener = jasmine.createSpy('resizeListener');

      component['resizeListerner'] = resizeListener;
      component.ngOnDestroy();

      expect(resizeListener).toHaveBeenCalled();
      expect(mockHtml5VideoTag.removeEventListener).toHaveBeenCalled();
    });

    it('should close desktop player for desktop device', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      component.ngOnDestroy();

      expect(desktopPlayerMock.dispose).toHaveBeenCalled();
      expect(mockHtml5VideoTag.removeEventListener).toHaveBeenCalled();
    });

    it('should not remove event listener if platform not Desktop ', () => {
      component['isDesktop'] = false;
      component.ngOnDestroy();

      expect(mockHtml5VideoTag.removeEventListener).not.toHaveBeenCalled();
    });

    it('should not remove event listener if html5VideoTag not defined ', () => {
      component['isDesktop'] = true;
      component['html5VideoTag'] = null;
      component.ngOnDestroy();

      expect(mockHtml5VideoTag.removeEventListener).not.toHaveBeenCalled();
    });
    it('should not remove event listener if html5VideoTag not defined ', () => {
      component['isDesktop'] = true;
      component['isMobile'] = true;
      component.ngOnDestroy();

      expect(mockHtml5VideoTag.removeEventListener).toHaveBeenCalled();
    });
  });

  describe('onSuccess', () => {
    let stream;

    beforeEach(() => {
      stream = {stream: 'qwe'} as IStreamProvidersResponse;
      component.streamCache.set(eventEntity.id, {} as IStreamProvidersResponse);
    });

    it('should set passed stream to streamCache', () => {
      component['streamActive'] = false;
      component['onSuccess'](stream);

      expect(component['streamActive']).toBeTruthy();
      expect(component.streamCache.get(eventEntity.id).stream).toEqual(stream);
    });

    it('should not add to tracked list event id if id is duplicated', () => {
      streamTrackingService.checkIdForDuplicates.and.returnValue(true);
      component['onSuccess'](stream);

      expect(streamTrackingService.addIdToTrackedList).not.toHaveBeenCalled();
    });

    it('should add to tracked list event id if all checks passed', () => {
      streamTrackingService.checkIdForDuplicates.and.returnValue(false);
      eventEntity.categoryCode = 'HORSE_RACING';
      component['onSuccess']('');

      expect(streamTrackingService.addIdToTrackedList).toHaveBeenCalledWith(eventEntity.id, 'liveStream');
    });
  });

  describe('renderHtml5Stream', () => {
    const url = 'stream';

    beforeEach(() => {
      component.showPlayer = true;
      eventEntity.isFinished = false;
    });

    it('should show error if device is not performProviderIsMobile', () => {
      deviceService.performProviderIsMobile.and.returnValue(false);

      component['ERROR_MESSAGES'].servicesCrashed = true;
      component['renderHtml5Stream'](url);

      expect(component.showPlayer).toBeFalsy();
      expect(localeService.getString).toHaveBeenCalledWith(`sb.${'onlyForMobile'}`);
      expect(component['ERROR_MESSAGES']['onlyForMobile']).toBeTruthy();
    });

    it('should set streaming url if device is performProviderIsMobile', () => {
      const elementWidth = 100;
      const parentNode = { tag: 'div' };

      deviceService.performProviderIsMobile.and.returnValue(true);
      elementRef.nativeElement.parentNode = parentNode;
      performGroupService.getElementWidth.and.returnValue(elementWidth);

      component['renderHtml5Stream'](url);

      expect(component.showPlayer).toBeTruthy();
      expect(component['streamingUrl']).toEqual(url);
      expect(component.frameWidth).toEqual(elementWidth);
      expect(component.frameHeight).toEqual(56);
    });
  });

  describe('showHideStream', () => {
    beforeEach(() => {
      component['showPlayer'] = false;
    });

    it('should return null if cached stream has error', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: []
        }, {
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component.streamCache.set(eventEntity.id, { error: 'notLoggedIn' } as IStreamProvidersResponse);
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(component['streamID']).toBeFalsy();
      expect(successHandler).toHaveBeenCalledWith(null);
    }));

    it('should return null if no performConfig were found', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: []
        }, {
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;
      component.performConfig = undefined;

      component.streamCache.set(eventEntity.id, {} as IStreamProvidersResponse);
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(component['streamID']).toBeFalsy();
      expect(successHandler).toHaveBeenCalledWith(null);
    }));

    it('should handle IMG provider by provider info', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'IMG Video Streaming',
        listOfMediaProviders: [{
          name: 'IMG Video Streaming',
          children: [{
            media: {
              accessProperties: 'igm,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['streamingConfig'] = {
        operatorId: '1',
        imgSecret: 'secret'
      } as any;

      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(component['streamID']).toEqual(',1231223:');
      expect(imgService.setConfigParams).toHaveBeenCalledWith((<any>component['streamingConfig']).operatorId,
        (<any>component['streamingConfig']).imgSecret);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle IMG provider by event mapped providers', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'iGameMedia',
        listOfMediaProviders: [{
          name: 'iGameMedia',
          children: [{
            media: {
              accessProperties: 'iGameMedia,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['streamingConfig'] = {
        operatorId: '1',
        imgSecret: 'secret'
      } as any;

      eventEntity.streamProviders.IMG = true;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(component['streamID']).toEqual(',1231223:');
      expect(imgService.setConfigParams).toHaveBeenCalledWith((<any>component['streamingConfig']).operatorId,
        (<any>component['streamingConfig']).imgSecret);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle Perform provider by provider info for wrapper', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'Perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['isWrapper'] = true;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(performGroupService.performGroupId).toHaveBeenCalledWith(providerInfo,
        component['performConfig'], 111);
      expect(racingStreamService.getVideoUrl).toHaveBeenCalledWith(providerInfo,
        component['performConfig']);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle Perform provider by provider info for not wrapper', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'Perform',
        listOfMediaProviders: [{
          name: 'Perform',
          children: [{
            media: {
              accessProperties: 'Perform,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['isWrapper'] = false;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(performGroupService.performGroupId).not.toHaveBeenCalled();
      expect(racingStreamService.getVideoUrl).toHaveBeenCalledWith(providerInfo,
        component['performConfig']);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle Perform provider by event mapped providers', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'iGameMedia',
        listOfMediaProviders: [{
          name: 'iGameMedia',
          children: [{
            media: {
              accessProperties: 'iGameMedia,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      eventEntity.streamProviders.Perform = true;
      component['isWrapper'] = false;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);

      expect(performGroupService.performGroupId).not.toHaveBeenCalled();
      expect(racingStreamService.getVideoUrl).toHaveBeenCalledWith(providerInfo,
        component['performConfig']);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle "At The Races" provider by provider info', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'At The Races',
        listOfMediaProviders: [{
          name: 'At The Races',
          children: [{
            media: {
              accessProperties: 'Perfoatrrm,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['streamingConfig'] = {
        partnerCode: '1',
        secret: 'secret'
      } as any;

      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(atTheRacesService.setConfigParams).toHaveBeenCalledWith((<any>component['streamingConfig']).partnerCode,
        (<any>component['streamingConfig']).secret);
      expect(atTheRacesService.getVideoUrl).toHaveBeenCalledWith(providerInfo);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle "At The Races" provider by event mapped providers', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'iGameMedia',
        listOfMediaProviders: [{
          name: 'iGameMedia',
          children: [{
            media: {
              accessProperties: 'iGameMedia,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['streamingConfig'] = {
        partnerCode: '1',
        secret: 'secret'
      } as any;

      eventEntity.streamProviders.ATR = true;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);

      expect(atTheRacesService.setConfigParams).toHaveBeenCalledWith((<any>component['streamingConfig']).partnerCode,
        (<any>component['streamingConfig']).secret);
      expect(atTheRacesService.getVideoUrl).toHaveBeenCalledWith(providerInfo);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle "RacingUK" provider by provider info', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'RacingUK',
        listOfMediaProviders: [{
          name: 'RacingUK',
          children: [{
            media: {
              accessProperties: 'RacingUK,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(racingStreamService.getVideoUrl).toHaveBeenCalledWith(providerInfo,
        component['performConfig']);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle "RacingUK" provider by event mapped providers', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'iGameMedia',
        listOfMediaProviders: [{
          name: 'iGameMedia',
          children: [{
            media: {
              accessProperties: 'iGameMedia,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      eventEntity.streamProviders.RacingUK = true;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);

      expect(racingStreamService.getVideoUrl).toHaveBeenCalledWith(providerInfo,
        component['performConfig']);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle "RPGTV" provider by provider info', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'RPGTV',
        listOfMediaProviders: [{
          name: 'RPGTV',
          children: [{
            media: {
              accessProperties: 'RPGTV,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(racingStreamService.getVideoUrl).toHaveBeenCalledWith(providerInfo,
        component['performConfig']);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should handle "RPGTV" provider by event mapped providers', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'iGameMedia',
        listOfMediaProviders: [{
          name: 'iGameMedia',
          children: [{
            media: {
              accessProperties: 'iGameMedia,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      eventEntity.streamProviders.RPGTV = true;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);

      expect(racingStreamService.getVideoUrl).toHaveBeenCalledWith(providerInfo,
        component['performConfig']);
      expect(successHandler).toHaveBeenCalledWith(providerInfo);
    }));

    it('should return an error when different provider mapped', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: 'iGameMedia',
        listOfMediaProviders: [{
          name: 'iGameMedia',
          children: [{
            media: {
              accessProperties: 'iGameMedia,1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      eventEntity.streamProviders.iGameMedia = true;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);

      expect(errorHandler).toHaveBeenCalledWith('servicesCrashed');
    }));
  });

  describe('ngOnInit', () => {
    let playSuccessErrorListener;

    beforeEach(() => {
      playSuccessErrorListener = jasmine.createSpy('playSuccessErrorListener');
      eventVideoStreamProvider.playSuccessErrorListener.subscribe(playSuccessErrorListener);

      component['performConfig'] = null;
      component['streamingConfig'] = null;
      component.eventEntity.id = 5;
    });

    it('should hide stream on init for wrapper', fakeAsync(() => {
      deviceService.isWrapper = true;
      component['isDesktop'] = false;
      component['isMobile'] = true;

      nativeBridgeService.playerStatus = true;
      nativeBridgeService.supportsVideo.and.returnValue(true);

      component.ngOnInit();
      tick();

      expect(component['isWrapper']).toEqual(true);
      expect(playSuccessErrorListener).toHaveBeenCalledWith(false);
      expect(mockHtml5VideoTag.pause).not.toHaveBeenCalled();
      expect(component.showPlayer).toBeFalsy();
      expect(component['streamActive']).toBeFalsy();
    }));

    it('should play stream on init for mobile', fakeAsync(() => {
      deviceService.isWrapper = false;
      component['isDesktop'] = false;

      component.ngOnInit();
      tick();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalled();
      expect(component.showPlayer).toBeFalsy();
      expect(component.desktopPlayer).toBe(null);
      expect(convivaService.setConfig).toHaveBeenCalled();
      expect(convivaService.preload).toHaveBeenCalled();
    }));

    it('should load desktop scripts and do not perform autoPlay', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;

      component.ngOnInit();
      tick();

      expect(loadVideoJsService.loadScripts).toHaveBeenCalled();
      expect(component['videJsTimeout']).not.toBeDefined();
      expect(component['showVideoPlayer']).toBeFalsy();
    }));

    it('should set resize timeframe for IOS', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;
      deviceService.isIos = true;
      deviceService.isMobile = true;

      component.ngOnInit();
      tick();

      expect(component['resizeTimeFrame']).toEqual(500);
    }));

    it('should set resize timeframe for not IOS', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;
      deviceService.isIos = false;

      component.ngOnInit();
      tick();

      expect(component['resizeTimeFrame']).toEqual(2000);
    }));
    it('check closing stage enabled', fakeAsync(() => {
      component.isReplayVideo = true;
      component.ngOnInit();
      tick();
      expect(component['showSwitcher']).toEqual(true);
    }));
    it('check closing stage disabled', fakeAsync(() => {
      component.isReplayVideo = false;
      component.ngOnInit();
      tick();
      expect(component['showSwitcher']).toEqual(false);
    }));

    it('should create html5 video player, disable context menu and hanlde "ended" event', fakeAsync(() => {
      const html5VideoTag = { tag: 'div', addEventListener: jasmine.createSpy('addEventListener') };

      component.autoPlay = false;
      component['isDesktop'] = true;
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn());
      elementRef.nativeElement.querySelector.and.returnValue(html5VideoTag);
      rendererService.renderer.listen.and.callFake((el, event, fn) => {
        fn();
      });
      component['ERROR_MESSAGES'].servicesCrashed = true;

      component.ngOnInit();
      tick();

      expect(rendererService.renderer.listen).toHaveBeenCalledWith(html5VideoTag, 'ended',
        jasmine.any(Function));
      expect(component.eventEntity.isFinished).toBeTruthy();
      expect(component['ERROR_MESSAGES']['eventFinished']).toBeTruthy();
      expect(html5VideoTag.addEventListener).toHaveBeenCalled();
    }));
    it('should create html5 video player, disable context menu and hanlde "ended" event for replay', fakeAsync(() => {
      const html5VideoTag = { tag: 'div', addEventListener: jasmine.createSpy('addEventListener') ,currentTime:600,      pause: jasmine.createSpy('pauseHtml5'),
    };

      component.autoPlay = false;
      component['isDesktop'] = true;
      component['isReplayVideo'] = true;
      component.filter='closingstage';

      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn());
      elementRef.nativeElement.querySelector.and.returnValue(html5VideoTag);
      rendererService.renderer.listen.and.callFake((el, event, fn) => {
        fn();
      });
      component['ERROR_MESSAGES'].servicesCrashed = true;
      component.ngOnInit();
      tick();

      expect(rendererService.renderer.listen).toHaveBeenCalledWith(html5VideoTag, 'ended',
        jasmine.any(Function));
      expect(component['ERROR_MESSAGES']['eventCompleted']).toBeTruthy();
      expect(html5VideoTag.addEventListener).toHaveBeenCalled();
    }));

    it('should init conviva', fakeAsync(() => {
      elementRef.nativeElement.querySelector.and.returnValue({ tag: 'video' });
      component['isDesktop'] = false;
      component['isConvivaEnabled'] = true;
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn());
      component.ngOnInit();
      tick();
      expect(convivaService.initVideoAnalytics).toHaveBeenCalled();
    }));

    it('should create html5 video player and hanlde "ended" event', () => {
      const html5VideoTag = null;
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn());
      elementRef.nativeElement.querySelector.and.returnValue(html5VideoTag);
      rendererService.renderer.listen = jasmine.createSpy('listen');

      component.ngOnInit();
      expect(rendererService.renderer.listen).not.toHaveBeenCalled();
    });

    it('should register command fn', fakeAsync(() => {
      let commandFn;

      component.autoPlay = false;
      component['isDesktop'] = true;
      commandService.register.and.callFake((name, fn) => commandFn = fn);

      component.ngOnInit();
      tick();

      expect(commandService.register).toHaveBeenCalledWith(commandService.API.GET_LIVE_STREAM_STATUS,
        jasmine.any(Function));

      component['streamID'] = '123';
      component['streamActive'] = true;
      observableFrom(commandFn()).subscribe(successHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith({
        streamID: '123',
        streamActive: true
      });
    }));

    it('should handle empty streamCache.meta', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;
      component['streamCache'].set(5, { meta: {}} as any);
      spyOn(console, 'warn');

      component.ngOnInit();
      tick();

      expect(component['performConfig']).toBeNull();
      expect(component['streamingConfig']).toEqual({} as any);
      expect(console.warn).not.toHaveBeenCalled();
    }));

    it('should handle empty streamCache', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;
      component['streamCache'].set(5, { } as any);
      spyOn(console, 'warn');

      component.ngOnInit();
      tick();

      expect(component['performConfig']).toBeNull();
      expect(component['streamingConfig']).toBeNull();
      expect(console.warn).toHaveBeenCalledWith(jasmine.any(String));
    }));

    it('should handle empty streamCache', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;
      spyOn(console, 'warn');

      component.ngOnInit();
      tick();

      expect(component['performConfig']).toBeNull();
      expect(component['streamingConfig']).toBeNull();
      expect(console.warn).toHaveBeenCalledWith(jasmine.any(String));
    }));

    it('should handle empty ATR', fakeAsync(() => {
      component['streamCache'].set(5, { meta: {
        operatorId: '1',
        imgSecret: 'secret'
      }} as any);
      component.autoPlay = false;
      component['isDesktop'] = true;
      spyOn(console, 'warn');

      component.ngOnInit();
      tick();

      expect(component['performConfig']).toBeNull();
      expect(component['streamingConfig']).toEqual({
        operatorId: '1',
        imgSecret: 'secret'
      });
      expect(console.warn).not.toHaveBeenCalled();
    }));

    it('should handle empty IMG', fakeAsync(() => {
      component['streamCache'].set(5, { meta: {
        partnerCode: '1',
        secret: 'secret'
      }} as any);
      component.autoPlay = false;
      component['isDesktop'] = true;
      spyOn(console, 'warn');

      component.ngOnInit();
      tick();

      expect(component['performConfig']).toBeNull();
      expect(component['streamingConfig']).toEqual({
        partnerCode: '1',
        secret: 'secret'
      } as any);
      expect(console.warn).not.toHaveBeenCalled();
    }));

    it('should set orientation change listener', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;
      deviceService.performProviderIsMobile.and.returnValue(true);

      component.ngOnInit();
      tick();

      expect(component['resizeListerner']).toEqual(jasmine.any(Number));
      expect(rendererService.renderer.listen).toHaveBeenCalledWith(windowRefService.nativeWindow,
        'orientationchange', component['resizeView']);
    }));
  });

  describe('renderStream', () => {
    let url = 'stream:rtmp';
    let eventId;
    const categoryCode = 'FOOTBALL';

    beforeEach(() => {
      eventId = eventEntity.id;
    });

    it('should run video js player for desktop when there is no player insance', () => {
      component['isDesktop'] = true;
      component['renderStream'](url, eventId, categoryCode);

      expect(component['desktopPlayer']).toBeFalsy();
    });

    it('should set withCredentials true', () => {
      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['streamCache'].set(eventId, {} as IStreamProvidersResponse);
      component['runVideoJsPlayer']('stream:rtmp');
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: true});
    });

    it('should set withCredentials true also', () => {
      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['streamCache'].set(eventId, {} as IStreamProvidersResponse);
      component.providerInfo = undefined;
      component['runVideoJsPlayer']('stream:rtmp');
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: true});
    });

    it('should set withCredentials false', () => {
      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['streamCache'].set(eventId, {} as IStreamProvidersResponse);
      component.providerInfo = { priorityProviderName: 'At The Races' } as IStreamProvidersResponse;
      component['runVideoJsPlayer']('stream:rtmp');
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: false});
    });

    it('should run video js player for desktop when there is no player insance', () => {
      let playerReadyCallback;

      component['showVideoPlayer'] = false;
      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['streamCache'].set(eventId, { error: 'someError' } as IStreamProvidersResponse);
      desktopPlayerMock.ready.and.callFake((fn) => playerReadyCallback = fn);

      component['renderStream'](url, eventId, categoryCode);

      expect(component['streamCache'].get(eventId).error).toBeNull();
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({
        type: jasmine.any(String),
        src: url,
        withCredentials: true
      });

      playerReadyCallback();
      expect(component['showVideoPlayer']).toBeTruthy();
      expect(desktopPlayerMock.play).toHaveBeenCalled();
    });

    it('should handle wrapper and not duplicated id', () => {
      url = 'https://stream.com';
      component['isDesktop'] = false;
      component['isWrapper'] = true;
      nativeBridgeService.supportsVideo.and.returnValue(true);
      streamTrackingService.checkIdForDuplicates.and.returnValue(false);

      component['renderStream'](url, eventId, categoryCode);

      expect(nativeBridgeService.showVideoIfExist).toHaveBeenCalledWith(url, eventId, categoryCode, 'UNKNOWN');
      expect(gtmService.push).toHaveBeenCalled();
      expect(streamTrackingService.addIdToTrackedList).toHaveBeenCalledWith(eventId, 'liveStream');
    });

    it('should handle wrapper and specify provider name ', () => {
      url = 'https://stream.com';
      component['isDesktop'] = false;
      component['isWrapper'] = true;
      nativeBridgeService.supportsVideo.and.returnValue(true);
      streamTrackingService.checkIdForDuplicates.and.returnValue(false);
      eventEntity.streamProviders.IMG = true;
      component['renderStream'](url, eventId, categoryCode);

      expect(nativeBridgeService.showVideoIfExist).toHaveBeenCalledWith(url, eventId, categoryCode, 'IMG');
      expect(gtmService.push).toHaveBeenCalled();
      expect(streamTrackingService.addIdToTrackedList).toHaveBeenCalledWith(eventId, 'liveStream');
    });

    it('should handle wrapper and specify provider name ', () => {
      url = 'https://stream.com';
      component['isDesktop'] = false;
      component['isWrapper'] = true;
      nativeBridgeService.supportsVideo.and.returnValue(true);
      streamTrackingService.checkIdForDuplicates.and.returnValue(false);
      eventEntity.streamProviders = undefined;
      component['renderStream'](url, eventId, categoryCode);

      expect(nativeBridgeService.showVideoIfExist).toHaveBeenCalledWith(url, eventId, categoryCode, 'UNKNOWN');
      expect(gtmService.push).toHaveBeenCalled();
      expect(streamTrackingService.addIdToTrackedList).toHaveBeenCalledWith(eventId, 'liveStream');
    });

    it('should handle wrapper and duplicated id', () => {
      url = 'https://stream.com';
      component['isDesktop'] = false;
      component['isWrapper'] = true;
      nativeBridgeService.supportsVideo.and.returnValue(true);
      streamTrackingService.checkIdForDuplicates.and.returnValue(true);

      component['renderStream'](url, eventId, categoryCode);

      expect(nativeBridgeService.showVideoIfExist).toHaveBeenCalledWith(url, eventId, categoryCode, 'UNKNOWN');
      expect(gtmService.push).not.toHaveBeenCalled();
      expect(streamTrackingService.addIdToTrackedList).not.toHaveBeenCalled();
    });

    it('should handle wrapper and url that not starts from http', () => {
      const playerElement = { tag: 'span' };
      const elementWidth = 100;
      const parentNode = { tag: 'div' };

      url = 'stream.com';
      component['isDesktop'] = false;
      component['isWrapper'] = true;
      nativeBridgeService.supportsVideo.and.returnValue(true);
      streamTrackingService.checkIdForDuplicates.and.returnValue(true);
      windowRefService.document = {
        getElementById: jasmine.createSpy('getElementById').and.returnValue(playerElement)
      };
      deviceService.performProviderIsMobile.and.returnValue(true);
      elementRef.nativeElement.parentNode = parentNode;
      performGroupService.getElementWidth.and.returnValue(elementWidth);

      component['renderStream'](url, eventId, categoryCode);

      expect(nativeBridgeService.showVideoIfExist).not.toHaveBeenCalledWith();
      expect(component['streamingUrl']).toEqual(url);
      expect(streamTrackingService.setTrackingForPlayer).toHaveBeenCalledWith(playerElement, eventEntity);
    });

    it('should handle wrapper and but does not support video', () => {
      const playerElement = { tag: 'span' };
      const elementWidth = 100;
      const parentNode = { tag: 'div' };

      url = 'stream.com';
      component['isDesktop'] = false;
      component['isWrapper'] = true;
      nativeBridgeService.supportsVideo.and.returnValue(false);
      streamTrackingService.checkIdForDuplicates.and.returnValue(true);
      windowRefService.document = {
        getElementById: jasmine.createSpy('getElementById').and.returnValue(playerElement)
      };
      deviceService.performProviderIsMobile.and.returnValue(true);
      elementRef.nativeElement.parentNode = parentNode;
      performGroupService.getElementWidth.and.returnValue(elementWidth);

      component['renderStream'](url, eventId, categoryCode);

      expect(nativeBridgeService.showVideoIfExist).not.toHaveBeenCalledWith();
      expect(streamTrackingService.setTrackingForPlayer).toHaveBeenCalledWith(playerElement, eventEntity);
    });
  });

  describe('useCachedData', () => {
    it('should show error when no cached stream has an error', () => {
      const reason = 'deniedByWatchRules';

      component['streamCache'].set(eventEntity.id, { error: null } as IStreamProvidersResponse);
      component['useCachedData']();
      component['streamCache'].set(eventEntity.id, { error: reason } as IStreamProvidersResponse);

      component['useCachedData']();

      expect(localeService.getString).toHaveBeenCalledWith(`sb.${reason}`);
      expect(component['ERROR_MESSAGES'][reason]).toBeTruthy();
    });

    it('should render stream', () => {
      const url = 'http://stream.com';
      component['isDesktop'] = false;
      component['isWrapper'] = true;
      nativeBridgeService.supportsVideo.and.returnValue(true);
      streamTrackingService.checkIdForDuplicates.and.returnValue(false);
      component['streamCache'].set(eventEntity.id, { stream: url } as IStreamProvidersResponse);

      component['useCachedData']();

      expect(nativeBridgeService.showVideoIfExist).toHaveBeenCalledWith(url, eventEntity.id, eventEntity.categoryCode, 'UNKNOWN');
      expect(gtmService.push).toHaveBeenCalled();
      expect(streamTrackingService.addIdToTrackedList).toHaveBeenCalledWith(eventEntity.id, 'liveStream');
    });
  });

  describe('playStream', () => {
    let errorListener,
      endedListener,
      retryplaylistListener,
      readyListener;

    const event  = {
      preventDefault: jasmine.createSpy('preventDefault')
    };

    it('should play desktop stream', fakeAsync(() => {
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['videJsTimeout'] = 123;
      component['isDesktop'] = true;
      desktopPlayerMock.on.and.callFake((name, handler) => {
        if (name === 'error') {
          errorListener = handler;
        } else if (name === 'ended') {
          endedListener = handler;
        } else if (name === 'ready') {
          readyListener = handler;
        }
      });
      component['isConvivaEnabled'] = true;
      component.playStream(event);
      component.streamUniqueId = 'rtmpe-hls';
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRefService.nativeWindow.videojs).toHaveBeenCalledWith('rtmpe-hls', {
        muted: true,
        techOrder: ['html5', 'flash'],
        fluid: true,
        controlBar: { fullscreenToggle: false , pictureInPictureToggle: false}
      });
      expect(desktopPlayerMock.on).toHaveBeenCalledTimes(3);
      errorListener();
      endedListener();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();

      readyListener();
      expect(streamTrackingService.setTrackingForPlayer).toHaveBeenCalledWith(desktopPlayerMock, eventEntity);
      expect(convivaService.initVideoJsAnalytics).toHaveBeenCalled();
    }));
    it('should stop the player when we hit retryplaylist 10 times', () => {
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['videJsTimeout'] = 10;
      component['isDesktop'] = true;
      component.providerInfo =  { priorityProviderName : "At The Races" } as IStreamProvidersResponse
      desktopPlayerMock.tech().on.and.callFake((name, handler) => {
         if (name === 'retryplaylist') {
          retryplaylistListener = handler;
        }
      });
      component.playStream(event);
      for (let i = 0; i <= 10; i++) {
        retryplaylistListener();
      }
      expect(desktopPlayerMock.tech).toHaveBeenCalled();
      expect(desktopPlayerMock.tech().on).toHaveBeenCalled();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();
    });    
    it('should stop the player when we hit retryplaylist 10 times with provider ATR from eventEntity', () => {
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['videJsTimeout'] = 10;
      component['isDesktop'] = true;
      component.eventEntity.streamProviders.ATR = true;
      desktopPlayerMock.tech().on.and.callFake((name, handler) => {
         if (name === 'retryplaylist') {
          retryplaylistListener = handler;
        }
      });
      component.playStream(event);
      for (let i = 0; i <= 10; i++) {
        retryplaylistListener();
      }
      expect(desktopPlayerMock.tech).toHaveBeenCalled();
      expect(desktopPlayerMock.tech().on).toHaveBeenCalled();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();
    });    
    it('should not play desktop stream if #rtmpe-hls not available', fakeAsync(() => {
      elementRef.nativeElement.querySelector.and.returnValue(null);
      component['isDesktop'] = true;
      component['performConfig'] = null;

      component.playStream();

      expect(windowRefService.nativeWindow.videojs).not.toHaveBeenCalled();
    }));

    describe('should not display proper error message', () => {
      beforeEach(() => {
        component.providerInfo = {} as any;
        component['onError'] = jasmine.createSpy('onError');
        component['getStreamUnavailableMessage'] = jasmine.createSpy('getStreamUnavailableMessage').and.returnValue('');
        component['getStreamNotStartedMessage'] = jasmine.createSpy('getStreamNotStartedMessage').and.returnValue(observableOf(''));
        component['performConfig'] = {} as any;
        component['checkCanWatch'] = jasmine.createSpy('checkCanWatch').and.returnValue(observableOf({}));
        component['onSuccess'] = jasmine.createSpy('onSuccess');
        component['useCachedData'] = jasmine.createSpy('useCachedData');
        component.eventVideoStreamProvider.playSuccessErrorListener.next = jasmine.createSpy('next');
      });


      it(' and pass streamFlow', () => {
        component['showHideStream'] = jasmine.createSpy('showHideStream').and.returnValue(observableOf('stream'));
        component.playStream();

        expect(component['onError']).toHaveBeenCalledTimes(0);
        expect(component['onError']).not.toHaveBeenCalledWith('');
        expect(component['onSuccess']).toHaveBeenCalledWith('stream');
        expect(component['useCachedData']).toHaveBeenCalled();
        expect(component.eventVideoStreamProvider.playSuccessErrorListener.next).toHaveBeenCalledWith(true);
      });

      it('should not display proper error message and success pass streamFlow', () => {
        component['showHideStream'] = jasmine.createSpy('showHideStream').and.returnValue(observableOf(''));
        component.playStream();

        expect(component['onError']).toHaveBeenCalledTimes(1);
        expect(component['onError']).toHaveBeenCalledWith();
        expect(component['onSuccess']).not.toHaveBeenCalledWith('stream');
        expect(component['useCachedData']).not.toHaveBeenCalled();
        expect(component.eventVideoStreamProvider.playSuccessErrorListener.next).not.toHaveBeenCalled();
      });

      it('should not display proper error message and checkCanWatch throw an errors', () => {
        component['showHideStream'] = jasmine.createSpy('showHideStream').and.returnValue(throwError('error'));
        component.playStream();

        expect(component['onError']).toHaveBeenCalledTimes(1);
        expect(component['onError']).toHaveBeenCalledWith('error');
        expect(component['onSuccess']).not.toHaveBeenCalledWith('stream');
        expect(component['useCachedData']).not.toHaveBeenCalled();
        expect(component.eventVideoStreamProvider.playSuccessErrorListener.next).toHaveBeenCalledWith(false);
      });

      afterEach(() => {
        expect(component['showHideStream']).toHaveBeenCalledWith(component.providerInfo);
      });
    });

    it('should display desktop error message if event no performConfig were found', fakeAsync(() => {
      component['performConfig'] = null;

      component.playStream(event);

      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
      expect(component.showVideoPlayer).toBeFalsy();
      expect(component.showPlayer).toBeFalsy();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'Livestream',
        eventAction: 'error',
        liveStreamError: jasmine.any(String)
      });
    }));
  });
  describe('replayStream', () => {
    let errorListener,
      endedListener,
      retryplaylistListener,
      readyListener;

    const event  = {
      preventDefault: jasmine.createSpy('preventDefault')
    };

    it('should play desktop stream', fakeAsync(() => {
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['videJsTimeout'] = 123;
      component['isDesktop'] = true;
      component['isReplayVideo'] = true;

      desktopPlayerMock.on.and.callFake((name, handler) => {
        if (name === 'error') {
          errorListener = handler;
        } else if (name === 'ended') {
          endedListener = handler;
        } else if (name === 'ready') {
          readyListener = handler;
        }
      });
      component['isConvivaEnabled'] = true;
      component.ReplayStream(event);
      component.streamUniqueId = 'rtmpe-hls';
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRefService.nativeWindow.videojs).toHaveBeenCalledWith('rtmpe-hls', {
        muted: true,
        techOrder: ['html5', 'flash'],
        fluid: true,
        html5: {
          hls: {
            enableLowInitialPlaylist: true,
            smoothQualityChange: true,
            overrideNative: true,
          },
        },
      controlBar: {
        fullscreenToggle: false,
        pictureInPictureToggle: false,
        remainingTimeDisplay: false,
        liveDisplay: false,
        progressControl: {
          seekBar: false
        },
      }
      });
      expect(desktopPlayerMock.on).toHaveBeenCalledTimes(3);
      errorListener();
      endedListener();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();

      readyListener();
      expect(streamTrackingService.setTrackingForPlayer).toHaveBeenCalledWith(desktopPlayerMock, eventEntity);
      expect(convivaService.initVideoJsAnalytics).toHaveBeenCalled();
    }));
  
    it('videostremplay', fakeAsync(() => {
      let playerReadyCallback;
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['showPlayer'] = true;
      component['streamActive'] = true;
      component['isDesktop'] = true;     
      component.desktopPlayer = desktopPlayerMock; 
      desktopPlayerMock.ready.and.callFake((fn) => playerReadyCallback = fn);
      component.ReplayStream(event);
      playerReadyCallback(); 
      expect(component['showVideoPlayer']).toBeTruthy();
      expect(desktopPlayerMock.play).toHaveBeenCalled();
    }));
   
    it('videostremerror', fakeAsync(() => {
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['showPlayer'] = true;
      component['streamActive'] = true;
      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component.videoStreamData={
        provider: "ATR",
        streamInfo: {
          bitrateLevel: "Adaptive",
          streamUrl:'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8#t=550,600'
    
        },
        status: "ERROR",
        closingStage:true,
        startTime:100,
        endTime:300,
        message: "Streaming error / authentication failed / VOD not available"
      };
      component.ReplayStream(event);
      expect(component.errorMessage).toBe(videoStreamData.message);
      expect(component.desktopPlayer.reset).toHaveBeenCalled();
      expect(component.desktopPlayer.errorDisplay.opened_).toBeFalsy();
    }));

    
    it('videostream for mobile and mybets', fakeAsync(() => {
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      const playerElement = { tag: 'span' };      
      windowRefService.document = {
        getElementById: jasmine.createSpy('getElementById').and.returnValue(playerElement)
      };
      component['desktopPlayer'] = desktopPlayerMock;

      component['showPlayer'] = true;
      component['streamActive'] = true;
      component['isDesktop'] = false;
      component['isMobile'] = true;
      component['isReplayVideo'] = true;

      deviceService.performProviderIsMobile.and.returnValue(true);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);

      //desktopPlayerMock.ready.and.callFake((fn) => playerReadyCallback = fn);
      component.ReplayStream(event);
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({ type: 'application/x-mpegURL', src: 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8#t=550,600' });
    

    }));

    describe('should not display proper error message', () => {
      beforeEach(() => {
        component.providerInfo = {} as any;
        component['onError'] = jasmine.createSpy('onError');
        component['getStreamUnavailableMessage'] = jasmine.createSpy('getStreamUnavailableMessage').and.returnValue('');
        component['getStreamNotStartedMessage'] = jasmine.createSpy('getStreamNotStartedMessage').and.returnValue(observableOf(''));
        component['performConfig'] = {} as any;
        component['checkCanWatch'] = jasmine.createSpy('checkCanWatch').and.returnValue(observableOf({}));
        component['onSuccess'] = jasmine.createSpy('onSuccess');
        component['useCachedData'] = jasmine.createSpy('useCachedData');
        component.eventVideoStreamProvider.playSuccessErrorListener.next = jasmine.createSpy('next');
      });


      it(' and pass streamFlow', () => {
        component['showHideStream'] = jasmine.createSpy('showHideStream').and.returnValue(observableOf('stream'));
        component.playStream();

        expect(component['onError']).toHaveBeenCalledTimes(0);
        expect(component['onError']).not.toHaveBeenCalledWith('');
        expect(component['onSuccess']).toHaveBeenCalledWith('stream');
        expect(component['useCachedData']).toHaveBeenCalled();
        expect(component.eventVideoStreamProvider.playSuccessErrorListener.next).toHaveBeenCalledWith(true);
      });

      it('should not display proper error message and success pass streamFlow', () => {
        component['showHideStream'] = jasmine.createSpy('showHideStream').and.returnValue(observableOf(''));
        component.playStream();

        expect(component['onError']).toHaveBeenCalledTimes(1);
        expect(component['onError']).toHaveBeenCalledWith();
        expect(component['onSuccess']).not.toHaveBeenCalledWith('stream');
        expect(component['useCachedData']).not.toHaveBeenCalled();
        expect(component.eventVideoStreamProvider.playSuccessErrorListener.next).not.toHaveBeenCalled();
      });

      it('should not display proper error message and checkCanWatch throw an errors', () => {
        component['showHideStream'] = jasmine.createSpy('showHideStream').and.returnValue(throwError('error'));
        component.playStream();

        expect(component['onError']).toHaveBeenCalledTimes(1);
        expect(component['onError']).toHaveBeenCalledWith('error');
        expect(component['onSuccess']).not.toHaveBeenCalledWith('stream');
        expect(component['useCachedData']).not.toHaveBeenCalled();
        expect(component.eventVideoStreamProvider.playSuccessErrorListener.next).toHaveBeenCalledWith(false);
      });

      afterEach(() => {
        expect(component['showHideStream']).toHaveBeenCalledWith(component.providerInfo);
      });
    });

    it('should display desktop error message if event no performConfig were found', fakeAsync(() => {
      component['performConfig'] = null;

      component.playStream(event);

      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
      expect(component.showVideoPlayer).toBeFalsy();
      expect(component.showPlayer).toBeFalsy();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'Livestream',
        eventAction: 'error',
        liveStreamError: jasmine.any(String)
      });
    }));
  });
  describe('handlePlayingStream', () => {
    let playSuccessErrorListener;

    beforeEach(() => {
      playSuccessErrorListener = jasmine.createSpy('playSuccessErrorListener');
      eventVideoStreamProvider.playSuccessErrorListener.subscribe(playSuccessErrorListener);

      component.showPlayer = true;
      component['streamActive'] = true;
    });

    it('should set showPlayer status from native and hide stream', fakeAsync(() => {
      component.showPlayer = false;
      deviceService.isWrapper = true;
      nativeBridgeService.playerStatus = true;

      component['handlePlayingStream']();
      tick();

      expect(playSuccessErrorListener).toHaveBeenCalledWith(false);
      expect(mockHtml5VideoTag.pause).not.toHaveBeenCalled();
      expect(component.showPlayer).toBeFalsy();
      expect(component['streamActive']).toBeFalsy();
    })); 
     it('replayvideo for handling play', fakeAsync(() => {
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component.showPlayer = false;
      component.isReplayVideo = true;
      deviceService.isWrapper = false;
      component['handlePlayingStream']();
      tick();
    }));

    it('should handle play desktop stream if #rtmpe-hls not available and show error', fakeAsync(() => {
      elementRef.nativeElement.querySelector.and.returnValue(null);
      deviceService.isWrapper = false;
      component['isDesktop'] = true;
      component['performConfig'] = {
        partnerId: '1'
      } as IPerformGroupConfig;
      component.eventEntity.startTime = '2028-06-30T16:57:00Z';
      component.showPlayer = false;

      component['handlePlayingStream']();

      expect(windowRefService.nativeWindow.videojs).not.toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith('sb.servicesCrashed');
    }));
  });
  
  it('#createFilters should create data for switchers on the page', () => {
    component['changeFilter'] = jasmine.createSpy().and.returnValue('changefilter');
    localeService.getString.and.returnValue('closingstage');

    component['createFilters']();

    expect(component.fullRaceType.viewByFilters).toBe('fullrace');
    expect(component.fullRaceType.onClick('fullrace')).toEqual('changefilter');
    expect(component.closingStageType.name).toBe('closingstage');
    expect(component.closingStageType.onClick('closingstage')).toEqual('changefilter');   
    expect(component.racingVideoTypes.length).toBe(2);
    expect(component.filter).toBe('fullrace');
  });
  describe('#setGtmData', () => {  
    it('storing GA object', () => {
      component.isMyBets =false;
      component.eventEntity = {
        typeName: 'UK',
        name:'UK'
      } as any;
      component.setGtmData('test');
      expect(component['gtmService'].push).toHaveBeenCalled();
    });
    it('storing GA object', () => {
      component.isMyBets =true;
      component.eventEntity = {
        typeName: 'UK',
        name:'UK'
      } as any;
      component.setGtmData('test');
      expect(component['gtmService'].push).toHaveBeenCalled();
    });
  });
  it('changefilter closingstage ', () => {
    component.videoStreamData={
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
    };
    component['changeFilter']('closingstage');
    expect(component['gtmService'].push).toHaveBeenCalled();
  
});
it('changefilter fullRace ', () => {
  component.videoStreamData={
    provider: "ATR",
    streamInfo: {
      bitrateLevel: "Adaptive",
      streamUrl:'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8#t=550,600'

    },
    status: "SUCCESS",
    message: "Streaming error / authentication failed / VOD not available"
  };
  component['changeFilter']('fullRace');
  expect(component['gtmService'].push).toHaveBeenCalled();

});
  it('skipForwardVideo', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      component.skipForwardVideo(550);
      expect(desktopPlayerMock.currentTime).toHaveBeenCalledWith(jasmine.any(Number));
  });
  it('getVideoClass for replay', () => {
    component.isReplayVideo=true;
    component.showPlayer=true;
    component.streamingUrl='abc';
    expect(component.getVideoClass()).toBe(false);
});
  it('getVideoClass for live', () => {
    component.isReplayVideo=false;
    component.showPlayer=true;
    component.streamingUrl='abc';
    component.isWrapper=true;
    expect(component.getVideoClass()).toBe(true);
  });
});
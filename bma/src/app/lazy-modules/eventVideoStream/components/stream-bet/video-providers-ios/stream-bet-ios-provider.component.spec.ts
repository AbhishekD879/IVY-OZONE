import { of as observableOf, Subject } from 'rxjs';

import {
  StreamBetIOSProviderComponent
} from '@lazy-modules/eventVideoStream/components/stream-bet/video-providers-ios/stream-bet-ios-provider.component';


import { ISportEvent } from '@core/models/sport-event.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('VideoStreamProvidersComponent', () => {
  let component: StreamBetIOSProviderComponent;
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
  let quickbetService;
  let pubsub;
  let changeDetectorRef;
  let remoteBetslipService;
  let clientUserAgentService;
  let iGameMediaService;
  let storageService;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.returnValue(Math.random()),
        clearTimeout: jasmine.createSpy('clearTimeout').and.returnValue(null),
        videojs: jasmine.createSpy('videojs'),
        orientation: jasmine.createSpy('orientation')
      },
      document: {
        getElementById: jasmine.createSpy('getElementById'),
        querySelector: jasmine.createSpy('querySelector').and.returnValue({ test: 'body' } as any)
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
        querySelector: jasmine.createSpy('querySelector').and.returnValue({}),
        querySelectorAll: jasmine.createSpy('querySelectorAll').and.returnValue({})
      }
    };
    deviceService = {
      isDesktop: true,
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
    storageService = {};

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
        listen: jasmine.createSpy('listen').and.returnValue(Math.random()),
        setStyle: jasmine.createSpy('setStyle'),
        removeStyle: jasmine.createSpy('removeStyle'),
        removeClass: jasmine.createSpy('removeClass')
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
      resolveComponentFactory: jasmine.createSpy().and.returnValue({ name: 'VideoStreamErrorDialogComponent' })
    };
    mockHtml5VideoTag = {
      pause: jasmine.createSpy('pauseHtml5'),
      removeEventListener: jasmine.createSpy('removeEventListener'),
      addEventListener: jasmine.createSpy('addEventListener')
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
    pubsub ={
      publish : jasmine.createSpy('publish'),
      API: pubSubApi
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        performGroup: cmsConfigs.performConfig,
        IMGStreaming: cmsConfigs.imgStreamingConfig,
        AtTheRaces: cmsConfigs.atTheRacesConfig,
        Conviva: cmsConfigs.Conviva
      }))
    };
    quickbetService = {
      quickBetOnOverlayCloseSubj: new Subject<string>(),
      getRestoredSelection: jasmine.createSpy('getRestoredSelection')
    };

    successHandler = jasmine.createSpy('success');
    errorHandler = jasmine.createSpy('errorHandler');

    component = new StreamBetIOSProviderComponent(performGroupService, domSanitizer, elementRef, userService, windowRefService,
      cmsService, commandService, atTheRacesService, watchRulesService, imgService, racingStreamService,
      nativeBridgeService, localeService, loadVideoJsService, streamTrackingService, gtmService,
      sessionService, deviceService, liveStreamService, eventVideoStreamProvider, rendererService, convivaService,
      dialogService, componentFactoryResolver, quickbetService, pubsub, changeDetectorRef, remoteBetslipService, clientUserAgentService, iGameMediaService, storageService
    );

    component.eventEntity = eventEntity;
    component.streamCache = new Map();
    component.streamUniqueId = "rtmpe-hls";
    component['html5VideoTag'] = mockHtml5VideoTag;
    component['performConfig'] = {
      partnerId: '2',
      seed: '123asd'
    } as any;
    desktopPlayerMock = {
      tech: jasmine.createSpy('tech').and.returnValue({
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
      fullscreenchange: jasmine.createSpy('fullscreenchange'),
      volume: jasmine.createSpy('volume'),
      isDisposed_: false,
      exitFullScreen: jasmine.createSpy('exitFullScreen'),
      enterFullWindow: jasmine.createSpy('enterFullWindow'),
      exitFullWindow: jasmine.createSpy('exitFullWindow'),
      requestFullscreen: jasmine.createSpy('requestFullscreen'),
      webkitRequestFullscreen: jasmine.createSpy('webkitRequestFullscreen')
    };
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });
  describe('renderLandscapeVideoMode', () => {
    it('should call appendOverlay and requestfullscreen for wrapper is true', () => {
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = true;
      component.isFullScreen = false;
      component['homeBody'] = { test: 'body' } as any;
      spyOn(component as any, 'appendOverlayElement');
      component['renderLandscapeVideoMode']();
      expect(component['tutorialPlayer'].enterFullWindow).toHaveBeenCalled();
      expect(component['desktopPlayer'].requestFullscreen).toHaveBeenCalled();
      expect(component['appendOverlayElement']).toHaveBeenCalled();
    });
    it('should call appendOverlay and requestfullscreen for wrapper is true', () => {
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['desktopPlayer'].requestFullscreen = null;
      component.isWrapper = true;
      component.isFullScreen = false;
      component['homeBody'] = { test: 'body' } as any;
      spyOn(component as any, 'appendOverlayElement');
      component['renderLandscapeVideoMode']();
      expect(component['tutorialPlayer'].enterFullWindow).toHaveBeenCalled();
      expect(component['desktopPlayer'].webkitRequestFullscreen).toHaveBeenCalled();
      expect(component['appendOverlayElement']).toHaveBeenCalled();
    });
    it('should call appendOverlay and setstyle and remove and cal renderLandscapeErrorScreen for not wrapper', () => {
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = false;
      component.isFullScreen = false;
      component['homeBody'] = { test: 'body' } as any;
      spyOn(component as any, 'renderLandscapeErrorScreen');
      spyOn(component as any, 'appendOverlayElement');
      component['renderLandscapeVideoMode']();
      expect(component['renderLandscapeErrorScreen']).toHaveBeenCalled();
      expect(component['appendOverlayElement']).toHaveBeenCalled();
    });
  });
  describe('handleStreamEnd', () => {
    it('should call renderLandscapeErrorScreen,setExitScreenFlags and exitFullScreen', () => {
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['homeBody'] = { test: 'body' } as any;
      spyOn(component as any, 'renderLandscapeErrorScreen');
      spyOn(component as any, 'setExitScreenFlags');
      spyOn(component as any, 'exitFullScreen');
      component['handleStreamEnd']();
      expect(component['setExitScreenFlags']).toHaveBeenCalled();
      expect(component['renderLandscapeErrorScreen']).toHaveBeenCalled();
      expect(component['exitFullScreen']).toHaveBeenCalled();
    });
    it('should call and renderLandscapeErrorScreen,setExitScreenFlags and exitFullScreen and isWrapper is false', () => {
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['homeBody'] = { test: 'body' } as any;
      component.isWrapper = false;
      spyOn(component as any, 'renderLandscapeErrorScreen');
      spyOn(component as any, 'setExitScreenFlags');
      spyOn(component as any, 'exitFullScreen');
      component['handleStreamEnd']();
      expect(component['setExitScreenFlags']).toHaveBeenCalled();
      expect(component['renderLandscapeErrorScreen']).toHaveBeenCalled();
      expect(component['exitFullScreen']).toHaveBeenCalled();
    });
  });
  describe('checkOrientationMode', () => {
    it('should call renderlandscapevideomode if in landscape', () => {
      component.windowRefService.nativeWindow.orientation = -90;
      component['homeBody'] = { test: 'body' } as any;
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      spyOn(component as any, 'renderLandscapeVideoMode');
      spyOn(component as any, 'handleDesktopPlayerVisibility');
      component['checkOrientationMode']();
      expect(component['renderLandscapeVideoMode']).toHaveBeenCalled();
    });
    it('should call renderlandscapevideomode and hideLandscapeErrorScreen if in landscape', () => {
      component.windowRefService.nativeWindow.orientation = -90;
      deviceService.isWrapper = true;
      component['homeBody'] = { test: 'body' } as any;
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      spyOn(component as any, 'renderLandscapeVideoMode');
      spyOn(component as any, 'handleDesktopPlayerVisibility');
      spyOn(component as any,'hideLandscapeErrorScreen');
      component['checkOrientationMode'](true);
      expect(component['renderLandscapeVideoMode']).toHaveBeenCalled();
      expect(component['hideLandscapeErrorScreen']).toHaveBeenCalled();
    });
    it('should not call renderlandscapevideomode if not in landscape and isWrapper true', () => {
      component.windowRefService.nativeWindow.orientation = -10;
      component['homeBody'] = { test: 'body' } as any;
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = true;
      spyOn(component as any, 'renderLandscapeVideoMode');
      component['checkOrientationMode']();
      expect(component['desktopPlayer'].exitFullWindow).toHaveBeenCalled();
      expect(component['tutorialPlayer'].exitFullWindow).toHaveBeenCalled();
    });
    it('should not call renderlandscapevideomode if not in landscape and isWrapper false', () => {
      component.windowRefService.nativeWindow.orientation = -10;
      component['homeBody'] = { test: 'body' } as any;
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = false;
      component.isFullScreen = true;
      spyOn(component as any, 'openFullScreen');
      component['checkOrientationMode']();
      expect(component['openFullScreen']).toHaveBeenCalled();
    });
  });
});
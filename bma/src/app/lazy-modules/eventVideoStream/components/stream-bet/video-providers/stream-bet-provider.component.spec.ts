import { fakeAsync, tick, flush } from '@angular/core/testing';
import { of as observableOf, Subject, throwError, from as observableFrom } from 'rxjs';

import {
  StreamBetProviderComponent
} from '@lazy-modules/eventVideoStream/components/stream-bet/video-providers/stream-bet-provider.component';

import { DialogService } from '@core/services/dialogService/dialog.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IPerformGroupConfig, IStreamProvidersResponse } from '@lazy-modules/eventVideoStream/models/video-stream.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';

describe('StreamBetProviderComponent', () => {
  let component: StreamBetProviderComponent;
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
  let videoSpinner;

  beforeEach(() => {
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.returnValue(Math.random()),
        clearTimeout: jasmine.createSpy('clearTimeout').and.returnValue(null),
        videojs: jasmine.createSpy('videojs'),
        document: {
          activeElement: { blur: jasmine.createSpy('blur') },
          querySelector: jasmine.createSpy('querySelector')
        },
        orientation: 0
      },
      document: {
        getElementById: jasmine.createSpy('getElementById').and.returnValue([{
          id:'overlay-edp',remove: jasmine.createSpy()
        }]),
        querySelector: jasmine.createSpy('querySelector').and.callFake((selector: string) => {
          if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
        }),
        querySelectorAll: jasmine.createSpy().and.returnValue([
          { className: 'top-bar', remove: jasmine.createSpy() },
          { className: 'network-indicator-parent', remove: jasmine.createSpy() },
          { className: 'network-indicator-parent-lads', remove: jasmine.createSpy() }
        ]),
        getElementsByClassName: jasmine.createSpy().and.returnValue([
          { className: 'footer-wrapper', remove: jasmine.createSpy() },
          { className: 'timeline', remove: jasmine.createSpy() }
        ]),
        appendChild: jasmine.createSpy('appendChild'),
        contains: jasmine.createSpy('contains')
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
        querySelector: jasmine.createSpy('querySelector').and.returnValue(
          { className: 'test', removeEventListener: jasmine.createSpy('native removeEventListener'), addEventListener: jasmine.createSpy('native addEventListener'), classList: { add: jasmine.createSpy('add'), contains: jasmine.createSpy('contains'), remove: jasmine.createSpy('remove') } }
        ),
        querySelectorAll: jasmine.createSpy('querySelector').and.returnValue(
          [{ className: 'test1', removeEventListener: jasmine.createSpy('native removeEventListener'), addEventListener: jasmine.createSpy('native addEventListener'), classList: { add: jasmine.createSpy('add'), contains: jasmine.createSpy('contains'), remove: jasmine.createSpy('remove') } }]
        ),
        appendChild: jasmine.createSpy('appendChild')
      }
    };
    deviceService = {
      isDesktop: true,
      performProviderIsMobile: jasmine.createSpy('performProviderIsMobile').and.callFake(v => v),
      isIos: false,
      isWrapper: false
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
      },
      StreamBetWeb: {
        tutorialVideoLimit: 5,
        toasterMsgNative: 'toaster native msg',
        toasterMsgWeb: 'toaster web msg',
        tutorialVideoUrl: 'https://stream.com',
        isAndroidStream: true,
        isAndroidStreamURL: 'https://stream.com',
        isIOSStream: true
      }
    };
    eventVideoStreamProvider = {
      playListener: new Subject<void>(),
      showHideStreamListener: new Subject<boolean>(),
      playSuccessErrorListener: new Subject<boolean>(),
      getStreamBetCmsConfig: jasmine.createSpy('getStreamBetCmsConfig').and.returnValue(observableOf(cmsConfigs.StreamBetWeb)),
      snbVideoFullScreenExitSubj: new Subject<void>(),
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
    iGameMediaService = {
      isEventStarted: jasmine.createSpy('isEventStarted').and.returnValue(false),
      getStream: jasmine.createSpy('getStream').and.callFake(v => observableOf(v))
    }
    racingStreamService = {
      isEventStarted: jasmine.createSpy('isEventStarted').and.returnValue(false),
      getVideoUrl: jasmine.createSpy('getVideoUrl').and.callFake(v => observableOf(v))
    };
    sessionService = {};
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    }
    liveStreamService = {
      checkIfRacingEvent: jasmine.createSpy('checkIfRacingEvent').and.returnValue(false)
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(Math.random()),
        setStyle: jasmine.createSpy(),
        removeStyle: jasmine.createSpy(),
        removeClass: jasmine.createSpy(),
        addClass: jasmine.createSpy()
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
      removeEventListener: jasmine.createSpy('html5 removeEventListener'),
      addEventListener: jasmine.createSpy('html5 addEventListener')
    };
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
      canplay: jasmine.createSpy('canplay'),
      on: jasmine.createSpy('play'),
      fullscreenchange: jasmine.createSpy('fullscreenchange'),
      volume: jasmine.createSpy('volume'),
      isDisposed_: false,
      exitFullscreen: jasmine.createSpy('exitFullscreen'),
      enterFullWindow: jasmine.createSpy('enterFullWindow'),
      exitFullWindow: jasmine.createSpy('exitFullWindow'),
      classList: { add: jasmine.createSpy('add'), contains: jasmine.createSpy('contains'), remove: jasmine.createSpy('remove') },
      isFullscreen: jasmine.createSpy('isFullscreen')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        performGroup: cmsConfigs.performConfig,
        IMGStreaming: cmsConfigs.imgStreamingConfig,
        AtTheRaces: cmsConfigs.atTheRacesConfig,
        Conviva: cmsConfigs.Conviva,
        StreamBetWeb: cmsConfigs.StreamBetWeb
      }))
    };
    quickbetService = {
      quickBetOnOverlayCloseSubj: new Subject<string>(),
      getRestoredSelection: jasmine.createSpy('getRestoredSelection')
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    changeDetectorRef = { detectChanges: jasmine.createSpy('detectChanges')};

    successHandler = jasmine.createSpy('success');
    errorHandler = jasmine.createSpy('errorHandler');

    component = new StreamBetProviderComponent(performGroupService, domSanitizer, elementRef, userService, windowRefService,
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
    component.streamBetCmsConfig = cmsConfigs.StreamBetWeb;
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('lads', () => {
    environment.brand = 'lads';
    component = new StreamBetProviderComponent(performGroupService, domSanitizer, elementRef, userService, windowRefService,
      cmsService, commandService, atTheRacesService, watchRulesService, imgService, racingStreamService,
      nativeBridgeService, localeService, loadVideoJsService, streamTrackingService, gtmService,
      sessionService, deviceService, liveStreamService, eventVideoStreamProvider, rendererService, convivaService,
      dialogService, componentFactoryResolver, quickbetService, pubsub, changeDetectorRef, remoteBetslipService, clientUserAgentService, iGameMediaService, storageService
    );
    expect(component['NETWORK_INDCIATIOR_CLASS']).toEqual('.network-indicator-parent-lads');
  });

  it('Coral', () => {
    environment.brand = 'bma';
    component = new StreamBetProviderComponent(performGroupService, domSanitizer, elementRef, userService, windowRefService,
      cmsService, commandService, atTheRacesService, watchRulesService, imgService, racingStreamService,
      nativeBridgeService, localeService, loadVideoJsService, streamTrackingService, gtmService,
      sessionService, deviceService, liveStreamService, eventVideoStreamProvider, rendererService, convivaService,
      dialogService, componentFactoryResolver, quickbetService, pubsub, changeDetectorRef, remoteBetslipService, clientUserAgentService, iGameMediaService, storageService
    );
    expect(component['NETWORK_INDCIATIOR_CLASS']).toEqual('.network-indicator-parent');
  });

  it('should hide elements when openFullScreen is called', () => {
    component['openFullScreen']();
    expect(windowRefService.document.querySelectorAll).toHaveBeenCalledWith('.top-bar');
  });

  it('should call disableContextMenu', () => {
    component['disableContextMenu']();
    expect(mockHtml5VideoTag.addEventListener).toHaveBeenCalled();
  });

  it('should remove overlay for iOS devices', () => {
    deviceService.isIos = true;
    component['removeOverlay'] = jasmine.createSpy('removeOverlay');
    component['openFullScreen']();
    expect(component['removeOverlay']).toHaveBeenCalled();
  });
  it('should addclass for iOS devices and not isWrapper', () => {
    deviceService.isIos = true;
    component.isWrapper = false;
    component['removeOverlay'] = jasmine.createSpy('removeOverlay');
    const homeBody = document.createElement('div');
    windowRefService.document.querySelector.and.returnValue(homeBody);
    component['openFullScreen']();
    expect(rendererService.renderer.addClass).toHaveBeenCalled();
  });
  it('should addclass for iOS devices and not isWrapper', () => {
    deviceService.isIos = true;
    component.isWrapper = false;
    component['removeOverlay'] = jasmine.createSpy('removeOverlay');
    const homeBody = document.createElement('div');
    windowRefService.document.querySelector.and.returnValue(homeBody);
    component['exitFullScreen']();
    expect(rendererService.renderer.removeClass).toHaveBeenCalled();
  });

  it('checkOrientationMode: #2 - removeChild', () => {
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    component.errorShown = true;
    deviceService.isWrapper = true;
    const overlayElem = document.createElement('div');
    const overlayHeaderElem = document.createElement('div');
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    const freebetdialog = document.createElement('div');
    freebetdialog.className = 'modals';
    const isVideoPlayer = document.createElement('div');
    const isTutVideoPlayer = document.createElement('div');
    isVideoPlayer.appendChild(freebetdialog);
    isVideoPlayer.appendChild(overlayElem);
    isVideoPlayer.appendChild(overlayHeaderElem);
    isVideoPlayer.appendChild(overlayHeaderElem);
    isVideoPlayer.id = component.streamUniqueId;
    isVideoPlayer.className = 'landscape-padding-top-zero';
    isTutVideoPlayer.className = 'landscape-padding-top-zero';

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
      if (selector === '#tutorial') return isTutVideoPlayer;
    });

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '.overlay-wrapper') return overlayElem;
      else if (selector === '.overlay-header-container') return overlayHeaderElem;
      else if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });

    spyOn(document, 'querySelector').and.callFake((className) => {
      if(className === '.modals') return freebetdialog;
    });

    component['openFullScreen'] = jasmine.createSpy('openFullScreen');
    component['checkOrientationMode']();
    expect(desktopPlayerMock.exitFullWindow).toHaveBeenCalled();
  });

  it('checkOrientationMode: #2 - removeOverlay', () => {
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    component.errorShown = true;
    deviceService.isWrapper = true;
    const overlayElem = document.createElement('div');
    const overlayHeaderElem = document.createElement('div');
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    const isTutVideoPlayer = document.createElement('div')
    const isVideoPlayer = document.createElement('div')
    isVideoPlayer.appendChild(overlayElem);
    isVideoPlayer.appendChild(overlayHeaderElem);
    isVideoPlayer.id = component.streamUniqueId;
    isVideoPlayer.className = 'landscape-padding-top-zero';
    isTutVideoPlayer.className = 'landscape-padding-top-zero';

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
      if (selector === '#tutorial') return isTutVideoPlayer;
    });

    elementRef.nativeElement.querySelectorAll.and.callFake((selector: string) => {
      if (selector === 'video') return null;
    });

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '.overlay-wrapper') return overlayElem;
      else if (selector === '.overlay-header-container') return overlayHeaderElem;
      else if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });
    component['openFullScreen'] = jasmine.createSpy('openFullScreen');
    component['checkOrientationMode']();
    expect(desktopPlayerMock.exitFullWindow).toHaveBeenCalled();
  });

  it('checkOrientationMode: #2 - removeOverlay - html5VideoTag - undefined', () => {
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    component.errorShown = true;
    deviceService.isWrapper = true;
    const overlayElem = document.createElement('div');
    const overlayHeaderElem = document.createElement('div');
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    const isTutVideoPlayer = document.createElement('div');
    const isVideoPlayer = document.createElement('div');
    isVideoPlayer.appendChild(overlayElem);
    isVideoPlayer.appendChild(overlayHeaderElem);
    isVideoPlayer.id = component.streamUniqueId;
    isVideoPlayer.className = 'landscape-padding-top-zero';
    isTutVideoPlayer.className = 'landscape-padding-top-zero';

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
      if (selector === '#tutorial') return isTutVideoPlayer;
    });

    elementRef.nativeElement.querySelectorAll.and.callFake((selector: string) => {
      if (selector === 'video') return undefined;
    });

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '.overlay-wrapper') return overlayElem;
      else if (selector === '.overlay-header-container') return overlayHeaderElem;
      else if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });

    spyOn(document, 'querySelector').and.callFake(() => {
      return (document.createElement('div'));
    }); 

    component['openFullScreen'] = jasmine.createSpy('openFullScreen');
    component['checkOrientationMode']();
    expect(desktopPlayerMock.exitFullWindow).toHaveBeenCalled();
  });

  it('checkOrientationMode: #2 - tutorialPlayer', () => {
    component.tutorialPlayer = desktopPlayerMock;
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    component.errorShown = true;
    deviceService.isWrapper = false;
    const overlayElem = document.createElement('div');
    const overlayHeaderElem = document.createElement('div');
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    const isVideoPlayer = document.createElement('div')
    isVideoPlayer.appendChild(overlayElem);
    isVideoPlayer.appendChild(overlayHeaderElem);
    isVideoPlayer.id = component.streamUniqueId;
    component.windowRefService.nativeWindow.orientation = 90;
    component.isWrapper = false;

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
    });

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '.overlay-wrapper') return overlayElem;
      else if (selector === '.overlay-header-container') return overlayHeaderElem;
      else if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });

    component['openFullScreen'] = jasmine.createSpy('openFullScreen');
    component['checkOrientationMode']();
    expect(component.isWrapper).toBeFalse();
  });

  it('checkOrientationMode: #2 - tutorialPlayer - wrapper', () => {
    component.tutorialPlayer = desktopPlayerMock;
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    component.errorShown = true;
    deviceService.isWrapper = true;
    const overlayElem = document.createElement('div');
    const overlayHeaderElem = document.createElement('div');
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    const isVideoPlayer = document.createElement('div')
    isVideoPlayer.appendChild(overlayElem);
    isVideoPlayer.appendChild(overlayHeaderElem);
    isVideoPlayer.id = component.streamUniqueId;
    component.windowRefService.nativeWindow.orientation = 90;
    component.isWrapper = true;

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
    });

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '.overlay-wrapper') return overlayElem;
      else if (selector === '.overlay-header-container') return overlayHeaderElem;
      else if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });

    component['openFullScreen'] = jasmine.createSpy('openFullScreen');
    component['checkOrientationMode']();
    expect(component.isWrapper).toBeTrue();
  })


  it('checkOrientationMode: #2 - tutorialPlayer - portrait', () => {
    component.errorShown = false;
    spyOn<any>(component, 'exitFullScreen');
    component.tutorialPlayer = desktopPlayerMock;
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    deviceService.isWrapper = true;
    const overlayElem = document.createElement('div');
    const overlayHeaderElem = document.createElement('div');
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    const isVideoPlayer = document.createElement('div')
    isVideoPlayer.appendChild(overlayElem);
    isVideoPlayer.appendChild(overlayHeaderElem);
    isVideoPlayer.id = component.streamUniqueId;
    component.windowRefService.nativeWindow.orientation = 0;
    component.isWrapper = true;

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
    });

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '.overlay-wrapper') return overlayElem;
      else if (selector === '.overlay-header-container') return overlayHeaderElem;
      else if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });

    const homeBody = document.createElement('div');
    windowRefService.document.querySelector.and.returnValue(homeBody);

    component['openFullScreen'] = jasmine.createSpy('openFullScreen');
    component['checkOrientationMode']();
    expect(component.isWrapper).toBeTrue();
  })

  it('checkOrientationMode: #3', () => {
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    component.errorShown = false;
    deviceService.isWrapper = true;
    const isVideoPlayer = document.createElement('div');
    isVideoPlayer.id = component.streamUniqueId;
    const nativeVideoPlayerPlaceholder = document.createElement('div');

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
    });

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });

    component['openFullScreen'] = jasmine.createSpy('openFullScreen');
    component['checkOrientationMode']();
    expect(desktopPlayerMock.exitFullWindow).toHaveBeenCalled();
  });

  it('should hide fullscreen when setExitScreenFlags is called', () => {
    desktopPlayerMock.isFullscreen.and.returnValue(false);
    component.desktopPlayer = desktopPlayerMock;
    component['setExitScreenFlags']();
    expect(component.isFullScreen).toEqual(false);
  });

  it('should hide fullscreen when onResizeOrOrientationChange is called', () => {
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
    deviceService.isAndroid = true;
    desktopPlayerMock.isFullscreen.and.returnValue(true);
    component.desktopPlayer = desktopPlayerMock;
    component['appendOverlayElement'] = jasmine.createSpy('appendOverlayElement');
    component['onResizeOrOrientationChange']();
    expect(component['appendOverlayElement']).toHaveBeenCalled();
    expect(component.isFullScreen).toEqual(true);
  });

  it('should hide fullscreen when onResizeOrOrientationChange is called - tutorial', () => {
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
    deviceService.isAndroid = true;
    desktopPlayerMock.isFullscreen.and.returnValue(true);
    component.tutorialPlayer = desktopPlayerMock;
    component['appendOverlayElement'] = jasmine.createSpy('appendOverlayElement');
    component['onResizeOrOrientationChange']();
    expect(component['appendOverlayElement']).toHaveBeenCalled();
    expect(component.isFullScreen).toEqual(true);
  });

  it('should append overlay elements when all dependencies are available', () => {
    const overlayElem = document.createElement('div');
    overlayElem.id = 'overlay-wrapper';
    const overlayHeaderElem = document.createElement('div');
    const nativeVideoPlayerPlaceholder = document.createElement('div');
    overlayHeaderElem.classList.add('overlay-header-container');
    const isVideoPlayer = document.createElement('div');
    isVideoPlayer.id = component.streamUniqueId;

    windowRefService.document.querySelector.and.callFake((selector: string) => {
      if (selector === '#overlay-wrapper') return overlayElem;
      if (selector === '.overlay-header-container') return overlayHeaderElem;
      else if (selector === '.native-video-player-placeholder') return nativeVideoPlayerPlaceholder;
    });

    elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
    });

    component['appendOverlayElement']();
    expect(isVideoPlayer.contains(overlayElem)).toBeTrue();
    expect(isVideoPlayer.contains(overlayHeaderElem)).toBeTrue();
  });

  it('should not append overlay elements when any of the dependencies is missing', () => {
    windowRefService.document.querySelector.and.returnValue(null);
    elementRef.nativeElement.querySelectorAll.and.returnValue(null);
    elementRef.nativeElement.querySelector.and.returnValue(null);

    component['appendOverlayElement']();
    expect(windowRefService.document.querySelector).toHaveBeenCalled();
    expect(elementRef.nativeElement.querySelector).toHaveBeenCalled();
  });

  it('should not append overlay elements when any of the dependencies is missing', () => {
    windowRefService.document.querySelector.and.returnValue(null);
    elementRef.nativeElement.querySelectorAll.and.returnValue(undefined);
    elementRef.nativeElement.querySelector.and.returnValue(undefined);

    component['appendOverlayElement']();
    expect(windowRefService.document.querySelector).toHaveBeenCalled();
    expect(elementRef.nativeElement.querySelector).toHaveBeenCalled();
  });

  it('should hide error when handleStreamEnd is called', () => {
    component['desktopPlayer'] = desktopPlayerMock;
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
    component['handleStreamEnd']();
    expect(component.errorShown).toEqual(true);
  });

  it('should add classes and blur active element in landscape mode', () => {
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
    component['renderLandscapeErrorScreen'](true);

    expect(rendererService.renderer.addClass).toHaveBeenCalledWith(
      windowRefService.nativeWindow.document.querySelector('.landscape-mobile-overlay'),
      'landscape-mode'
    );
    expect(rendererService.renderer.addClass).toHaveBeenCalledWith(windowRefService.document.body, 'mobile-overlay-active');
    expect(windowRefService.nativeWindow.document.activeElement.blur).toHaveBeenCalled();
  });

  it('should not add classes or blur active element in portrait mode', () => {
    spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
    component['renderLandscapeErrorScreen'](false);

    expect(rendererService.renderer.addClass).not.toHaveBeenCalled();
    expect(windowRefService.nativeWindow.document.activeElement.blur).not.toHaveBeenCalled();
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

  it('should init video player', () => {
    component.playStream();
    component.streamUniqueId = 'rtmpe-hls';
    expect(elementRef.nativeElement.querySelector).toHaveBeenCalledWith('#rtmpe-hls');
    expect(windowRefService.nativeWindow.videojs).toHaveBeenCalled();
  });

  it('should showErrorMessage', () => {
    component.ERROR_MESSAGES.loginRequired = true;
    component['deviceService'].isDesktop = false;
    component.showErrorMessage('eventNotStarted');

    expect(component.ERROR_MESSAGES.loginRequired).toBeFalsy();
    expect(component.ERROR_MESSAGES.eventNotStarted).toBeTruthy();
    component.showErrorMessage('onlyLoginRequired');

    expect(localeService.getString).toHaveBeenCalledWith('sb.onlyLoginRequired');
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
      expect(dialogService.openDialog).toHaveBeenCalled();
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
      expect(component.showPlayer).toBeFalsy();
      expect(component['streamActive']).toBeFalsy();
    }));

    it('should handle not desktop mode but wrapper mode', fakeAsync(() => {
      deviceService.isWrapper = true;
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
    }));

    it('should handle desktop mode with desktop player', fakeAsync(() => {
      deviceService.isDesktop = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['hideStream']();
      tick();

      expect(playSuccessErrorListener).toHaveBeenCalledWith(false);
      expect(mockHtml5VideoTag.pause).not.toHaveBeenCalled();
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

    it('should calculate frame width based on elementWidth with landscape mode', () => {
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      const elementWidth = 100;
      performGroupService.getElementWidth.and.returnValue(elementWidth);
      const parentNode = { tag: 'div' };

      elementRef.nativeElement.parentNode = parentNode;
      component['setPlayerSize']();

      expect(component.frameWidth).toEqual(elementWidth);
      expect(component.frameHeight).toEqual(56);
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

      component['getStreamId']({ listOfMediaProviders: [] } as IStreamProvidersResponse);
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
      iGameMediaService.isEventStarted.and.returnValue(true);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);

      expect(successHandler).toHaveBeenCalledWith('');
      iGameMediaService.isEventStarted.and.returnValue(false);
      component['getStreamNotStartedMessage']().subscribe(successHandler, errorHandler);
      expect(errorHandler).toHaveBeenCalledWith('eventNotStarted');
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

      expect(component['showVideoPlayer']).toBeFalsy();
    });

    it('should load scripts and do not perform autoPlay', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;

      component['autoPlayStream']();
      tick();

      expect(loadVideoJsService.loadScripts).toHaveBeenCalled();
      expect(component['videJsTimeout']).toBeDefined();
      expect(component['showVideoPlayer']).toBeFalsy();
    }));

    it('should load scripts and do perform autoPlay', fakeAsync(() => {
      component.autoPlay = true;
      component['isDesktop'] = true;

      component['autoPlayStream']();
      tick();

      expect(loadVideoJsService.loadScripts).toHaveBeenCalled();
      expect(component['showVideoPlayer']).toBeFalsy();
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(component['playStream']);
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

      expect(gtmService.push).not.toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        event: 'trackEvent',
        eventCategory: 'Livestream',
        eventAction: 'error'
      }));
      expect(localeService.getString).not.toHaveBeenCalledWith('sb.geoBlocked');
    });
  });

  describe('resizeView', () => {
    it('should set timeout property', () => {
      component.desktopPlayer = desktopPlayerMock;
      component['resizeTimeFrame'] = 500;
      component.isFullScreen = true;
      component['resizeView']();

      expect(windowRefService.nativeWindow.clearTimeout).not.toHaveBeenCalled();
      expect(component['resizeTimeout']).toEqual(jasmine.any(Number));
    });

    it('should return from resizeView', () => {
      component.desktopPlayer = desktopPlayerMock;
      component['resizeTimeFrame'] = 500;
      component.isFullScreen = false;
      deviceService.isWrapper = false;
      windowRefService.nativeWindow.orientation = 90;
      component['resizeView']();

      expect(windowRefService.nativeWindow.clearTimeout).not.toHaveBeenCalled();
    });

    it('should clear timeout before storing new one set timeout property', () => {
      component.desktopPlayer = desktopPlayerMock;
      component['resizeTimeFrame'] = 500;
      component.isFullScreen = true;
      component['resizeView']();
      component['resizeView']();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(jasmine.any(Number));
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(component['setPlayerSize'],
        500);
    });

    it('should set timeout property in landscapae mode', () => {
      component['resizeTimeFrame'] = 500;
      deviceService.isWrapper = true;
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      desktopPlayerMock.isFullscreen.and.returnValue(false);
      component.desktopPlayer = desktopPlayerMock;
      component['resizeView']();

      expect(windowRefService.nativeWindow.clearTimeout).not.toHaveBeenCalled();
      expect(component['resizeTimeout']).toEqual(jasmine.any(Number));
    });

    it('should set timeout property in landscape mode with player in disposed state', () => {
      component['resizeTimeFrame'] = 500;
      deviceService.isWrapper = true;
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      component.desktopPlayer = {...desktopPlayerMock, isDisposed_ : true};
      desktopPlayerMock.isFullscreen.and.returnValue(false);
      component.tutorialPlayer  = desktopPlayerMock;
      component.tutorialStreaming = true
      component['resizeView']();

      expect(windowRefService.nativeWindow.clearTimeout).not.toHaveBeenCalled();
      expect(component['resizeTimeout']).toEqual(jasmine.any(Number));
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
    });

    it('should call ngOnDestroy', () => {
      const homeBody = document.createElement('div');
      windowRefService.document.querySelector.and.returnValue(homeBody);
      component.tutorialPlayer = { isDisposed_: '', dispose: () => { } };
      component['videJsTimeout'] = 1234;
      component.ngOnDestroy();

      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(component['videJsTimeout']);
      expect(commandService.unregister).toHaveBeenCalledWith(commandService.API.GET_LIVE_STREAM_STATUS);
    });

    it('should unsubscribe for action listener', () => {
      component['actionSubscriber'] = eventVideoStreamProvider.playListener.subscribe();

      spyOn(component['actionSubscriber'], 'unsubscribe').and.callThrough();
      component.ngOnDestroy();

      expect(component['actionSubscriber'].unsubscribe).toHaveBeenCalled();
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
    });

    it('should close desktop player for desktop device', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      component.ngOnDestroy();

      expect(desktopPlayerMock.dispose).toHaveBeenCalled();
    });

    it('should close tutorial player', () => {
      component['desktopPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component['tutorialPlayer '] = { ...desktopPlayerMock, isDisposed_: false };
      component.isConvivaEnabled = true;
      component.ngOnDestroy();

      expect(desktopPlayerMock.dispose).toHaveBeenCalled();
    });
  });

  describe('checkOrientation', () => {
    beforeEach(() => {
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      deviceService.isWrapper = true;
      component.windowRefService.nativeWindow.orientation = 90;
    });
    it('checkOrientationMode: #1', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = true;
      deviceService.isWrapper = true;
      const isVideoPlayer = document.createElement('div');
      isVideoPlayer.id = component.streamUniqueId;

      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
        if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
      });
      component['openFullScreen'] = jasmine.createSpy('openFullScreen');
      component['checkOrientationMode']();
      expect(component['openFullScreen']).toHaveBeenCalled();
      expect(desktopPlayerMock.enterFullWindow).toHaveBeenCalled();
    });
    it('checkOrientationMode: with tutorial player', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = true;
      deviceService.isWrapper = true;
      const isTutVideoPlayer = document.createElement('div');

      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
        if (selector === '#tutorial') return isTutVideoPlayer;
      });
      component['openFullScreen'] = jasmine.createSpy('openFullScreen');
      component['checkOrientationMode'](true);
      expect(component['openFullScreen']).toHaveBeenCalled();
      expect(desktopPlayerMock.enterFullWindow).toHaveBeenCalled();
    });
    it('checkOrientationMode: with tutorial player and no wrapper', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = false;
      deviceService.isWrapper = false;
      const isTutVideoPlayer = document.createElement('div');

      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
        if (selector === '#tutorial') return isTutVideoPlayer;
      });
      component['openFullScreen'] = jasmine.createSpy('openFullScreen');
      component['checkOrientationMode'](true);
      expect(component['openFullScreen']).not.toHaveBeenCalled();
    });
    it('checkOrientationMode: #2 - isLandscape', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      component['tutorialPlayer'] = { ...desktopPlayerMock, isDisposed_: false };
      component.isWrapper = false;
      deviceService.isWrapper = false;
      const isVideoPlayer = document.createElement('div');
      isVideoPlayer.id = component.streamUniqueId;
      spyOn<any>(component, 'renderLandscapeErrorScreen').and.callThrough();

      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
        if (selector === '#' + component.streamUniqueId) return isVideoPlayer;
      });
      component['openFullScreen'] = jasmine.createSpy('openFullScreen');
      component['checkOrientationMode']();
      expect(component['renderLandscapeErrorScreen']).toHaveBeenCalled();
    });
  });

  describe('onSuccess', () => {
    let stream;

    beforeEach(() => {
      stream = { stream: 'qwe' } as IStreamProvidersResponse;
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

    it('should handle Perform provider by provider info for not wrapper -1 ', fakeAsync(() => {
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
      // spyOn<any>(component.performGroupService, 'performGroupId').and.callThrough();
      component.showCSBIframe = true;
      component['isWrapper'] = false;
      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(component.performGroupService.performGroupId).toHaveBeenCalled();
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

    it('should handle showHideStream - error', fakeAsync(() => {
      const providerInfo = {
        priorityProviderName: '',
        listOfMediaProviders: [{
          name: '',
          children: [{
            media: {
              accessProperties: ',1231223:0'
            }
          }]
        }]
      } as IStreamProvidersResponse;

      component['showHideStream'](providerInfo).subscribe(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalled();
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
      component.providerInfo = {
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
      component['showHideStream'](component.providerInfo).subscribe(successHandler, errorHandler);

      expect(iGameMediaService.getStream).toHaveBeenCalledWith(eventEntity, component.providerInfo, true);
      expect(successHandler).toHaveBeenCalledWith(eventEntity);
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
      expect(convivaService.setConfig).toHaveBeenCalled();
      expect(convivaService.preload).toHaveBeenCalled();
    }));

    it('should load desktop scripts and do not perform autoPlay', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;

      component.ngOnInit();
      tick();

      expect(loadVideoJsService.loadScripts).toHaveBeenCalled();
      expect(component['videJsTimeout']).toBeDefined();
      expect(component['showVideoPlayer']).toBeFalsy();
    }));

    it('should set resize timeframe for IOS', fakeAsync(() => {
      component.autoPlay = false;
      component['isDesktop'] = true;
      deviceService.isIos = true;

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

      expect(component['resizeTimeFrame']).toEqual(500);
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
      component['streamCache'].set(5, { meta: {} } as any);
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
      component['streamCache'].set(5, {} as any);
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
      component['streamCache'].set(5, {
        meta: {
          operatorId: '1',
          imgSecret: 'secret'
        }
      } as any);
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
      component['streamCache'].set(5, {
        meta: {
          partnerCode: '1',
          secret: 'secret'
        }
      } as any);
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
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({
        type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: true
      });
    });

    it('should set isIOSStream', () => {
      component.streamBetCmsConfig.isAndroidStream = false;
      component.streamBetCmsConfig.isIOSStream = true;

      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['desktopPlayer'].ready = jasmine.createSpy('desktopPlayer').and.callFake((fun) => {
        fun();
      });
      component['streamCache'].set(eventId, {} as IStreamProvidersResponse);
      component['runVideoJsPlayer']('stream:rtmp');
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({
        type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: true
      });
    });

    it('should set dummy false', () => {
      component.streamBetCmsConfig.isAndroidStream = false;
      component.streamBetCmsConfig.isIOSStream = false;
      storageService.get.and.returnValue(undefined);

      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['streamCache'].set(eventId, {} as IStreamProvidersResponse);
      component['runVideoJsPlayer']('stream:rtmp');
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({
        type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: true
      });
    });

    it('should set withCredentials true also', () => {
      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['streamCache'].set(eventId, {} as IStreamProvidersResponse);
      component.providerInfo = undefined;
      component['runVideoJsPlayer']('stream:rtmp');
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({
        type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: true
      });
    });

    it('should set withCredentials false', () => {
      component['isDesktop'] = true;
      component['desktopPlayer'] = desktopPlayerMock;
      component['streamCache'].set(eventId, {} as IStreamProvidersResponse);
      component.providerInfo = { priorityProviderName: 'At The Races' } as IStreamProvidersResponse;
      component['runVideoJsPlayer']('stream:rtmp');
      expect(desktopPlayerMock.src).toHaveBeenCalledWith({
        type: jasmine.any(String),
        src: 'stream:rtmp',
        withCredentials: false
      });
    });

    it('should run video js player for desktop when there is no player insance -1', () => {
      let playerReadyCallback;
      windowRefService.nativeWindow.setTimeout = jasmine.createSpy('setTimeout').and.callFake((fun) => {
        fun();
      })
      storageService.get.and.returnValue('10');
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

    it('should run video js player for desktop when there is no player insance and display loader', () => {
      let playerReadyCallback;
      windowRefService.nativeWindow.setTimeout = jasmine.createSpy('setTimeout').and.callFake((fun) => {
        fun();
      })
      windowRefService.document.querySelector.and.callFake((selector) => {
        if(['.vjs-loading-spinner', '.native-video-player-placeholder'].includes(selector)) return document.createElement('div');
      });
      storageService.get.and.returnValue('10');
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

      expect(component['streamingUrl']).not.toBeDefined();
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
      expect(component['streamingUrl']).not.toBeDefined();

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

      expect(gtmService.push).toHaveBeenCalled();
      expect(streamTrackingService.addIdToTrackedList).toHaveBeenCalledWith(eventEntity.id, 'liveStream');
    });
  });

  describe('playStream', () => {
    let errorListener,
      endedListener,
      retryplaylistListener,
      fullscreenchangeListener,
      readyListener,
      canPlayListener,
      waitingListener;

    const event = {
      preventDefault: jasmine.createSpy('preventDefault')
    };
    videoSpinner = jasmine.createSpy('videoSpinner').and.returnValue(document.createElement('div'));

    it('should play desktop stream', fakeAsync(() => {
      component.streamCache.set(eventEntity.id, { error: errorHandler } as IStreamProvidersResponse);
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      desktopPlayerMock.isFullscreen.and.returnValue(true);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      windowRefService.document.querySelector.and.returnValue(document.createElement('div'));
      component['videJsTimeout'] = 123;
      component['isDesktop'] = true;
      component.isFullScreen = false;
      // const videoSpinner = jasmine.createSpy('videoSpinner').and.returnValue(document.createElement('div'));
      desktopPlayerMock.on.and.callFake((name, handler) => {
        if (name === 'error') {
          errorListener = handler;
        } else if (name === 'ended') {
          endedListener = handler;
        } else if (name === 'ready') {
          readyListener = handler;
        } else if (name === 'fullscreenchange') {
          fullscreenchangeListener = handler;
        } else if (name === 'canplay') {
          canPlayListener = handler;
        }
      });
      component['isConvivaEnabled'] = true;
      component.playStream(event);
      component.streamUniqueId = 'rtmpe-hls';
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRefService.nativeWindow.videojs).toHaveBeenCalledWith('rtmpe-hls', { muted: false, techOrder: ['html5', 'flash'], fluid: true, preferFullWindow: true, html5: Object({ nativeTextTracks: false }), controlBar: Object({ fullscreenToggle: true, pictureInPictureToggle: false }), suppressNotSupportedError: true, userActions: Object({ click: false, doubleClick: false }), inactivityTimeout: 0 });
      expect(desktopPlayerMock.on).toHaveBeenCalledTimes(5);
      errorListener();
      endedListener();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();

      fullscreenchangeListener();
      expect(component.isFullScreen).toEqual(true);        
      flush();
    }));

    it('should play desktop stream with value changes in fullscreen button', fakeAsync(() => {
      component.streamCache.set(eventEntity.id, { error: errorHandler } as IStreamProvidersResponse);
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      desktopPlayerMock.isFullscreen.and.returnValue(false);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      windowRefService.document.querySelector.and.callFake((selector) => {
        if(['.vjs-loading-spinner', '.native-video-player-placeholder'].includes(selector)) return document.createElement('div');
      });
      component['videJsTimeout'] = 123;
      component['isDesktop'] = true;
      component.isFullScreen = true;
      component.playingTutorialVideo = false;
      desktopPlayerMock.on.and.callFake((name, handler) => {
        if (name === 'error') {
          errorListener = handler;
        } else if (name === 'ended') {
          endedListener = handler;
        } else if (name === 'ready') {
          readyListener = handler;
        } else if (name === 'fullscreenchange') {
          fullscreenchangeListener = handler;
        } else if (name === 'canplay') {
          canPlayListener = handler;
        } else if (name === 'waiting') {
          waitingListener = handler;
        }
      });
      component['isConvivaEnabled'] = true;
      component.playStream(event);
      component.streamUniqueId = 'rtmpe-hls';
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRefService.nativeWindow.videojs).toHaveBeenCalledWith('rtmpe-hls', {
        muted: component.deviceService.isIos,
        techOrder: ['html5', 'flash'],
        fluid: true,
        preferFullWindow: true,
        html5: { nativeTextTracks: false },
        controlBar: {
          fullscreenToggle: true,
          pictureInPictureToggle: false
        },
        suppressNotSupportedError: true,
        userActions: {
          click: false, doubleClick: false
        }
        , inactivityTimeout: 0
      });
      expect(desktopPlayerMock.on).toHaveBeenCalledTimes(5);
      errorListener();
      endedListener();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();

      fullscreenchangeListener();
      expect(component.isFullScreen).toEqual(false);
      canPlayListener();
      waitingListener();
      expect(convivaService.initVideoJsAnalytics).toHaveBeenCalled();
      flush();
    }));

    it('should play desktop stream with value changes in fullscreen button for iOS', fakeAsync(() => {
      component.streamCache.set(eventEntity.id, { error: errorHandler } as IStreamProvidersResponse);
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      desktopPlayerMock.isFullscreen.and.returnValue(false);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      windowRefService.document.querySelector.and.callFake((selector) => {
        if(['.vjs-loading-spinner', '.native-video-player-placeholder'].includes(selector)) return document.createElement('div');
      });
      component['videJsTimeout'] = 123;
      component['isDesktop'] = true;
      component.isFullScreen = true;
      component.playingTutorialVideo = false;
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
      deviceService.isIos = true;
      deviceService.isWrapper = true;
      desktopPlayerMock.on.and.callFake((name, handler) => {
        if (name === 'error') {
          errorListener = handler;
        } else if (name === 'ended') {
          endedListener = handler;
        } else if (name === 'ready') {
          readyListener = handler;
        } else if (name === 'fullscreenchange') {
          fullscreenchangeListener = handler;
        } else if (name === 'canplay') {
          canPlayListener = handler;
        } else if (name === 'waiting') {
          waitingListener = handler;
        }
      });
      component['isConvivaEnabled'] = true;
      component.playStream(event);
      component.streamUniqueId = 'rtmpe-hls';
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRefService.nativeWindow.videojs).toHaveBeenCalledWith('rtmpe-hls', {
        muted: component.deviceService.isIos,
        techOrder: ['html5', 'flash'],
        fluid: true,
        preferFullWindow: true,
        html5: { nativeTextTracks: false },
        controlBar: {
          fullscreenToggle: true,
          pictureInPictureToggle: false
        },
        suppressNotSupportedError: true,
        userActions: {
          click: false, doubleClick: false
        }
        , inactivityTimeout: 0
      });
      expect(desktopPlayerMock.on).toHaveBeenCalledTimes(5);
      errorListener();
      endedListener();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();

      fullscreenchangeListener();
      expect(component.isFullScreen).toEqual(false);
      canPlayListener();
      waitingListener();
      expect(convivaService.initVideoJsAnalytics).toHaveBeenCalled();
      flush();
    }));

    it('should play desktop stream with value changes in fullscreen button for iOS#1', fakeAsync(() => {
      component.streamCache.set(eventEntity.id, { error: errorHandler } as IStreamProvidersResponse);
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      desktopPlayerMock.isFullscreen.and.returnValue(true);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      windowRefService.document.querySelector.and.callFake((selector) => {
        if(['.vjs-loading-spinner', '.native-video-player-placeholder'].includes(selector)) return document.createElement('div');
      });
      component['videJsTimeout'] = 123;
      component['isDesktop'] = true;
      component.isFullScreen = true;
      component.playingTutorialVideo = false;
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      deviceService.isIos = true;
      deviceService.isWrapper = true;
      desktopPlayerMock.on.and.callFake((name, handler) => {
        if (name === 'error') {
          errorListener = handler;
        } else if (name === 'ended') {
          endedListener = handler;
        } else if (name === 'ready') {
          readyListener = handler;
        } else if (name === 'fullscreenchange') {
          fullscreenchangeListener = handler;
        } else if (name === 'canplay') {
          canPlayListener = handler;
        } else if (name === 'waiting') {
          waitingListener = handler;
        }
      });
      component['isConvivaEnabled'] = true;
      component.playStream(event);
      component.streamUniqueId = 'rtmpe-hls';
      expect(windowRefService.nativeWindow.clearTimeout).toHaveBeenCalledWith(123);
      expect(windowRefService.nativeWindow.videojs).toHaveBeenCalledWith('rtmpe-hls', {
        muted: component.deviceService.isIos,
        techOrder: ['html5', 'flash'],
        fluid: true,
        preferFullWindow: true,
        html5: { nativeTextTracks: false },
        controlBar: {
          fullscreenToggle: true,
          pictureInPictureToggle: false
        },
        suppressNotSupportedError: true,
        userActions: {
          click: false, doubleClick: false
        }
        , inactivityTimeout: 0
      });
      expect(desktopPlayerMock.on).toHaveBeenCalledTimes(5);
      errorListener();
      endedListener();
      expect(desktopPlayerMock.dispose).toHaveBeenCalled();

      fullscreenchangeListener();
      expect(component.isFullScreen).toEqual(true);
      canPlayListener();
      waitingListener();
      expect(convivaService.initVideoJsAnalytics).toHaveBeenCalled();
      flush();
    }));

    it('playtutorialvideo: should play desktop stream with value changes in fullscreen button', fakeAsync(() => {
      elementRef.nativeElement.querySelector.and.callFake((selector) => {
        if(selector === '.stream-msg-wrapper') return document.createElement('div');
        else return mockHtml5VideoTag
      });
      elementRef.nativeElement.querySelectorAll.and.returnValue([desktopPlayerMock]);
      windowRefService.document.querySelector.and.returnValue(document.createElement('div'));
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['videJsTimeout'] = 123;
      component['isDesktop'] = true;
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      component.isFullScreen = true;
      deviceService.isWrapper = true;
      component['desktopPlayer'] = desktopPlayerMock;
      desktopPlayerMock.on.and.callFake((name, handler) => {
        if (name === 'error') {
          errorListener = handler;
        }
        else if (name === 'ended') {
          endedListener = handler;
        } else if (name === 'ready') {
          readyListener = handler;
        } else if (name === 'fullscreenchange') {
          fullscreenchangeListener = handler;
        } else if (name === 'canplay') {
          handler();
        }
      });
      component.playtutorialvideo();
      component.streamUniqueId = 'rtmpe-hls';
      expect(windowRefService.nativeWindow.videojs).toHaveBeenCalledWith('tutorial', { muted: true, techOrder: ['html5', 'flash'], preferFullWindow: true, fluid: true, html5: Object({ nativeTextTracks: false }), nativeControlsForTouch: false, controlBar: Object({ fullscreenToggle: false, pictureInPictureToggle: false }) });
      expect(desktopPlayerMock.on).toHaveBeenCalledTimes(3);
      endedListener();

      expect(desktopPlayerMock.volume).toHaveBeenCalled();
      expect(desktopPlayerMock.play).toHaveBeenCalled();

      readyListener();
      expect(desktopPlayerMock.volume).toHaveBeenCalled();
      flush();
    }));

    it('playtutorialvideo: should not play desktop stream if #rtmpe-hls not available', fakeAsync(() => {
      elementRef.nativeElement.querySelectorAll.and.returnValue(null);
      elementRef.nativeElement.querySelector.and.returnValue(null);

      component.playtutorialvideo();

      expect(windowRefService.nativeWindow.videojs).not.toHaveBeenCalled();
      expect(component.tutorialPlayer).toEqual(null);
    }));

    it('should stop the player when we hit retryplaylist 10 times', () => {
      component.streamCache.set(eventEntity.id, { error: errorHandler } as IStreamProvidersResponse);
      elementRef.nativeElement.querySelector.and.returnValue(mockHtml5VideoTag);
      windowRefService.nativeWindow.videojs.and.returnValue(desktopPlayerMock);
      component['videJsTimeout'] = 10;
      component['isDesktop'] = true;
      component.providerInfo = { priorityProviderName: "At The Races" } as IStreamProvidersResponse
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
      component.streamCache.set(eventEntity.id, { error: errorHandler } as IStreamProvidersResponse);
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

    it(' iosstream true', () => {
      component.streamBetCmsConfig.isIOSStream = true;
      component.streamBetCmsConfig.isAndroidStream = false;
      component.streamCache.set(eventEntity.id, { error: errorHandler } as IStreamProvidersResponse);
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
      expect(component['showPlayer']).toBeTrue();
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
        component.streamBetCmsConfig.isAndroidStream = false;
        component.streamBetCmsConfig.isIOSStream = false;
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
        component.streamBetCmsConfig.isIOSStream = false;
        expect(component['showHideStream']).toHaveBeenCalledWith(component.providerInfo);
      });
    });

    describe('should not display proper error message: iGame Media', () => {
      beforeEach(() => {
        component.providerInfo = {
          priorityProviderName: 'iGame Media',
          listOfMediaProviders: [{
            name: 'iGameMedia',
            children: [{
              media: {
                accessProperties: 'iGameMedia,1231223:0'
              }
            }]
          }]
        } as IStreamProvidersResponse;
        component['onError'] = jasmine.createSpy('onError');
        component['getStreamUnavailableMessage'] = jasmine.createSpy('getStreamUnavailableMessage').and.returnValue('');
        component['getStreamNotStartedMessage'] = jasmine.createSpy('getStreamNotStartedMessage').and.returnValue(observableOf(''));
        component['performConfig'] = {} as any;
        component['checkCanWatch'] = jasmine.createSpy('checkCanWatch').and.returnValue(observableOf({}));
        component['onSuccess'] = jasmine.createSpy('onSuccess');
        component['useCachedData'] = jasmine.createSpy('useCachedData');
        component.eventVideoStreamProvider.playSuccessErrorListener.next = jasmine.createSpy('next');
        component.streamBetCmsConfig.isAndroidStream = false;
        component.streamBetCmsConfig.isIOSStream = false;
      });

      it(' and pass streamFlow: iGame Media', () => {
        component['showHideStream'] = jasmine.createSpy('showHideStream').and.returnValue(observableOf({ streamLink: 'test' }));
        component.playStream();
        expect(component['onSuccess']).toHaveBeenCalledWith('test');
        expect(component['useCachedData']).toHaveBeenCalled();
        expect(component.eventVideoStreamProvider.playSuccessErrorListener.next).toHaveBeenCalledWith(true);
      });
    });

    it('should display desktop error message if event no performConfig were found', fakeAsync(() => {
      component.streamBetCmsConfig.isAndroidStream = false;
      component.streamBetCmsConfig.isIOSStream = false;
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

  describe('handleFullScreenControl', () => {

    it('should handle fullscreen control vjs-fullscreen-control undefined', () => {
      component.elementRef.nativeElement.querySelector = jasmine.createSpy('querySelector').and.returnValue(undefined);
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
      component['handleFullScreenControl']();

      expect(component['isLandscapeMode']()).not.toBe(true);
    });

    it('should handle fullscreen control vjs-fullscreen-control null', () => {
      component.elementRef.nativeElement.querySelector = jasmine.createSpy('querySelector').and.returnValue(null);
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
      component['handleFullScreenControl']();

      expect(component['isLandscapeMode']()).not.toBe(true);
    });

    it('should handle fullscreen control screen null', () => {
      component.elementRef.nativeElement.querySelector = jasmine.createSpy('querySelector').and.returnValue({
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((event, handler, config) => {
          if (event === 'touchend') {
            handler();
          }
          return () => { };
        })
      });
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(false);
      component['handleFullScreenControl']();

      expect(component['isLandscapeMode']()).not.toBe(true);
    });

    it('should handle fullscreen control in landscape orientation', () => {
      spyOn<any>(component, 'exitFullScreen').and.callThrough();
      component.elementRef.nativeElement.querySelector = jasmine.createSpy('querySelector').and.returnValue({
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((event, handler, config) => {
          if (event === 'touchend') {
            handler();
          }
          return () => { };
        })
      });
      spyOnProperty(screen, 'orientation').and.returnValue({
        type: 'landscape-primary',
      });
      component.windowRefService.nativeWindow.orientation = 90;
      component['handleFullScreenControl']();

      expect(component['isLandscapeMode']()).toBe(true);
      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.STREAM_BET_VIDEO_MODE, false);
      expect(component['exitFullScreen']).not.toHaveBeenCalled();
    });

    it('should handle fullscreen control in landscape orientation -90', () => {
      spyOn<any>(component, 'exitFullScreen').and.callThrough();
      component.elementRef.nativeElement.querySelector = jasmine.createSpy('querySelector').and.returnValue({
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((event, handler, config) => {
          if (event === 'touchend') {
            handler();
          }
          return () => { };
        })
      });
      spyOnProperty(screen, 'orientation').and.returnValue({
        type: 'landscape-primary',
      });
      component.windowRefService.nativeWindow.orientation = -90;
      component['handleFullScreenControl']();

      expect(component['isLandscapeMode']()).toBe(true);
      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.STREAM_BET_VIDEO_MODE, false);
      expect(component['exitFullScreen']).not.toHaveBeenCalled();
    });

    it('should handle fullscreen control in landscape orientation 180', () => {
      spyOn<any>(component, 'exitFullScreen').and.callThrough();
      component.elementRef.nativeElement.querySelector = jasmine.createSpy('querySelector').and.returnValue({
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((event, handler, config) => {
          if (event === 'touchend') {
            handler();
          }
          return () => { };
        })
      });
      spyOnProperty(screen, 'orientation').and.returnValue({
        type: 'landscape-primary',
      });
      component.windowRefService.nativeWindow.orientation = 180;
      component['handleFullScreenControl']();

      expect(component['isLandscapeMode']()).toBe(false);
      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.STREAM_BET_VIDEO_MODE, false);
      expect(component['exitFullScreen']).toHaveBeenCalled();
    });

    it('should handle fullscreen control in portrait orientation', () => {
      component['desktopPlayer'] = desktopPlayerMock;
      // spyOn<any>(component.desktopPlayer, 'exitFullScreen').and.callThrough();
      component.elementRef.nativeElement.querySelector = jasmine.createSpy('querySelector').and.returnValue({
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((event, handler, config) => {
          if (event === 'touchend') {
            handler();
          }
          return () => { };
        })
      });
      component.windowRefService.nativeWindow.orientation = 0;
      // elementRef.nativeElement.querySelector = jasmine.createSpy('showHideStream').and.returnValue(observableOf());
      component.deviceService.isWrapper = true;
      component.isFullScreen = true;
      spyOnProperty(screen, 'orientation').and.returnValue({
        type: 'portrait-primary',
      });
      component['handleFullScreenControl']();

      expect(component.desktopPlayer.exitFullscreen).toHaveBeenCalled();
    });
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
    }));
  });
  describe('handleDesktopPlayerVisibility',()=>{
    it('should call handleVideoPlayerPlaceholder after the 3000ms if desktopPlayer is true',fakeAsync(()=>{
     component.errorMessage = '';
     component.showPlayer = true;
     deviceService.isWrapper = true;
     windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn())
     elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      const toasterElement = document.createElement('div');
      if (selector === '#toaster') return toasterElement;
    });
     spyOn(component as any,'handleVideoPlayerPlaceholder')
     component['handleDesktopPlayerVisibility']();
     tick(3000);
     expect(component['handleVideoPlayerPlaceholder']).toHaveBeenCalledWith(true, false);
    }));
    
    it('should call handleVideoPlayerPlaceholder and checkorientation with desktopPlayer',fakeAsync(()=>{
      component.errorMessage = '';
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      component.showPlayer = true;
      deviceService.isWrapper = true;
      desktopPlayerMock.isFullscreen.and.returnValue(false);
      component.desktopPlayer = {...desktopPlayerMock};
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn())
      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
       const toasterElement = document.createElement('div');
       if (selector === '#toaster') return toasterElement;
     });
      spyOn(component as any,'handleVideoPlayerPlaceholder')
      component['handleDesktopPlayerVisibility']();
      tick(3000);
      expect(component['handleVideoPlayerPlaceholder']).toHaveBeenCalledWith(true, false);
     }));
     it('should call handleVideoPlayerPlaceholder and checkorientation with tutorial player',fakeAsync(()=>{
      component.errorMessage = '';
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      component.showPlayer = true;
      deviceService.isWrapper = true;
      component.desktopPlayer  = {...desktopPlayerMock, isDisposed_ : true};
      desktopPlayerMock.isFullscreen.and.returnValue(false);
      component.tutorialPlayer  = {...desktopPlayerMock};
      windowRefService.nativeWindow.setTimeout.and.callFake(fn => fn())
      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
       const toasterElement = document.createElement('div');
       if (selector === '#toaster') return toasterElement;
     });
      spyOn(component as any,'handleVideoPlayerPlaceholder')
      component['handleDesktopPlayerVisibility']();
      tick(3000);
      expect(component['handleVideoPlayerPlaceholder']).toHaveBeenCalledWith(true, false);
     }));
  });
  describe('handleVideoPlayerPlaceholder',()=>{
    it('should set top bar style if isVideoDisplayed is true and publish',fakeAsync(()=>{
      component.errorMessage = '';
      component.showPlayer = true;
      deviceService.isWrapper = true;
      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      const desktopVideoContainer = document.createElement('div');
      if (selector === '.desktop-video-container') return {desktopVideoContainer,clientHeight:1};
    });
    const nativeVideoContainer = document.createElement('div');
    windowRefService.document.querySelector.and.returnValue(nativeVideoContainer);
     component['handleVideoPlayerPlaceholder'](true);
     tick();
     expect(nativeVideoContainer.style.height).toEqual('1px');
     expect(pubsub.publish).toHaveBeenCalled();
    }));
    it('should set top bar style if isVideoDisplayed is true and publish-iOS',fakeAsync(()=>{
      component.errorMessage = '';
      component.showPlayer = true;
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      const desktopVideoContainer = document.createElement('div');
      if (selector === '.desktop-video-container') return {desktopVideoContainer,clientHeight:1};
    });
    const nativeVideoContainer = document.createElement('div');
    windowRefService.document.querySelector.and.returnValue(nativeVideoContainer);
     component['handleVideoPlayerPlaceholder'](true);
     tick();
     expect(nativeVideoContainer.style.height).toEqual('1px');
     expect(pubsub.publish).toHaveBeenCalled();
    }));
    it('should not set top bar style and publish as mobile in landscape mode',fakeAsync(()=>{
      component.errorMessage = '';
      spyOn(component, 'isLandscapeMode' as any).and.returnValue(true);
      component.showPlayer = true;
      deviceService.isWrapper = true;
      deviceService.isIos = true;
      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
      const desktopVideoContainer = document.createElement('div');
      if (selector === '.desktop-video-container') return {desktopVideoContainer,clientHeight:1};
    });
    const nativeVideoContainer = document.createElement('div');
    windowRefService.document.querySelector.and.returnValue(nativeVideoContainer);
     component['handleVideoPlayerPlaceholder'](true);
     tick();
     expect(pubsub.publish).not.toHaveBeenCalled();
    }));
    it('should set top bar style if isVideoDisplayed is false and publish',fakeAsync(()=>{
      component.errorMessage = '';
      component.showPlayer = true;
      deviceService.isWrapper = true;
      elementRef.nativeElement.querySelector.and.callFake((selector: string) => {
        const desktopVideoContainer = document.createElement('div');
       if (selector === '.desktop-video-container') return {desktopVideoContainer};
     });
     const nativeVideoContainer = document.createElement('div');
     windowRefService.document.querySelector.and.returnValue(nativeVideoContainer);
      component['handleVideoPlayerPlaceholder'](false);
      tick();
      expect(nativeVideoContainer.style.height).toEqual('0px');
      expect(pubsub.publish).toHaveBeenCalled();
     }));
  });
});
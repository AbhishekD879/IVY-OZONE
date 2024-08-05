import { of } from 'rxjs';
import { ConvivaService } from './conviva.service';
import environment from '@environment/oxygenEnvConfig';

describe('ConvivaService', () => {
  let service, asyncScriptLoader, deviceService, userService, windowRef, rendererService;
  let videoAnalytics, eventEntity, Conviva, htmlVideoElement, videoJsPlayer;

  const createService = () => {
    return new ConvivaService(asyncScriptLoader, deviceService, userService, windowRef, rendererService);
  };

  // backup before every environment manipulation! goes with afterAll
  let envBackup;
  beforeAll(() => {
    envBackup = Object.assign({}, environment);
  });

  beforeEach(() => {

    videoAnalytics = {
      setPlayer: jasmine.createSpy('setPlayer'),
      reportPlaybackRequested: jasmine.createSpy('reportPlaybackRequested'),
      reportPlaybackEnded: jasmine.createSpy('reportPlaybackEnded'),
      setContentInfo: jasmine.createSpy('setContentInfo'),
      release: jasmine.createSpy('release'),
    };

    eventEntity = {
      id: 1,
      originalName: 'sportEvent',
      categoryName: 'category',
      typeName: 'league',
      streamProviders: {
        foo: false,
        bar: true,
        zap: true
      }
    };

    Conviva = {
      Constants: {
        GATEWAY_URL: 'GATEWAY_URL',
        LOG_LEVEL: 'LOG_LEVEL',
        STREAM_URL: 'STREAM_URL',
        ASSET_NAME: 'ASSET_NAME',
        PLAYER_NAME: 'PLAYER_NAME',
        IS_LIVE: 'IS_LIVE',
        VIEWER_ID: 'VIEWER_ID',
        LogLevel: {
          DEBUG: 'DEBUG'
        },
        StreamType: {
          LIVE: 'LIVE'
        }
      },
      Analytics: {
        init: jasmine.createSpy('init'),
        buildVideoAnalytics: jasmine.createSpy('buildVideoAnalytics').and.returnValue(videoAnalytics),
        setDeviceMetadata: jasmine.createSpy('setDeviceMetadata')
      }
    };

    htmlVideoElement = {
    } as any;

    videoJsPlayer = {
      currentSrc: jasmine.createSpy('currentSrc').and.returnValue('url'),
      on: jasmine.createSpy('on').and.callFake((event, fn) => {
        videoJsPlayer[event] = fn;
      }),
      off: jasmine.createSpy('off')
    } as any;

    asyncScriptLoader = {
      loadJsFile: jasmine.createSpy('loadJsFile').and.callFake(() => {
        windowRef.nativeWindow.Conviva = Conviva;
        return of('');
      })
    };
    deviceService = {
      isDesktop: false
    };
    userService = {
      username: 'username'
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        navigator: { connection: { effectiveType: '4g' } },
        location: { href: 'url' }
      }
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.callFake((element, event, fn) => {
          element[event] = fn;
          return () => event;
        })
      }
    };
    service = createService();
  });

  describe('preload', () => {
    it('should load conviva library', () => {
      service.preload();
      expect(Conviva.Analytics.init).toHaveBeenCalled();
    });
    it('should die respectively', () => {
      asyncScriptLoader = {
        loadJsFile: jasmine.createSpy('loadJsFile').and.returnValue(of(''))
      };
      windowRef = {
        nativeWindow: {}
      };
      service = createService();
      service.preload();
      expect(Conviva.Analytics.init).not.toHaveBeenCalled();
      expect(service['Analytics']).toBeNull();
    });
  });

  describe('production mode', () => {
    let backup;
    beforeEach(() => {
      backup = environment.production;
      environment.production = true;
    });
    it('should set test mode false', () => {
      service = createService();
      expect(service['testMode']).toBeFalsy();
    });
    afterEach(() => {
      environment.production = backup;
    });
  });

  describe('setConfig', () => {
    it('should setup config', () => {
      service.setConfig({ testMode: false });
      expect(service['testMode']).toEqual(false);
      expect(service['config'].customerKey).toBeDefined();
    });
  });

  describe('initVideoAnalytics', () => {
    beforeEach(() => {
      service.initVideoAnalytics(htmlVideoElement, eventEntity);
    });
    it('should call reportPlaybackRequested', () => {
      expect(htmlVideoElement.play).toEqual(jasmine.any(Function));
      htmlVideoElement.play();
      expect(videoAnalytics.reportPlaybackRequested).toHaveBeenCalled();
    });
    it('should call reportPlaybackEnded', () => {
      htmlVideoElement.ended();
      expect(videoAnalytics.reportPlaybackEnded).toHaveBeenCalled();
    });
    it('should call release', () => {
      service.release(eventEntity.id);
      expect(videoAnalytics.release).toHaveBeenCalled();
    });
    it('should setDeviceMetadata', () => {
      service.setDeviceMetadata({});
      expect(Conviva.Analytics.setDeviceMetadata).toHaveBeenCalled();
    });
  });

  describe('initVideoJsAnalytics', () => {
    beforeEach(() => {
      deviceService.isDesktop = true;
      service.initVideoJsAnalytics(videoJsPlayer, eventEntity);
    });
    it('should call reportPlaybackRequested', () => {
      videoJsPlayer.playing();
      expect(videoAnalytics.reportPlaybackRequested).toHaveBeenCalled();
    });
    it('should call reportPlaybackRequested 2', () => {
      videoJsPlayer.play();
      expect(videoAnalytics.reportPlaybackRequested).toHaveBeenCalled();
    });
    it('should reportPlaybackEnded', () => {
      videoJsPlayer.play();
      videoJsPlayer.ended();
      expect(videoAnalytics.reportPlaybackEnded).toHaveBeenCalled();
    });
    it('should call release', () => {
      videoJsPlayer.play();
      service.release(eventEntity.id);
      expect(videoAnalytics.release).toHaveBeenCalled();
    });
  });

  describe('getContentInfo should generate valid data', () => {
    let expected;
    beforeEach(() => {
      environment.brand = 'bma';
      environment.version = '1.2.3';

      expected = {
        STREAM_URL: 'url',
        ASSET_NAME: '[1] sportEvent',
        PLAYER_NAME: 'Coral Mobile',
        IS_LIVE: 'LIVE',
        VIEWER_ID: 'username',
        isLive: 'true',
        App_Type_Version: '1.2.3',
        Connection_Type: '4g',
        Channel_Type: 'Mobile',
        Sport_Type: 'category',
        League_Type: 'league',
        Event_Streamed: 'sportEvent',
        Brand: 'Coral',
        Page_URL: 'url',
        Stream_Provider: 'bar'
      };
    });

    it('base case', () => {});
    it('desktop', () => {
      deviceService.isDesktop = true;
      deviceService.isAndroid = true;
      deviceService.isIos = true;
      expected.PLAYER_NAME = 'Coral Desktop';
      expected.Channel_Type = 'Desktop';
    });
    it('Android', () => {
      deviceService.isAndroid = true;
      deviceService.isIos = true;
      expected.PLAYER_NAME = 'Coral Android';
    });
    it('iOS', () => {
      deviceService.isIos = true;
      expected.PLAYER_NAME = 'Coral iOS';
    });

    describe('navigator', () => {
      it('does not support connection API)', () => {
        windowRef.nativeWindow.navigator.connection = undefined;
        expected.Connection_Type = 'UNKNOWN';
      });
      it('does not have defined connection.effectiveType property', () => {
        windowRef.nativeWindow.navigator.connection.effectiveType = undefined;
      });
      afterEach(() => {
        expected.Connection_Type = 'UNKNOWN';
      });
    });

    describe('stream provider', () => {
      it('data is not available', () => {
        eventEntity.streamProviders = undefined;
      });
      it('data has no active stream', () => {
        eventEntity.streamProviders.bar = false;
        eventEntity.streamProviders.zap = false;
      });
      afterEach(() => {
        expected.Stream_Provider = 'UNKNOWN';
      });
    });

    it('ladbrokes brand', () => {
      environment.brand = 'ladbrokes';
      expected.PLAYER_NAME = 'Ladbrokes Mobile';
      expected.Brand = 'Ladbrokes';
    });

    afterEach(() => {
      service.initVideoJsAnalytics(videoJsPlayer, eventEntity);
      videoJsPlayer.playing();
      expect(videoAnalytics.reportPlaybackRequested).toHaveBeenCalledWith(expected);
    });
  });

  describe('initAnalytics', () => {
    it('should not call initAnalytics', () => {
      service['initialized'] = true;
      service['testMode'] = false;
      service['initAnalytics']().subscribe(() => {
        expect(Conviva.Analytics.init).not.toHaveBeenCalled();
      });
    });
    it('should call initAnalytics', () => {
      service['initialized'] = false;
      service['testMode'] = false;
      service['initAnalytics']().subscribe(() => {
        expect(Conviva.Analytics.init).toHaveBeenCalled();
      });
    });
  });

  describe('getVideoAnalytics', () => {
    it('should return videoAnalitics instance', () => {
      service.preload();
      const state = {} as any;
      service['getVideoAnalytics'](state);
      expect(state.videoAnalytics).toBeTruthy();
    });
    it('should set player', () => {
      service.preload();
      const state = { player: htmlVideoElement } as any;
      service['getVideoAnalytics'](state);
      expect(state.videoAnalytics).toBeTruthy();
      expect(videoAnalytics.setPlayer).toHaveBeenCalled();
    });
  });

  describe('startReporting', () => {
    it('should not call reportPlaybackRequested', () => {
      service['startReporting']({ requested: true });
      expect(videoAnalytics.reportPlaybackRequested).not.toHaveBeenCalled();
    });
  });

  describe('stopReporting', () => {
    it('should not call reportPlaybackEnded', () => {
      service['stopReporting']({ requested: true });
      expect(videoAnalytics.reportPlaybackEnded).not.toHaveBeenCalled();
    });
  });

  afterAll(() => {
    Object.assign(environment, envBackup);
  });
});


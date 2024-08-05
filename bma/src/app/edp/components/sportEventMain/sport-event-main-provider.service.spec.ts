import { DeviceService } from '@core/services/device/device.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { SportEventMainProviderService } from '@edp/components/sportEventMain/sport-event-main-provider.service';
import { HttpClient } from '@angular/common/http';
import { ISportEvent } from '@core/models/sport-event.model';
import { of as observableOf, of } from 'rxjs';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { fakeAsync, tick } from '@angular/core/testing';
import { IOptaScoreboardConfig } from '@edp/models/opta-scoreboard';
import {
  SPORTBYMAPPING,
  BETRADARBYMAPPING,
  BETRADARDEVICEMAPPING,
  BETRADARNOMAPPING,
  SPORTBYMAPPINGDISABLED,
  CONFIGMAPPINGS,
  IMG_ARENA_BYMAPPING,
  IMG_ARENA_EVENT_NO_BYMAPPING,
  IMG_ARENA_DEVICE_MAPPING
} from './mock/sport-bymapping';

describe('SportEventMainProviderService', () => {
  let service: SportEventMainProviderService;
  let deviceService: DeviceService;
  let asyncScriptLoaderService: AsyncScriptLoaderService;
  let cmsService: CmsService;
  let http: HttpClient;
  let windowRef: WindowRefService;
  let optaScoreboardLoaderService;
  const event: ISportEvent = {
    id: 1
  } as any;

  beforeEach(() => {
    deviceService = {
      requestPlatform: 'mobile',
      strictViewType: 'mobile'
    } as any;
    asyncScriptLoaderService = {
      loadJsFile: jasmine.createSpy('loadJsFile'),
      loadCssFile: jasmine.createSpy('loadCssFile')
    } as any;
    cmsService = {
      getSystemConfig: jasmine.createSpy('get').and.returnValue(observableOf({
        OPTAScoreboard: {
          'mobile': true
        }
      })),
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(observableOf(
        {
          16: true,
          34: false
        }
      ))
    } as any;
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf({})),
      head: jasmine.createSpy('head').and.returnValue(observableOf({})),
    } as any;
    windowRef = {
      document: {
        domain: 'localhost'
      },
      nativeWindow: {
        fetch: () => { },
        EventSource: {},
        customElements: {}
      }
    } as any;

    service = new SportEventMainProviderService(
      windowRef as any,
      http as any,
      deviceService as any,
      asyncScriptLoaderService as any,
      optaScoreboardLoaderService as any,
      cmsService as any
    );

    optaScoreboardLoaderService = {
      loadBundle: jasmine.createSpy('loadBundle').and.returnValue(of({}) as any),
    };

    service['optaConfig'] = {
      apiKeys: 'someApiKey',
      endpoints: {
        bymapping: 'bymapping',
        prematch: 'prematch'
      }
    };
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getConfigForByMapping', () => {
    beforeEach(() => {
      http = {
        get: jasmine.createSpy('get').and.returnValue(observableOf({ SPORTBYMAPPING })),
      } as any;
    });
    it('getConfigForByMapping', fakeAsync(() => {
      spyOn(service as any, 'getConfig').and.returnValue(observableOf(CONFIGMAPPINGS));
      event.categoryId = '59';
      event.id = 14981048;
      event.categoryCode = 'TABLE_TENNIS';
      service['getConfigForByMapping'](event).subscribe();
      tick();
    }));
  });

  describe('#loadBundle', () => {
    it('should try to load js and css bundle', fakeAsync(() => {
      asyncScriptLoaderService.loadJsFile = jasmine.createSpy('loadJsFile').and.returnValue(observableOf(''));
      asyncScriptLoaderService.loadCssFile = jasmine.createSpy('loadCssFile').and.returnValue(observableOf(''));

      service['loadBundle']().subscribe();

      expect(asyncScriptLoaderService.loadJsFile)
        .toHaveBeenCalledWith(`${environment.OPTA_SCOREBOARD.CDN}/scoreboard.bundle.js`);

      expect(asyncScriptLoaderService.loadCssFile)
        .toHaveBeenCalledWith(`${environment.OPTA_SCOREBOARD.CDN}/scoreboard.bundle.css`, true);
    }));
  });

  describe('#getApiKey', () => {
    it('should return correct api key if in config there are several keys mapped to sports', () => {
      const config: IOptaScoreboardConfig = {
        apiKeys: {
          BASKETBALL: 'foo',
          FOOTBALL: 'bar'
        },
        endpoints: {
          bymapping: '',
          prematch: ''
        }
      };

      event.categoryCode = 'BASKETBALL';

      expect(service['getApiKey'](config, event)).toBe('foo');
    });
  });

  describe('#loadConfig', () => {
    it('should return error if there is no opta env config in json', fakeAsync(() => {
      const configJson = {
        environments: {
          'someOtherEnv': {}
        }
      };
      http.get = jasmine.createSpy('get').and.returnValue(observableOf(configJson));
      delete service['optaConfig'];

      service['loadConfig']().subscribe(
        () => { },
        error => {
          expect(error).toBe(`Opta Scoreboard: no config available for environment ${environment.OPTA_SCOREBOARD.ENV}`);
        }
      );
      tick();
    }));

    it('should return and store config if there is opta env config in json', fakeAsync(() => {
      const configJson = {
        environments: {}
      };
      configJson.environments[environment.OPTA_SCOREBOARD.ENV] = { 'foo': 'bar' };
      http.get = jasmine.createSpy('get').and.returnValue(observableOf(configJson));
      delete service['optaConfig'];

      service['loadConfig']().subscribe(
        result => {
          expect(result)
            .toBe(configJson.environments[environment.OPTA_SCOREBOARD.ENV]);
          expect(service['optaConfig'])
            .toBe(configJson.environments[environment.OPTA_SCOREBOARD.ENV]);
        },
      );
      tick();
    }));
  });

  describe('#checkOptaScoreboardAvailability', () => {
    it('should return error if no API key is available for sport', fakeAsync(() => {
      (service['optaConfig'] as any) = {
        apiKeys: {
          'BASKETBALL': 'foobar',
        }
      };
      event.categoryCode = 'FOOTBALL';
      event.categoryId = '16';
      service.checkOptaScoreboardAvailability(event)
        .subscribe(
          () => { },
          err => { expect(err).toBe('Opta Scoreboard: no api key available for 16 (FOOTBALL)'); }
        );
    }));

    it('should return error if no by mapping is provided', fakeAsync(() => {
      (service['getConfigForByMapping'] as any) = jasmine.createSpy('get').and.returnValue(observableOf(
        SPORTBYMAPPINGDISABLED));
      event.categoryId = 'foo';
      event.categoryCode = 'BAR';

      service.checkOptaScoreboardAvailability(event)
        .subscribe(
          () => { },
          err => { expect(err).toBe('Opta Scoreboard Disabled for ByMapping event foo (BAR)'); }
        );

      tick();
    }));

    it('should return error if sport is not supported', fakeAsync(() => {
      (service['getConfigForByMapping'] as any) = jasmine.createSpy('get').and.returnValue(observableOf(
        SPORTBYMAPPING));
      event.categoryId = 'foo';
      event.categoryCode = 'BAR';

      service.checkOptaScoreboardAvailability(event)
        .subscribe(
          () => { },
          err => { expect(err).toBe('Opta Scoreboard Disabled for foo (BAR)'); }
        );

      tick();
    }));

    it('should call head for allowed sport', fakeAsync(() => {
      (service['getConfigForByMapping'] as any) = jasmine.createSpy('get').and.returnValue(observableOf(
        SPORTBYMAPPING));
      event.categoryId = '16';
      event.categoryCode = 'FOOTBALL';

      spyOn(service as any, 'loadPolyfills').and.returnValue(observableOf(true));
      spyOn(service as any, 'loadBundle').and.returnValue(observableOf(true));
      service.checkOptaScoreboardAvailability(event)
        .subscribe();

      expect(cmsService.getFeatureConfig).toHaveBeenCalledWith('ScoreboardsSports');
      expect(http.head).toHaveBeenCalledWith(jasmine.any(String));
    }));

    it('should not call head for disabled sport', fakeAsync(() => {
      (service['getConfigForByMapping'] as any) = jasmine.createSpy('get').and.returnValue(observableOf(
        SPORTBYMAPPING));
      event.categoryId = '34';
      event.categoryCode = 'BASKETBALL';

      service.checkOptaScoreboardAvailability(event)
        .subscribe(null, err => {
          expect(err).toEqual('Opta Scoreboard Disabled for 34 (BASKETBALL)');
        });
      expect(http.head).not.toHaveBeenCalledWith(jasmine.any(String));
    }));

    it('should not call head for desktop', fakeAsync(() => {
      (service['getConfigForByMapping'] as any) = jasmine.createSpy('get').and.returnValue(observableOf(
        SPORTBYMAPPING));
      deviceService.requestPlatform = 'desktop';
      service.checkOptaScoreboardAvailability(event);
      event.categoryId = '16';
      event.categoryCode = 'FOOTBALL';

      deviceService.strictViewType = 'desktop';
      service.checkOptaScoreboardAvailability(event)
        .subscribe(null, err => {
          expect(err).toEqual('Opta Scoreboard Disabled for desktop');
        });

      expect(http.head).not.toHaveBeenCalledWith(jasmine.any(String));
    }));
  });

  describe('#checkBetRadarScoreboardAvailability', () => {
    it('should return error if sport is not supported', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = BETRADARBYMAPPING;
      event.categoryId = 'foo';
      event.categoryCode = 'BAR';

      service.checkBetradarAvailability(event)
        .subscribe(
          () => { },
          err => { expect(err).toBe('Bet Radar Scoreboard Disabled for foo (BAR)'); }
        );
    }));
  });



  describe('#checkBetRadarScoreboardAvailability', () => {
    it('should return bet radar mapping if valid sport is provided', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = BETRADARBYMAPPING;
      event.categoryId = '59';
      event.categoryCode = 'TABLE_TENNIS';

      service.checkBetradarAvailability(event)
        .subscribe(
          (res) => { expect(res).toEqual(BETRADARBYMAPPING[2]); },
          err => { }
        );
    }));
  });


  describe('#checkBetRadarScoreboardAvailability', () => {
    it('should return error if no by mapping is provided', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = undefined;
      event.categoryId = '59';
      event.categoryCode = 'TABLE_TENNIS';

      service.checkBetradarAvailability(event)
        .subscribe(
          (res) => { },
          err => { expect(err).toBe('Unable to fetch BetRadar ByMapping for 59 (TABLE_TENNIS)'); }
        );
    }));
  });

  describe('#checkBetRadarScoreboardAvailability', () => {
    it('should return error if no by provider is provided', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = BETRADARNOMAPPING;
      event.categoryId = '59';
      event.categoryCode = 'TABLE_TENNIS';

      service.checkBetradarAvailability(event)
        .subscribe(
          (res) => { },
          err => { expect(err).toBe('Bet Radar Disabled for ByMapping event 59 (TABLE_TENNIS)'); }
        );
    }));
  });

  describe('#checkBetRadarScoreboardAvailability', () => {
    it('should return error if device is not supported', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = BETRADARDEVICEMAPPING;
      event.categoryId = '59';
      event.categoryCode = 'TABLE_TENNIS';

      service.checkBetradarAvailability(event)
        .subscribe(
          () => { },
          err => { expect(err).toBe('Bet Radar Scoreboard Disabled for mobile'); }
        );
    }));
  });

  describe('#loadPolyfills', () => {
    const cdnURL = environment.OPTA_SCOREBOARD.CDN;

    it('should load polyfills for fetch if not supported by browser', fakeAsync(() => {
      delete windowRef.nativeWindow.fetch;

      service['loadPolyfills']();

      expect(asyncScriptLoaderService.loadJsFile)
        .toHaveBeenCalledWith(`${cdnURL}/polyfill-fetch.js`);
    }));

    it('should load polyfills for EventSource if not supported by browser', fakeAsync(() => {
      delete windowRef.nativeWindow.EventSource;

      service['loadPolyfills']();

      expect(asyncScriptLoaderService.loadJsFile)
        .toHaveBeenCalledWith(`${cdnURL}/polyfill-event-source.js`);
    }));

    it('should load polyfills for webcomponents if customElements is not supported by browser', fakeAsync(() => {
      delete windowRef.nativeWindow.customElements;

      service['loadPolyfills']();

      expect(asyncScriptLoaderService.loadJsFile)
        .toHaveBeenCalledWith(`${cdnURL}/polyfill-webcomponents.js`);
    }));
  });

  describe('#checkImgArenaScoreboardAvailability', () => {

    it('should return error if sport is not supported', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = IMG_ARENA_BYMAPPING;
      event.categoryId = 'foo';
      event.categoryCode = 'BAR';

      service.checkImgArenaScoreboardAvailability(event)
        .subscribe(
          () => { },
          err => { expect(err).toBe('Img Arena Scoreboard Disabled for foo (BAR)'); }
        );
    }));

    it('should return IMG mapping if valid sport (GOLF) is provided', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = IMG_ARENA_BYMAPPING;
      event.categoryId = '18';
      event.categoryCode = 'GOLF';

      service.checkImgArenaScoreboardAvailability(event)
        .subscribe(
          (res) => { expect(res).toEqual(IMG_ARENA_BYMAPPING[1]); },
          err => { }
        );
    }));

    it('should return error if no by mapping is provided', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = undefined;
      event.categoryId = '18';
      event.categoryCode = 'GOLF';

      service.checkImgArenaScoreboardAvailability(event)
        .subscribe(
          (res) => { },
          err => { expect(err).toBe('Unable to fetch Img Arena Scoreboard ByMapping for 18 (GOLF)'); }
        );
    }));

    it('should return error if no by provider is provided', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = IMG_ARENA_EVENT_NO_BYMAPPING;
      event.categoryId = '18';
      event.categoryCode = 'GOLF';

      service.checkImgArenaScoreboardAvailability(event)
        .subscribe(
          (res) => { },
          err => { expect(err).toBe('Img Arena Scoreboard Disabled for ByMapping event 18 (GOLF)'); }
        );
    }));

    it('should return error if device is not supported', fakeAsync(() => {
      (service['sysConfigsWithEventByMapping'] as any) = IMG_ARENA_DEVICE_MAPPING;
      event.categoryId = '18';
      event.categoryCode = 'GOLF';

      service.checkImgArenaScoreboardAvailability(event)
        .subscribe(
          () => { },
          err => { expect(err).toBe('Img Arena Scoreboard Disabled for mobile'); }
        );
    }));

  });
});

import { OptaScoreboardLoaderService } from '@edp/services/optaScoreboard/opta-scoreboard-loader.service';
import { of } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';

describe('OptaScoreboardLoaderService', () => {
  let service: OptaScoreboardLoaderService;
  let windowRef;
  let asyncScriptLoaderService;
  let cdnURL;

  beforeEach(() => {
    cdnURL = environment.OPTA_SCOREBOARD.CDN;

    windowRef = {
      document: { domain: 'domain' },
      nativeWindow: {
        fetch: Symbol('fetch'),
        EventSource: Symbol('fetch'),
        customElements: Symbol('fetch'),
        navigator: {
          userAgent: 'UA'
        }
      }
    };
    asyncScriptLoaderService = {
      loadJsFile: jasmine.createSpy('loadJsFile').and.returnValue(of('js')),
      loadCssFile: jasmine.createSpy('loadCssFile').and.returnValue(of('css'))
    };
    service = new OptaScoreboardLoaderService(windowRef, asyncScriptLoaderService);
  });

  describe('loadBundle', () => {
    let nextSpy, result;
    beforeEach(() => {
      spyOn(service as any, 'loadPolyfills').and.callThrough();
      nextSpy = jasmine.createSpy('next');
    });

    it('should check polyfills necessity and then load scoreboard JS and CSS files', () => {
      result = service.loadBundle();
      expect((service as any).loadPolyfills).toHaveBeenCalled();
      result.subscribe(nextSpy);
      expect(asyncScriptLoaderService.loadJsFile).toHaveBeenCalledWith(`${cdnURL}/scoreboard.bundle.js`);
      expect(asyncScriptLoaderService.loadCssFile).toHaveBeenCalledWith(`${cdnURL}/scoreboard.bundle.css`, true);
      expect(nextSpy).toHaveBeenCalledWith(['js', 'css']);
    });
  });

  describe('loadPolyfills', () => {
    beforeEach(() => {
    });

    it('should load JS polyfills for unsupported features', () => {
      delete windowRef.nativeWindow.fetch;
      delete windowRef.nativeWindow.EventSource;
      delete windowRef.nativeWindow.customElements;
      service.loadBundle();
      expect(asyncScriptLoaderService.loadJsFile.calls.allArgs()).toEqual([
        [`${cdnURL}/polyfill-fetch.js`],
        [`${cdnURL}/polyfill-event-source.js`],
        [`${cdnURL}/polyfill-webcomponents.js`]
      ]);
    });
  });
});

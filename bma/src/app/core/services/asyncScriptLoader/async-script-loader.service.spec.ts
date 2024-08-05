import { of as observableOf } from 'rxjs';
import { AsyncScriptLoaderService } from './async-script-loader.service';
import { concatMap } from 'rxjs/operators';
import { fakeAsync, tick } from '@angular/core/testing';
import environment from "@environment/oxygenEnvConfig";

describe('AsyncScriptLoaderService', () => {
  let service: AsyncScriptLoaderService;
  let windowRef;
  let http;
  let url: string;
  const scripts = [
    { src: "main1.js"},
    { src: "main.js"},
    { src: "ClientDist/main.js"},
  ];
  beforeEach(() => {
    windowRef = {
      document: {
        createElement: jasmine.createSpy('createElement'),
        getElementsByTagName: jasmine.createSpy('createElement'),
        body: {
          appendChild: jasmine.createSpy('appendChild'),
          getElementsByTagName: jasmine.createSpy('createElement').and.returnValue(scripts),
        }
      }
    };
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf(null))
    };
    url = 'https://oxygen-test-lib.com';

    service = new AsyncScriptLoaderService(windowRef, http);
  });

  describe('loadJsFile', () => {
    it('already loaded', () => {
      service['loadedFiles'].set(url, true);
      service.loadJsFile(url);
      expect(windowRef.document.createElement).not.toHaveBeenCalled();
    });

    it('load', fakeAsync(() => {
      const el: any = {};
      windowRef.document.createElement.and.returnValue(el);

      service.loadJsFile(url).subscribe();
      el.onload();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('script');
      expect(service['loadedFiles'].has(url)).toBeTruthy();
    }));

    it('load with attrs (error)', fakeAsync(() => {
      const el: any = {
        setAttribute: jasmine.createSpy('setAttribute')
      };
      windowRef.document.createElement.and.returnValue(el);

      service.loadJsFile(url, { id: '1' }).subscribe({ error: () => {} });
      el.onerror();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('script');
      expect(el.setAttribute).toHaveBeenCalledTimes(1);
      expect(service['loadedFiles'].has(url)).toBeTruthy();
    }));

    it('load with attrs (error) for id name', fakeAsync(() => {
      const el: any = {
        setAttribute: jasmine.createSpy('setAttribute')
      };
      windowRef.document.createElement.and.returnValue(el);

      service.loadJsFile(url, { id: '1' }, 'uid_12').subscribe({ error: () => {} });
      el.onerror();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('script');
      expect(el.setAttribute).toHaveBeenCalledTimes(1);
      expect(service['loadedFiles'].has(url)).toBeTruthy();
      expect(el.id).toBe('uid_12');
    }));
  });

  describe('loadCssFile', () => {
    it('already loaded', () => {
      service['loadedFiles'].set(url, true);
      service.loadCssFile(url);
      expect(windowRef.document.createElement).not.toHaveBeenCalled();
    });

    it('load after target', fakeAsync(() => {
      const el: any = {};
      windowRef.document.createElement.and.returnValue(el);
      windowRef.document.getElementsByTagName.and.returnValue([{
        appendChild: () => {}
      }]);
      spyOn(service, 'tagetedElement').and.returnValue({insertAdjacentElement: (link1, link2) => {return true;}})
      service.loadCssFile(url, true, true).subscribe();
      el.onload();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('link');
    }));
    it('load into head', fakeAsync(() => {
      const el: any = {};
      windowRef.document.createElement.and.returnValue(el);
      windowRef.document.getElementsByTagName.and.returnValue([{
        appendChild: () => {}
      }]);

      service.loadCssFile(url, true).subscribe();
      el.onload();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('link');
      expect(windowRef.document.getElementsByTagName).toHaveBeenCalledWith('head');
      expect(service['loadedFiles'].has(url+'?'+ environment.CSS_Lazy_loadash)).toBeTruthy();
    }));

    it('load into body (error)', fakeAsync(() => {
      const el: any = {};
      windowRef.document.createElement.and.returnValue(el);

      service.loadCssFile(url).subscribe({ error: () => {} });
      el.onerror();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('link');
      expect(windowRef.document.body.appendChild).toHaveBeenCalledTimes(1);
      expect(service['loadedFiles'].has(url+'?'+ environment.CSS_Lazy_loadash)).toBeTruthy();
    }));

    it('should append timestamp when file name is assets-bet-history.css', fakeAsync(() => {
      const el: any = {};
      windowRef.document.createElement.and.returnValue(el);
      windowRef.document.getElementsByTagName.and.returnValue([{
        appendChild: () => {}
      }]);
      spyOn(service, 'tagetedElement').and.returnValue({insertAdjacentElement: (link1, link2) => {return true;}})
      service.loadCssFile('assets-bet-history.css', true, true).subscribe();
      el.onload();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('link');
    }));
    it('should append timestamp when file name is assets-bet-history.css and not proxied', fakeAsync(() => {
      const el: any = {};
      service['isProxiedEnv'] = false;
      windowRef.document.createElement.and.returnValue(el);
      windowRef.document.getElementsByTagName.and.returnValue([{
        appendChild: () => {}
      }]);
      spyOn(service, 'tagetedElement').and.returnValue({insertAdjacentElement: (link1, link2) => {return true;}})
      service.loadCssFile('assets-bet-history.css', true, true).subscribe();
      el.onload();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('link');
    }));
    it('should append timestamp when file name is assets-bet-history1.css and not proxied', fakeAsync(() => {
      const el: any = {};
      service['isProxiedEnv'] = false;
      windowRef.document.createElement.and.returnValue(el);
      windowRef.document.getElementsByTagName.and.returnValue([{
        appendChild: () => {}
      }]);
      spyOn(service, 'tagetedElement').and.returnValue({insertAdjacentElement: (link1, link2) => {return true;}})
      service.loadCssFile('assets-bet-history1.css', true, true).subscribe();
      el.onload();
      tick();

      expect(windowRef.document.createElement).toHaveBeenCalledWith('link');
    }));
  });

  describe('loadSvgIcons', () => {
    it('should load', () => {
      service.loadSvgIcons(url).subscribe(() => {
        expect(http.get).toHaveBeenCalled();
        expect(service['loadedFiles'].get(url)).toBe(true);
      });
    });

    it('should cache', () => {
      service.loadSvgIcons(url)
        .pipe(concatMap(() => service.loadSvgIcons(url)))
        .subscribe(() => {
          expect(http.get).toHaveBeenCalled();
        });
    });

    it('should ignore cache', fakeAsync(() => {
      service.loadSvgIcons(url).subscribe(() => {
        service.loadSvgIcons(url, false);
      });
      tick();

      expect(http.get).toHaveBeenCalledTimes(2);
    }));
  });

  describe('getSvgSprite', () => {
    it('should return sprite', fakeAsync(() => {
      http.get.and.returnValue(observableOf({
        content: 'virtual'
      }));

      service.getSvgSprite('virtual').subscribe((data) => {
        expect(data).toBe('virtual');
      });
      tick();
      expect(http.get).toHaveBeenCalledWith('virtual');
    }));
  });
  describe('getAbsolutePath', () => {
    it('should call with bma and mobile', fakeAsync(() => {
     environment.brand = 'bma';
     environment.CURRENT_PLATFORM = 'mobile';
     expect(service.getAbsolutePath()).toEqual("ClientDist/coralMobile/");
    }));
    it('should call with bma and desktop', fakeAsync(() => {
     environment.brand = 'bma';
     environment.CURRENT_PLATFORM = 'desktop';
     expect(service.getAbsolutePath()).toEqual("ClientDist/coralDesktop/");
    }));
    it('should call with ladbrokes and mobile', fakeAsync(() => {
      environment.brand = 'ladbrokes';
      environment.CURRENT_PLATFORM = 'mobile';
      expect(service.getAbsolutePath()).toEqual("ClientDist/ladbrokesMobile/");
     }));
     it('should call with ladbrokes and desktop', fakeAsync(() => {
      environment.brand = 'ladbrokes';
      environment.CURRENT_PLATFORM = 'desktop';
      expect(service.getAbsolutePath()).toEqual("ClientDist/ladbrokesDesktop/");
     }));
  });
});

import { of as observableOf, throwError } from 'rxjs';
import { ScoreboardComponent } from '@edp/components/scoreboard/scoreboard.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('ScoreboardComponent', () => {
  let component: ScoreboardComponent;

  let pubSubService;
  let asyncScriptLoaderService;
  let windowRefService;
  let elementRef;
  let http;
  let changeDetectorRef;

  const body = {};

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi,
    };
    asyncScriptLoaderService = {
      loadJsFile: jasmine.createSpy('loadJsFile').and.returnValue(observableOf({}))
    };
    windowRefService = {
      nativeWindow: {
        location: {
          protocol: ''
        },
        setInterval: jasmine.createSpy('setInterval').and.callFake(cb => cb && cb()),
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(cb => cb && cb()),
        clearInterval: jasmine.createSpy('clearInterval')
      }
    };
    elementRef = {
      nativeElement: {
        firstChild: {
          hasChildNodes: jasmine.createSpy('hasChildNodes').and.returnValue(true)
        },
        querySelectorAll: jasmine.createSpy('querySelectorAll')
      }
    };
    http = {
      get: jasmine.createSpy('get').and.returnValue(observableOf({ body: body }))
    };

    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new ScoreboardComponent(
      pubSubService,
      asyncScriptLoaderService,
      windowRefService,
      elementRef,
      http,
      changeDetectorRef
    );
  });

  it('onGPScoreboardLoad', () => {
    const htmlElement = document.createElement('script');
    htmlElement.text = 'console.log();';
    const scripts = [htmlElement];
    const hasChildNodes = true;
    spyOn<any>(eval, 'call');
    elementRef.nativeElement.querySelectorAll.and.returnValue([scripts]);
    spyOn(component.isLoaded, 'emit');

    component.onGPScoreboardLoad();

    expect(elementRef.nativeElement.querySelectorAll).toHaveBeenCalledWith('script');
    expect(eval.call).toHaveBeenCalledTimes(scripts.length);
    expect(elementRef.nativeElement.firstChild.hasChildNodes).toHaveBeenCalled();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SCOREBOARD_VISIBILITY, hasChildNodes);
    expect(component.isLoaded.emit).toHaveBeenCalledWith(true);
    expect(component['windowRefService'].nativeWindow.setTimeout).toHaveBeenCalledWith(
      jasmine.any(Function), 500
    );
  });

  it('getGPScoreboard', () => {
    const url = 'score/board/url';
    component['scoreBoardUrl'] = url;

    component.getGPScoreboard().subscribe((result) => {
      expect(result).toBe(body);
    });

    expect(http.get).toHaveBeenCalledWith(url, {
      responseType: 'text',
      observe: 'response'
    });
  });

  describe('loadScoreboard', () => {
    it('loadScoreboard', () => {
      spyOn<any>(component, 'getGPScoreboard').and.returnValue(observableOf(body));
      spyOn<any>(component, 'onGPScoreboardLoad');
      component.loadScoreboard();

      expect(component.getGPScoreboard).toHaveBeenCalled();
      expect(component.onGPScoreboardLoad).toHaveBeenCalled();
    });

    it(`should publish SCOREBOARD_VISUALIZATION_LOADED event`, () => {
      component.loadScoreboard();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
    });

    it(`should emmit isLoaded if Eror`, () => {
      spyOn(component.isLoaded, 'emit');
      spyOn<any>(component, 'getGPScoreboard').and.returnValue(throwError(jasmine.any(Error)));

      component.loadScoreboard();

      expect(component.isLoaded).toBeTruthy();
      expect(component.isLoaded.emit).toHaveBeenCalledWith(true);
      expect(component['windowRefService'].nativeWindow.setTimeout).toHaveBeenCalledWith(
        jasmine.any(Function), 500
      );
    });
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn<any>(component, 'loadScoreboard');
    });

    it('should not load jQuery call loading scoreboard', () => {
      component['windowRefService'].nativeWindow['$'] = () => {
      };
      component.ngOnInit();

      expect(asyncScriptLoaderService.loadJsFile).not.toHaveBeenCalled();
      expect(component.loadScoreboard).toHaveBeenCalled();
    });

    it('should load scoreboard jQuery and call loading scoreboard', () => {
      component.ngOnInit();

      expect(asyncScriptLoaderService.loadJsFile).toHaveBeenCalledWith(component['jqueryUrl']);
      expect(component.loadScoreboard).toHaveBeenCalled();
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalledWith(component['detectListener']);
  });
});

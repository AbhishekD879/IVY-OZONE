import { of } from 'rxjs';
import { BetGeniusScoreboardComponent } from '@edp/components/betGeniusScoreboard/bet-genius-scoreboard.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BetGeniusScoreboardComponent', () => {
  let component: BetGeniusScoreboardComponent;

  let domSanitizer,
    asyncScriptLoaderFactory,
    windowRef,
    hostElement,
    rendererService,
    pubSubService;

  beforeEach(() => {
    domSanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy().and.returnValue('testUrl')
    };
    asyncScriptLoaderFactory = {
      loadJsFile: jasmine.createSpy().and.returnValue(of(null))
    };
    windowRef = {
      nativeWindow: {
        IFrameApi: undefined
      }
    };
    hostElement = {
      nativeElement: {}
    };
    rendererService = {
      renderer: {
        setStyle: jasmine.createSpy('setStyle')
      }
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi,
    };

    component = new BetGeniusScoreboardComponent(
      domSanitizer,
      asyncScriptLoaderFactory,
      windowRef,
      hostElement,
      rendererService,
      pubSubService
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    spyOn<any>(component, 'loadScorecentreApi');
    component.config = {
      available: true,
      eventId: 123
    };

    component.ngOnInit();

    expect(component.adjustScoreboardWidth).toBeDefined();
    expect(component['hideScoreboard']).toBeDefined();
    expect(component.IFRAME_URL).toContain('?eventId=123');
    expect(component.scoreboardUrl).toEqual('testUrl');
    expect(component['loadScorecentreApi']).toHaveBeenCalled();
  });

  describe('handleScoreboardLoad', () => {
    it('should handle loading of scoreboard iframe', () => {
      component['windowRef'].nativeWindow.IFrameApi = jasmine.createSpy('IFrameApi');
      component.handleScoreboardLoad();

      expect(component['windowRef'].nativeWindow.IFrameApi).toHaveBeenCalled();
    });

    it('should Not handle loading of scoreboard iframe', () => {
      component.handleScoreboardLoad();

      expect(component['windowRef'].nativeWindow.IFrameApi).not.toBeDefined();
    });

    it(`should publish SCOREBOARD_VISUALIZATION_LOADED event`, () => {
      component.handleScoreboardLoad();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
    });
  });

  describe('adjustScoreboardWidth', () => {
    it('should adjusts scoreboard iframe width - sets iframe width to current', () => {
      const width = component['hostElement'].nativeElement.offsetWidth;
      component.iframeElement = { nativeElement: null };
      component.adjustScoreboardWidth();

      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(null, 'width', `${width}px`);
    });

    it('should NOT sets iframe width to current', () => {
      component.iframeElement = undefined;
      component.adjustScoreboardWidth();

      expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
    });
  });


  it('should sets config available as true', () => {
    component.config = {
      available: true
    };
    component['hideScoreboard']();

    expect(component.config.available).toBeFalsy();
  });

  describe('loadScorecentreApi', () => {
    beforeEach(() => {
      spyOn<any>(component, 'hideScoreboard');
      component['BET_GENIUS_SCOREBOARD'] = {
        'api': '/some/api/url'
      } as any;
    });

    it('should hide BetGenius scoreboard if scorecentre API failed to load', () => {
      component.iframeElement = undefined;
      component['loadScorecentreApi']();

      expect(asyncScriptLoaderFactory.loadJsFile).toHaveBeenCalledWith(component['BET_GENIUS_SCOREBOARD'].api);
      expect(component['hideScoreboard']).toHaveBeenCalled();
      expect(component.iframeVisible).not.toBeDefined();
    });

    it('should loads BetGenius scorecentre API - sets iframe width to current', () => {
      component.iframeElement = { nativeElement: null };
      spyOn<any>(component, 'adjustScoreboardWidth');

      component['loadScorecentreApi']();

      expect(asyncScriptLoaderFactory.loadJsFile).toHaveBeenCalledWith(component['BET_GENIUS_SCOREBOARD'].api);
      expect(component['hideScoreboard']).not.toHaveBeenCalled();
      expect(component['adjustScoreboardWidth']).toHaveBeenCalled();
      expect(component.iframeVisible).toBeTruthy();
    });
  });
});

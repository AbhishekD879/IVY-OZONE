import { BetRadarProviderComponent } from './bet-radar-provider.component';
import { of } from 'rxjs';

describe('BetRadarProviderComponent', () => {
  let component: BetRadarProviderComponent;
  let ngZone, asyncScriptLoaderFactory, windowRef;
  beforeEach(() => {
    ngZone = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular'),
    };
    windowRef = {
      nativeWindow:  {
        SIR: jasmine.createSpy('nativeWindow.SIR')
      }
    };
    asyncScriptLoaderFactory = {
      loadJsFile: jasmine.createSpy().and.returnValue(of(null))
    };
    component = new BetRadarProviderComponent(
      ngZone,
      windowRef,
      asyncScriptLoaderFactory
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    component.betRadarMatchId = 22392363;
    component.ngOnInit();
    expect(component.showBetRadarLoader).toEqual(false);
  });

  describe('add Bet radar widget', () => {
    beforeEach(() => {
      windowRef = {
        nativeWindow:  {
          SIR: jasmine.createSpy('nativeWindow.SIR')
        }
      };
    });
    it('Sportradar Isomorphic Rendering(SIR) object defined', () => {
      component['addBetRadarWidget']();
      expect(component.showBetRadarLoader).toEqual(false);
    });
  });

  describe('add Bet radar widget', () => {
    beforeEach(() => {
      windowRef = {
        nativeWindow:  {
          SIR: undefined
        }
      };
      ngZone = {
        runOutsideAngular: jasmine.createSpy('runOutsideAngular'),
      };
      asyncScriptLoaderFactory = {
        loadJsFile: jasmine.createSpy().and.returnValue(of(null))
      };
      component = new BetRadarProviderComponent(
        ngZone,
        windowRef,
        asyncScriptLoaderFactory
      );
    });
    it('Sportradar Isomorphic Rendering(SIR) object defined', () => {
      component['addBetRadarWidget']();
      expect(windowRef.nativeWindow.SIR).toBeUndefined();
      expect(component.showBetRadarLoader).toEqual(false);
    });
  });

  describe('loadBetRadarWidget for available Widget License', () => {
    it('Sportradar Isomorphic Rendering(SIR) object defined', () => {
      spyOn<any>(component, 'addBetRadarWidget');
      component['loadBetRadarWidget']();
      expect(component.showBetRadarLoader).toEqual(true);
      expect(component['addBetRadarWidget']).toHaveBeenCalled();
    });
  });


  describe('loadBetRadarWidget for initialising widget loader', () => {
    beforeEach(() => {
      windowRef = {
        nativeWindow:  {
          SIR: undefined
        }
      };
      ngZone = {
        runOutsideAngular: jasmine.createSpy('runOutsideAngular'),
      };
      asyncScriptLoaderFactory = {
        loadJsFile: jasmine.createSpy().and.returnValue(of(null))
      };
      component = new BetRadarProviderComponent(
        ngZone,
        windowRef,
        asyncScriptLoaderFactory
      );
    });
    it('Sportradar Isomorphic Rendering(SIR) object undefined for widget initialisation', () => {
      spyOn<any>(component, 'initWidgetLoader');
      component['loadBetRadarWidget']();
      expect(component.showBetRadarLoader).toEqual(true);
      expect(component['initWidgetLoader']).toHaveBeenCalled();
    });
  });

  describe('ngAfterViewInit', () => {
    it('ngAfterViewInit call for ngZone', () => {
      ngZone.runOutsideAngular.and.callFake(cb => cb());
      spyOn(component as any, 'loadBetRadarWidget').and.callFake(() => jasmine.createSpy());
      component.ngAfterViewInit();
      expect(component['loadBetRadarWidget']).toHaveBeenCalledTimes(1);
    });
  });

  describe('initWidgetLoader', () => {
      beforeEach(() => {
        spyOn<any>(component, 'addBetRadarWidget');
        component['BETRADARURL'] = {
          'api': 'https://widgets.sir.sportradar.com/7a46ac03acda6cd30e5817cf905ae88d/widgetloader'
        } as any;
      });
      it('should call addBetRadarWidget if bet radar api is called', () => {
        component['initWidgetLoader']();
        expect(asyncScriptLoaderFactory.loadJsFile).toHaveBeenCalledWith(component['BETRADARURL'].api);
        expect(component['addBetRadarWidget']).toHaveBeenCalled();
      });
  });

  describe('ngOnDestroy', () => {
    it('#ngOnDestroy asyncLoaderSub', () => {
      component['asyncLoaderSub'] = <any>{
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();
      expect(component['asyncLoaderSub'].unsubscribe).toHaveBeenCalled();
    });
  });
});

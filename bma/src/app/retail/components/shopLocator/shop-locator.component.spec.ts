import { ShopLocatorComponent } from './shop-locator.component';
import { GRID_GA_TRACKING } from '@app/retail/constants/retail.constant';
describe('ShopLocatorComponent', () => {
  let component: ShopLocatorComponent;
  let rendererService;
  let domSanitizer;
  let zone;
  let changeDetector;
  let windowRef;
  let domTools;
  let gtmService;

  beforeEach(() => {
    rendererService = {
      renderer: {
        setStyle: jasmine.createSpy('setStyle')
      }
    };
    domSanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy('bypassSecurityTrustResourceUrl')
    };
    zone = {
      run: jasmine.createSpy('run').and.callFake(cb => {
        cb();
      })
    };
    changeDetector = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(cb => {
          cb();
        }),
        innerHeight: 1000,
        setInterval: jasmine.createSpy('setInterval').and.callFake((fn) => fn && fn()),
        clearInterval: jasmine.createSpy('clearInterval'),
        localStorage: {
          getItem: jasmine.createSpy('getItem').and.returnValue('0'),
          setItem: jasmine.createSpy('setItem')
        },
        navigator:{
          geolocation:{
            getCurrentPosition:jasmine.createSpy('getCurrentPosition')
          }
        },
      }
    };
    domTools = {
      HeaderEl: {
        offsetHeight: 40
      },
      FooterEl: {
        offsetHeight: 40
      }
    };
    gtmService = {
      push: jasmine.createSpy('push'),
      shopLocatorTrack: false
    };
    component = new ShopLocatorComponent(
      rendererService,
      domSanitizer,
      zone,
      changeDetector,
      windowRef,
      domTools,
      gtmService
    );
  });

  describe('#ngOnInit', () => {
    it('Should Start Timer', () => {
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.returnValue('1');
      component['gtmService']['shopLocatorTrack'] = true;
      component.ngOnInit();
      expect(windowRef.nativeWindow.setInterval).toHaveBeenCalledWith(jasmine.any(Function), 1000);
    });

    it('should execute Geolocation onSuccess' , () => {
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.returnValue('1');
      component['gtmService']['shopLocatorTrack'] = true;
      component.trackStatus = false;
      windowRef.nativeWindow.navigator.geolocation.getCurrentPosition = jasmine.createSpy('getCurrentPosition').and.callFake(function() {
        // @ts-ignore
        // eslint-disable-next-line prefer-rest-params
        arguments[0]({coords: { latitude: 1, longitude: 2} });
      });
      component.ngOnInit();
      expect(component.trackStatus).toBe(true);
    });

    it('should execute Geolocation onError' , () => {
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.returnValue('1');
      component['gtmService']['shopLocatorTrack'] = true;
      component.trackStatus = false;
      windowRef.nativeWindow.navigator.geolocation.getCurrentPosition = jasmine.createSpy('getCurrentPosition').and.callFake(function() {
        // @ts-ignore
        // eslint-disable-next-line prefer-rest-params
        arguments[1]({error: 'FAILED'});
      });
      component.ngOnInit();
      expect(component.trackStatus).toBe(true);
    });

    it('should read User Location on allow', ()=> {
      component.trackStatus = false;
      component.trackShopLocatorPermissions('Ok');
      GRID_GA_TRACKING.eventLabel = 'Ok';
      expect(component.trackStatus).toBe(true);
      expect(GRID_GA_TRACKING.eventLabel).toEqual('Ok');
      expect(component['gtmService'].push).toHaveBeenCalledWith('trackEvent', GRID_GA_TRACKING);
    });

    it('should not read User Location on deny', ()=> {
      component.trackStatus = false;
      component.trackShopLocatorPermissions('Dont Allow');
      GRID_GA_TRACKING.eventLabel = 'Dont Allow';
      expect(component.trackStatus).toBe(true);
      expect(GRID_GA_TRACKING.eventLabel).toEqual('Dont Allow');
      expect(component['gtmService'].push).toHaveBeenCalledWith('trackEvent', GRID_GA_TRACKING);
    });

    it('should allow only first time User Location on deny true', ()=> {
      component.trackStatus = true;
      component.trackShopLocatorPermissions('Dont Allow');
    });

    it('should allow only first time User Location on Ok true', ()=> {
      component.trackStatus = true;
      component.trackShopLocatorPermissions('Dont Allow');
    });

    it('localStorage false', () => {
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.returnValue('1');
      component.ngOnInit();
      expect(component.trackStatus).toBe(false);
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(windowRef.nativeWindow.clearInterval).toHaveBeenCalledWith(component['timeInterval']);
  });

  it('ngAfterViewInit', done => {
    component['setShopLocatorHeight'] = jasmine.createSpy('setShopLocatorHeight');
    component.ngAfterViewInit();
    expect(domSanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalled();
    expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
    expect(component['setShopLocatorHeight']).toHaveBeenCalled();
    done();
  });

  it('setShopLocatorHeight', () => {
    component['calcFreeHeight'] = jasmine.createSpy('calcFreeHeight').and.returnValue('500');
    component['shopLocatorView'] = {
      nativeElement: {}
    };
    component['setShopLocatorHeight']();
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(
      jasmine.any(Object),
      'min-height',
      jasmine.any(String)
    );
    expect(component['calcFreeHeight']).toHaveBeenCalled();
  });

  describe('calcFreeHeight', () => {
    beforeEach(() => {
      component['shopLocatorView'] = { nativeElement: { offsetTop: 0 } };
    });

    it('should return height (with footer)', () => {
      expect(component['calcFreeHeight']()).toBe(920);
    });

    it('should return height (without footer)', () => {
      domTools.FooterEl = null;
      expect(component['calcFreeHeight']()).toBe(960);
    });
  });
});

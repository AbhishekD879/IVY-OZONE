import { of, throwError } from 'rxjs';
import { QuantumLeapComponent } from '@racing/components/quantumLeap/quantum-leap.component';
import { fakeAsync, tick } from '@angular/core/testing';
import * as _ from 'underscore';

describe('QuantumLeapComponent', () => {
  let component: QuantumLeapComponent;

  let sanitizer,
    windowRef,
    asyncScriptLoaderService,
    streamTrackingService,
    changeDetectorRef;

  beforeEach(() => {
    sanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    windowRef = {
      nativeWindow: {
        clearInterval: jasmine.createSpy('clearInterval')
      }
    };
    asyncScriptLoaderService = {
      loadJsFile: jasmine.createSpy('loadJsFile').and.returnValue(of({}))
    };
    streamTrackingService = {
      resetTimer: jasmine.createSpy('resetTimer'),
      setTrackingForPlayer: jasmine.createSpy('setTrackingForPlayer')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('changeDetectorRef.detectChanges'),
      detach: jasmine.createSpy('changeDetectorRef.detach')
    };

    component = new QuantumLeapComponent(
      sanitizer,
      windowRef,
      asyncScriptLoaderService,
      streamTrackingService,
      changeDetectorRef
    );
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.spinner = <any>{};
      component.eventEntity = <any>{
        isUKorIRE: true
      };
      spyOn(component, 'initQuantumLeap');
    });

    it('isUKorIRE', () => {
      component.ngOnInit();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.initQuantumLeap).toHaveBeenCalled();
    });

    it('isUKorIRE error', () => {
      asyncScriptLoaderService.loadJsFile.and.returnValue(throwError({}));
      component.ngOnInit();
      expect(component.initQuantumLeap).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should detach change detector and clear tracking interval', () => {
      component.eventEntity = <any>{
        isUKorIRE: false
      };
      windowRef.nativeWindow['_QLGoingDown'] = {};

      component.ngOnInit();
      component.ngOnDestroy();
      expect(changeDetectorRef.detach).toHaveBeenCalled();
      expect(windowRef.nativeWindow.clearInterval).toHaveBeenCalled();
    });

    it('should reset tracking timer', () => {
      windowRef.nativeWindow['_QLGoingDown'] = {
        videoJSplayer: {}
      };
      component['isVideoTracked'] = true;
      component.ngOnDestroy();

      expect(streamTrackingService.resetTimer).toHaveBeenCalled();
    });

    it('should stopLiveSim if _QLGoingDown has needed API', () => {
      const disposeLiveSim = jasmine.createSpy('disposeLiveSim');
      windowRef.nativeWindow['_QLGoingDown'] = {
        videoJSplayer: {
          dispose: disposeLiveSim
        }
      };

      component.ngOnDestroy();

      expect(disposeLiveSim).toHaveBeenCalled();
    });

    it('should stopLiveSim if _QLGoingDown has needed API and catch error', () => {
      const disposeLiveSim = jasmine.createSpy('disposeLiveSim').and.callFake(() => {
        throw new Error('quantum leap 3rdparty error');
      });
      windowRef.nativeWindow['_QLGoingDown'] = {
        videoJSplayer: {
          dispose: disposeLiveSim
        }
      };

      component.ngOnDestroy();

      expect(disposeLiveSim).toHaveBeenCalled();
    });

    it('should NOT call loadScriptSubscription.unsubscribe if loadScriptSubscription is falsy', () => {
      component['loadScriptSubscription'] = null;
      expect(() => component.ngOnDestroy()).not.toThrow();
    });

    describe('initQuantumLeap', () => {
      it('should call populateGoingDown and setObserverForJwPlayer', () => {
        windowRef.nativeWindow['_QLGoingDown'] = {};
        windowRef.nativeWindow._QLGoingDown.populateGoingDown = jasmine.createSpy('populateGoingDown');
        component.setObserverForJwPlayer = jasmine.createSpy('setObserverForJwPlayer');

        component.initQuantumLeap();

        expect(component.setObserverForJwPlayer).toHaveBeenCalled();
        expect(windowRef.nativeWindow._QLGoingDown.populateGoingDown).toHaveBeenCalled();
      });

      it('should NOT do anything if _QLGoingDown is falsy', () => {
        windowRef.nativeWindow['_QLGoingDown'] = null;
        component.setObserverForJwPlayer = jasmine.createSpy('setObserverForJwPlayer');

        component.initQuantumLeap();

        expect(component.setObserverForJwPlayer).not.toHaveBeenCalled();
      });

      it('should log error on console', () => {
        windowRef.nativeWindow['_QLGoingDown'] = {};
        windowRef.nativeWindow._QLGoingDown.populateGoingDown = jasmine.createSpy('populateGoingDown').and.throwError('test');
        component.setObserverForJwPlayer = jasmine.createSpy('setObserverForJwPlayer');
        spyOn(console, 'warn');

        component.initQuantumLeap();

        expect(console.warn).toHaveBeenCalled();
      });
    });

    describe('setObserverForJwPlayer', () => {
      it('should NOT do anything if interval is truthy', () => {
        component['interval'] = true as any;
        windowRef.nativeWindow.setInterval = jasmine.createSpy();

        expect(component.setObserverForJwPlayer()).toBeUndefined();
      });

      it('should NOT do anything if isVideoTracked is truthy', () => {
        component['isVideoTracked'] = true;
        windowRef.nativeWindow.setInterval = jasmine.createSpy();

        expect(component.setObserverForJwPlayer()).toBeUndefined();
      });

      it('should set interval to 50', fakeAsync(() => {
        component['interval'] = false as any;
        component['isVideoTracked'] = false;
        windowRef.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
          callback && callback();
        });

        component.setObserverForJwPlayer();

        expect(windowRef.nativeWindow.setInterval).toHaveBeenCalledWith(jasmine.any(Function), 50, false);
      }));

      it('should call methods with proper args inside if', fakeAsync(() => {
        const eventEntity = <any>{
          id: 1
        };
        const res = {
          id: 2,
          _events: {},
          id_: '2_1'
        };
        component.eventEntity = eventEntity;
        windowRef.nativeWindow['_QLGoingDown'] = {};
        windowRef.nativeWindow['_QLGoingDown']['jwplayer'] = { id: 2 };
        windowRef.nativeWindow['_QLGoingDown']['jwplayer']['_events'] = {};
        windowRef.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
          callback && callback();
        });
        spyOn(_, 'extend').and.callThrough();

        component.setObserverForJwPlayer();
        tick();

        expect(streamTrackingService.setTrackingForPlayer).toHaveBeenCalledWith(res, eventEntity);
        expect(windowRef.nativeWindow.clearInterval).toHaveBeenCalledTimes(1);
        expect(component['isVideoTracked']).toEqual(true);
      }));
    });
  });
});

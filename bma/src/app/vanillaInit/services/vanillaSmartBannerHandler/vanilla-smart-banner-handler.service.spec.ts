import { VanillaSmartBannerHandlerService } from './vanilla-smart-banner-handler.service';

xdescribe('VanillaSmartBannerHandlerService', () => {
  let service,
    windowRef,
    renderer,
    mutationObserverMock;

  beforeEach(() => {
    mutationObserverMock = {
      _callback: (...args) => {},
      observe: jasmine.createSpy('observe'),
      disconnect: jasmine.createSpy('disconnect')
    };

    windowRef = {
      _elementsByClassName: {
        'styleA': [{ tagName: 'elementA1' }, { tagName: 'elementA2' }],
        'styleB': [],
        'styleC': [{ tagName: 'elementC1'}]
      },
      document: {
        head: {
          appendChild: jasmine.createSpy('appendChild')
        },
        querySelector: jasmine.createSpy('querySelector'),
        getElementsByClassName: jasmine.createSpy('getElementsByClassName')
          .and.callFake(className => windowRef._elementsByClassName[className]),
        createElement: jasmine.createSpy('createElement').and.callFake(tagName => ({ tagName }))
      },
      nativeWindow: {
        MutationObserver: jasmine.createSpy('MutationObserverMock').and.callFake( function (cb) {
          mutationObserverMock._callback = cb;
          return mutationObserverMock;
        })
      }
    };

    renderer = {
      _listenersMap: {},
      listen: jasmine.createSpy('listen').and.callFake((element, event, cb) => {
        renderer._listenersMap[event] = cb;
      }),
      removeClass: jasmine.createSpy('removeClass'),
    };

    service = new VanillaSmartBannerHandlerService(windowRef, { renderer });
  });

  it('should init component', () => {
    expect(service).toBeTruthy();
  });

  it('should initialize properties', () => {
    expect(service['mutationObserverConfig']).toEqual({ childList: true });
    expect(service['fixStyleNodes']).toEqual({});
    expect(service['smartBannerBottom']).toEqual(0);
    expect(service['marginTopFixClass']).toEqual('vn-smart-banner-margin-top');
  });

  describe('ngOnDestroy', () => {
    it('should call removeScrollListener', () => {
      spyOn(service as any, 'removeScrollListener').and.callThrough();
      service.ngOnDestroy();
      expect((service as any).removeScrollListener).toHaveBeenCalled();
    });
  });

  describe('init', () => {
    it('should exit if vn-app container is not found', () => {
      windowRef.document.querySelector.and.returnValue(null);
      service.init();
      expect(windowRef.nativeWindow.MutationObserver).not.toHaveBeenCalled();
      expect(mutationObserverMock.observe).not.toHaveBeenCalled();
    });

    describe('if vn-app container exists', () => {
      beforeEach(() => {
        windowRef.document.querySelector.and.returnValues({ tagName: 'vn-app' }, null);
        service.init();
      });

      it('should create MutationObserver', () => {
        expect(windowRef.nativeWindow.MutationObserver).toHaveBeenCalledWith(jasmine.any(Function));
      });

      it('should observe the mutations of vn-app', () => {
        expect(mutationObserverMock.observe).toHaveBeenCalledWith({ tagName: 'vn-app' }, { childList: true });
      });

      describe('when mutations of vn-app occur', () => {
        beforeEach(() => {
          spyOn(service as any, 'initSmartBannerTracking').and.callThrough();
        });
        describe('when mutation list is not empty', () => {
          beforeEach(() => {
            mutationObserverMock._callback([{ addedNodes: [], removedNodes: [] }, {}]);
          });
          it('should init tracking', () => {
            expect((service as any).initSmartBannerTracking).toHaveBeenCalled();
          });
          it('should disconnect from MutationObserver', () => {
            expect(mutationObserverMock.disconnect).toHaveBeenCalled();
          });
        });

        describe('should do nothing', () => {
          it('when mutation list is empty', () => {
            mutationObserverMock._callback([]);
          });
          it('when mutation list is not provided', () => {
            mutationObserverMock._callback(undefined);
          });
          afterEach(() => {
            expect((service as any).initSmartBannerTracking).not.toHaveBeenCalled();
            expect(mutationObserverMock.disconnect).not.toHaveBeenCalled();
          });
        });
      });
    });

    afterEach(() => {
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('vn-app');
    });
  });

  describe('initSmartBannerTracking', () => {
    it('should exit if vn-smart-banner container is not found', () => {
      windowRef.document.querySelector.and.returnValue(null);
      (service as any).initSmartBannerTracking();
      expect((service as any).vnSmartBanner).toEqual(null);
      expect(windowRef.nativeWindow.MutationObserver).not.toHaveBeenCalled();
      expect(mutationObserverMock.observe).not.toHaveBeenCalled();
    });

    describe('if vn-smart-banner container exists', () => {
      let smartBanner;
      beforeEach(() => {
        smartBanner = { getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({ bottom: 0 }) };
        windowRef.document.querySelector.and.returnValue(smartBanner);
        (service as any).initSmartBannerTracking();
      });

      it('should save vnSmartBanner reference', () => {
        expect((service as any).vnSmartBanner).toEqual(smartBanner);
      });
      it('should create MutationObserver', () => {
        expect(windowRef.nativeWindow.MutationObserver).toHaveBeenCalledWith(jasmine.any(Function));
      });

      it('should observe the mutations of vn-smart-banner', () => {
        expect(mutationObserverMock.observe).toHaveBeenCalledWith(smartBanner, { childList: true });
      });

      describe('when mutations of vn-smart-banner occur', () => {
        beforeEach(() => {
          spyOn(service as any, 'toggleSmartBannerFix').and.callThrough();
          spyOn(service as any, 'initScrollListener').and.callThrough();
          spyOn(service as any, 'cleanUpFixes').and.callThrough();
          spyOn(service as any, 'removeScrollListener').and.callThrough();
        });

        describe('should do nothing', () => {
          it('when mutation list is empty', () => {
            mutationObserverMock._callback([]);
          });
          it('when mutation list is not provided', () => {
            mutationObserverMock._callback(undefined);
          });
          it('when addedNodes and removedNodes properties of first mutation object are empty', () => {
            mutationObserverMock._callback([{ addedNodes: [], removedNodes: [] }, {}]);
          });
          afterEach(() => {
            expect((service as any).toggleSmartBannerFix).not.toHaveBeenCalled();
            expect((service as any).initScrollListener).not.toHaveBeenCalled();
            expect((service as any).cleanUpFixes).not.toHaveBeenCalled();
            expect((service as any).removeScrollListener).not.toHaveBeenCalled();
            expect(mutationObserverMock.disconnect).not.toHaveBeenCalled();
          });
        });

        describe('when first mutation in list is not empty', () => {
          describe('should toggle smart banner fix and init scroll listener', () => {
            it('and has non-empty addedNodes property ', () => {
              mutationObserverMock._callback([{ addedNodes: [ {} ] }]);
            });
            it('and has non-empty addedNodes property (with removedNodes present)', () => {
              mutationObserverMock._callback([{ addedNodes: [ {} ], removedNodes: [ {} ] }]);
            });
            afterEach(() => {
              expect((service as any).toggleSmartBannerFix).toHaveBeenCalled();
              expect((service as any).initScrollListener).toHaveBeenCalled();
              expect((service as any).cleanUpFixes).not.toHaveBeenCalled();
              expect((service as any).removeScrollListener).not.toHaveBeenCalled();
              expect(mutationObserverMock.disconnect).not.toHaveBeenCalled();
            });
          });

          describe('should clean-up fixes, disconnect observer and remove scroll listener', () => {
            it('and has non-empty removedNodes property, while addedNodes is empty)', () => {
              mutationObserverMock._callback([{ addedNodes: [], removedNodes: [ {} ] }]);
              expect((service as any).toggleSmartBannerFix).not.toHaveBeenCalled();
              expect((service as any).initScrollListener).not.toHaveBeenCalled();
              expect((service as any).cleanUpFixes).toHaveBeenCalled();
              expect((service as any).removeScrollListener).toHaveBeenCalled();
              expect(mutationObserverMock.disconnect).toHaveBeenCalled();
            });
          });
        });
      });
    });

    afterEach(() => {
      expect(windowRef.document.querySelector).toHaveBeenCalledWith('vn-smart-banner');
    });
  });

  describe('toggleSmartBannerFix', () => {
    let smartBanner, clientRectMock;
    beforeEach(() => {
      spyOn(service as any, 'applyMarginTopFix').and.callThrough();
      spyOn(service as any, 'applyStyleFix').and.callThrough();
      clientRectMock = { bottom: 10 };
      smartBanner = { getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue(clientRectMock) };
      (service as any).vnSmartBanner = smartBanner;
      (service as any).smartBannerBottom = 10;
    });
    it('should get bottom of vn-smart-banner', () => {
      (service as any).toggleSmartBannerFix();
      expect(smartBanner.getBoundingClientRect).toHaveBeenCalled();
    });

    describe('should do nothing if vnSmartBanner.bottom value did not change', () => {
      it('(bottom > 0)', () => {});
      it('(bottom === 0)', () => {
        clientRectMock.bottom = 0;
        (service as any).smartBannerBottom = 0;
      });
      it('(bottom < 0)', () => {
        clientRectMock.bottom = -10;
        (service as any).smartBannerBottom = 0;
      });

      afterEach(() => {
        (service as any).toggleSmartBannerFix();
        expect((service as any).applyMarginTopFix).not.toHaveBeenCalled();
      });
    });

    it('should call applyMarginTopFix and save bottom value if vnSmartBanner.bottom value did change', () => {
      clientRectMock.bottom = 20;
      (service as any).toggleSmartBannerFix();
      expect((service as any).applyMarginTopFix).toHaveBeenCalledWith(20);
      expect((service as any).applyStyleFix).toHaveBeenCalledWith('vn-smart-banner-margin-top',
        '.vn-smart-banner-margin-top { margin-top: 20px; } .vn-smart-banner-margin-top .modal { padding-top: 20px; }');
      expect((service as any).smartBannerBottom).toEqual(20);
    });
  });

  describe('applyStyleFix', () => {
    let styleA;

    beforeEach(() => {
      styleA = { innerHTML: '.styleA {}' };
      service['fixStyleNodes'] = { styleA };
    });

    it('should update existing style node if it is already created for given classname', () => {
      service['applyStyleFix']('styleA', '.styleA { display: none; }');
      expect(styleA.innerHTML).toEqual('.styleA { display: none; }');
      expect(windowRef.document.head.appendChild).not.toHaveBeenCalled();
      expect(windowRef.document.createElement).not.toHaveBeenCalled();
      expect(service['fixStyleNodes']).toEqual( { styleA: { innerHTML: '.styleA { display: none; }' } });
    });

    it('should create and append to head new style node if it is not created yet for given classname', () => {
      service['applyStyleFix']('styleB', '.styleB {}');
      expect(windowRef.document.createElement).toHaveBeenCalledWith('style');
      expect(windowRef.document.head.appendChild).toHaveBeenCalledWith({ tagName: 'style', innerHTML: '.styleB {}' });
      expect(service['fixStyleNodes']).toEqual(
        { styleA: { innerHTML: '.styleA {}' }, styleB: { tagName: 'style', innerHTML: '.styleB {}' } });
    });
  });

  describe('cleanUpFixes', () => {
    describe('should iterate over fix style nodes map and for each node', () => {
      let styleA, styleB, styleC,
        removeChildA, removeChildB;

      beforeEach(() => {
        removeChildA = jasmine.createSpy('removeChildA');
        removeChildB = jasmine.createSpy('removeChildB');
        styleA = { parentNode: { removeChild: removeChildA }, innerHTML: '.styleA {}' };
        styleB = { parentNode: { removeChild: removeChildB }, innerHTML: '.styleB {}' };
        styleC = { innerHTML: '.styleC {}' };
        service['fixStyleNodes'] = { styleA, styleB, styleC };
        service['cleanUpFixes']();
      });

      it('and find elements with corresponding class names', () => {
        expect(windowRef.document.getElementsByClassName).toHaveBeenCalledWith('styleA');
        expect(windowRef.document.getElementsByClassName).toHaveBeenCalledWith('styleB');
        expect(windowRef.document.getElementsByClassName).toHaveBeenCalledWith('styleC');
      });

      it('and remove class from all found elements', () => {
        expect(renderer.removeClass).toHaveBeenCalledWith({ tagName: 'elementA1' }, 'styleA');
        expect(renderer.removeClass).toHaveBeenCalledWith({ tagName: 'elementA2' }, 'styleA');
        expect(renderer.removeClass).not.toHaveBeenCalledWith(jasmine.anything(), 'styleB');
        expect(renderer.removeClass).toHaveBeenCalledWith({ tagName: 'elementC1' }, 'styleC');
      });

      it('and remove style nodes from DOM and empty its innerHTML', () => {
        expect(removeChildA).toHaveBeenCalledWith(styleA);
        expect(removeChildB).toHaveBeenCalledWith(styleB);
        expect(styleA.innerHTML).toEqual('');
        expect(styleB.innerHTML).toEqual('');
        expect(styleC.innerHTML).toEqual('');
      });
    });
  });

  describe('initScrollListener', () => {
    it('should create subscription to scroll event', () => {
      const unsubscribeSpy = jasmine.createSpy('unsubscriber');
      renderer.listen.and.returnValue(unsubscribeSpy);
      service['initScrollListener']();
      service['scrollListener']();
      expect(unsubscribeSpy).toHaveBeenCalled();
    });
    it('on scroll event should call toggleSmartBannerFix with true parameter', () => {
      spyOn(service as any, 'toggleSmartBannerFix');
      service['initScrollListener']();
      renderer._listenersMap['scroll']();
      expect((service as any).toggleSmartBannerFix).toHaveBeenCalled();
    });
    afterEach(() => {
      expect(renderer.listen).toHaveBeenCalledWith(windowRef.nativeWindow, 'scroll', jasmine.any(Function));
    });
  });

  describe('removeScrollListener', () => {
    it('should do nothing if scrollListener is not defined', () => {
      const callSpy = jasmine.createSpy('call'),
        getSpy = jasmine.createSpy('getter').and.returnValues(null, callSpy);
      Object.defineProperty(service, 'scrollListener', { get: getSpy });
      (service as any).removeScrollListener();
      expect(getSpy).toHaveBeenCalledTimes(1);
      expect(callSpy).not.toHaveBeenCalled();
    });
    it('should call scrollListener unsubscriber if defined', () => {
      (service as any).scrollListener = jasmine.createSpy('scrollListener');
      (service as any).removeScrollListener();
      expect((service as any).scrollListener).toHaveBeenCalled();
    });
  });
});

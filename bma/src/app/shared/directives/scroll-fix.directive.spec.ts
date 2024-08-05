import { ScrollFixDirective } from '@shared/directives/scroll-fix.directive';

describe('ScrollFixDirective', () => {
  let directive: ScrollFixDirective;
  let windowRef;
  let deviceService;
// eslint-disable-next-line max-len
const mockOverlayClass = `.football-content-overlay, .quickbet-opened, .fiveasideentry-content-overlay, .fiveasideentry-rules-overlay, .fiveaside-cards-overlay, .fiveaside-lobby-overlay`;
// eslint-disable-next-line max-len
const mockScrollableClass = `.scrollable-content, #football-tutorial-overlay, #fiveaside-entry-overlay, #fiveaside-terms-rules, #fiveaside-welcome-overlay, #fiveaside-lobby-tutorial`;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        _listenCbMap: {},
        addEventListener: jasmine.createSpy('addEventListener').and.callFake((event, cb) => {
          windowRef.nativeWindow._listenCbMap[event] = cb;
        }),
        removeEventListener: jasmine.createSpy('removeEventListener')
      },
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue(null)
      }
    };
    deviceService = {
      isIos: true
    };
    directive = new ScrollFixDirective(windowRef, deviceService);
  });

  describe('constructor', () => {
    it('should initialize properties', () => {
      expect(directive.touchYPos).toEqual(null);
      expect(directive.options).toEqual({
        overlayOpenedClass: mockOverlayClass,
        scrollableClass: mockScrollableClass
      });
    });
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      spyOn(directive as any, 'touchHandler');
    });
    describe('if device is iOS', () => {
      it('should add listeners to touch events', () => {
        directive.ngOnInit();
        expect(windowRef.nativeWindow.addEventListener.calls.allArgs()).toEqual([
          ['touchstart', (directive as any).touchHandler],
          ['touchmove', (directive as any).touchHandler]
        ]);
      });
      it('should call handlers on touch events', () => {
        directive.ngOnInit();
        windowRef.nativeWindow._listenCbMap['touchstart']('touchstart event');
        windowRef.nativeWindow._listenCbMap['touchmove']('touchmove event');
        expect((directive as any).touchHandler.calls.allArgs()).toEqual([
          ['touchstart event'],
          ['touchmove event']
        ]);
      });
    });
    it('should not add listeners to touch events if device is not iOS', () => {
      deviceService.isIos = false;
      directive.ngOnInit();
      expect(windowRef.nativeWindow.addEventListener).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should remove event listeners', () => {
      directive.ngOnDestroy();
      expect(windowRef.nativeWindow.removeEventListener.calls.allArgs()).toEqual([
        ['touchstart', (directive as any).touchHandler],
        ['touchmove', (directive as any).touchHandler]
      ]);
    });
  });

  describe('event handling', () => {
    let event;

    beforeEach(() => {
      event = {
        touches: [{ pageY: 100 }],
        preventDefault: jasmine.createSpy('preventDefault')
      };
    });

    describe('getYpos', () => {
      it('should return provided event.touches[0].pageY property value, if available', () => {
        expect((directive as any).getYpos(event)).toEqual(100);
      });
      describe('should return undefined', () => {
        it('if provided event.touches[0] has no pageY property', () => { delete event.touches[0].pageY; });
        it('if provided event.touches array is empty', () => { event.touches = []; });
        it('if provided event does not have touches property', () => { delete event.touches; });
        it('if event is not provided', () => { event = undefined; });
        afterEach(() => { expect((directive as any).getYpos(event)).toEqual(undefined); });
      });
    });

    describe('touchHandler', () => {
      beforeEach(() => {
        spyOn(directive as any, 'isOverlayOpened');
        spyOn(directive as any, 'getYpos');
        spyOn(directive as any, 'getScrollableContainer');
      });
      it('should return immediately if overlay is not opened', () => {
        (directive as any).isOverlayOpened.and.returnValue(false);
        (directive as any).touchHandler(event);
        expect((directive as any).isOverlayOpened).toHaveBeenCalled();
        expect((directive as any).getYpos).not.toHaveBeenCalled();
        expect((directive as any).getScrollableContainer).not.toHaveBeenCalled();
      });

      describe('when overlay is open it should get event.touch[0].pageY position and scrollable container element reference', () => {
        beforeEach(() => {
          (directive as any).isOverlayOpened.and.returnValue(true);
          (directive as any).getYpos.and.returnValue(100);
          (directive as any).getScrollableContainer.and.returnValue(null);
          directive.touchYPos = 110;
        });

        it('and on touchstart event should only update touchYPos property', () => {
          event.type = 'touchstart';
          (directive as any).touchHandler(event);
          expect(directive.touchYPos).toEqual(100);
          expect(event.preventDefault).not.toHaveBeenCalled();
          expect((directive as any).getScrollableContainer).not.toHaveBeenCalled();
        });

        describe('and on touchmove event it should not update touchYPos property', () => {
          let container;

          beforeEach(() => {
            event.type = 'touchmove';
            container = {
              classList: [],
              scrollTop: 20,
              scrollHeight: 150,
              offsetHeight: 100
            };
            (directive as any).getScrollableContainer.and.returnValue(container);
          });

          it('and not call event.preventDefault if scrollable container is available and no preventing conditions are met', () => {
            // isPreventScrollClassPresent = isTouchedTop = isScrolledToBottom = false
            (directive as any).touchHandler(event);
            expect(event.preventDefault).not.toHaveBeenCalled();
          });

          describe('and call event.preventDefault', () => {
            it('when container is unavailable', () => {
              (directive as any).getScrollableContainer.and.returnValue(null);
            });
            it('when container has "prevented-container" class', () => {
              container.classList = ['prevented-container'];
            });

            describe('when isTouchedTop (touchY - this.touchYPos > 0)', () => {
              beforeEach(() => { (directive as any).getYpos.and.returnValue(110); });
              it('when container.scrollTop === 0', () => { container.scrollTop = 0; });
              it('when container.scrollTop < 0', () => { container.scrollTop = -10; });
            });

            describe('when isTouchedTop (touchY - this.touchYPos === 0)', () => {
              beforeEach(() => { (directive as any).getYpos.and.returnValue(120); });
              it('when container.scrollTop === 0', () => { container.scrollTop = 0; });
              it('when container.scrollTop < 0', () => { container.scrollTop = -10; });
            });

            describe('when container is scrolled to bottom', () => {
              it(' (container.scrollTop < container.scrollHeight - container.offsetHeight)', () => { container.scrollHeight = 110; });
              it(' (container.scrollTop === container.scrollHeight - container.offsetHeight)', () => { container.scrollHeight = 120; });
            });
            afterEach(() => {
              (directive as any).touchHandler(event);
              expect(event.preventDefault).toHaveBeenCalled();
            });
          });

          afterEach(() => {
            expect(directive.touchYPos).toEqual(110);
            expect((directive as any).getScrollableContainer).toHaveBeenCalled();
          });
        });

        afterEach(() => {
          expect((directive as any).getYpos).toHaveBeenCalledWith(event);
        });
      });
    });

    describe('isOverlayOpened', () => {
      it('should return false if overlayOpenedClass element does not exist in DOM', () => {
        expect((directive as any).isOverlayOpened()).toEqual(false);
      });
      it('should return true if overlayOpenedClass element exists in DOM', () => {
        windowRef.document.querySelector.and.returnValue({ tagName: 'element' });
        expect((directive as any).isOverlayOpened()).toEqual(true);
      });
      afterEach(() => {
        expect(windowRef.document.querySelector).toHaveBeenCalledWith(mockOverlayClass);
      });
    });

    describe('getScrollableContainer', () => {
      it('should return scrollableClass element', () => {
        windowRef.document.querySelector.and.returnValue({ tagName: 'element' });
        expect((directive as any).getScrollableContainer()).toEqual({ tagName: 'element' });
        expect(windowRef.document.querySelector)
          .toHaveBeenCalledWith(mockScrollableClass);
      });
    });
  });
});

import { OverscrollFixDirective } from '@shared/directives/overscroll-fix';

describe('OverscrollFixDirective', () => {
  let directive: OverscrollFixDirective;
  let renderer;
  let nativeElement;

  beforeEach(() => {
    renderer = {
      _listenCbMap: {},
      _unsubscribeSpyMap: {},
      listen: jasmine.createSpy('listen').and.callFake((el, event, cb) => {
        renderer._listenCbMap[event] = cb;
        renderer._unsubscribeSpyMap[event] = jasmine.createSpy();
        return renderer._unsubscribeSpyMap[event];
      })
    };
    nativeElement = {
      scrollTop: 0,
      scrollHeight: 100,
      clientHeight: 100
    };
    directive = new OverscrollFixDirective({ renderer }, { nativeElement });
  });

  describe('ngOnInit', () => {
    it('should assign reference to element', () => {
      expect((directive as any).element).toEqual(undefined);
      directive.ngOnInit();
      expect((directive as any).element).toBe(nativeElement);
    });

    describe('should create event listeners to mouse events', () => {
      it('and save the unsubscription functions to the corresponding properties', () => {
        expect((directive as any).touchStartListener).toEqual(undefined);
        expect((directive as any).touchMoveListener).toEqual(undefined);
        expect((directive as any).wheelMoveListener).toEqual(undefined);
        directive.ngOnInit();
        expect((directive as any).touchStartListener).toEqual(renderer._unsubscribeSpyMap['touchstart']);
        expect((directive as any).touchMoveListener).toEqual(renderer._unsubscribeSpyMap['touchmove']);
        expect((directive as any).wheelMoveListener).toEqual(renderer._unsubscribeSpyMap['wheel']);
      });

      it('should execute handlers on those events', () => {
        spyOn(directive as any, 'touchStartHandler').and.stub();
        spyOn(directive as any, 'touchMoveHandler').and.stub();
        spyOn(directive as any, 'wheelHandler').and.stub();
        directive.ngOnInit();
        renderer._listenCbMap['touchstart']('touchstart event');
        expect((directive as any).touchStartHandler).toHaveBeenCalledWith('touchstart event');
        renderer._listenCbMap['touchmove']('touchmove event');
        expect((directive as any).touchMoveHandler).toHaveBeenCalledWith('touchmove event');
        renderer._listenCbMap['wheel']('wheel event');
        expect((directive as any).wheelHandler).toHaveBeenCalledWith('wheel event');
      });

      afterEach(() => {
        expect(renderer.listen.calls.allArgs()).toEqual([
          [nativeElement, 'touchstart', (directive as any).touchStartHandler],
          [nativeElement, 'touchmove', (directive as any).touchMoveHandler],
          [nativeElement, 'wheel', (directive as any).wheelHandler]
        ]);
      });
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe from event listeners', () => {
      directive.ngOnInit();
      directive.ngOnDestroy();
      expect(renderer._unsubscribeSpyMap['touchstart']).toHaveBeenCalled();
      expect(renderer._unsubscribeSpyMap['touchmove']).toHaveBeenCalled();
      expect(renderer._unsubscribeSpyMap['wheel']).toHaveBeenCalled();
    });
  });

  describe('event handling', () => {
    let event;

    beforeEach(() => {
      event = {
        touches: [{ clientY: 100 }],
        preventDefault: jasmine.createSpy('preventDefault')
      };
    });

    describe('shouldBePrevented', () => {
      beforeEach(() => {
        directive.overscrollFix = undefined;
        (directive as any).element = { style: {} };
      });
      it('should return false if element does not have fixed position and overscrollFix input is not provided as "always"', () => {
        expect((directive as any).shouldBePrevented()).toEqual(false);
      });
      describe('should return true', () => {
        it('if overscrollFix input is set to "always"', () => directive.overscrollFix = 'always');
        it('if element has CSS fixed position', () => (directive as any).element.style.position = 'fixed');
        afterEach(() => {
          expect((directive as any).shouldBePrevented()).toEqual(true);
        });
      });
    });

    describe('getTouchY', () => {
      it('should return provided event.touches[0].clientY property value, if available', () => {
        expect((directive as any).getTouchY(event)).toEqual(100);
      });
      describe('should return 0', () => {
        it('if provided event.touches[0] has no clientY property', () => { delete event.touches[0].clientY; });
        it('if provided event.touches array is empty', () => { event.touches = []; });
        it('if provided event does not have touches property', () => { delete event.touches; });
        it('if event is not provided', () => { event = null; });
        afterEach(() => {
          expect((directive as any).getTouchY(event)).toEqual(0);
        });
      });
    });

    describe('hasScrollableContent', () => {
      let targetElement, parentElement;
      beforeEach(() => {
        spyOn(directive as any, 'hasScrollableContent').and.callThrough();
        (directive as any).element = nativeElement;
        parentElement = { parentElement: nativeElement, scrollHeight: 90, clientHeight: 100 };
        targetElement = { parentElement, scrollHeight: 100, clientHeight: 100 };
      });

      it('should return false and exit recursion when the base element and its children up from target are not scrollable', () => {
        expect((directive as any).hasScrollableContent(targetElement)).toEqual(false);
        expect((directive as any).hasScrollableContent.calls.allArgs()).toEqual([
          [targetElement], [parentElement], [nativeElement]
        ]);
      });
      describe('should return true and exit recursion as soon as scrollable element is found', () => {
        beforeEach(() => {
          nativeElement.scrollHeight = 110;
        });
        it('when base element is scrollable', () => {
          expect((directive as any).hasScrollableContent(targetElement)).toEqual(true);
          expect((directive as any).hasScrollableContent.calls.allArgs()).toEqual([[targetElement], [parentElement], [nativeElement]]);
        });
        it('when base element child is scrollable', () => {
          parentElement.scrollHeight = 110;
          expect((directive as any).hasScrollableContent(targetElement)).toEqual(true);
          expect((directive as any).hasScrollableContent.calls.allArgs()).toEqual([[targetElement], [parentElement]]);
        });
        it('when base element grandchild is scrollable', () => {
          targetElement.scrollHeight = 110;
          expect((directive as any).hasScrollableContent(targetElement)).toEqual(true);
          expect((directive as any).hasScrollableContent.calls.allArgs()).toEqual([[targetElement]]);
        });
      });
    });

    describe('isScrollableDown', () => {
      let targetElement, parentElement;
      beforeEach(() => {
        spyOn(directive as any, 'isScrollableDown').and.callThrough();
        (directive as any).element = nativeElement;
        parentElement = { parentElement: nativeElement, scrollHeight: 100, clientHeight: 100, scrollTop: 10 };
        targetElement = { parentElement, scrollHeight: 110, clientHeight: 100, scrollTop: 10 };
      });

      it('should return false and exit recursion when the base element and its children up from target are not scrollable down', () => {
        expect((directive as any).isScrollableDown(targetElement)).toEqual(false);
        expect((directive as any).isScrollableDown.calls.allArgs()).toEqual([
          [targetElement], [parentElement], [nativeElement]
        ]);
      });
      describe('should return true and exit recursion as soon as scrollable down element is found', () => {
        beforeEach(() => {
          nativeElement.scrollHeight = 110;
        });
        it('when base element is scrollable down', () => {
          expect((directive as any).isScrollableDown(targetElement)).toEqual(true);
          expect((directive as any).isScrollableDown.calls.allArgs()).toEqual([[targetElement], [parentElement], [nativeElement]]);
        });
        it('when base element child is scrollable down', () => {
          parentElement.scrollHeight = 120;
          expect((directive as any).isScrollableDown(targetElement)).toEqual(true);
          expect((directive as any).isScrollableDown.calls.allArgs()).toEqual([[targetElement], [parentElement]]);
        });
        it('when base element grandchild is scrollable down', () => {
          targetElement.scrollHeight = 120;
          expect((directive as any).isScrollableDown(targetElement)).toEqual(true);
          expect((directive as any).isScrollableDown.calls.allArgs()).toEqual([[targetElement]]);
        });
      });
    });

    describe('isScrollableUp', () => {
      let targetElement, parentElement;
      beforeEach(() => {
        spyOn(directive as any, 'isScrollableUp').and.callThrough();
        (directive as any).element = nativeElement;
        parentElement = { parentElement: nativeElement, scrollTop: 0 };
        targetElement = { parentElement, scrollTop: 0 };
      });

      it('should return false and exit recursion when the base element and its children up from target are not scrollable up', () => {
        expect((directive as any).isScrollableUp(targetElement)).toEqual(false);
        expect((directive as any).isScrollableUp.calls.allArgs()).toEqual([
          [targetElement], [parentElement], [nativeElement]
        ]);
      });
      describe('should return true and exit recursion as soon as scrollable up element is found', () => {
        beforeEach(() => {
          nativeElement.scrollTop = 10;
        });
        it('when base element is scrollable up', () => {
          expect((directive as any).isScrollableUp(targetElement)).toEqual(true);
          expect((directive as any).isScrollableUp.calls.allArgs()).toEqual([[targetElement], [parentElement], [nativeElement]]);
        });
        it('when base element child is scrollable up', () => {
          parentElement.scrollTop = 10;
          expect((directive as any).isScrollableUp(targetElement)).toEqual(true);
          expect((directive as any).isScrollableUp.calls.allArgs()).toEqual([[targetElement], [parentElement]]);
        });
        it('when base element grandchild is scrollable up', () => {
          targetElement.scrollTop = 10;
          expect((directive as any).isScrollableUp(targetElement)).toEqual(true);
          expect((directive as any).isScrollableUp.calls.allArgs()).toEqual([[targetElement]]);
        });
      });
    });

    describe('touchStartHandler', () => {
      it('should set initialTouchY property value form event.touches[0].clientY property', () => {
        spyOn(directive as any, 'getTouchY').and.callThrough();
        (directive as any).touchStartHandler(event);
        expect((directive as any).initialTouchY).toEqual(100);
      });
    });

    describe('touchMoveHandler', () => {
      beforeEach(() => {
        spyOn(directive as any, 'shouldBePrevented').and.returnValue(false);
        spyOn(directive as any, 'getTouchY').and.returnValue(100);
        spyOn(directive as any, 'hasScrollableContent').and.returnValue(true);
        spyOn(directive as any, 'isScrollableUp').and.returnValue(true);
        spyOn(directive as any, 'isScrollableDown').and.returnValue(true);
        (directive as any).initialTouchY = 90;
        event.target = nativeElement;
        event.touches.push({ clientY: 200 }); // not isSingleTouch;
      });

      it('should update initialTouchY value', () => {
        (directive as any).touchMoveHandler(event);
        expect((directive as any).getTouchY).toHaveBeenCalled();
        expect((directive as any).initialTouchY).toEqual(100);
      });

      describe('should not call event.preventDefault', () => {
        it('when shouldBePrevented is false', () => {
          (directive as any).touchMoveHandler(event);
          expect((directive as any).hasScrollableContent).not.toHaveBeenCalled();
          expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
        });

        it('when it is not a single touch', () => {
          (directive as any).shouldBePrevented.and.returnValue(true);
          (directive as any).touchMoveHandler(event);
          expect((directive as any).hasScrollableContent).not.toHaveBeenCalled();
          expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
        });

        describe('when shouldBePrevented is true and it is a single touch but target element hasScrollableContent and', () => {
          beforeEach(() => {
            (directive as any).shouldBePrevented.and.returnValue(true);
            event.touches.pop(); // isSingleTouch;
          });
          it('isScrollableDown while being swiped up', () => {
            (directive as any).getTouchY.and.returnValue(80);
            (directive as any).touchMoveHandler(event);
            expect((directive as any).isScrollableDown).toHaveBeenCalledWith(nativeElement);
            expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          });
          it('isScrollableUp while being swiped down', () => {
            (directive as any).getTouchY.and.returnValue(100);
            (directive as any).touchMoveHandler(event);
            expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
            expect((directive as any).isScrollableUp).toHaveBeenCalledWith(nativeElement);
          });
          it('is not being swiped up or down (coverage case)', () => {
            (directive as any).getTouchY.and.returnValue(90);
            (directive as any).touchMoveHandler(event);
            expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
            expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
          });
          afterEach(() => {
            expect((directive as any).hasScrollableContent).toHaveBeenCalled();
          });
        });

        afterEach(() => {
          expect((directive as any).shouldBePrevented).toHaveBeenCalled();
          expect(event.preventDefault).not.toHaveBeenCalled();
        });
      });

      describe('should call event.preventDefault when shouldBePrevented is true and isSingleTouch is true', () => {
        beforeEach(() => {
          (directive as any).shouldBePrevented.and.returnValue(true);
          event.touches.pop(); // isSingleTouch;
        });

        it('and base element has no scrollable content', () => {
          (directive as any).hasScrollableContent.and.returnValue(false);
          (directive as any).touchMoveHandler(event);
          expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
        });

        it('and element tree is not scrollable up, when swiping up', () => {
          (directive as any).getTouchY.and.returnValue(80);
          (directive as any).isScrollableDown.and.returnValue(false);
          (directive as any).touchMoveHandler(event);
          expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          expect((directive as any).isScrollableDown).toHaveBeenCalledWith(nativeElement);
        });

        it('and element tree is not scrollable down, when swiping down', () => {
          (directive as any).getTouchY.and.returnValue(100);
          (directive as any).isScrollableUp.and.returnValue(false);
          (directive as any).touchMoveHandler(event);
          expect((directive as any).isScrollableUp).toHaveBeenCalledWith(nativeElement);
          expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
        });

        afterEach(() => {
          expect((directive as any).hasScrollableContent).toHaveBeenCalledWith(nativeElement);
          expect((directive as any).shouldBePrevented).toHaveBeenCalled();
          expect(event.preventDefault).toHaveBeenCalled();
        });
      });
    });

    describe('wheelHandler', () => {
      beforeEach(() => {
        spyOn(directive as any, 'shouldBePrevented').and.returnValue(false);
        spyOn(directive as any, 'hasScrollableContent').and.returnValue(true);
        spyOn(directive as any, 'isScrollableUp').and.returnValue(true);
        spyOn(directive as any, 'isScrollableDown').and.returnValue(true);
        event.target = nativeElement;
      });

      describe('should not call event.preventDefault', () => {
        it('when shouldBePrevented is false', () => {
          (directive as any).wheelHandler(event);
          expect((directive as any).hasScrollableContent).not.toHaveBeenCalled();
          expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
        });

        describe('when shouldBePrevented is true but target element hasScrollableContent and', () => {
          beforeEach(() => {
            (directive as any).shouldBePrevented.and.returnValue(true);
          });
          it('isScrollableUp while being scrolled up', () => {
            event.deltaY = -1;
            (directive as any).wheelHandler(event);
            expect((directive as any).isScrollableUp).toHaveBeenCalledWith(nativeElement);
            expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
          });
          it('isScrollableDown while being scrolled down', () => {
            event.deltaY = 1;
            (directive as any).wheelHandler(event);
            expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
            expect((directive as any).isScrollableDown).toHaveBeenCalledWith(nativeElement);
          });
          it('is not being scrolled up or down (coverage case)', () => {
            event.deltaY = 0;
            (directive as any).wheelHandler(event);
            expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
            expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
          });
          afterEach(() => {
            expect((directive as any).hasScrollableContent).toHaveBeenCalled();
          });
        });

        afterEach(() => {
          expect((directive as any).shouldBePrevented).toHaveBeenCalled();
          expect(event.preventDefault).not.toHaveBeenCalled();
        });
      });

      describe('should call event.preventDefault when shouldBePrevented is true', () => {
        beforeEach(() => {
          (directive as any).shouldBePrevented.and.returnValue(true);
        });

        it('and base element has no scrollable content', () => {
          (directive as any).hasScrollableContent.and.returnValue(false);
          (directive as any).wheelHandler(event);
          expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
        });

        it('and element tree is not scrollable up, when scrolling up', () => {
          (directive as any).isScrollableUp.and.returnValue(false);
          event.deltaY = -1;
          (directive as any).wheelHandler(event);
          expect((directive as any).isScrollableUp).toHaveBeenCalledWith(nativeElement);
          expect((directive as any).isScrollableDown).not.toHaveBeenCalled();
        });

        it('and element tree is not scrollable down, when scrolling down', () => {
          event.deltaY = 1;
          (directive as any).isScrollableDown.and.returnValue(false);
          (directive as any).wheelHandler(event);
          expect((directive as any).isScrollableUp).not.toHaveBeenCalled();
          expect((directive as any).isScrollableDown).toHaveBeenCalledWith(nativeElement);
        });

        afterEach(() => {
          expect((directive as any).hasScrollableContent).toHaveBeenCalledWith(nativeElement);
          expect((directive as any).shouldBePrevented).toHaveBeenCalled();
          expect(event.preventDefault).toHaveBeenCalled();
        });
      });
    });
  });
});

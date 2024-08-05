import { ScrollableRacingDirective } from '@shared/directives/scrollable-racing.directive';
import { fakeAsync, tick } from '@angular/core/testing';

describe('ScrollableRacingDirective', () => {
  let directive;
  let rendererService, device, windowRef, storage, el;

  beforeEach(() => {
    rendererService = storage = device = {};
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn: Function) => fn())
      }
    };
    el = {
      nativeElement: {
        scrollLeft: 0,
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          offsetLeft: 180,
          previousElementSibling: {
            offsetLeft: 120,
            previousElementSibling: {
              offsetLeft: 60
            }
          }
        } as any)
      }
    };

    directive = new ScrollableRacingDirective(
      rendererService,
      device,
      windowRef,
      storage,
      el
    );
    directive.element = el.nativeElement;
  });

    it('@ngAfterViewInit should init scrolls on ngAfterViewInit', fakeAsync(() => {
      spyOn(directive, 'setScrollable');
      directive.ngAfterViewInit();
      tick();
      expect(directive.windowRef.nativeWindow.setTimeout).toHaveBeenCalled();
      expect(directive.setScrollable).toHaveBeenCalled();
      expect(directive.element.scrollLeft).toBe(60);
    }));

     describe('@scrollToSelected', () => {
      it('should scroll to selected', () => {
        directive['scrollToSelected']();
        expect(directive.element.scrollLeft).toBe(60);
      });

       it('should scroll to selected if no element', () => {
         el.nativeElement.querySelector.and.returnValue(null);
         directive['scrollToSelected']();
         expect(directive.element.scrollLeft).toBe(0);
       });

      it('should scroll to 1 before selected', () => {
        el.nativeElement.querySelector.and.returnValue({
          offsetLeft: 180,
          previousElementSibling: {
            offsetLeft: 120
          }
        } as any);
        directive['scrollToSelected']();
        expect(directive.element.scrollLeft).toBe(0);
      });

      it('should not scroll', () => {
        el.nativeElement.querySelector.and.returnValue({
          offsetLeft: 180
        } as any);
        directive['scrollToSelected']();
        expect(directive.element.scrollLeft).toBe(0);
      });

      it('should scroll to li.race-on', () => {
        el.nativeElement.querySelector.and.callFake((str: string) => {
          return str === '.active' ? null : {
                  offsetLeft: 180,
                  previousElementSibling: {
                    offsetLeft: 120,
                    previousElementSibling: {
                      offsetLeft: 60
                    }
                  }
                };
            });
        directive['scrollToSelected']();
        expect(directive.element.scrollLeft).toBe(60);
      });

      it('should scroll to 1 before li.race-on', () => {
        el.nativeElement.querySelector.and.callFake((str: string) => {
          return str === '.active' ? null : {
              offsetLeft: 180,
              previousElementSibling: {
                offsetLeft: 120
              }
            };
        });
        directive['scrollToSelected']();
        expect(directive.element.scrollLeft).toBe(0);
      });

      it('should scroll to 1 before li.race-on', () => {
        el.nativeElement.querySelector.and.callFake((str: string) => {
          return str === '.active' ? null : {
              offsetLeft: 180
          };
        });
        directive['scrollToSelected']();
        expect(directive.element.scrollLeft).toBe(0);
      });
    });
});

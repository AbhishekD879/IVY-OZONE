import { LazyRenderDirective } from '@shared/directives/lazy-render.directive';
import { fakeAsync, tick } from '@angular/core/testing';


describe('LazyRenderDirective', () => {
  let directive, window, element, rendererService;

  beforeEach(() => {
    window = {
      nativeWindow: {
        scrollY: 0,
        innerHeight: 0
      }
    };
    element = {
      nativeElement: {
        getBoundingClientRect: () => ({ top: 0 }),
        clientHeight: 0
      }
    };
    rendererService = {
      renderer: {
        listen: jasmine.createSpy().and.callFake((node, event, callback) => callback)
      }
    };
    directive = new LazyRenderDirective(window, element, rendererService);
  });

  it('should create instance', () => {
    expect(directive).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it('should emit limit', fakeAsync(() => {
      directive.lazyLimitChange.subscribe(value => {
        expect(value).toEqual(3);
        directive.lazyLimitChange.unsubscribe();
      });
      directive.ngOnInit();
      tick();
    }));
  });

  describe('ngOnChanges', () => {
    it('should call setLazyRender', () => {
      spyOn(directive, 'setLazyRender').and.callThrough();
      directive.ngOnChanges({ lazyIsOpen: { previousValue: false, currentValue: true } });
      expect(directive['setLazyRender']).toHaveBeenCalled();
    });
    it('should not call setLazyRender', () => {
      spyOn(directive, 'setLazyRender').and.callThrough();
      directive.ngOnChanges({ lazyIsOpen: { previousValue: undefined, currentValue: true } });
      expect(directive['setLazyRender']).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should clear timeout', () => {
      spyOn(directive, 'clearTimeout').and.callThrough();
      directive['loadTimeout'] = 1;
      directive.ngOnDestroy();
      expect(directive['clearTimeout']).toHaveBeenCalled();
    });
    it('should call scrollListener', () => {
      directive['scrollListener'] = jasmine.createSpy();
      directive.ngOnDestroy();
      expect(directive['scrollListener']).toHaveBeenCalled();
    });
  });

  describe('setLazyRender', () => {
    it('should set scrollListener', () => {
      directive.lazyIsScroll = true;
      directive.lazyRender = 5;
      directive.ngOnChanges({ lazyIsOpen: { previousValue: false, currentValue: true } });
      expect(directive['scrollListener']).toBeDefined();
      directive['scrollListener']();
      expect(directive.limit).toEqual(8);
    });
    it('should call scrollListener', () => {
      directive.lazyIsScroll = true;
      directive.lazyRender = 5;
      element.nativeElement.clientHeight = 10;
      directive.ngOnChanges({ lazyIsOpen: { previousValue: false, currentValue: true } });
      directive['scrollListener']();
      expect(directive.limit).toEqual(3);
    });
    it('should call loadMoreOnTimeout', () => {
      directive.lazyRender = 5;
      directive.ngOnChanges({ lazyIsOpen: { previousValue: false, currentValue: true } });
      expect(directive.limit).toEqual(8);
      directive.ngOnChanges({ lazyIsOpen: { previousValue: false, currentValue: true } });
      expect(directive.limit).toEqual(8);
    });
  });



});

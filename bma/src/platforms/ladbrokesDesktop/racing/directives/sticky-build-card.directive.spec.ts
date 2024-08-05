import { StickyBuildCardDirective } from './sticky-build-card.directive';

describe('LadbrokesDesktopExtraPlaceComponent', () => {
  let component: StickyBuildCardDirective;
  let windowRef;
  let elementRef;
  let domTools;
  let rendererService;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue({
            clientWidth: 300
          }),
          addEventListener: jasmine.createSpy('addEventListener')
        },
        pageYOffset: 200,
        addEventListener: jasmine.createSpy('addEventListener')
      }
    };
    elementRef = {
      nativeElement: {
        getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({
          top: 100,
          left: 50
        }),
        clientWidth: 600
      }
    };
    domTools = {
      HeaderEl: {
        offsetHeight: 60
      }
    };
    rendererService = {
      renderer: {
        setStyle: jasmine.createSpy('setStyle'),
        removeClass: jasmine.createSpy('removeClass'),
        addClass: jasmine.createSpy('addClass')
      }
    };

    component = new StickyBuildCardDirective(windowRef, elementRef, domTools, rendererService);
  });

  describe('setStickySize', () => {
    it('should set style to sticky element', () => {
      component.ngOnInit();
      component.setStickySize();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(component['stickyElement'], 'width', '300px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(component['stickyElement'], 'top', '60px');
    });
  });

  describe('scrollHandler', () => {
    beforeEach(() => {
      windowRef = {
        nativeWindow: {
          document: {
            querySelector: jasmine.createSpy('querySelector').and.returnValue({
              clientWidth: 10,
              getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({
                top: -10,
                left: 50
              }),
            }),
            addEventListener: jasmine.createSpy('addEventListener')
          },
          pageYOffset: 200,
          addEventListener: jasmine.createSpy('addEventListener')
        }
      };
      elementRef = {
        nativeElement: {
          getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({
            top: -10,
            left: 50
          }),
          clientWidth: 100
        }
      };
      domTools = {
        getElementBottomPosition: jasmine.createSpy('getElementBottomPosition'),
        HeaderEl: {
          offsetHeight: 60
        }
      };
      component = new StickyBuildCardDirective(windowRef, elementRef, domTools, rendererService);
    });
    it('should set scroll Handler styles', () => {
      component.ngOnInit();
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(component['stickyElement'], 'left', '50px');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith(component['stickyElement'], 'top', '60px');
    });
  });
});

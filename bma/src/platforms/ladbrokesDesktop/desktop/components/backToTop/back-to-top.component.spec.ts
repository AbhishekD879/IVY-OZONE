import { BackToTopComponent } from '@desktop/components/backToTop/back-to-top.component';

describe('BackToTopComponent', () => {
  let renderer;
  let windowRef;
  let domToolsService;
  let changeDetectorRef;

  let component: BackToTopComponent;

  beforeEach(() => {
    renderer = {};

    windowRef = {
      nativeWindow: {},
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue('html body'),
        body: {
          scrollTop: null
        },
        documentElement: {
          scrollTop: null
        }
      }
    };

    domToolsService = {
      HeaderEl: {
        offsetHeight: 40
      },
      getHeight: jasmine.createSpy('getHeight'),
    };

    changeDetectorRef = {
      detach: jasmine.createSpy('detach'),
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new BackToTopComponent(
      renderer,
      windowRef,
      domToolsService,
      changeDetectorRef
    );
  });

  describe('#scroll', () => {

    it('should call scroll to top', function () {
      component.scrollToTop();
      expect(windowRef.document.body.scrollTop).toEqual(0);
      expect(windowRef.document.documentElement.scrollTop).toEqual(0);

    });
    it('#scroll pageYOffset > 0', () => {
      component.window = {
        pageYOffset: 50
      };
      component.showBackButton = true;
      component.scroll();
      expect(domToolsService.getHeight).toHaveBeenCalled();
      expect(component.showBackButton).toBeTruthy();
    });

    it('#scroll pageYOffset < 0', () => {
      component.window = {
        pageYOffset: -11
      };
      component.showBackButton = false;
      component.scroll();
      expect(domToolsService.getHeight).toHaveBeenCalled();
      expect(component.showBackButton).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });
});

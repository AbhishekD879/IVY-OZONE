import { TabsPanelComponent } from '@coralDesktop/shared/components/tabsPanel/tabs-panel.component';

describe('DesktopTabsPanelComponent', () => {
  let component: TabsPanelComponent;
  let elementRef;
  let locale;
  let router;
  let domToolsService;
  let gtmTrackingServic;
  let navigationService;
  let casinoMyBetsIntegratedService;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    locale = {};
    router = {};
    domToolsService = {
      getScrollLeft: jasmine.createSpy('getScrollLeft').and.returnValue(5),
      getWidth: jasmine.createSpy('getWidth').and.returnValue(5)
    };
    gtmTrackingServic = {};
    navigationService = {};
    casinoMyBetsIntegratedService = {};

    component = new TabsPanelComponent(
      elementRef,
      locale,
      router,
      gtmTrackingServic,
      casinoMyBetsIntegratedService,
      navigationService,
      domToolsService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('mouseOver', () => {
    component.mouseOver();
    expect(elementRef.nativeElement.querySelector).toHaveBeenCalledWith('.scroll-container');
  });

  it('mouseLeave', () => {
    component.mouseLeave();
    expect(component.isShowRightArrow).toEqual(false);
  });

  describe('scrollLeft', () => {
    it('scrollLeft (event)', () => {
      const event = {
        stopPropagation: jasmine.createSpy('stopPropagation')
      };
      component['scrollable'] = <any>{
        scrollLeft: 0
      };
      component.scrollLeft(<any>event);
      expect(event.stopPropagation).toHaveBeenCalled();
    });

    it('scrollLeft', () => {
      component['scrollable'] = <any>{
        scrollLeft: 0
      };
      component.scrollLeft(null);
      expect(domToolsService.getScrollLeft).toHaveBeenCalled();
    });
  });

  describe('scrollLeft', () => {
    it('getInnerWidth', () => {
      expect(component['getInnerWidth']()).toEqual(0);
    });

    it('getInnerWidth', () => {
      component['scrollable'] = <any>{
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scrollWidth: 10
        })
      };
      expect(component['getInnerWidth']()).toEqual(10);
    });
  });

  describe('scrollLeft', () => {
    it('isScrollLeftAvailable (true)', () => {
      component['scrollable'] = <any>{
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scrollWidth: 10
        })
      };
      expect(component['isScrollLeftAvailable']()).toEqual(true);
    });

    it('isScrollLeftAvailable (false)', () => {
      component['scrollable'] = <any>{
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scrollWidth: 4
        })
      };
      expect(component['isScrollLeftAvailable']()).toEqual(false);
    });
  });

  describe('isScrollRightAvailable', () => {
    it('isScrollRightAvailable (true)', () => {
      component['scrollable'] = <any>{
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scrollWidth: 12
        })
      };
      expect(component['isScrollRightAvailable']()).toEqual(true);
    });

    it('isScrollRightAvailable (false)', () => {
      component['scrollable'] = <any>{
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          scrollWidth: 10
        })
      };
      expect(component['isScrollRightAvailable']()).toEqual(false);
    });
  });
});


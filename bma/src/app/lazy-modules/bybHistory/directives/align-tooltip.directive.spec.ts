import { AlignTooltipDirective } from '@bybHistoryModule/directives/align-tooltip.directive';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('AlignTooltipDirective', () => {
  let directive: AlignTooltipDirective;
  let element, domToolsService, windowRefService, pubSubService, deviceService;

  beforeEach(() => {
    element = {
      nativeElement: {}
    };

    domToolsService = {
      getWidth: jasmine.createSpy('getWidth').and.callFake(el => {
        if (el === 'mainContentContainer') {
          return 0;
        }

        return 300;
      }),
      css: jasmine.createSpy('css')
    };

    windowRefService = {
      document: {
        body: {},
        getElementById: jasmine.createSpy('getElementById').and.callFake(id => {
          if (id === 'home-betslip-tabs') {
            return 'widgetContainer';
          } else if (id === 'content') {
            return 'mainContentContainer';
          }

          return 'pageWrapperContainer';
        }),
      },
      nativeWindow: {
        getComputedStyle: jasmine.createSpy('getWidth').and.returnValue({ paddingRight: 0 }),
      }
    };

    pubSubService = {
      publishSync: jasmine.createSpy('publishSync'),
      API: pubSubApi
    };

    deviceService = {
      isDesktop: false,
      isTablet: false
    };

    directive = new AlignTooltipDirective(element, domToolsService, windowRefService, pubSubService, deviceService);
    directive.infoIconXPosition = 50;
    directive.isUsedFromWidget = false;
  });

  it('should align tooltip position if tooltip outside of window from the left and it is not a widget', () => {
    directive.alignTooltipPosition();

    expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-40px`});
  });

  it('should align tooltip position if tooltip outside of widget from the right(Desktop widget)', () => {
    directive.isUsedFromWidget = true;
    deviceService.isDesktop = true;
    directive.infoIconXPosition = 280;
    directive.alignTooltipPosition();

    expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-292px`});
  });

  it('should align tooltip position if tooltip outside of widget from the right(Desktop widget)', () => {
    directive.isUsedFromWidget = true;
    deviceService.isDesktop = false;
    deviceService.isTablet = true;
    directive.infoIconXPosition = 280;

    directive.alignTooltipPosition();

    expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-292px`});
  });

  it('should NOT align tooltip position', () => {
    directive.infoIconXPosition = 150;
    directive.alignTooltipPosition();

    expect(domToolsService.css).not.toHaveBeenCalled();
  });

  it('@ngAfterViewInit: should NOT align tooltip position', () => {
    directive.infoIconXPosition = 150;
    directive.ngAfterViewInit();

    expect(domToolsService.css).not.toHaveBeenCalled();
  });

  it('@clickOutside: should publish pubsub event to close all tooltips', () => {
    directive.clickOutside({ preventDefault: () => {} } as any);

    expect(pubSubService.publishSync).toHaveBeenCalledWith('CLOSE_TOOLTIPS');
  });

  describe('@handleMobileTooltipPosition', () => {
    it('should align tooltip position if tooltip outside of window from the left', () => {
      directive.handleMobileTooltipPosition(300, 300, 150, '0px');

      expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-40px`});
    });

    it('should align tooltip position if tooltip outside of window from the right', () => {
      directive.infoIconXPosition = 280;
      directive.handleMobileTooltipPosition(300, 300, 150, '0px');

      expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-290px`});
    });

    it('should NOT align tooltip position', () => {
      directive.infoIconXPosition = 150;
      directive.handleMobileTooltipPosition(300, 300, 150, '0px');

      expect(domToolsService.css).not.toHaveBeenCalled();
    });
  });

  describe('@handleDesktopTooltipPositions', () => {
    it('should align tooltip position if tooltip outside of widget from the left', () => {
      directive.isUsedFromWidget = true;
      directive.handleDesktopTooltipPositions(300, 300, 150, '0px');

      expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-44px`});
    });

    it('should align tooltip position if tooltip outside of widget from the left on tablet', () => {
      directive.isUsedFromWidget = true;
      deviceService.isTablet = true;
      directive.handleDesktopTooltipPositions(300, 300, 150, '0px');

      expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-44px`});
    });

    it('should align tooltip position if tooltip outside of main content container from the left', () => {
      directive.handleDesktopTooltipPositions(300, 300, 150, '0px');

      expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-44px`});
    });

    it('should align tooltip position if tooltip outside of widget from the right', () => {
      directive.infoIconXPosition = 280;
      directive.isUsedFromWidget = true;
      directive.handleDesktopTooltipPositions(300, 300, 150, '0px');

      expect(domToolsService.css).toHaveBeenCalledWith({}, { left: `-292px`});
    });

    it('should NOT align tooltip position for desktop widget', () => {
      directive.isUsedFromWidget = true;
      directive.infoIconXPosition = 150;
      directive.handleDesktopTooltipPositions(300, 300, 150, '0px');

      expect(domToolsService.css).not.toHaveBeenCalled();
    });
  });
});

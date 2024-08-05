import { VirtualCarouselMenuComponent } from '@ladbrokesDesktop/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';

describe('VirtualCarouselMenuComponent', () => {
  let component: VirtualCarouselMenuComponent;
  let elementRef,
      locale,
      router,
      navigationService,
      domToolsService,
      gtmTrackingService,
      casinoMyBetsIntegratedService;

  let mockMenuItems = [
    {
      name: 'hourse',
      inApp: true,
      svgId: 'string',
      targetUri: '/hourse',
      targetUriSegment: '/hourse',
      priority: 1,
      childMenuItems: [
        {
          name: 'hourse',
          inApp: true,
          svgId: 'string',
          targetUri: '/hourse',
          targetUriSegment: '/hourse',
          priority: 1,
          childMenuItems: [],
          label: null,
          displayOrder: 1,
          alias: 'hourse',
          svg: 'svg',
          isActive: true
        },
        {
          name: 'hourse',
          inApp: true,
          svgId: 'string',
          targetUri: '/hourse',
          targetUriSegment: '/hourse',
          priority: 1,
          childMenuItems: [],
          label: null,
          displayOrder: 1,
          alias: 'hourse-racing',
          svg: 'svg',
          isActive: false
        }
      ],
      label: null,
      displayOrder: 1,
      alias: '/hourse',
      svg: 'svg',
      isActive: true
    },
    {
      name: 'football',
      inApp: true,
      svgId: 'svgId',
      targetUri: '/football',
      targetUriSegment: 'football',
      priority: 1,
      childMenuItems: [],
      label: null,
      displayOrder: 1,
      alias: 'football',
      svg: 'icon',
      isActive: true
    }
  ];

  beforeEach(() => {
    elementRef = {};
    locale = {};
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    navigationService = {
      openUrl: jasmine.createSpy()
    };

    domToolsService = {};
    gtmTrackingService = {};
    casinoMyBetsIntegratedService = {};

    component = new VirtualCarouselMenuComponent(
      elementRef,
      locale,
      router,
      navigationService,
      domToolsService,
      casinoMyBetsIntegratedService,
      gtmTrackingService
    );
  });

  describe('VirtualCarouselMenuComponent for Desktop', () => {

    it('should create VirtualCarouselMenuComponent instance', () => {
      expect(component).toBeTruthy();
    });

    it('should call trackByMenu method', () => {
      const result = component.trackByMenu(1, mockMenuItems[0] as any);
      expect(result).toEqual('1hourse');
    });

    it('should call goToVirtual()', () => {
      component.menuElements = mockMenuItems;
      component.goToVirtual(mockMenuItems[0] as any);

      expect(navigationService.openUrl).toHaveBeenCalled();
    });

    it('should call goToVirtual() if child category called', () => {
      component.menuElements = mockMenuItems;
      component.goToVirtual(mockMenuItems[0].childMenuItems[0] as any, true);

      expect(navigationService.openUrl).toHaveBeenCalled();
    });

    it('should not call goToVirtual() if menuElements is empty', () => {
      mockMenuItems = [];
      component.menuElements = mockMenuItems;
      expect(navigationService.openUrl).not.toHaveBeenCalled();
    });
  });
});

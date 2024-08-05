import { VirtualCarouselMenuComponent } from '@app/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';

describe('VirtualCarouselMenuComponent', () => {
  let component: VirtualCarouselMenuComponent;
  let navigationService;

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
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
      };
    component = new VirtualCarouselMenuComponent(navigationService);
  });

  it('should create VirtualSportsPageComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('should call trackByMenu method', () => {
    const result = component.trackByMenu(1, mockMenuItems[0]);
    expect(result).toEqual('1hourse');
  });

  it('should call goToVirtual()', () => {
    component.menuElements = mockMenuItems;
    component.goToVirtual(mockMenuItems[0]);

    expect(navigationService.openUrl).toHaveBeenCalled();
  });

  it('should call goToVirtual() if child category called', () => {
    component.menuElements = mockMenuItems;
    component.goToVirtual(mockMenuItems[0].childMenuItems[0], true);

    expect(navigationService.openUrl).toHaveBeenCalled();
  });

  it('should not call goToVirtual() if menuElements is empty', () => {
    mockMenuItems = [];
    component.menuElements = mockMenuItems;
    expect(navigationService.openUrl).not.toHaveBeenCalled();
  });
});

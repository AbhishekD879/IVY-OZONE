import { of as observableOf } from 'rxjs';
import { RetailMenuComponent } from '@app/retail/components/retailMenu/retail-menu.component';
import { IVerticalMenu } from '@core/services/cms/models';
import { GRID_GA_TRACKING } from '@app/retail/constants/retail.constant';

describe('#RetailMenuComponent', () => {
  let retailMenuComponent: RetailMenuComponent;
  let gtmService;
  let userService;
  let retailMenuService;
  let navigationService;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push').and.callThrough()
    };
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    userService = {
      cardNumber: 2,
      isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(true)
    };
    retailMenuService = { retailMenuItems$: observableOf([]) };
    retailMenuComponent = new RetailMenuComponent(gtmService, userService, retailMenuService, navigationService);
    retailMenuComponent['showCardNumber'] = true;
    retailMenuComponent['subscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
  });

  describe('showTopBorder public property', () => {
    it('should be false by default', () => {
      expect(retailMenuComponent.showTopBorder).toBe(false);
    });

    it('should be true when no menu Items', () => {
      retailMenuComponent.ngOnInit();

      expect(retailMenuComponent.showTopBorder).toBe(true);
    });

    it('should be false when menu items are available', () => {
      retailMenuService.retailMenuItems$ = observableOf([{ linkSubtitle: 'subtitile' } as IVerticalMenu]);

      retailMenuComponent.ngOnInit();

      expect(retailMenuComponent.showTopBorder).toBe(false);
      expect(retailMenuComponent.cardMenuItem).toEqual({ title: 2, svgId: '#retail-card' } as any);
    });

    it('should cardMenuItem = null', () => {
      retailMenuService.retailMenuItems$ = observableOf([{ linkSubtitle: 'subtitile' } as IVerticalMenu]);
      retailMenuComponent['showCardNumber'] = false;

      retailMenuComponent.ngOnInit();

      expect(retailMenuComponent.showTopBorder).toBe(false);
      expect(retailMenuComponent.cardMenuItem).toEqual(null);
    });

    it('should cardMenuItem = null', () => {
      retailMenuService.retailMenuItems$ = observableOf([{ linkSubtitle: 'subtitile' } as IVerticalMenu]);
      userService.cardNumber = 0;

      retailMenuComponent.ngOnInit();

      expect(retailMenuComponent.showTopBorder).toBe(false);
      expect(retailMenuComponent.cardMenuItem).toEqual(null);
    });

    it('should cardMenuItem = null', () => {
      retailMenuService.retailMenuItems$ = observableOf([{ linkSubtitle: 'subtitile' } as IVerticalMenu]);
      userService.isInShopUser = jasmine.createSpy('isInShopUser').and.returnValue(false);

      retailMenuComponent.ngOnInit();

      expect(retailMenuComponent.showTopBorder).toBe(false);
      expect(retailMenuComponent.cardMenuItem).toEqual(null);
    });

  });

  it('showRetailMenu', () => {
    retailMenuService.retailMenuItems$ = observableOf([{ linkSubtitle: 'subtitile' } as IVerticalMenu]);
    retailMenuComponent.ngOnInit();
    expect(retailMenuComponent.menuItems).toEqual([{ linkSubtitle: 'subtitile' } as IVerticalMenu]);
  });

  it('@ngOnDestroy', () => {
    retailMenuComponent.ngOnDestroy();

    expect(retailMenuComponent['subscription'].unsubscribe).toHaveBeenCalled();
  });

  it('@trackNavigation', () => {
    const menuItem = { linkTitle: 'linkTitle' } as any;
    retailMenuComponent['itemClick'].emit = jasmine.createSpy('emit').and.callThrough();

    retailMenuComponent.trackNavigation(menuItem);

    expect(GRID_GA_TRACKING.eventLabel).toEqual(menuItem.linkTitle);
    expect(gtmService.push).toHaveBeenCalled();
    expect(retailMenuComponent['itemClick'].emit).toHaveBeenCalledWith(menuItem);
  });

  describe('trackGridNavigation', () => {
    it('should delegate opening to navigationService', () => {
      const inApp = undefined;
      const menuItem = { linkTitle: 'linkTitle', targetUri: 'test' } as any;
      retailMenuComponent['itemClick'].emit = jasmine.createSpy('emit').and.callThrough();
      retailMenuComponent.trackGridNavigation(menuItem);
      expect(GRID_GA_TRACKING.eventLabel).toEqual(menuItem.linkTitle);
      expect(gtmService.push).toHaveBeenCalled();
      expect(navigationService.openUrl).toHaveBeenCalledWith('test', inApp);
    });
    it('should delegate opening not navigationService', () => {
      const menuItem = { linkTitle: 'linkTitle', targetUri:'/bet-filter' } as any;
      retailMenuComponent['itemClick'].emit = jasmine.createSpy('emit').and.callThrough();
      retailMenuComponent.trackGridNavigation(menuItem);
      expect(GRID_GA_TRACKING.eventLabel).toEqual(menuItem.linkTitle);
      expect(gtmService.push).toHaveBeenCalled();
    });
  });
});

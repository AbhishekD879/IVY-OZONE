import { of as observableOf, of } from 'rxjs';
import { LeftMenuComponent } from '@ladbrokesDesktop/desktop/components/leftMenu/left-menu.component';
import { category } from './category.mock';
import { IDesktopQuickLink } from '@core/services/cms/models';

describe('LeftMenuComponentLadbrokes', () => {
  let component;
  let navigationService;
  let leftMenuService;
  let germanSupportService;
  let pubSubService;
  let changeDetectorRef;
  let cmsService;
  let userService;
  let bonusSuppressionService;
  const quickLinks: IDesktopQuickLink[] = [
    {
      title: 'Football',
      target: 'sport/football',
      isAtoZQuickLink: true
    },
    {
      title: 'BasketBall',
      target: '/sport/basketball',
      isAtoZQuickLink: false
    }
  ] as IDesktopQuickLink[];
  const body = [123, 1];

  beforeEach(() => {
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    germanSupportService = {
      toggleItemsList: jasmine.createSpy('toggleItemsList').and.returnValue([category])
    };
    leftMenuService = {
      getMenuItems: jasmine.createSpy('getMenuItems').and.returnValue(observableOf([category])),
      getFavouriteItems: jasmine.createSpy('getFavouriteItems').and.returnValue(observableOf(body)),
      storeFavouriteItems: jasmine.createSpy('storeFavouriteItems').and.returnValue(observableOf(body))
    };
    navigationService = jasmine.createSpyObj(['openUrl']);
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => callback()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        SESSION_LOGIN: 'SESSION_LOGIN',
        SESSION_LOGOUT: 'SESSION_LOGOUT'
      }
    };

    cmsService = {
      getDesktopQuickLinks: jasmine.createSpy('cmsQuickLinks').and.returnValue(observableOf(quickLinks)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        FavouriteCount: {
          maxFavourites: 2
        }
      })),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };
    userService = {
      bppToken: 'abc123',
      status: true,
    }
    
    bonusSuppressionService = {
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled ').and.returnValue(true)
    }

    component = new LeftMenuComponent(
      navigationService,
      leftMenuService,
      germanSupportService,
      pubSubService,
      changeDetectorRef,
      cmsService,
      userService,
      bonusSuppressionService);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(LeftMenuComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  it('#ngOnInit', () => {
    component['setTargetUriParts'] = jasmine.createSpy().and.callFake((item) => item);
    component.filterRestrictedSports = jasmine.createSpy();
    component.favLimit = 5;
    component.ngOnInit();
    expect(leftMenuService.getMenuItems).toHaveBeenCalled();
    expect(component['setTargetUriParts']).toHaveBeenCalledWith(category);
    expect(component.filterRestrictedSports).toHaveBeenCalledWith(component.menuItems);
    expect(leftMenuService.getFavouriteItems).toHaveBeenCalled();
    expect(component.menuItems).toEqual([category]);
  });

  it('#should call Update favourite items', () => {
    component.menuItems = [category];
    component.favouriteIds = [1];
    component.favourites = [1];
    component['updateFavouriteItems']();
    expect(component.favouriteItems.length).toEqual(1);
  });

  it('#ngOnInit: should take else path in favourites count ', ()=> {
    cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}));
    component.ngOnInit();
    expect(component.favCount).toBeUndefined();
  });

  it('#ngOnInit: should assign favourites', () => {
    component['setTargetUriParts'] = jasmine.createSpy().and.callFake((item) => item);
    
    component.favouriteIds = [1];
    component.favourites = [1];
    component.ngOnInit();
    expect(leftMenuService.getMenuItems).toHaveBeenCalled();
    expect(component['setTargetUriParts']).toHaveBeenCalledWith(category);
    expect(component.menuItems).toEqual([category]);
  });

  it('should load quicklinks', () => {
    component.ngOnInit();
    expect(component.quickLinks[0].target).toEqual('/sport/football');
    expect(component.quickLinks.length).toEqual(1);
  });

  it('should filter quickLinks based on RG Yellow status with quickLinks available', () => {
    component.quickLinks = quickLinks;
    component.ngOnInit();

    expect(component.quickLinks.length).toEqual(1);
  });

  it('should filter quickLinks based on RG Yellow status with quickLinks not available', () => {
    cmsService.getDesktopQuickLinks = jasmine.createSpy('cmsQuickLinks').and.returnValue(observableOf([])),
    component.ngOnInit();

    expect(component.quickLinks.length).toEqual(0);
  });

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('LeftMenuComponent');
  });

  it('#filterRestrictedSports, should call correct methods', () => {
    component.filterRestrictedSports([category]);
    expect(component.menuItems).toEqual([category]);
    expect(germanSupportService.toggleItemsList).toHaveBeenCalledTimes(1);
    expect(component['changeDetectorRef'].markForCheck).toHaveBeenCalled();
  });

  it('#trackById, should return correct result', () => {
    const menuItem = { id: '14' } as any;
    const index = 3;
    expect(component.trackById(index, menuItem)).toBe('14');
  });

  it('#setTargetUriParts, should extend category with targetUriParts property', () => {
    const result = component['setTargetUriParts'](category);
    expect(result.targetUriParts).toEqual(jasmine.arrayContaining(['/', 'sport', 'american-football']));
  });

  it('#set/update favourites, should display favourites', () => {
    component.menuItems = [category];
    component.enabledCategories = [category];
    component.favouriteIds = [];
    component.favourites = [];
    component.favLimit = 5;
    component['openUrl']({target:{dataset:{crlat:'favouriteCheckbox'}}}, category);
    leftMenuService.storeFavouriteItems('Test token', {categories:[category.categoryId]});
    component['updateFavouriteItems']();
    expect(component.favouriteIds.length).toEqual(1);
  });

  it('should not call favourite methods', () => {
    component.menuItems = [category];
    component.enabledCategories = [category];
    component.favouriteIds = [];
    component.favourites = [];    
    component['openUrl']({target:{dataset:{crlat:'favouriteCheckbox1'}}}, category);
    expect(leftMenuService.storeFavouriteItems).not.toHaveBeenCalled();
  });

  it('#set/update favourites, should display new favourites and header', () => {
    const menuItems = [{category}, {...category, categoryId: 12}];
    component.menuItems = menuItems;
    component.enabledCategories = menuItems;
    component.favouriteIds = [12];
    component.favourites = [12];
    component.favLimit = 5;
    component['setFavourite']({target:{dataset:{crlat:'favouriteCheckbox'}}}, category);
    component['updateFavouriteItems']();
    expect(component.favouriteIds.length).toEqual(1);
  });

  it('#set/update favourites, should not display new favourites and header', () => {
    const menuItems = [{category}, {...category, categoryId: 12}];
    component.menuItems = menuItems;
    component.enabledCategories = menuItems;
    component.favouriteIds = [12, 1];
    component.favourites = [12, 1];
    component.favouriteItems = menuItems;
    component.favLimit = 5;
    component['setFavourite']({target:{checked: false, dataset:{crlat:'favouriteCheckbox'}}}, category);
    component['updateFavouriteItems']();
    expect(component.favouriteIds.length).toEqual(1);
  });

  it('#set/update favourites, should not display favourites', () => {
    const menuItems = [{category}];
    component.menuItems = menuItems;
    component.enabledCategories = menuItems;
    component.favLimit = 5;
    component.favourites = [1];
    component.favouriteIds = [1];
    component.favouriteItems = [{...category, 'categoryId': 1}];
    component['setFavourite']({target:{dataset:{crlat:'favouriteCheckbox'}}}, category);
    expect(component.favouriteIds.length).toEqual(0);
  });

  it('should call navigation service', () => {
    component.menuItems = [category];
    component['openUrl']({target:{dataset:{crlat:'favouriteCheckbox1'}}}, category);
    expect(navigationService.openUrl).toHaveBeenCalled();
  });

  describe('getFavourites', () => {
    it('favLimit set to 0', () => {
      component.favLimit = 0;
      component.getFavourites();
      expect(leftMenuService.getFavouriteItems).not.toHaveBeenCalled();
    });
    it('favLimit greater to 0 and userservice bppToken is undefined', () => {
      component.favLimit = 1;
      userService.bppToken = undefined;
      component.getFavourites();
      expect(leftMenuService.getFavouriteItems).not.toHaveBeenCalled();
    });
    it('favLimit greater to 0 and userservice token defined', () => {
      component.favLimit = 1;
      userService.bppToken = 'token';
      component.getFavourites();
      expect(leftMenuService.getFavouriteItems).toHaveBeenCalled();
    });
  });
});
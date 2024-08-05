
import { of, throwError } from 'rxjs';

import { NavigationEditComponent } from './navigation-edit.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';

describe('NavigationEditComponent', () => {
  let component: NavigationEditComponent;
  let globalLoaderService;
  let dialogService;
  let activatedRoute;
  let router;
  let snackBar;
  let sortableTableService;
  let apiClientService;
  let mocknavigationGroups;
  let mockParentData;

  beforeEach(() => {
    mocknavigationGroups = {
      'id': '62c6b7c1c1bbb96a5e621896',
      'title': 'Cricket',
      'status': false,
      'updatedAt': '2022-07-07T10:38:57.450Z',
      brand: 'ladbrokes',
      promotionIds: ['123', '111'],
      navItems: [{
        'id': '62c80d5cbc54f74ed94d52d9',
        'createdBy': '54905d04a49acf605d645271',
        'createdByUserName': null,
        'updatedBy': '54905d04a49acf605d645271',
        'updatedByUserName': null,
        'createdAt': '2022-07-08T10:56:28.126Z',
        'updatedAt': '2022-07-08T10:56:28.126Z',
        'sortOrder': -3.0,
        'brand': 'ladbrokes',
        'name': 'Cricket2',
        'url': '/test',
        'navigationGroupId': '62c6b7c1c1bbb96a5e621896',
        navType: 'url',
      }]
    };
    mockParentData = {
      title: 'Cricket2',
      status: true,
      id: '62c6b7c1c1bbb96a5e621896',
      brand: 'ladbrokes',
      createdBy: '54905d04a49acf605d645271',
      createdAt: '54905d04a49acf605d645271',
      updatedBy: '54905d04a49acf605d645271',
      updatedAt: '54905d04a49acf605d645271',
      updatedByUserName: '54905d04a49acf605d645271',
      createdByUserName: '54905d04a49acf605d645271',
    }

    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
    };

    activatedRoute = {
      params: of({ 'id': '123' })
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    sortableTableService = {
      addSorting: jasmine.createSpy('addSorting'),
    };

    router = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    apiClientService = {
      promotionsNavigationsService: jasmine.createSpy('promotionsNavigationsService').and.returnValue({
        remove: jasmine.createSpy('remove').and.returnValue(of({ body: [] })),
        getNavListById: jasmine.createSpy('getNavListById').and.returnValue(of({ body: [] })),
        removeNavContent: jasmine.createSpy('removeNavContent').and.returnValue(of({ body: [] })),
        postNewNavItemOrder: jasmine.createSpy('postNewNavItemOrder').and.returnValue(of({ body: [] })),
        updateNavGroup: jasmine.createSpy('updateNavGroup').and.returnValue(of({ body: mocknavigationGroups as any })),
      })
    };
    snackBar = {
      open: jasmine.createSpy('open')
    }

    component = new NavigationEditComponent(
      globalLoaderService, apiClientService, activatedRoute, dialogService, router, snackBar,
      sortableTableService
    );

    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any as ActionButtonsComponent;
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  it('ngOnInit', () => {

    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
  });

  it('revertChanges', () => {

    component.revertChanges();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
  });

  it('revertChanges', () => {

    component.revertChanges();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
  });

  it('loadInitData', fakeAsync(() => {

    let mockmocknavigationGroupsData = mocknavigationGroups;
    mockmocknavigationGroupsData.promotionIds = [];
    component.navigationGroups = mockmocknavigationGroupsData;
    apiClientService.promotionsNavigationsService().getNavListById.and.returnValue(throwError('message'))
    
    component['loadInitData']('123');
    tick();
    tick();
    expect(apiClientService.promotionsNavigationsService().getNavListById).toHaveBeenCalled();
  }));

  describe('removeNavigationGroups', () => {
    it('Load Navigation Groups if Promotion ids have empty array', fakeAsync(() => {

      component.navigationGroups = mocknavigationGroups
      component.removeNavigationGroups();
      tick();
      tick();
      expect(apiClientService.promotionsNavigationsService().remove).toHaveBeenCalled();
    }));
    it('Load Navigation Groups if Promotion ids have length', fakeAsync(() => {

      let mockmocknavigationGroupsData = mocknavigationGroups;
      mockmocknavigationGroupsData.promotionIds = [];
      component.navigationGroups = mockmocknavigationGroupsData;
      component.removeNavigationGroups();
      tick();
      tick();
      expect(apiClientService.promotionsNavigationsService().remove).toHaveBeenCalled();
    }));
  });


  describe('isValidForm', () => {
    it('isValidForm if form has  title field', () => {


      component.isValidForm(mockParentData);

      expect(component.isValidForm(mockParentData)).toBeTruthy();
    });
    it('isValidForm if form has no title field', () => {

      mockParentData.title = null;
      component.isValidForm(mockParentData);

      expect(component.isValidForm(mockParentData)).toBeFalsy();
    });
  });

  describe('actionsHandler', () => {
    it('if event is save', () => {
      const spySaveNavigationGroup = spyOn(component, 'saveNavigationGroup');

      component.actionsHandler('save');

      expect(spySaveNavigationGroup).toHaveBeenCalled();
    });
    it('if event is remove', () => {
      const spyRemoveNavigationGroups = spyOn(component, 'removeNavigationGroups');

      component.actionsHandler('remove');

      expect(spyRemoveNavigationGroups).toHaveBeenCalled();
    });
    it('if event is revert', () => {
      const spyRevertChanges = spyOn(component, 'revertChanges');

      component.actionsHandler('revert');

      expect(spyRevertChanges).toHaveBeenCalled();
    });
    it('default action', () => {
      const spyConsole = spyOn(console, 'error');

      component.actionsHandler('revert11');

      expect(spyConsole).toHaveBeenCalled();
    });
  });

  describe('addNavItem', () => {
    it('if navigationGroups navItems length is greator than 9', () => {

      component.navigationGroups = mocknavigationGroups;
      component.navigationGroups.navItems.length = 10;
      component.addNavItem();

      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
    it('if navigationGroups navItems length is less than 9', () => {
      component.navigationGroups = mocknavigationGroups;

      component.addNavItem();

      expect(router.navigateByUrl).toHaveBeenCalled();
    });
  });

  describe('removeNavItems', () => {
    it('if navGroup exists', () => {
      component.navigationGroups = mocknavigationGroups;
      component.removeNavItems(0);

      expect(dialogService.showConfirmDialog).toHaveBeenCalled();
    });
    it('if navGroup does not exists', () => {
      component.navigationGroups = mocknavigationGroups;
      component.navigationGroups.navItems[0].id = null;
      component.removeNavItems(0);

      expect(component.isDisabledBtn).toBeFalsy();
    });
  });

  describe('addReorderingToTable', () => {
    it('if navGroup exists', () => {
      component.navigationGroups = mocknavigationGroups;
      component.addReorderingToTable();

      expect(sortableTableService.addSorting).toHaveBeenCalled();
    });
  });

  describe('navigateToEdit', () => {
    it('if navGroup exists', () => {

      component.navigateToEdit('url');

      expect(router.navigate).toHaveBeenCalled();
    });
  });

  describe('reorderHandler', () => {
    it('reorderHandler', () => {
      const mockOrder = {
        order: ['a', 'b'],
        id: '123',
        segmentName: 'abc'
      }

      component.reorderHandler(mockOrder);

      expect(snackBar.open).toHaveBeenCalled();
    });
  });

  describe('ngOnChanges', () => {
    it('ngOnChanges', () => {
      const spyAddReorderingToTable = spyOn(component, 'addReorderingToTable')
      component.ngOnChanges();

      expect(spyAddReorderingToTable).toHaveBeenCalled();
    });
  });

  describe('saveNavigationGroup', () => {

    it('saveNavigationGroup', fakeAsync(() => {

      component.navigationGroups = mocknavigationGroups;
      component.saveNavigationGroup();
      tick();
      tick();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    }));
  });

  describe('displayType', () => {
    it('if type is leaderboard', () => {

      component.displayType('leaderboard');

      expect(component.navdisplayType).toBe('Leaderboard');
    });
    it('if event is description', () => {

      component.displayType('description');

      expect(component.navdisplayType).toBe('Description');
    });
    it('default action', () => {

      component.displayType('url');

      expect(component.navdisplayType).toBe('URL');
    });

  });
});

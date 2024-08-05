import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { UserMenusListComponent } from './user-menus-list.component';

describe('UserMenusListComponent', () => {
  let component: UserMenusListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;

  beforeEach(() => {
    apiClientService = {
      userMenu: jasmine.createSpy('userMenu').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({
          body: {}
        }))
      })
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    snackBar = {};
    router = {};

    component = new UserMenusListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router);
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();

    expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.userMenu);
    expect(component.userMenus).toBeDefined();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
  }));
});

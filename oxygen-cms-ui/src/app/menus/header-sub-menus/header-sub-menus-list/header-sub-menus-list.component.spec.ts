import { HeaderSubMenusListComponent } from './header-sub-menus-list.component';
import { of } from "rxjs";

describe('HeaderSubMenusListComponent', () => {
  let component: HeaderSubMenusListComponent;
  let router, snackBar, apiClientService, dialogService, globalLoaderService;

  beforeEach(() => {
    router = {};
    snackBar = {};
    apiClientService = {
      headerSubMenu: jasmine.createSpy('findAllByBrand').and.returnValue(
        { findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of([])) }
      )
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    component = new HeaderSubMenusListComponent(apiClientService, dialogService, globalLoaderService, snackBar, router);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.headerSubMenu().findAllByBrand).toHaveBeenCalled();
  });
});

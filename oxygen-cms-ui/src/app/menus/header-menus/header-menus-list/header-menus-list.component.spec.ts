import { HeaderMenusListComponent } from './header-menus-list.component';
import {of} from "rxjs";

describe('HeaderMenusListComponent', () => {
  let component: HeaderMenusListComponent;
  let router, snackBar, apiClientService, dialogService, globalLoaderService;
  let headerMenus;

  beforeEach(() => {
    headerMenus = [
      {
        id: 1,
        disabled: false,
        inApp: false,
        lang: '',
        linkTitle: '',
        targetUri: '',
        level: '2',
        parent: ''
      }
    ];

    router = {};
    snackBar = {};
    apiClientService = {
      headerMenu: jasmine.createSpy('headerMenu').and.returnValue(
        { findAllByBrand: jasmine.createSpy('showLoader').and.returnValue(of({body: headerMenus})) }
      )
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    component = new HeaderMenusListComponent(apiClientService, dialogService, globalLoaderService, snackBar, router);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.headerMenu).toHaveBeenCalled();
  });
});

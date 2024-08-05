import { of } from 'rxjs';
import { RightMenusListComponent } from './right-menus-list.component';

describe('RightMenusListComponent', () => {
  let component: RightMenusListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;
  let rightMenuService;

  beforeEach(() => {
    apiClientService = {
      rightMenu: () => rightMenuService
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    snackBar = {};
    router = {};
    rightMenuService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: {} }))
    };

    component = new RightMenusListComponent(
      apiClientService, dialogService, globalLoaderService, snackBar, router
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(rightMenuService.findAllByBrand).toHaveBeenCalled();
  });
});

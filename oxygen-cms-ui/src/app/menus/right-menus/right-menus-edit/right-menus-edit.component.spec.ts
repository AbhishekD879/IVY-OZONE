import { RightMenusEditComponent } from './right-menus-edit.component';
import { of } from 'rxjs';

describe('RightMenusEditComponent', () => {
  let component: RightMenusEditComponent;
  let router;
  let activatedRoute;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let rightMenuService;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({})
    };
    apiClientService = {
      rightMenu: () => rightMenuService
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    snackBar = {};
    rightMenuService = {
      findOne: jasmine.createSpy('findOne').and.returnValue(of({ body: {} }))
    };

    component = new RightMenusEditComponent(
      router, activatedRoute, apiClientService, dialogService, globalLoaderService, snackBar
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(rightMenuService.findOne).toHaveBeenCalled();
  });
});

import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { UserMenusEditComponent } from './user-menus-edit.component';

describe('UserMenusEditComponent', () => {
  let component: UserMenusEditComponent;
  let router;
  let activatedRoute;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({ id: 0 })
    };
    apiClientService = {
      userMenu: jasmine.createSpy('userMenu').and.returnValue({
        findOne: jasmine.createSpy('findOne').and.returnValue(of({
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

    component = new UserMenusEditComponent(
      router,
      activatedRoute,
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar);
  });

  it('ngOnInit', fakeAsync(() => {
    spyOn(component, 'loadInitData').and.callThrough();

    component.ngOnInit();
    tick();

    expect(component.loadInitData).toHaveBeenCalled();
  }));
});

import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { ConnectMenusEditComponent } from './connect-menus-edit.component';

describe('ConnectMenusEditComponent', () => {
  let component: ConnectMenusEditComponent;
  let router;
  let activatedRoute;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let brandService;


  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({})
    };
    apiClientService = {
      connectMenu: jasmine.createSpy('connectMenu').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({
          body: {
            disabled: true
          }
        }))
      })
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    snackBar = {};
    brandService = {
      isIMActive: jasmine.createSpy('isIMActive')
    };

    component = new ConnectMenusEditComponent(
      router,
      activatedRoute,
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      brandService);
  });

  it('ngOnInit', fakeAsync(() => {
    spyOn(component, 'loadInitData').and.callThrough();

    component.ngOnInit();
    tick();

    expect(component.loadInitData).toHaveBeenCalled();
  }));
});

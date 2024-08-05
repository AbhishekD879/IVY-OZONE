import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { ConnectMenusListComponent } from './connect-menus-list.component';

describe('ConnectMenusListComponent', () => {
  let component: ConnectMenusListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;

  beforeEach(() => {
    apiClientService = {
      connectMenu: jasmine.createSpy('connectMenu').and.returnValue({
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

    component = new ConnectMenusListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router
    );
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();

    expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.connectMenu);
    expect(apiClientService.connectMenu).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  }));
});

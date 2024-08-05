import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { BankingMenusEditComponent } from './banking-menus-edit.component';

describe('BankingMenusEditComponent', () => {
  let component: BankingMenusEditComponent;
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
      params: of({ id: 0 })
    };
    apiClientService = {
      bankingMenu: jasmine.createSpy('bankingMenu').and.returnValue({
        findOne: jasmine.createSpy('findOne').and.returnValue(of({
          body: {
            linkTitle: ''
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
      isIMActive: jasmine.createSpy('isIMActive').and.returnValue(true)
    };

    component = new BankingMenusEditComponent(
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

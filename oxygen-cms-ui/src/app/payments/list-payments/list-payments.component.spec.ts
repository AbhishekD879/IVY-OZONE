import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { ListPaymentsComponent } from './list-payments.component';

describe('ListPaymentsComponent', () => {
  let component: ListPaymentsComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;

  beforeEach(() => {
    apiClientService = {
      paymentMethods: jasmine.createSpy('connectMenu').and.returnValue({
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

    component = new ListPaymentsComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router);
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();

    expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.paymentMethods);
    expect(component.paymentMethods).toBeDefined();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  }));
});

import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { EditPaymentComponent } from './edit-payment.component';

describe('EditPaymentComponent', () => {
  let component: EditPaymentComponent;
  let activatedRoute;
  let router;
  let apiClientService;
  let globalLoaderService;
  let dialogService;

  beforeEach(() => {
    activatedRoute = {
      params: of({ id: 0 })
    };
    router = {};
    apiClientService = {
      paymentMethods: jasmine.createSpy('paymentMethods').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({
          body: [
            { id: 0, name: 'test0' },
            { id: 1, name: 'test1' }
          ]
        }))
      })
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};

    component = new EditPaymentComponent(
      activatedRoute,
      router,
      apiClientService,
      globalLoaderService,
      dialogService);
  });

  it('ngOnInit', fakeAsync(() => {
    spyOn<any>(component, 'loadInitialData').and.callThrough();

    component.ngOnInit();
    tick();

    expect(component.identifierTypes).toBeDefined();
    expect(component['loadInitialData']).toHaveBeenCalled();
  }));
});

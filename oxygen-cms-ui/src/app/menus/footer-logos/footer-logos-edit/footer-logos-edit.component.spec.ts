import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { FooterLogosEditComponent } from './footer-logos-edit.component';

describe('FooterLogosEditComponent', () => {
  let component: FooterLogosEditComponent;
  let router;
  let activatedRoute;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({})
    };
    apiClientService = {
      footerLogo: jasmine.createSpy('footerLogo').and.returnValue({
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

    component = new FooterLogosEditComponent(
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
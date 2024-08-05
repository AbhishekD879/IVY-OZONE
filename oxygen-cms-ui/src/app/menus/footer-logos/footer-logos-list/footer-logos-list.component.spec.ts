import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { FooterLogosListComponent } from './footer-logos-list.component';

describe('FooterLogosListComponent', () => {
  let component: FooterLogosListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;

  beforeEach(() => {
    apiClientService = {
      footerLogo: jasmine.createSpy('connectMenu').and.returnValue({
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

    component = new FooterLogosListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router);
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();

    expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.footerLogo);
    expect(apiClientService.footerLogo).toHaveBeenCalled();
    expect(component.footerLogos).toBeDefined();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  }));
});

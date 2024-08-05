import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { BankingMenusListComponent } from './banking-menus-list.component';

describe('BankingMenusListComponent', () => {
  let component: BankingMenusListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;

  beforeEach(() => {
    apiClientService = {
      bankingMenu: jasmine.createSpy('bankingMenu').and.returnValue({
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

    component = new BankingMenusListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router);
  });

  describe('ngOnInit', () => {
    it('should show loader', fakeAsync(() => {
      component.ngOnInit();

      tick();

      expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.bankingMenu);
    }));

    it('should hide loader', fakeAsync(() => {
      component.ngOnInit();

      tick();

      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    }));

    it('should init data for banking menus', fakeAsync(() => {
      component.ngOnInit();

      tick();

      expect(component.bankingMenus).toBeDefined();
    }));
  });
});

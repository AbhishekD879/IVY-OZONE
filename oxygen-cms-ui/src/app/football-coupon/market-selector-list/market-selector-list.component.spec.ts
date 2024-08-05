import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable } from 'rxjs/Observable';
import { Order } from '@app/client/private/models/order.model';

import { MarketSelectorListComponent } from './market-selector-list.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { MarketSelector } from '@app/client/private/models/marketselector.model';
import { AppConstants } from '@app/app.constants';

describe('MarketSelectorListComponent', () => {
  let component: MarketSelectorListComponent;
  const marketSelector: MarketSelector = {
    title: 'Title1',
    id: 1
  } as any;

  let apiClientService;
  let dialogService: Partial<DialogService>;
  let globalLoaderService: Partial<GlobalLoaderService>;
  let snackBar: Partial<MatSnackBar>;

  beforeEach(() => {
    snackBar = {
      open: jasmine.createSpy('open')
    };
    dialogService = {
      showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((dialogComponent, {
        width, title, yesOption, noOption, yesCallback
      }) => {
        yesCallback();
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    apiClientService = {
      marketSelector: jasmine.createSpy('marketSelector').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(Observable.of({ body: [marketSelector] })),
        add: jasmine.createSpy('add').and.returnValue(Observable.of({ body: marketSelector })),
        delete: jasmine.createSpy('delete').and.returnValue(Observable.of({ body: {} })),
        reorder: jasmine.createSpy('reorder').and.returnValue(Observable.of({ body: {} }))
      })
    };

    component = new MarketSelectorListComponent(
      apiClientService as any,
      dialogService as any,
      globalLoaderService as any,
      snackBar as any
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('#ngOnInit should get market selectors', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector).toHaveBeenCalled();
    expect(apiClientService.marketSelector().findAllByBrand).toHaveBeenCalled();
    expect(component.marketSelectors).toEqual([marketSelector]);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#ngOnInit should handle error', () => {
    apiClientService.marketSelector().findAllByBrand.and.returnValue(Observable.throw({}));

    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.marketSelectors).not.toEqual([marketSelector]);
  });

  it('#createMarketSelector should show dialog and create market selector', () => {
    component.marketSelectors = [];
    component.createMarketSelector();
    expect(dialogService.showCustomDialog).toHaveBeenCalled();
    expect(component.marketSelectors).toEqual([marketSelector]);
  });

  it('#removeHandler should remove market selector from list', () => {
    component.marketSelectors = [marketSelector];
    component.removeHandler(marketSelector);
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Coupon Market Selector',
      message: 'Are You Sure You Want to Remove Market Selector?',
      yesCallback: jasmine.any(Function)
    });
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.marketSelector().delete).toHaveBeenCalledWith(marketSelector.id);
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.marketSelectors).toEqual([]);
  });

  it('#removeHandler should handle error', () => {
    apiClientService.marketSelector().delete.and.returnValue(Observable.throw({}));
    component.marketSelectors = [marketSelector];
    component.removeHandler(marketSelector);

    expect(component.marketSelectors).toEqual([marketSelector]);
  });

  it('#reorderHandler ', () => {
    const newOrder: Order = {
      order: ['1', '3', '2'],
      id: '5'
    };
    component.reorderHandler(newOrder);
    expect(apiClientService.marketSelector().reorder).toHaveBeenCalledWith(newOrder);
    expect(snackBar.open).toHaveBeenCalledWith(`Market selector order saved!`, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  });
});

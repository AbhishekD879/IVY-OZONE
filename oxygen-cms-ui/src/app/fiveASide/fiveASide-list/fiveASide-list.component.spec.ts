import { MatSnackBar } from '@angular/material/snack-bar';
import {Observable} from 'rxjs/Observable';

import {FiveASideListComponent} from './fiveASide-list.component';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {FiveASideFormation} from '@app/client/private/models/fiveASideFormation.model';
import {FiveASideApiService} from '@app/fiveASide/services/fiveASide.api.service';

describe('MarketSelectorListComponent', () => {
  let component: FiveASideListComponent;
  const fiveASideFormation: FiveASideFormation = {
    title: 'Title1',
    id: 1
  } as any;

  let apiClientService;
  let fiveASideApiService: Partial<FiveASideApiService>;
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

    fiveASideApiService = {
      getFormationsList: jasmine.createSpy('getFormationsList').and.returnValue(Observable.of({ body: [fiveASideFormation] })),
      deleteFormation: jasmine.createSpy('deleteFormation').and.returnValue(Observable.of({ id: '123' }))
    };

    apiClientService = {
      marketSelector: jasmine.createSpy('marketSelector').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(Observable.of({ body: [fiveASideFormation] })),
        add: jasmine.createSpy('add').and.returnValue(Observable.of({ body: fiveASideFormation })),
        delete: jasmine.createSpy('delete').and.returnValue(Observable.of({ body: {} })),
        reorder: jasmine.createSpy('reorder').and.returnValue(Observable.of({ body: {} }))
      }),

      fiveASideFormations: jasmine.createSpy('fiveASideFormations').and.returnValue(fiveASideApiService)
    };

    component = new FiveASideListComponent(
      fiveASideApiService as any,
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
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#ngOnInit should handle error', () => {
    apiClientService.marketSelector().findAllByBrand.and.returnValue(Observable.throw({}));

    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it('#removeHandler should remove formation from list', () => {
    component.ngOnInit();
    component.removeHandler(fiveASideFormation);
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: '5 A Side Formation',
      message: 'Are You Sure You Want to Remove Formation?',
      yesCallback: jasmine.any(Function)
    });
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    expect(component.fiveASideFormations).toEqual([]);
  });

  it('#removeHandler should handle error', () => {
    apiClientService.marketSelector().delete.and.returnValue(Observable.throw({}));
    component.fiveASideFormations = [fiveASideFormation];
    component.removeHandler(fiveASideFormation);

    expect(component.fiveASideFormations).toEqual([]);
  });
});

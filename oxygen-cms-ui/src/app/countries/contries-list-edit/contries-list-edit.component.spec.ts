import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { ContriesListEditComponent } from './contries-list-edit.component';

describe('ContriesListEditComponent', () => {
  let component: ContriesListEditComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;

  beforeEach(() => {
    apiClientService = {
      country: jasmine.createSpy('country').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({}))
      })
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};

    component = new ContriesListEditComponent(
      apiClientService,
      globalLoaderService,
      dialogService);
  });

  it('ngOnInit', fakeAsync(() => {
    spyOn<any>(component, 'loadInitialData').and.callThrough();

    component.ngOnInit();
    tick();

    expect(component['loadInitialData']).toHaveBeenCalled();
  }));
});

import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { OlympicsPagesListPageComponent } from './olympics.page.component';

describe('OlympicsPagesListPageComponent', () => {
  let component: OlympicsPagesListPageComponent;
  let dialogService;
  let olympicsAPIService;
  let snackBar;

  beforeEach(() => {
    dialogService = {};
    olympicsAPIService = {
      getOlympicsListData: jasmine.createSpy('getOlympicsListData').and.returnValue(of({
        body: []
      }))
    };
    snackBar = {};

    component = new OlympicsPagesListPageComponent(
      dialogService,
      olympicsAPIService,
      snackBar);
  });

  it('ngOnInit', fakeAsync(() => {
    component.ngOnInit();
    tick();

    expect(olympicsAPIService.getOlympicsListData).toHaveBeenCalled();
    expect(component.olympicsPagesData).toBeDefined();
  }));
});

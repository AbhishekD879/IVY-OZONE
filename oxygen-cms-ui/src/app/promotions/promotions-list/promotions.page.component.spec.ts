import { async } from '@angular/core/testing';
import {PromotionsPageComponent} from './promotions.page.component';
import { of } from 'rxjs';

describe('PromotionsPageComponent', () => {
  let component,
    snackBar,
    router,
    dialogService,
    apiClientService,
    promotionsAPIService,
    globalLoaderService;

  beforeEach(async(() => {
    snackBar = {};
      router = {};
      dialogService = {};
      apiClientService = {};
      promotionsAPIService = {
        getPromotionsData: jasmine.createSpy('getPromotionsData').and.returnValue(of({
          body: []
        })),
        getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of({
          body: []
        }))
      };
      globalLoaderService = {};

    component = new PromotionsPageComponent(
      snackBar,
      router,
      dialogService,
      apiClientService,
      promotionsAPIService,
      globalLoaderService,
    );

    component.ngOnInit();
  }));


  it('should init', () => {
    expect(promotionsAPIService.getPromotionsData).toHaveBeenCalled();
    expect(promotionsAPIService.getSportCategories).toHaveBeenCalled();
    expect(component.promotionsData).toBeDefined();
  });
});

import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { CreateEdpMarketComponent } from './create-edp-market.component';

describe('CreateEdpMarketComponent', () => {
  let component: CreateEdpMarketComponent;
  let dialogRef;
  let brandService;
  let apiClientService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};
    apiClientService = {
      edp: jasmine.createSpy('edp').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({
          body: [{
            name: ''
          }]
        }))
      })
    };

    component = new CreateEdpMarketComponent(dialogRef, brandService, apiClientService);
  });

  describe('ngOnInit', () => {
    it('should call apiClientService.edp', fakeAsync(() => {
      component.ngOnInit();

      tick();

      expect(apiClientService.edp).toHaveBeenCalled();
    }));

    it('should init edpMarket', () => {
      component.ngOnInit();

      expect(component.edpMarket).toBeDefined();
    });
  });
});

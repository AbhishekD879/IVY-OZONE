import { BannersAutocompleteComponent } from './banners-autocomplete.component';
import { of } from 'rxjs';

describe('BannersAutocompleteComponent', () => {
  let component,
    apiClientService;

  beforeEach(() => {
    apiClientService = {
      betReceiptMobileBanner: jasmine.createSpy('betReceiptMobileBanner').and.returnValue({
        findAllByBrand: jasmine.createSpy('betReceiptMobileBanner.findAllByBrand').and.returnValue(of({
          body: []
        }))
      })
    };

    component = new BannersAutocompleteComponent(
      apiClientService
    );

    component.type = 'Mobile';
    component.ngOnInit();
  });

  it('should create', () => {
    expect(apiClientService.betReceiptMobileBanner).toHaveBeenCalled();

    expect(component.banners).toBeDefined();
  });
});

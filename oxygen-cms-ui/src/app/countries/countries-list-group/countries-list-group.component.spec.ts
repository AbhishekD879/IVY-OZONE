import { CountriesListGroupComponent } from './countries-list-group.component';

describe('CountriesListGroupComponent', () => {
  let component: CountriesListGroupComponent;

  beforeEach(() => {
    component = new CountriesListGroupComponent();
  });

  describe('get data', () => {
    beforeEach(() => {
      component.countries = [
        { val: 'a', label: 'A'},
        { val: 'b', label: 'B'},
      ] as any;
    });

    it('should return countries array', () => {
      component.searchField = '';

      expect(component.data).toEqual(component.countries);
    });

    it('should return filtered country code', () => {
      component.searchField = 'a';

      expect(component.data).toEqual([component.countries[0]]);
    });
  });
});

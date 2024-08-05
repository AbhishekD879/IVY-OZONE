import { BtnOddsComponent } from './btn-odds.component';

describe('BtnOddsComponent', () => {
  let component;

  beforeEach(() => {
    component = new BtnOddsComponent();
  });

  describe('ngOnInit', () => {
    it('should set emptyPriceLabel to "-.-"', () => {
      component.oddsFormat = 'dec';

      component.ngOnInit();

      expect(component.emptyPriceLabel).toEqual('-.-');
    });

    it('should set emptyPriceLabel to "-/-"', () => {
      component.oddsFormat = 'frac';

      component.ngOnInit();

      expect(component.emptyPriceLabel).toEqual('-/-');
    });
  });
});

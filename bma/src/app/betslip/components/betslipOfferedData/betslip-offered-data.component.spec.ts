import { BetslipOfferedDataComponent } from './betslip-offered-data.component';

describe('BetslipOfferedDataComponent', () => {
  let component, fracToDecService;

  beforeEach(() => {
    fracToDecService = {
      getFormattedValue: jasmine.createSpy().and.returnValue('3/2'),
    };

    component = new BetslipOfferedDataComponent(fracToDecService);
    component.isOddsChanged = true;
    component.oldPrice = [{
      price: {
        priceNum: '3',
        priceDen: '2'
      }
    }];
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('isSp is true', () => {
      component.isSp = true;
      component.price = 'foo';

      component.ngOnInit();
      expect(component.oldPriceText).toBe('foo');
    });

    it('should not assign oldPriceText when no priceNum and priceDen where found', () => {
      component.isSp = false;
      component.oldPrice = [{ price: {} }];

      component.ngOnInit();
      expect(component.oldPriceText).toBeUndefined();
    });

    it('should call getFormattedValue', () => {

      component.ngOnInit();
      expect(component.fracToDecService.getFormattedValue).toHaveBeenCalledWith('3', '2');
    });

    it('isOddsChanged is false', () => {
      component.isOddsChanged = false;

      component.ngOnInit();
      expect(component.oldPriceText).toBe(undefined);
      expect(component.isPrevPriceSP).toBe(undefined);
      expect(component.isPriceChanged).toBe(false);
    });

    describe('isOddsTypeChanged SP => LP', () => {
      it('should set isPrevPriceSP true if current price is LP', () => {
        component.isOddsChanged = true;
        component.isSp = false;
        component.isOddsTypeChanged = true;
        component.price = '10/2';
        component.ngOnInit();

        expect(component.oldPriceText).toBeUndefined();
        expect(component.isPrevPriceSP).toBe(true);
        expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
      });

      it('should format current LP price if price type not changed', () => {
        component.isOddsChanged = true;
        component.isSp = false;
        component.isOddsTypeChanged = false;
        component.price = '10/2';
        component.ngOnInit();

        expect(component.oldPriceText).toBe('3/2');
        expect(component.isPrevPriceSP).toBeUndefined();
        expect(fracToDecService.getFormattedValue).toHaveBeenCalledWith(component.oldPrice[0].price.priceNum,
          component.oldPrice[0].price.priceDen);
      });
    });
  });

});

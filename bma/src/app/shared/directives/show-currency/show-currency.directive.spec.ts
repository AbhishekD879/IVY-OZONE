import { ShowCurrencyDirective } from '@shared/directives/show-currency/show-currency.directive';

describe('ShowCurrencyDirective', () => {
  let directive: ShowCurrencyDirective;

  beforeEach(() => {
    directive = new ShowCurrencyDirective();
    directive.showCurrency = {
      currency: 'AUD',
      value: 4567,
      limit: 4
    } as any;
    directive.isShowCurrency = false;
  });

  it('@isCurrencyValueOverflow', () => {
    expect(directive['isCurrencyValueOverflow']()).toBe(true);

    directive.showCurrency.limit = 10;
    expect(directive['isCurrencyValueOverflow']()).toBe(false);
  });

  describe('@ngOnChanges', () => {
    it('if no changes', () => {
      directive.ngOnChanges({ } as any);
      expect(directive.isShowCurrency).toBe(false);
    });

    it('if changes and no currency', () => {
      directive.showCurrency.currency = undefined;
      directive.ngOnChanges({ showCurrency: { } } as any);
      expect(directive.isShowCurrency).toBe(false);
    });

    it('if changes and no value', () => {
      directive.showCurrency.value = undefined;
      directive.ngOnChanges({ showCurrency: { } } as any);
      expect(directive.isShowCurrency).toBe(false);
    });

    it('if changes and overflow', () => {
      directive.showCurrency.limit = 10;
      directive.ngOnChanges({ showCurrency: { } } as any);
      expect(directive.isShowCurrency).toBe(true);
    });
  });
});

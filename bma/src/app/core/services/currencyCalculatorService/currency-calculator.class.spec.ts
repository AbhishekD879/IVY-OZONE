import { CurrencyCalculator } from './currency-calculator.class';

describe('CurrencyCalculator', () => {
  let calculator: CurrencyCalculator;

  const USD = '$';
  const EUR = '€';

  const rates: any = [
    { currency: USD, exchangeRate: '0.035' },
    { currency: EUR, exchangeRate: '0.031' }
  ];

  beforeEach(() => {
    calculator = new CurrencyCalculator(rates);
  });

  it('constructor', () => {
    expect(calculator).toBeTruthy();
    expect(calculator['rates']).toBe(rates);
  });

  it('currencyExchange', () => {
    expect( calculator.currencyExchange(USD, USD, 100) ).toBe('100.00');
    expect( calculator.currencyExchange(USD, EUR, 100) ).toBe('88.57');
    expect( calculator.currencyExchange(EUR, USD, 100) ).toBe('112.90');
  });

  it('getCurrencyRates', () => {
    expect(
      calculator['getCurrencyRates'](USD, USD)
    ).toEqual({ native: 0.035, tote: 1 });

    expect(
      calculator['getCurrencyRates'](USD, EUR)
    ).toEqual({ native: 0.031, tote: 0.035 });

    expect(
      calculator['getCurrencyRates'](EUR, USD)
    ).toEqual({ native: 0.035, tote: 0.031 });
  });
});

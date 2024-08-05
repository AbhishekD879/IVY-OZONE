import { PoolSizeComponent } from '@uktote/components/poolSize/pool-size.component';

describe('PoolSizeComponent', () => {
  let component: PoolSizeComponent;

  let coreToolsService,deviceService, user, currencyPipe;

  const currSymbStub = '£';

  beforeEach(() => {
    user = {};
    coreToolsService = { getCurrencySymbolFromISO: () => currSymbStub };
    currencyPipe = {
      transform: jasmine.createSpy().and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };

    component = new PoolSizeComponent(user, deviceService, coreToolsService, currencyPipe);
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  describe('getFormattedPoolSize', () => {
    beforeEach(() => {
      component.currencyCalculator = { currencyExchange: () => 431 } as any;
    });

    it(`should return 'poolSize' if user is NOT loggedIn`, () => {
      component.currentPool = { poolValue: 123 } as any;

      expect(component['getFormattedPoolSize']()).toEqual(`${123}${currSymbStub}`);
    });

    it(`should return null if user is NOT loggedIn and 'poolSize' is empty`, () => {
      component.currentPool = {}  as any;

      expect(component['getFormattedPoolSize']()).toBeNull();
    });

    it(`should return 'poolSize' if user is NOT loggedIn and 'userCurrency' is equal 'poolCurrency'`, () => {
      component['user'] = { currency: 'EUR' } as any;
      component.currentPool = { poolValue: 123, currencyCode: 'EUR' }  as any;

      expect(component['getFormattedPoolSize']())
        .toEqual(`${123}${currSymbStub}`);
    });

    it(`should return null if user is NOT loggedIn and 'poolSize' is empty and 'userCurrency' is equal 'poolCurrency'`, () => {
      component['user'] = { currency: 'EUR' } as any;
      component.currentPool = { currencyCode: 'EUR' }  as any;

      expect(component['getFormattedPoolSize']()).toBeNull();
    });

    it(`should return null if user is loggedIn and poolSize is empty`, () => {
      component['user'] = { status: true } as any;
      component.currentPool = {}  as any;

      expect(component['getFormattedPoolSize']()).toBeNull();
    });

    it(`should return 'calculatedPoolSize' with 'poolSize'`, () => {
      component['user'] = { status: true, currencySymbol: '€', currency: 'EUR' } as any;
      component.currentPool = { poolValue: 123 }  as any;

      expect(component['getFormattedPoolSize']()).toEqual('431€ / 123£');
    });

    it(`should call isnotLegEvents`, () => {
      component.currentPool = { poolType: 'UPLC' }  as any;
      expect(component['isnotLegEvents']()).toBeTrue();
    });

    it(`should return null if 'poolSize' is null`, () => {
      component['user'] = { status: true } as any;
      component.currentPool = { poolValue: null, currencyCode: 'EUR' } as any;

      expect(component['getFormattedPoolSize']()).toBeNull();
    });
  });
});

import { RacingSpecialsTabComponent } from '@racing/components/racingSpecialsTab/racing-specials-tab.component';
import { IMarket } from '@core/models/market.model';

describe('RacingSpecialsTabComponent', () => {
  let component: RacingSpecialsTabComponent;
  let smartBoostsService;
  let filtersService;
  let sbFiltersService;

  const testStr = 'TestString';
  const wasPriceStub = 'TestWasPrice';

  beforeEach(() => {
    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
    };
    filtersService = jasmine.createSpyObj(['date', 'orderBy']);
    sbFiltersService = jasmine.createSpyObj(['orderOutcomeEntities']);

    component = new RacingSpecialsTabComponent(filtersService, sbFiltersService, smartBoostsService);
  });

  describe('ngOnInit', () => {
    it('should transform SmartBoosts Market', () => {
      component.racing = {
        events: [{ markets: [{ outcomes: [{ name: '' }] }] }],
        classesTypeNames: {}
      }  as any;

      component.ngOnInit();

      expect(component.racing.events[0].markets[0].isSmartBoosts).toBeTruthy();
    });
  });

  describe('transformSmartBoostsMarket', () => {
    let marketStub;

    beforeEach(() => {
      marketStub = { outcomes: [{ name: '' }] } as IMarket;
    });

    it(`isSmartBoosts property should equal true if market is SmartBoosts`, () => {
      component['transformSmartBoostsMarket'](marketStub);
      expect(marketStub.isSmartBoosts).toBeTruthy();
    });

    it(`isSmartBoosts property should equal false if market is SmartBoosts`, () => {
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarket'](marketStub);
      expect(marketStub.isSmartBoosts).toBeFalsy();
    });

    it(`should change outcomes 'name' if market is SmartBoosts`, () => {
      marketStub.outcomes[0].name = '';
      component['transformSmartBoostsMarket'](marketStub);

      expect(marketStub.outcomes[0].name).toEqual(testStr);
    });

    it(`should set outcomes 'wasPrice' if market is SmartBoosts`, () => {
      delete marketStub.outcomes[0].wasPrice;
      component['transformSmartBoostsMarket'](marketStub);

      expect(marketStub.outcomes[0].wasPrice).toEqual(wasPriceStub);
    });

    it(`should Not change outcomes 'name' if market is Not SmartBoosts`, () => {
      marketStub.outcomes[0].name = '';
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarket'](marketStub);

      expect(marketStub.outcomes[0].name).toEqual('');
    });

    it(`should Not set outcomes 'wasPrice' if market is Not SmartBoosts`, () => {
      delete marketStub.outcomes[0].wasPrice;
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component['transformSmartBoostsMarket'](marketStub);
      expect(marketStub.outcomes[0].wasPrice).toBeUndefined();
    });

    it(`should Not set outcomes 'wasPrice' if parsedName has Not 'wasPrice'`, () => {
      component['smartBoostsService'].parseName = jasmine.createSpy().and.returnValue({ name: '' });

      component['transformSmartBoostsMarket'](marketStub);
      expect(marketStub.outcomes[0].wasPrice).toBeUndefined();
    });
  });
});

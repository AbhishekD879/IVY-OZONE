import { SportEventPageService } from "../../services/sportEventPage/sport-event-page.service";
import { IMarket } from "@core/models/market.model";

describe('SportEventPageService', () => {
    let service; 
    let filtersService;
    let smartBoostsService;
    const testStr = 'TestString';
    const wasPriceStub = 'TestWasPrice';

    beforeEach(() => {
        filtersService = {
            groupBy: jasmine.createSpy(),
            filterAlphabetsOnly: jasmine.createSpy('filterAlphabetsOnly').and.returnValue('filterAlphabetsOnly'),
            filterNumbersOnly: jasmine.createSpy('filterNumbersOnly').and.returnValue('filterNumbersOnly')
          };
      
          smartBoostsService = {
            isSmartBoosts: jasmine.createSpy().and.returnValue(true),
            parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
          };
        service = new SportEventPageService(filtersService, smartBoostsService);
    });

    describe('transformMarkets', ()=>{
      it(`isSmartBoosts property should equal true if market is SmartBoosts`, () => {
        const markets = [{ outcomes: [{ name: '' }] }] as IMarket[];
  
        service['transformMarkets'](markets);
        expect(markets[0].isSmartBoosts).toBeTruthy();
      });
  
      it(`should change outcomes 'name' if market is SmartBoosts`, () => {
        const markets = [{ outcomes: [{ name: '' }] }] as IMarket[];
  
        service['transformMarkets'](markets);
        expect(markets[0].outcomes[0].name).toEqual(testStr);
      });
  
      it(`should set outcomes 'wasPrice' if market is SmartBoosts`, () => {
        const markets = [{ outcomes: [{ name: '' }] }] as IMarket[];
  
        service['transformMarkets'](markets);
        expect(markets[0].outcomes[0].wasPrice).toEqual(wasPriceStub);
      });
  
      it(`should Not change outcomes 'name' if market is Not SmartBoosts`, () => {
        const markets = [{ outcomes: [{ name: '' }] }] as IMarket[];
        service['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);
  
        service['transformMarkets'](markets);
        expect(markets[0].outcomes[0].name).toEqual('');
      });
  
      it(`should Not set outcomes 'wasPrice' if market is Not SmartBoosts`, () => {
        const markets = [{ outcomes: [{ name: '' }] }] as IMarket[];
        service['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);
  
        service['transformMarkets'](markets);
        expect(markets[0].outcomes[0].wasPrice).toBeUndefined();
      });
  
      it(`should Not set outcomes 'wasPrice' if parsedName has Not 'wasPrice'`, () => {
        const markets = [{ outcomes: [{ name: '' }] }] as IMarket[];
        service['smartBoostsService'].parseName = jasmine.createSpy().and.returnValue({ name: '' });
  
        service['transformMarkets'](markets);
        expect(markets[0].outcomes[0].wasPrice).toBeUndefined();
      });
  
      it(`should set outcome alphabetName && numbersName`, () => {
        const markets = [{ viewType: 'WDW', outcomes: [{ name: '' }] }] as IMarket[];
        service['transformMarkets'](markets);
        expect(markets[0].outcomes[0].alphabetName).toEqual('filterAlphabetsOnly');
        expect(markets[0].outcomes[0].numbersName).toEqual('filterNumbersOnly');
      });
      it('should filter empty groupedOutcomes', ()=>{
        const markets = [{viewType: 'WDW', outcomes: [{name: '1'}]}] as IMarket[];
        filtersService.groupBy.and.returnValue([{name: '1'}]);
        service['transformMarkets'](markets);
        expect(markets[0].groupedOutcomes.length).toEqual(1);
      });
      it('When outcomes are empty', ()=>{
        const markets = [{}] as IMarket[];
        service['transformMarkets'](markets);
        expect(markets[0].isSmartBoosts).toBeTruthy();
      });
    });
  });
import { PriceOddsValueDirective } from '@shared/components/priceOddsButton/price-odds-value.directive';

describe('PriceOddsValueDirective', () => {
  let directive: PriceOddsValueDirective, fracToDecService, changeDetectorRef,
    priceOddsButtonService, pubSubService, coreToolsService;

  const outcome = {
    name: 'Outcome',
    id: '432234',
    prices: [{
      priceType: 'LP'
    }]
  } as any;

  const outcomeNoPrices = {
    name: 'Outcome',
    id: '432234'
  } as any;

  beforeEach(() => {
    fracToDecService = {
      getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('3/4')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    priceOddsButtonService = {
      isRacingOutcome: jasmine.createSpy('isRacingOutcome').and.returnValue(false)
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        SET_ODDS_FORMAT: 'SET_ODDS_FORMAT'
      }
    };
    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('uuid_value')
    };
    directive = new PriceOddsValueDirective(fracToDecService, changeDetectorRef,
      priceOddsButtonService, pubSubService, coreToolsService);
    directive.oddsPriceChange.emit = jasmine.createSpy('emit');
  });

  describe('@ngOnInit', () => {
    it('should set Price Odds value on Init', () => {
      directive.priceOddsValue = [outcome, 3, 4, 'LP'];
      directive.ngOnInit();
      expect(coreToolsService.uuid).toHaveBeenCalled();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('bet-432234-uuid_value', 'SET_ODDS_FORMAT', jasmine.any(Function));
      expect(directive.oddsPriceChange.emit).toHaveBeenCalledWith('3/4');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should set "SUSP" Price Odds value on Init', () => {
      directive.priceOddsValue = [outcomeNoPrices, 3, 4, 'LP'];
      directive.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('bet-432234-uuid_value', 'SET_ODDS_FORMAT', jasmine.any(Function));
      expect(directive.oddsPriceChange.emit).toHaveBeenCalledWith('SUSP');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should set "SP" Price Odds value on Init', () => {
      priceOddsButtonService.isRacingOutcome = jasmine.createSpy('isRacingOutcome').and.returnValue(true);
      directive.priceOddsValue = [outcome, 3, 4, 'LP'];
      directive.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalledWith('bet-432234-uuid_value', 'SET_ODDS_FORMAT', jasmine.any(Function));
      expect(directive.oddsPriceChange.emit).toHaveBeenCalledWith('SP');
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('@ngOnChanges', () => {
    it('should set Prices on OnChanges', () => {
      directive.priceOddsValue = [outcomeNoPrices, 3, 4, 'LP'];
      const changes = {
        priceOddsValue: {
          firstChange: false
        }
      } as any;
      directive.ngOnChanges(changes);
      expect(directive.oddsPriceChange.emit).toHaveBeenCalled();
    });

    it('should not set Prices on OnChanges', () => {
      const changes = {
        priceOddsValue: {
          firstChange: true
        }
      } as any;
      directive['setPrices'] = jasmine.createSpy('setPrices');
      directive.ngOnChanges(changes);
      expect(directive['setPrices']).not.toHaveBeenCalled();
    });
  });

  describe('@ngOnDestroy', () => {
    it('should destroy listeners', () => {
      directive.priceOddsValue = [outcome, 3, 4, 'LP'];
      directive.ngOnInit();
      directive.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('bet-432234-uuid_value');
    });
  });
});

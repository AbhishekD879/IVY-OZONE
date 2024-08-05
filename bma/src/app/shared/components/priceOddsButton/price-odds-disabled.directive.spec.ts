import { PriceOddsDisabledDirective } from '@shared/components/priceOddsButton/price-odds-disabled.directive';
import { IOutcomePrice } from '@core/models/outcome-price.model';

describe('PriceOddsDisabledDirective', () => {
  let directive: PriceOddsDisabledDirective, elementRef, priceOddsButtonService;

  const outcome = {
    name: 'Outcome',
    nonRunner: false,
    prices: [{
      priceType: 'LP'
    }]
  } as any;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        setAttribute: jasmine.createSpy('setAttribute'),
        removeAttribute: jasmine.createSpy('removeAttribute'),
        parentElement: {
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };
    priceOddsButtonService = {
      isRacingOutcome: jasmine.createSpy('isRacingOutcome').and.returnValue(false)
    };
    directive = new PriceOddsDisabledDirective(elementRef, priceOddsButtonService);
    directive.oddsPriceDisabled.emit = jasmine.createSpy('emit');
  });

  describe('@ngOnInit', () => {
    it('should set Status disabled on Init', () => {
      directive.priceOddsDisabled = [outcome, 'S', 'S', 'S', 'N', 'LP', {} as IOutcomePrice, true];
      directive.ngOnInit();
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('disabled', true);
      expect(directive.oddsPriceDisabled.emit).toHaveBeenCalledWith(false);
    });

    it('should set Status disabled', () => {
      const outcomeTest = {
        name: 'Outcome',
        nonRunner: true,
        prices: [{
          priceType: 'LP'
        }]
      } as any;
      directive.priceOddsDisabled = [outcomeTest, 'S', 'S', 'S', 'N', 'LP', {} as IOutcomePrice, false];
      directive.ngOnInit();
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('disabled', true);
      expect(elementRef.nativeElement.parentElement.classList.add).toHaveBeenCalledWith('disabled');
      expect(directive.oddsPriceDisabled.emit).toHaveBeenCalledWith(true);
    });

    it('should remove Status disabled on Init', () => {
      directive.priceOddsDisabled = [outcome, 'A', 'A', 'A', '', 'LP', {} as IOutcomePrice, false];
      directive.ngOnInit();
      expect(elementRef.nativeElement.removeAttribute).toHaveBeenCalledWith('disabled');
      expect(elementRef.nativeElement.parentElement.classList.remove).toHaveBeenCalledWith('disabled');
      expect(directive.oddsPriceDisabled.emit).toHaveBeenCalledWith(false);
    });

    it('should remove Status disabled on Init if it is Racing Outcome', () => {
      const outcomeTest = {
        name: 'Outcome'
      } as any;
      priceOddsButtonService.isRacingOutcome = jasmine.createSpy('isRacingOutcome').and.returnValue(true);
      directive.priceOddsDisabled = [outcomeTest, 'A', 'A', 'A', '', 'SP, LP', {} as IOutcomePrice, false];
      directive.ngOnInit();
      expect(elementRef.nativeElement.removeAttribute).toHaveBeenCalledWith('disabled');
    });
  });

  describe('@ngOnChanges', () => {
    it('should set Status disabled on OnChanges', () => {
      const changes = {
        priceOddsDisabled: {
          firstChange: false
        }
      } as any;
      directive.priceOddsDisabled = [outcome, 'S', 'S', 'S', '', 'LP', {} as IOutcomePrice, false];
      directive.ngOnChanges(changes);
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('disabled', true);
    });

    it('should not set Status disabled on OnChanges', () => {
      const changes = {
        priceOddsDisabled: {
          firstChange: true
        }
      } as any;
      directive['setStatus'] = jasmine.createSpy('setStatus');
      directive.ngOnChanges(changes);
      expect(directive['setStatus']).not.toHaveBeenCalled();
    });
  });

  it('should set status', () => {
    directive.priceOddsDisabled = [outcome, 'S', 'S', 'S', '', 'LP', {} as IOutcomePrice, false];
    directive['setStatus']();

    expect(directive.outcome).toEqual(outcome);
    expect(directive.outcomeStatusCode).toEqual('S');
    expect(directive.marketStatusCode).toEqual('S');
    expect(directive.eventStatusCode).toEqual('S');
    expect(directive.eventDisplayed).toEqual('');
    expect(directive.priceTypeCodes).toEqual('LP');
    expect(directive.prices).toEqual({} as IOutcomePrice);
    expect(directive.isRacing).toEqual(false);
  });
});

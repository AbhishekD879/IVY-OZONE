import { IOutcomePrice } from '@core/models/outcome-price.model';
import { SBPriceOddsDisabledDirective } from './sb-price-odds-disabled.directive';

describe('SBPriceOddsDisabledDirective', () => {
  let directive: SBPriceOddsDisabledDirective, elementRef, priceOddsButtonService;

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
    directive = new SBPriceOddsDisabledDirective(elementRef, priceOddsButtonService);
    directive.sboddsPriceDisabled.emit = jasmine.createSpy('emit');
  });

  describe('@ngOnInit', () => {
    it('should set Status disabled on Init', () => {
      directive.sbpriceOddsDisabled = [outcome, 'S', 'S', 'S', 'N', 'LP', {} as IOutcomePrice, true];
      directive.ngOnInit();
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('disabled', true);
      expect(directive.sboddsPriceDisabled.emit).toHaveBeenCalledWith(true);
    });

    it('should set Status active , event not displayed on Init - isRacing true', () => {
      outcome.nonRunner = true;
      directive.sbpriceOddsDisabled = [outcome, 'A', 'A', 'A', 'N', 'LP', {} as IOutcomePrice, true];
      directive.ngOnInit();
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('disabled', false);
      expect(directive.sboddsPriceDisabled.emit).toHaveBeenCalledWith(false);
    });

    it('should set Status active , event not displayed on Init ', () => {
      outcome.nonRunner = true;
      directive.sbpriceOddsDisabled = [outcome, 'A', 'A', 'A', 'N', 'LP', {} as IOutcomePrice, false];
      directive.ngOnInit();
      expect(elementRef.nativeElement.parentElement.classList.add).toHaveBeenCalledWith('disabled');
      expect(directive.sboddsPriceDisabled.emit).toHaveBeenCalledWith(true);
    });

    it('should set Status disabled', () => {
      const outcomeTest = {
        name: 'Outcome',
        nonRunner: true,
        prices: [{
          priceType: 'LP'
        }]
      } as any;
      directive.sbpriceOddsDisabled = [outcomeTest, 'S', 'S', 'S', 'N', 'LP', {} as IOutcomePrice, false];
      directive.ngOnInit();
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('disabled', true);
      expect(elementRef.nativeElement.parentElement.classList.add).toHaveBeenCalledWith('disabled');
      expect(directive.sboddsPriceDisabled.emit).toHaveBeenCalledWith(true);
    });

    it('should remove Status disabled on Init', () => {
      outcome.nonRunner = false;
      directive.sbpriceOddsDisabled = [outcome, 'A', 'A', 'A', '', 'LP', {} as IOutcomePrice, false];
      directive.ngOnInit();
      expect(elementRef.nativeElement.removeAttribute).toHaveBeenCalledWith('disabled');
      expect(elementRef.nativeElement.parentElement.classList.remove).toHaveBeenCalledWith('disabled');
      expect(directive.sboddsPriceDisabled.emit).toHaveBeenCalledWith(false);
    });

    it('should remove Status disabled on Init if it is Racing Outcome', () => {
      const outcomeTest = {
        name: 'Outcome'
      } as any;
      priceOddsButtonService.isRacingOutcome = jasmine.createSpy('isRacingOutcome').and.returnValue(true);
      directive.sbpriceOddsDisabled = [outcomeTest, 'A', 'A', 'A', '', 'SP, LP', {} as IOutcomePrice, false];
      directive.ngOnInit();
      expect(elementRef.nativeElement.removeAttribute).toHaveBeenCalledWith('disabled');
    });
  });

  describe('@ngOnChanges', () => {
    it('should set Status disabled on OnChanges', () => {
      const changes = {
        sbpriceOddsDisabled: {
          firstChange: false
        }
      } as any;
      directive.sbpriceOddsDisabled = [outcome, 'S', 'S', 'S', '', 'LP', {} as IOutcomePrice, false];
      directive.ngOnChanges(changes);
      expect(elementRef.nativeElement.setAttribute).toHaveBeenCalledWith('disabled', true);
    });

    it('should not set Status disabled on OnChanges', () => {
      const changes = {
        sbpriceOddsDisabled: {
          firstChange: true
        }
      } as any;
      directive['setStatus'] = jasmine.createSpy('setStatus');
      directive.ngOnChanges(changes);
      expect(directive['setStatus']).not.toHaveBeenCalled();
    });
  });

  it('should set status', () => {
    directive.sbpriceOddsDisabled = [outcome, 'S', 'S', 'S', '', 'LP', {} as IOutcomePrice, false];
    directive['isOddsDisabled'] = true;
    directive['isOddsDisabledAndNonRunner'] = true;
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

import { RacingOutcomeResultedCardComponent } from '@racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';
import { IToteOutcome } from '@core/models/outcome.model';
import { IRacingEvent } from '@core/models/racing-event.model';
import { IRacingMarket } from '@core/models/racing-market.model';

describe('RacingOutcomeResultedCardComponent', () => {
  let component: RacingOutcomeResultedCardComponent, outcome: IToteOutcome;
  let raceOutcomeDetailsService, filterService, fracToDecService, localeService: any;

  beforeEach(() => {
    outcome = {
      isFavourite: true,
      racingFormOutcome: {
        silkName: 'silk name'
      },
      name: 'outcome name',
      runnerNumber: '7',
      results: {
        position: 1,
        priceNum: 1,
        priceDen: 7
      }
    } as IToteOutcome;

    raceOutcomeDetailsService = {
      isNumberNeeded: jasmine.createSpy('isNumberNeeded').and.returnValue(true),
      isGreyhoundSilk: jasmine.createSpy('isGreyhoundSilk').and.returnValue(false),
      getSilkStyle: jasmine.createSpy('getSilkStyle').and.returnValue('')
    };
    filterService = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol').and.returnValue('nameWithoutLine'),
      numberSuffix: jasmine.createSpy('numberSuffix').and.returnValue('testSuffix')
    };
    fracToDecService = {
      getFormattedValue: jasmine.createSpy('getFormattedValue').and.returnValue('1/7')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('locale string')
    };

    component = new RacingOutcomeResultedCardComponent(
      raceOutcomeDetailsService as any,
      filterService as any,
      fracToDecService as any,
      localeService as any
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit with full data', () => {
    component['getRunnerName'] = jasmine.createSpy('getRunnerName').and.returnValue('runner name');
    component['getPositionWithSuffix'] = jasmine.createSpy('getPositionWithSuffix').and.returnValue('1st');
    component.outcomeEntity = outcome;
    component.marketEntity = {} as IRacingMarket;
    component.eventEntity = {} as IRacingEvent;

    component.ngOnInit();
    expect(component.isOutcomeCardAvailable).toEqual(true);
    expect(component.runnerNumberDisplay).toEqual(false);
    expect(component['getRunnerName']).toHaveBeenCalled();
    expect(component.runnerName).toEqual('runner name');
    expect(raceOutcomeDetailsService.isGreyhoundSilk).toHaveBeenCalledWith(component.marketEntity, component.outcomeEntity);
    expect(component.isGreyhoundSilk).toEqual(false);
    expect(raceOutcomeDetailsService.getSilkStyle).toHaveBeenCalledWith(component.marketEntity, component.outcomeEntity, '0');

    expect(component['getPositionWithSuffix']).toHaveBeenCalledTimes(1);
    expect(component.outcomePositionSufx).toEqual('1st');
    expect(fracToDecService.getFormattedValue).toHaveBeenCalledWith(1, 7);
    expect(component.oddsPrice).toEqual('1/7');
  });

  it('#ngOnInit with partial data', () => {
    component['getRunnerName'] = jasmine.createSpy('getRunnerName').and.returnValue('runner name');
    component['getPositionWithSuffix'] = jasmine.createSpy('getPositionWithSuffix').and.returnValue('1st');
    component.outcomeEntity = {} as any;
    component.marketEntity = {} as IRacingMarket;
    component.eventEntity = {} as IRacingEvent;

    component.ngOnInit();
    expect(component.silkStyle).toEqual(undefined);
    expect(raceOutcomeDetailsService.getSilkStyle).not.toHaveBeenCalled();
    expect(component.outcomePositionSufx).toEqual(undefined);
    expect(component['getPositionWithSuffix']).not.toHaveBeenCalled();
    expect(component.oddsPrice).toEqual('');
    expect(fracToDecService.getFormattedValue).not.toHaveBeenCalled();
  });

  it('#nameWithoutLineSymbol should call filterService', () => {
    expect(component['nameWithoutLineSymbol']('input name')).toEqual('nameWithoutLine');
    expect(filterService.removeLineSymbol).toHaveBeenCalledWith('input name');
  });

  it('#getPositionWithSuffix should return suffix', () => {
    component.outcomeEntity = outcome;
    expect(component['getPositionWithSuffix']()).toEqual('1locale string');
    expect(filterService.numberSuffix).toHaveBeenCalledWith(1);
    expect(localeService.getString).toHaveBeenCalledWith('testSuffix');
  });

  it('#getPositionWithSuffix should return empty suffix', () => {
    component.outcomeEntity = { results: {} } as any;
    expect(component['getPositionWithSuffix']()).toEqual('-');
    expect(filterService.numberSuffix).not.toHaveBeenCalled();
    expect(localeService.getString).not.toHaveBeenCalled();
  });

  it('#getRunnerName should return runner name', () => {
    component.outcomeEntity = outcome;
    component['nameWithoutLineSymbol'] = jasmine.createSpy('nameWithoutLineSymbol')
      .and.returnValue('nameWithoutLine');
    component.raceType = '';

    expect(component['getRunnerName']()).toEqual('nameWithoutLine');
    expect(component['nameWithoutLineSymbol']).toHaveBeenCalledWith('outcome name');

    component.raceType = 'HORSE_RACING';
    expect(component['getRunnerName']()).toEqual('nameWithoutLine');
    expect(component['nameWithoutLineSymbol']).toHaveBeenCalledWith('outcome name');

    component.outcomeEntity.isFavourite = false;
    expect(component['getRunnerName']()).toEqual('7 - nameWithoutLine');
    expect(component['nameWithoutLineSymbol']).toHaveBeenCalledWith('outcome name');
  });
});

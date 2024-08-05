import { RacingOutcomeCardComponent } from '@racing/components/racingOutcomeCard/racing-outcome-card.component';
import { IToteOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';

describe('RacingOutcomeCardComponent', () => {
  let component: RacingOutcomeCardComponent;
  let raceOutcomeData;
  let filterService;
  let gtmService;

  beforeEach(() => {
    raceOutcomeData = {
      isNumberNeeded: jasmine.createSpy().and.returnValue(true)
    };
    filterService = {};
    gtmService = {
      push: jasmine.createSpy('push')
    };
    component = new RacingOutcomeCardComponent(raceOutcomeData, filterService, gtmService);
    component.outcomeEntity = {} as any;
    component.outcomIndex = 1;
  });

  it('ngOnInit', () => {
    component.outcomeEntity = {
      isFavourite: true
    } as IToteOutcome;
    component.marketEntity = {} as IMarket;
    component.eventEntity = {} as ISportEvent;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();
    expect(component.isOutcomeCardAvailable).toEqual(true);
    expect(component.runnerNumberDisplay).toEqual(false);
  });

  describe('getDefaultSilk', () => {
    const event: any = {};
    it('When there is no racing form outcome and sportId is not equal to categoryId', () => {
      const outcome: any = {};
      event.sportId = '20';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(false);
    });

    it('When there is no racing form outcome and sportId is equal to categoryId', () => {
      const outcome: any = {};
      event.sportId = '21';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(true);
    });

    it('When there is racing form outcome and sportId is not equal to categoryId', () => {
      const outcome: any = { racingFormOutcome: { silkName: 'silkName' } };
      event.sportId = '20';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(false);
    });

    it('When there is racing form outcome and sportId is equal to categoryId', () => {
      const outcome: any = { racingFormOutcome: { silkName: 'silkName' } };
      event.sportId = '21';
      horseracingConfig.config.request.categoryId = '21';
      const expectedResult = component.getDefaultSilk(event, outcome);
      expect(expectedResult).toEqual(false);
    });
  });

  it('isAntepost should set false', () => {
    component.eventEntity = null;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();
    expect(component.isAntepostMarket).toBeFalsy();
  });

  it('isAntepost should set false', () => {
    component.eventEntity = {} as any;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();
    expect(component.isAntepostMarket).toBeFalsy();
  });

  it('isAntepost should set false', () => {
    component.eventEntity = {
      markets: []
    } as any;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();
    expect(component.isAntepostMarket).toBeFalsy();
  });

  it('isAntepost should set false', () => {
    component.eventEntity = {
      markets: [{}]
    } as any;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();
    expect(component.isAntepostMarket).toBeFalsy();
  });

  it('isAntepost should set false', () => {
    component.eventEntity = {
      markets: [{ isAntepost: 'false' }]
    } as any;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();
    expect(component.isAntepostMarket).toBeFalsy();
  });

  it('isAntepost should set true', () => {
    component.eventEntity = {
      markets: [{ isAntepost: 'true' }]
    } as any;
    component.marketEntity = {
      outcomes: []
    } as any;
    component.ngOnInit();
    expect(component.isAntepostMarket).toBeTruthy();
  });

  it('getSprites with silkName', () => {
    component.marketEntity = {
      outcomes: [{ racingFormOutcome: { silkName: 'silkName' } },
      { racingFormOutcome: { silkName: 'silkName2' } },
      { racingFormOutcome: { silkName: 'silkName2' } },
      { racingFormOutcome: { silkName: 'silkName1' } }
      ]
    } as any;
    component.getSprites();
  });

  it('getSprites without silkName', () => {
    component.marketEntity = {
      outcomes: []
    } as any;
    component.getSprites();
  });

  it('nameWithoutNonRunner should call removenNonRunnerFromHorseName method', () => {
    filterService.removenNonRunnerFromHorseName = jasmine.createSpy('removenNonRunnerFromHorseName');
    component.nameWithoutNonRunner('test');
    expect(filterService.removenNonRunnerFromHorseName).toHaveBeenCalledWith('test');
  });

  it('nameWithoutLineSymbol should call removeLineSymbol method', () => {
    filterService.removeLineSymbol = jasmine.createSpy('removeLineSymbol');
    component.nameWithoutLineSymbol('test');
    expect(filterService.removeLineSymbol).toHaveBeenCalledWith('test');
  });

  it('call onExpand when this.outcomeEntity.isFavourite and this.outcomeEntity.nonRunner is true ', () => {
    component.outcomeEntity.isFavourite = false;
    component.outcomeEntity.nonRunner = false;
    component.onExpand();
    expect(component.outcomIndex).toBe(1);
  });

  it('call onExpand when this.outcomeEntity.isFavourite and this.outcomeEntity.nonRunner is true ', () => {
    component.outcomeEntity.isFavourite = true;
    component.outcomeEntity.nonRunner = true;
    component.onExpand();
    expect(component.outcomIndex).toBe(1);
  });
});

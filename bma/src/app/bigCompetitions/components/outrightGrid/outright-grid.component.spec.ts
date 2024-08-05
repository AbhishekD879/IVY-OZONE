import { GridViewWidgetComponent } from '@app/bigCompetitions/components/outrightGrid/outright-grid.component';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('GridViewWidgetComponent', () => {

  let component: GridViewWidgetComponent;

  let templateService;
  let timeService;

  const market = {
    isEachWayAvailable: true,
    outcomes: [{}, {}, {}]
  } as IMarket;

  beforeEach(() => {
    templateService = {
      genTerms: jasmine.createSpy().and.returnValue('terms')
    };
    timeService = {
      formatByPattern: jasmine.createSpy().and.returnValue('formatted')
    };

    component = new GridViewWidgetComponent(templateService, timeService);
    component.market = market;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.maxDisplay = 5;
    component.ngOnInit();
    expect(component.limit).toBe(component.maxDisplay);
    expect(component.outcomesCount).toBe(component.market.outcomes.length);
    expect(component.market.terms).toBe('TERMS');
    expect(templateService.genTerms).toHaveBeenCalledWith(component.market);
  });

  it('#ngOnInit when market.isEachWayAvailable = undefined', () => {
    component.market.isEachWayAvailable = undefined;
    component.ngOnInit();
    expect(templateService.genTerms).not.toHaveBeenCalled();
  });

  it('should return correct result and set properties', () => {
    component.limit = 2;
    const outcomes = [{}, {}, {}] as IOutcome[];
    const result = component.limitTo(outcomes);
    expect(component.outcomesCount).toBe(outcomes.length);
    expect(result.length).toBe(component.limit);
    expect(result[0]).toBe(outcomes[0]);
    expect(result[1]).toBe(outcomes[1]);
  });

  it('should return correct result and set properties when component.limit = 0', () => {
    component.limit = 0;
    const outcomes = [] as IOutcome[];
    const result = component.limitTo(outcomes);

    expect(result.length).toBe(component.limit);
    expect(result).toBe(outcomes);
  });

  it('should return correct result', () => {
    const outcome = { id: '17' } as IOutcome;
    const index = 3;
    expect(component.trackByFn(index, outcome)).toBe('317');
  });

  it('should set correct property value', () => {
    component.maxDisplay = 5;
    component.limit = null;
    component.expandSelections();
    expect(component.limit).toBe(component.maxDisplay);
  });

  it('should set correct property value', () => {
    component.limit = 5;
    component.expandSelections();
    expect(component.limit).toBeNull();
  });

  it('should return correct result', () => {
    component.eventEntity = {
      startTime: ''
    } as ISportEvent;
    component.market.terms = 'terms';
    expect(component.setHeader()).toBe('formatted');
  });

  it('should return correct result', () => {
    const date = new Date().toISOString();
    component.eventEntity = {
      startTime: date
    } as ISportEvent;
    component.market.terms = null;
    const date1 = new Date(date);
    expect(component.setHeader()).toBe('formatted');
    expect(timeService.formatByPattern).toHaveBeenCalledWith(date1, 'EEEE, dd-MMM-yy h:mm a');
  });

  it('should return correct result', () => {
    const participants = {
      HOME: {
        name: 'HOME TEAM',
        abbreviation: ''
      },
      AWAY: {
        name: 'AWAY TEAM',
        abbreviation: ''
      }
    };
    const result = component.getOutcomeName(participants);
    expect(result).toBe('HOME TEAM vs AWAY TEAM');
  });

  it('should return correct result', () => {
    const participants = {
      HOME: {
        name: 'HOME TEAM',
        abbreviation: ''
      },
      AWAY: null
    };
    const result = component.getOutcomeName(participants);
    expect(result).toBe('HOME TEAM');
  });

  it('should return true', () => {
    component.limit = 5;
    component.outcomesCount = 4;
    expect(component.isTwoColumns()).toBeTruthy();
  });

  it('should return true', () => {
    component.limit = 2;
    component.outcomesCount = 7;
    expect(component.isTwoColumns()).toBeTruthy();
  });

  it('should return true', () => {
    component.limit = 4;
    component.outcomesCount = 8;
    expect(component.isTwoColumns()).toBeTruthy();
  });
});

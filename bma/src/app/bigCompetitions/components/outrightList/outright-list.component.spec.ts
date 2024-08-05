import { ListViewWidgetComponent } from '@app/bigCompetitions/components/outrightList/outright-list.component';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('ListViewWidgetComponent', () => {

  let component: ListViewWidgetComponent;

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

    component = new ListViewWidgetComponent(templateService, timeService);
    component.market = market;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.maxDisplay = 3;
    component.ngOnInit();
    expect(component.limit).toBe(component.maxDisplay);
    expect(component.outcomesCount).toBe(component.market.outcomes.length);
    expect(component.market.terms).toBe('terms');
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
    const outcome = { id: '23' } as IOutcome;
    const index = 5;
    expect(component.trackByFn(index, outcome)).toBe('523');
  });

  it('should set correct property value', () => {
    component.maxDisplay = 2;
    component.limit = null;
    component.expandSelections();
    expect(component.limit).toBe(component.maxDisplay);
  });

  it('should set correct property value', () => {
    component.limit = 2;
    component.expandSelections();
    expect(component.limit).toBeNull();
  });

  it('should return correct result setHeaderDate', () => {
    component.eventEntity = {
      startTime: ''
    } as ISportEvent;
    component.market.terms = null;
    expect(component.setHeader()).toBe('formatted');
    expect(timeService.formatByPattern).toHaveBeenCalledWith(jasmine.any(Date), 'EEEE, dd-MMM-yy h:mm a');
  });
});

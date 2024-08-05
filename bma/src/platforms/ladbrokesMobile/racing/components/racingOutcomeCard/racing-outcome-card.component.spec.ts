import { LadbrokesRacingOutcomeCardComponent } from './racing-outcome-card.component';

describe('LadbrokesRacingOutcomeCardComponent', () => {
  let component: LadbrokesRacingOutcomeCardComponent;
  let gtmService;
  let filterService;
  let raceOutcomeData;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push')
    };
    filterService = {
      distance: jasmine.createSpy('distance').and.returnValue('test distance'),
      date: jasmine.createSpy('date').and.returnValue('2018-10-30')
    };
    raceOutcomeData = {
      isNumberNeeded: jasmine.createSpy('isNumberNeeded').and.returnValue(true),
      isGreyhoundSilk: jasmine.createSpy('isGreyhoundSilk').and.returnValue(false),
      getSilkStyle: jasmine.createSpy('getSilkStyle').and.returnValue('')
    };
    component = new LadbrokesRacingOutcomeCardComponent(
      raceOutcomeData,
      filterService,
      gtmService
    );
  });

  it('init', () => {
    component.outcomeEntity = {} as any;
    component.marketEntity = {
      outcomes: []
    } as any;

    component.isNotRacingSpecials = true;
    component.ngOnInit();
    expect(component.isNotGreyhoundSpecials).toEqual(true);

    component.isNotRacingSpecials = false;
    component.isGreyhoundEdp = true;
    component.ngOnInit();
    expect(component.isNotGreyhoundSpecials).toEqual(false);

    component.isNotRacingSpecials = false;
    component.isGreyhoundEdp = false;
    component.ngOnInit();
    expect(component.isNotGreyhoundSpecials).toEqual(true);
  });
});

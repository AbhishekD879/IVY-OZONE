import { LadbrokesDesktopRacingOutcomeCardComponent } from './racing-outcome-card.component';

describe('LadbrokesDesktopRacingOutcomeCardComponent', () => {
  let component: LadbrokesDesktopRacingOutcomeCardComponent ;
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

    component = new LadbrokesDesktopRacingOutcomeCardComponent(
      raceOutcomeData,
      filterService,
      gtmService
    );
  });
  it('isBFlag is true ', () => {
    component.courseDistanceWinners = ['CD'];
    let flag = component.isFlagsDisp(true, 'UTRI');
    expect(flag).toBeTruthy();
    component.courseDistanceWinners = ['CD', 'C'];
    flag = component.isFlagsDisp(false, 'UTRI');
    expect(flag).toBeTruthy();
    component.courseDistanceWinners = ['CD', 'C'];
    flag = component.isFlagsDisp(true, 'EXA');
    expect(flag).toBeFalsy();
  });
});

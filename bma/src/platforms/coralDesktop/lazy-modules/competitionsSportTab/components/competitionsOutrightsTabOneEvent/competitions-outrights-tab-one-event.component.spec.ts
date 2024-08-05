// eslint-disable-next-line max-len
import { CompetitionsOutrightsTabOneEventComponent } from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsOutrightsTabOneEvent/competitions-outrights-tab-one-event.component';

describe('#CompetitionsOutrightsTabOneEventComponent', () => {
  let component: CompetitionsOutrightsTabOneEventComponent;
  let sbFiltersService;
  let sportsEventHelperService;
  let templateService;
  let filtersService;

  beforeEach(() => {
    sportsEventHelperService = {};
    sbFiltersService = {};
    filtersService = {
      date: jasmine.createSpy('date')
    };
    templateService = {};

    component = new CompetitionsOutrightsTabOneEventComponent(
      sbFiltersService,
      sportsEventHelperService,
      templateService,
      filtersService
    );
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('getStartTime', () => {
    const event = <any>{
      startTime: '12:20'
    };
    component.getStartTime(event);
    expect(filtersService.date).toHaveBeenCalledWith('12:20', 'EEEE, d-MMM-yy hh:mm');
  });
});

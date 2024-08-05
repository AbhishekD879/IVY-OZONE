import {
  PrematchCardDetailsComponent
} from '@app/bigCompetitions/components/cardViewWidget/prematchCardDetails/prematch-card-details.component';

describe('PrematchCardDetailsComponent', () => {
  let component;
  let timeService;

  const event = {
    startTime : 'Mon Feb 11 2019 12:00:59 GMT+0200 (Eastern European Standard Time)'
  };

  beforeEach(() => {
    timeService = {
      getEventTime: jasmine.createSpy()
    };

    component = new PrematchCardDetailsComponent(timeService);
    component.event = event;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.ngOnInit();
    expect(timeService.getEventTime).toHaveBeenCalledWith(component.event.startTime);
  });
});

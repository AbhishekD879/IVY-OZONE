import { ToteEventsByMeetingComponent } from './tote-events-by-meeting.component';

describe('ToteEventsByMeetingComponent', () => {
  let component: ToteEventsByMeetingComponent, lpAvailabilityService;

  beforeEach(() => {
    lpAvailabilityService = {
      check: jasmine.createSpy('lpAvailabilityService.check').and.returnValue(true)
    };

    component = new ToteEventsByMeetingComponent(lpAvailabilityService);
  });

  it('ngOnInit', () => {
    component.meetings = [{id: 1}] as any;
    component.ngOnInit();

    expect(component.meetingsOrder).toEqual(['typeDisplayOrder', 'name']);
    expect(component.eventsOrder).toEqual(['localTime', 'typeName']);
    expect(component.meetings).toEqual( [ {id: 1}] as any );
  });

  it('ngOnInit (no meetings)', () => {
    component.ngOnInit();
    expect(component.meetings).toEqual([]);
  });

  it('isLpAvailable', () => {
    const eventMock = { id: '1' } as any;
    const result = component.isLpAvailable(eventMock);

    expect(lpAvailabilityService.check).toHaveBeenCalledWith(eventMock);
    expect(result).toBeTruthy();
  });
});

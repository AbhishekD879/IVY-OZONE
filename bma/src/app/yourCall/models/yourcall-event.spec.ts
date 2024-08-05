import { YourCallEvent } from './yourcall-event';

describe('#YourCallEvent', () => {
  let service: YourCallEvent;

  beforeEach(() => {
    service = new YourCallEvent(
      12345,
      123,
      16,
      'title',
      'homeTeam',
      'visitingTeam',
      'startDate',
      true,
      {
        isEnabledYCTab: true,
        isFiveASideAvailable: true,
        isFiveASideNewIconAvailable: true
      },
      {
        byb: true
      }
    );
  });

  it('should create model (getters)', () => {
    expect(service).toBeTruthy();
    // getters
    expect(service.obEventId).toEqual(12345);
    expect(service.isEnabledYCTab).toEqual(true);
    expect(service.isFiveASideAvailable).toEqual(true);
    expect(service.isFiveASideNewIconAvailable).toEqual(true);
    expect(service.title).toEqual('title');
    expect(service.hasPlayerProps).toEqual(true);
    expect(service.obSportId).toEqual(16);
    expect(service.homeTeam).toEqual({} as any);
    expect(service.visitingTeam).toEqual({} as any);
    expect(service.startDate).toEqual('startDate');
    expect(service.isActive).toEqual(false);
    expect(service.byb).toEqual({} as any);
  });

  it('should create model (setters)', () => {
    expect(service).toBeTruthy();
    // setters
    expect(service.isEnabledYCTab).toEqual(true);
    expect(service.isFiveASideAvailable).toEqual(true);

    service.isEnabledYCTab = false;
    service.isFiveASideAvailable = false;

    expect(service.isEnabledYCTab).toEqual(false);
    expect(service.isFiveASideAvailable).toEqual(false);
  });
});

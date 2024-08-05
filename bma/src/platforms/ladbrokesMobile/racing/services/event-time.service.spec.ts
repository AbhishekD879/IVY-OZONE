import { EventTimeService } from '@ladbrokesMobile/racing/services/event-time.service';

describe('RacingEventTimeService', () => {
  let service: any;
  const filterService: any = {
    date: jasmine.createSpy().and.returnValue('Monday 10 June 2019 - 3:00'),
    numberTranslatedSuffix: jasmine.createSpy().and.returnValue('th')
  };

  const eventMock = {
    startTime: 124098129857
  };

  beforeEach(() => {
    service = new EventTimeService(filterService);
  });

  describe('get event Date view from Service', () => {
    it('should getDate', () => {
      const result = service.getDate(eventMock);

      expect(filterService.date).toHaveBeenCalledWith(eventMock.startTime, 'EEEE d MMMM yyyy - HH:mm');
      expect(filterService.numberTranslatedSuffix).toHaveBeenCalledWith('10');

      expect(result).toEqual('Monday 10th June 2019 - 3:00');
    });
  });
});

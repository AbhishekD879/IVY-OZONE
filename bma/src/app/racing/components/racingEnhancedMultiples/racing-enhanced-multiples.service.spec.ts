import { throwError } from 'rxjs';
import { RacingEnhancedMultiplesService } from './racing-enhanced-multiples.service';

describe('RacingEnhancedMultiplesService', () => {
  let service;
  let enhancedMultiplesService;
  let filtersService;
  let timeService;

  beforeEach(() => {
    enhancedMultiplesService = {
      getRacingEnhancedMultiplesEvents:
        jasmine.createSpy('getRacingEnhancedMultiplesEvents').and.returnValue(throwError('errorTest')),
    };
    filtersService = {
      chainSort: jasmine.createSpy('chainSort')
    };
    timeService = {
      getEventTime: jasmine.createSpy('getEventTime').and.returnValue('21:30')
    };

    service = new RacingEnhancedMultiplesService(enhancedMultiplesService, filtersService, timeService);
  });

  describe('error path for racingEnhancedMultiplesService', () => {
    it('should store data subscription', () => {
      service.getEnhancedMultiplesEvents('test').subscribe((result) => {
        expect(enhancedMultiplesService.getRacingEnhancedMultiplesEvents).toHaveBeenCalledWith('test');
        expect(result).toEqual('errorTest');
      });
    });
  });

  describe('#sortOutcomesByDate', () => {
    it('should sort events by startTime', () => {
      service['sortOutcomesByDate']([] as any);

      expect(filtersService.chainSort).toHaveBeenCalledWith([], ['startTime']);
    });
  });

  it('setEventDate - should set Event Date', () => {
    const events = [{
      startTime: '2020-05-28T18:30:00Z',
      time: undefined,
      dateTime: undefined
    }] as any;

    service.setEventDate(events);

    expect(events).toEqual([{
      startTime: '2020-05-28T18:30:00Z',
      time: '21:30',
      dateTime: jasmine.any(String)
    }] as any);
  });
});

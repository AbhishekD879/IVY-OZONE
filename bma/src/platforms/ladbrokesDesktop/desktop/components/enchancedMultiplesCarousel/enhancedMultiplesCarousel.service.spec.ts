import { EnhancedMultiplesCarouselService } from './enhancedMultiplesCarousel.service';

describe('EnhancedMultiplesCarouselService', () => {
  let service: EnhancedMultiplesCarouselService;
  let enhancedMultiplesService;
  let filtersService;
  let timeService;

  beforeEach(() => {
    enhancedMultiplesService = {
      getEnhancedMultiplesEvents: jasmine.createSpy('getEnhancedMultiplesEvents')
    };
    timeService = {
      getEventTime: jasmine.createSpy('getEventTime').and.returnValue('21:30')
    };
    filtersService = {
      chainSort: jasmine.createSpy('chainSort')
    };

    service = new EnhancedMultiplesCarouselService(
      enhancedMultiplesService,
      filtersService,
      timeService
    );
  });

  it('should create service', () => {
    expect(service).toBeTruthy();
  });

  describe('#buildEnhancedMultiplesData', () => {
    it('should call buildEnhancedMultiplesData for horseracing', () => {
      const events = [{
        startTime: '2020-05-28T18:30:00Z',
        eventStatusCode: 'A'
      }] as any;
      filtersService.chainSort.and.returnValue(events);

      const result = service.buildEnhancedMultiplesData(events, 'horseracing');

      expect(result).toEqual(events);
    });

    it('should call buildEnhancedMultiplesData for horseracing for darts', () => {
      const events = [{
        startTime: '2020-05-28T18:30:00Z'
      }] as any;
      filtersService.chainSort.and.returnValue(events);


      const result = service.buildEnhancedMultiplesData(events, 'darts');

      expect(result).toEqual([{
        startTime: '2020-05-28T18:30:00Z'
      }] as any);
    });
  });

  it('should set Event Date', () => {
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

  it('should sort outcomes by date and name', () => {
    service['sortOutcomesByDateAndName']([{}, {}] as any);

    expect(service['filtersService'].chainSort).toHaveBeenCalledWith([{}, {}], [
      'categoryDisplayOrder',
      'startTime',
      'markets[0].outcomes[0].name',
      'name'
    ]);
  });

  it('should parse time', () => {
    service['parseTime']('1234');

    expect(service['timeService'].getEventTime).toHaveBeenCalledWith(jasmine.any(String));
  });

  it('should get Enhanced Multiples Events', () => {
    service['getEnhancedMultiplesEvents']('football');

    expect(service['enhancedMultiplesService'].getEnhancedMultiplesEvents).toHaveBeenCalledWith('football');
  });
});

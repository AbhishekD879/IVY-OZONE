import { SimpleFiltersService } from '@ss/services/simple-filters.service';

describe('SimpleFiltersService', () => {
  let service: SimpleFiltersService,
    timeService;

  beforeEach(() => {
    timeService = {
      getRacingTimeRangeForRequest: jasmine.createSpy('getRacingTimeRangeForRequest'),
      getTimeRangeForRequest: jasmine.createSpy('getTimeRangeForRequest'),
      roundTo30seconds: jasmine.createSpy('roundTo30seconds')
    };

    service = new SimpleFiltersService(timeService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('createFilterStrings', () => {
    it('should be defined', () => {
      expect(service.createFilterStrings).toBeDefined();
    });

    it('should return array of strings', () => {
      const value = 'eventStatusCode',
        dictionaryProp = ['simpleFilter=event.eventStatusCode:equals:'];

      expect(service.createFilterStrings(dictionaryProp, value)).toEqual(['simpleFilter=event.eventStatusCode:equals:eventStatusCode']);
    });

    it('should contain empty string instead of boolean value', () => {
      const dictionaryProp = ['externalKeys=event'];

      expect(service.createFilterStrings(dictionaryProp, true)).toEqual(dictionaryProp);
    });

    it('should contain comma in response array elements', () => {
      const dictionaryProp = ['simpleFilter=event.typeId:notEquals:'],
        typeId = ['1', '2', '3'];

      expect(service.createFilterStrings(dictionaryProp, typeId as any)[0]).toContain(',');
    });
  });

  describe('genFilters', () => {
    const params = { eventStatusCode: 'A' };

    it('should be defined', () => {
      expect(service.genFilters).toBeDefined();
    });

    it('should return string', () => {
      expect(service.genFilters(params)).toEqual('simpleFilter=event.eventStatusCode:equals:A');
    });

    it('should return empty string if params are not passed', () => {
      expect(service.genFilters()).toEqual('');
    });

    it('should not contain param in result if it is absent in dictionary', () => {
      const param = { customParam: 'Custom value' };

      expect(service.genFilters(param as any)).not.toContain(param.customParam);
    });
  });

  describe('getFilterParams', () => {
    const params = {
        suspendAtTime: '123',
        eventStatusCode: 'A',
        outcomeStatusCode: 'A'
      },
      filterLst = ['suspendAtTime', 'eventStatusCode'];

    it('should be defined', () => {
      expect(service.getFilterParams).toBeDefined();
    });

    it('should return empty object', () => {
      expect(service.getFilterParams({}, [])).toEqual({});
    });

    it('should return request object object', () => {
      expect(service.getFilterParams({}, [], true, false)).toEqual({});
    });

    it('should call genFilters once', () => {
      const result = service.getFilterParams(params, filterLst, true, false);

      expect(result).toEqual({
        simpleFilters: '&simpleFilter=event.suspendAtTime:greaterThan:123&simpleFilter=event.eventStatusCode:equals:A'
      });
    });

    it('should contain ampersand at the beginning', () => {
      const result = service.getFilterParams(params, filterLst, true, false);

      expect(result.simpleFilters.indexOf('&') === 0).toBe(true);
    });

    it('should contain ampersand at the end', () => {
      const result = service.getFilterParams(params, filterLst, false, true);

      expect(result.simpleFilters[result.simpleFilters.length - 1]).toEqual('&');
    });

    it('should call getRacingTimeRangeForRequest once in case isRacing is true', () => {
      service.getFilterParams({ isRacing: true }, []);

      expect(timeService.getRacingTimeRangeForRequest).toHaveBeenCalledTimes(1);
    });

    it('should call getTimeRangeForRequest once in other cases', () => {
      service.getFilterParams({}, []);

      expect(timeService.getTimeRangeForRequest).toHaveBeenCalledTimes(1);
    });

    it('should round startTime and endTime to 30 seconds', () => {
      const parameters = {
        startTime: '2019-02-10T13:00:00.000Z',
        endTime: '2019-02-11T13:02:33.123Z'
      };
      service.getFilterParams(parameters, []);

      expect(timeService.roundTo30seconds).toHaveBeenCalledTimes(2);
      expect(timeService.roundTo30seconds).toHaveBeenCalledWith('2019-02-11T13:02:33.123Z');
    });

    it('should Not round startTime and endTime to 30 seconds', () => {
      const parameters = {};
      service.getFilterParams(parameters, []);

      expect(timeService.roundTo30seconds).not.toHaveBeenCalled();
    });
  });
});

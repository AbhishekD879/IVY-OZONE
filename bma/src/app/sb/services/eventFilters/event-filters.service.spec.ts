import { EventFiltersService } from '@sb/services/eventFilters/event-filters.service';
import { ISportEvent } from '@core/models/sport-event.model';

describe('EventFiltersService', () => {
  let service: EventFiltersService;
  const eventStub = {
    eventIsLive: true,
    markets: [{ outcomes: [{ id: '1', prices: [{ id: '1' }] }, { id: '2' }] }]
  };
  const eventArr = [{
    eventIsLive: false,
    markets: [{ outcomes: [] }]
  }, eventStub, {}];

  let isFirstIteration: boolean = true;

  service = new EventFiltersService();
  const { started, hasOutcomes, hasPrices } = service['allFilters'];

  beforeEach(() => {
    if (isFirstIteration) { return; }
    service = new EventFiltersService();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
    isFirstIteration = false;
  });

  describe('applyFilters', () => {
    it('should apply filters', () => {
      const applyFilters = service.applyFilters(['started', 'hasPrices']);
      expect(applyFilters(eventArr)).toEqual([eventStub]);
    });
  });

  describe('filterEvents', () => {
    it(`should filter events by 'prices`, () => {
      expect(service.filterEvents([hasPrices], eventArr as ISportEvent[]))
        .toEqual([eventStub] as ISportEvent[]);
    });

    it(`should filter events by 'outcomes`, () => {
      expect(service.filterEvents([hasOutcomes], eventArr as ISportEvent[]))
        .toEqual([eventStub] as ISportEvent[]);
    });

    it(`should filter events by 'eventIsLive`, () => {
      expect(service.filterEvents([started], eventArr as ISportEvent[]))
        .toEqual([eventStub] as ISportEvent[]);
    });
  });

  describe('getFilters', () => {
    it('should return functions responsible of filters', () => {
      expect(service.getFilters(['hasPrices', 'hasPrices']))
        .toEqual([hasPrices, hasPrices]);
    });
  });

  describe('started', () => {
    it('should be Truthy if event is Live', () => {
      expect(started(eventStub as ISportEvent)).toBeTruthy();
    });

    it('should be Falsy if event is Not Live', () => {
      expect(started({ eventIsLive: false } as ISportEvent)).toBeFalsy();
    });
  });

  describe('hasOutcomes', () => {
    it('should be Truthy if event has Outcomes', () => {
      expect(hasOutcomes(eventStub as ISportEvent)).toBeTruthy();
    });

    it('should be Falsy if event has Not Outcomes', () => {
      expect(hasOutcomes({ markets: [] } as ISportEvent)).toBeFalsy();
    });
  });

  describe('hasPrices', () => {
    it('should be Truthy if event has Prices', () => {
      expect(hasPrices(eventStub as ISportEvent)).toBeTruthy();
    });

    it('should be Falsy if event has Not Prices', () => {
      expect(hasPrices({ markets: [] } as ISportEvent)).toBeFalsy();
    });
  });
});

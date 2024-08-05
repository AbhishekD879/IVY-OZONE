import { SiteServerEventToOutcomeService } from '@ss/services/site-server-event-to-outcome.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('SiteServerEventToOutcomeService', () => {
  let service: SiteServerEventToOutcomeService,
    buildUtility,
    simpleFilters,
    loadByPortions,
    ssRequestHelper;

  beforeEach(() => {
    ssRequestHelper = {
      getEventsByMarkets: jasmine.createSpy('getEventsByMarkets'),
      getEventToOutcomeForOutcome: jasmine.createSpy('getEventToOutcomeForOutcome')
    } as any;

    simpleFilters = {
      genFilters: jasmine.createSpy('genFilters')
    } as any;

    loadByPortions = {
      get: jasmine.createSpy('get').and.callFake(
        (method, reqparams, idsPropName, ids) => {
          method('test_data');

          return Promise.resolve({});
        }
      )
    } as any;

    buildUtility = {
      buildEventsWithRacingForm: jasmine.createSpy('buildEventsWithRacingForm'),
      buildEventsWithExternalKeys: jasmine.createSpy('buildEventsWithExternalKeys'),
      buildEvents: jasmine.createSpy('buildEvents')
    } as any;

    service = new SiteServerEventToOutcomeService(
      buildUtility,
      simpleFilters,
      loadByPortions,
      ssRequestHelper
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('getEventToOutcomeForMarket', () => {
    it('should call buildEventsWithRacingForm once in case of racingFormEvent or racingFormOutcome is present', fakeAsync(() => {
      service.getEventToOutcomeForMarket({ racingFormEvent: true, racingFormOutcome: true });

      tick();

      expect(buildUtility.buildEventsWithRacingForm).toHaveBeenCalledTimes(1);
    }));

    it('should call buildEvents once in other cases', fakeAsync(() => {
      service.getEventToOutcomeForMarket({});

      tick();

      expect(buildUtility.buildEvents).toHaveBeenCalledTimes(1);
    }));

    it('should call genFilters once', () => {
      const params = { racingFormEvent: true, racingFormOutcome: true };

      service.getEventToOutcomeForMarket(params);

      expect(simpleFilters.genFilters).toHaveBeenCalledTimes(1);
      expect(simpleFilters.genFilters).toHaveBeenCalledWith(params);
    });

    it('should call get once', () => {
      service.getEventToOutcomeForMarket({});

      expect(loadByPortions.get).toHaveBeenCalledTimes(1);
    });

    it('should call getEventsByMarkets once', () => {
      service.getEventToOutcomeForMarket({});

      expect(ssRequestHelper.getEventsByMarkets).toHaveBeenCalledTimes(1);
      expect(ssRequestHelper.getEventsByMarkets).toHaveBeenCalledWith('test_data');
    });
  });

  describe('getEventToOutcomeForOutcome', () => {
    const outcomesIds = [1, 2, 3];

    it('should call get once', () => {
      service.getEventToOutcomeForOutcome(outcomesIds);

      expect(loadByPortions.get).toHaveBeenCalledTimes(1);
    });

    it('should call getEventToOutcomeForOutcome once', () => {
      service.getEventToOutcomeForOutcome(outcomesIds);

      expect(ssRequestHelper.getEventToOutcomeForOutcome).toHaveBeenCalledTimes(1);
      expect(ssRequestHelper.getEventToOutcomeForOutcome).toHaveBeenCalledWith('test_data');
    });

    it('should call buildEventsWithExternalKeys once', fakeAsync(() => {
      service.getEventToOutcomeForOutcome(outcomesIds);

      tick();

      expect(buildUtility.buildEventsWithExternalKeys).toHaveBeenCalledTimes(1);
    }));

    it('should call buildEvents once', fakeAsync(() => {
      service.getEventToOutcomeForOutcome(outcomesIds);

      tick();

      expect(buildUtility.buildEvents).toHaveBeenCalledTimes(1);
    }));
  });
});

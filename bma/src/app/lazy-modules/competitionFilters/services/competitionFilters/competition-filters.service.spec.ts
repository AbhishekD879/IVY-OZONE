import { CompetitionFiltersService } from '@lazy-modules/competitionFilters/services/competitionFilters/competition-filters.service';
import { ISportConfigTab, ILeagueFilter } from '@core/services/cms/models/sport-config-tab.model';
import { FILTER_TYPES } from '@lazy-modules/competitionFilters/models/competition-filter';
import { of } from 'rxjs';

describe('CompetitionFiltersService', () => {
  let service: CompetitionFiltersService;
  let eventsBySections;
  let leagueFilter, timeFilter;
  let cmsService;
  let coreToolsService;
  let routingHelperService;

  const id = 'competitions';
  const tab: ISportConfigTab = {
    label: 'tab',
    id,
    filters: { league: [] }
  };

  const joc = data => jasmine.objectContaining(data);
  const groupByDate = (_eventsBySections) => {
    return _eventsBySections.map((eventsBySection, index) => {
      return {
        typeId: eventsBySection.typeId,
        groupedByDate: [{
          title: `group ${ index + 1 }`,
          events: eventsBySection.events
        }]
      };
    });
  };

  beforeEach(() => {
    const now = new Date(),
      hoursLater = (hours: number): string => {
        const later = new Date();
        later.setHours(now.getHours() + hours);
        return later.toJSON();
      };

    eventsBySections = [{
      typeId: '1',
      events: [
        { id: 11, startTime: hoursLater(8) },
        { id: 12, startTime: hoursLater(2) }
      ]
    }, {
      typeId: '2',
      events: [
        { id: 21, startTime: hoursLater(12) },
        { id: 22, startTime: hoursLater(4) }
      ]
    }, {
      typeId: '3',
      events: [
        { id: 31, startTime: hoursLater(10) },
        { id: 32, startTime: hoursLater(6) }
      ]
    }] as any;

    leagueFilter = { id: '1', active: true, name: 'Top League', type: 'League', value: [1, 3] };

    timeFilter = { id: '2', active: true, name: '2h', type: 'Time', value: 6 };

    coreToolsService = {
      deepClone: jasmine.createSpy('deepClone').and.callFake((arg) => JSON.parse(JSON.stringify(arg)))
    };
    routingHelperService ={
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('/event/teamA-teamB')
    }
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig')
    };

    service = new CompetitionFiltersService(cmsService, coreToolsService,routingHelperService);
  });

  describe('filterEvents', () => {
    let result;
    beforeEach(() => {
      spyOn(service as any, 'filterEventsByLeague').and.callThrough();
      spyOn(service as any, 'filterEventsByTime').and.callThrough();
    });

    describe('should return original eventsBySection array', () => {
      it('if no filters are available', () => {
        leagueFilter = null;
        timeFilter = null;
      });
      it('if no filters are provided', () => {
        leagueFilter.active = false;
        timeFilter.active = false;
      });
      afterEach(() => {
        result = service.filterEvents(leagueFilter, timeFilter, eventsBySections);

        expect(result).toEqual(eventsBySections);
        expect((service as any).filterEventsByTime).not.toHaveBeenCalled();
        expect((service as any).filterEventsByLeague).not.toHaveBeenCalled();
        expect(coreToolsService.deepClone).toHaveBeenCalledWith(eventsBySections);
      });
    });

    describe('should return events starting in selected time range', () => {
      describe('when filter of time type is enabled', () => {
        it('and league filter is not provided', () => {
          leagueFilter = null;
        });
        it('and league filter is disabled', () => {
          leagueFilter.active = false;
        });
        afterEach(() => {
          result = service.filterEvents(leagueFilter, timeFilter, eventsBySections);

          expect(result).toEqual([
            { typeId: '1', events: [joc({ id: 12 })] },
            { typeId: '2', events: [joc({ id: 22 })] },
            { typeId: '3', events: [joc({ id: 32 })] }
          ]);
          expect((service as any).filterEventsByTime).toHaveBeenCalled();
          expect((service as any).filterEventsByLeague).not.toHaveBeenCalled();
        });
      });

      it('when events are listed from groupedByDate', () => {
        const groupedByDate = groupByDate(eventsBySections);

        leagueFilter = null;

        result = service.filterEvents(leagueFilter, timeFilter, groupedByDate);

        const expected = [
          { typeId: '1', groupedByDate: [{ title: 'group 1', events: [joc({ id: 12 })] }] },
          { typeId: '2', groupedByDate: [{ title: 'group 2', events: [joc({ id: 22 })] }] },
          { typeId: '3', groupedByDate: [{ title: 'group 3', events: [joc({ id: 32 })] }] }
        ];

        expect(result).toEqual(expected);
        expect((service as any).filterEventsByTime).toHaveBeenCalled();
        expect((service as any).filterEventsByLeague).not.toHaveBeenCalled();
      });
    });

    describe('should return events of a selected league', () => {
      describe('when filter of league type is enabled', () => {
        it('and time filter is not provided', () => {
          timeFilter = null;
        });
        it('and time filter is disabled', () => {
          timeFilter.active = false;
        });
        afterEach(() => {
          result = service.filterEvents(leagueFilter, timeFilter, eventsBySections);

          expect(result).toEqual([
            { typeId: '1', events: [joc({ id: 11 }), joc({ id: 12 })] },
            { typeId: '3', events: [joc({ id: 31 }), joc({ id: 32 })] }
          ]);
          expect((service as any).filterEventsByLeague).toHaveBeenCalled();
          expect((service as any).filterEventsByTime).not.toHaveBeenCalled();
        });
      });
    });

    it('should return events of a selected league filtered by time if both filters are provided', () => {
      result = service.filterEvents(leagueFilter, timeFilter, eventsBySections);
      expect(result).toEqual([
        { typeId: '1', events: [joc({ id: 12 })] },
        { typeId: '3', events: [joc({ id: 32 })] }
      ]);
      expect((service as any).filterEventsByLeague).toHaveBeenCalledBefore((service as any).filterEventsByTime);
      expect((service as any).filterEventsByTime).toHaveBeenCalled();
    });

    it('should return empty array if no events match filter params', () => {
      leagueFilter.value = [3];
      timeFilter.value = 4;
      result = service.filterEvents(leagueFilter, timeFilter, eventsBySections);
      expect(result).toEqual([]);
      expect((service as any).filterEventsByLeague).toHaveBeenCalled();
      expect((service as any).filterEventsByTime).toHaveBeenCalled();
    });
  });

  describe('filterEventsByHiddenMarkets', () => {
    let result;

    beforeEach(() => {
      spyOn(service as any, 'filterByHiddenMarkets').and.callThrough();
    });

    describe('when market is selected', () => {
      beforeEach(() => {
        service.selectedMarket = 'selectedMarket';

        eventsBySections = eventsBySections.map((eventsBySection, index) => {
          return {
            typeId: eventsBySection.typeId,
            events: eventsBySection.events.map(event => {
              return {
                id: event.id,
                startTime: event.startTime,
                markets: [{
                  templateMarketName: index === 0 ? 'selectedMarket' : 'notSelectedMarket',
                  hidden: !(index % 2 === 0) // 0 and even index events have not hidden markets
                }]
              };
            })
          };
        });
      });

      it('should return grouped by date events filtered by hidden markets', () => {
        const groupedByDate = groupByDate(eventsBySections);

        result = service.filterEventsByHiddenMarkets(groupedByDate);

        expect(result).toEqual([
          { typeId: '1', groupedByDate: [{ title: 'group 1', events: [joc({ id: 11 }), joc({ id: 12 })] }] }
        ]);
      });

      it('should return raw events filtered by hidden markets', () => {
        result = service.filterEventsByHiddenMarkets(eventsBySections);

        expect(result).toEqual([
          { typeId: '1', events: [joc({ id: 11 }), joc({ id: 12 })] }
        ]);
      });
    });

    describe('when market is not selected', () => {
      it('should return same grouped by date events', () => {
        const groupedByDate = groupByDate(eventsBySections);

        result = service.filterEventsByHiddenMarkets(groupedByDate);

        expect(result).toEqual([
          { typeId: '1', groupedByDate: [{ title: 'group 1', events: [joc({ id: 11 }), joc({ id: 12 })] }] },
          { typeId: '2', groupedByDate: [{ title: 'group 2', events: [joc({ id: 21 }), joc({ id: 22 })] }] },
          { typeId: '3', groupedByDate: [{ title: 'group 3', events: [joc({ id: 31 }), joc({ id: 32 })] }] }
        ]);
      });

      it('should return same raw events', () => {
        result = service.filterEventsByHiddenMarkets(eventsBySections);

        expect(result).toEqual([
          { typeId: '1', events: [joc({ id: 11 }), joc({ id: 12 })] },
          { typeId: '2', events: [joc({ id: 21 }), joc({ id: 22 })] },
          { typeId: '3', events: [joc({ id: 31 }), joc({ id: 32 })] }
        ]);
      });
    });

    afterEach(() => {
      expect((service as any).filterByHiddenMarkets).toHaveBeenCalled();
    });
  });

  describe('formTimeFilters', () => {
    it('should return empty array if tab did not match or no time filters', () => {
      expect(service.formTimeFilters('competitions', [{ ...tab, id: '' }])).toEqual([]);
      expect(service.formTimeFilters('competitions', [{ ...tab, filters: {} as any }])).toEqual([]);
      expect(service.formTimeFilters('competitions', [{ ...tab, filters: { time: [] } as any }])).toEqual([]);
    });

    it('should return array of time filters with ids starting from league filters length', () => {
      const time: number[] = [1, 2, 3];

      expect(service.formTimeFilters('competitions', [{ ...tab, filters: { time } }], []))
        .toEqual([
          { id: '1', type: FILTER_TYPES.TIME, name: '1h', value: 1, active: false },
          { id: '2', type: FILTER_TYPES.TIME, name: '2h', value: 2, active: false },
          { id: '3', type: FILTER_TYPES.TIME, name: '3h', value: 3, active: false }
        ]);
    });
  });

  describe('formLeagueFilters', () => {
    it('should return empty array if tab did not match or no league filters', () => {
      expect(service.formLeagueFilters('competitions', [{ ...tab, id: '' }])).toEqual([]);
      expect(service.formLeagueFilters('competitions', [{ ...tab, filters: {} as any }])).toEqual([]);
      expect(service.formLeagueFilters('competitions', [{ ...tab, filters: { league: [] } as any }])).toEqual([]);
    });

    it('should return array of league filters', () => {
      const league: ILeagueFilter = { leagueName: 'Super League', leagueIds: [1, 2, 3] };

      expect(service.formLeagueFilters('competitions', [{ ...tab, filters: { league: [league] } }]))
        .toEqual([
          { id: '1', type: FILTER_TYPES.LEAGUE, name: league.leagueName, value: league.leagueIds, active: false }
        ]);
    });
  });

  describe('getSportEventFiltersAvailability', () => {
    it('should return `true` if key exists and set to true', (done: DoneFn) => {
      cmsService.getSystemConfig.and.returnValue(of({ FeatureToggle: { SportEventFilters: true } }));

      service.getSportEventFiltersAvailability()
        .subscribe((res: boolean) => {
          expect(res).toBeTruthy();
          done();
        });
    });

    it('should return `false` if filters key does note exist', (done: DoneFn) => {
      cmsService.getSystemConfig.and.returnValue(of({ FeatureToggle: {} }));

      service.getSportEventFiltersAvailability()
        .subscribe((res: boolean) => {
          expect(res).toBeFalsy();
          done();
        });
    });

    it('should return `false` if FeatureToggle key does not exist', (done: DoneFn) => {
      cmsService.getSystemConfig.and.returnValue(of({}));

      service.getSportEventFiltersAvailability()
        .subscribe((res: boolean) => {
          expect(res).toBeFalsy();
          done();
        });
    });

    afterEach(() => {
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
    });
  });
  describe('getSeoSchemaEvents', () => {
    const events = [{ id: 1 }] as any;
    it('should assgin url to the event to every event in the array', () => {
      const resultedEvents = service.getSeoSchemaEvents(events);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(events[0]);
      expect(resultedEvents).toEqual([{ id: 1, url: '/event/teamA-teamB' }] as any);
    });
    it('should not assgin url to the event to every event in the array', () => {
      const events = [];
      const resultedEvents = service.getSeoSchemaEvents(events);
      expect(routingHelperService.formEdpUrl).not.toHaveBeenCalledWith(events[0]);
      expect(resultedEvents).toEqual([]);
    });
    it('should not assgin url to the event to every event in the array', () => {
      const events = null;
      const resultedEvents = service.getSeoSchemaEvents(events);
      expect(resultedEvents).toEqual(null);
    });
  });
});

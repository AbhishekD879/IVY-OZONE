import { Injectable } from '@angular/core';
import { IGroupedByDateItem, ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FILTER_TYPES, ICompetitionFilter } from '@lazy-modules/competitionFilters/models/competition-filter';
import { ISportConfigTab, ILeagueFilter } from '@core/services/cms/models/sport-config-tab.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { IMarket } from '@core/models/market.model';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';

@Injectable({ providedIn: 'root' })
export class CompetitionFiltersService {
  selectedMarket: string;

  private readonly filtersKey: string = 'SportEventFilters';

  constructor(
    private cmsService: CmsService,
    private coreToolsService: CoreToolsService,
    private routingHelperService: RoutingHelperService
  ) {
  }

  /**
   * Filter [events | filtered events] with a given filter
   * @param {ICompetitionFilter} league ([activated | deactivated] league filter)
   * @param {ICompetitionFilter} time ([activated | deactivated] time filter)
   * @param {ITypeSegment[] | IGroupedByDateItem[]} events
   * @returns {ITypeSegment[] | IGroupedByDateItem[]}
   */
  filterEvents(
    league: ICompetitionFilter,
    time: ICompetitionFilter,
    events: (ITypeSegment | IGroupedByDateItem)[]
  ): ITypeSegment[] | IGroupedByDateItem[] {
    // because both ITypeSegment and IGroupedByDateItem contains events, we specify ITypeSegment as a type

    const eventsBySections: ITypeSegment[] = this.coreToolsService.deepClone(events);

    if (league && time && league.active && time.active) { // when both league and time filters selected
      return this.filterEventsByTime(
        this.filterEventsByLeague(eventsBySections, league.value as number[]),
        time.value as number
      );
    } else if (league && league.active) { // when league filter selected
      return this.filterEventsByHiddenMarkets(  // because filtering by time is doing filtering by hidden markets
        this.filterEventsByLeague(eventsBySections, league.value as number[])
      );
    } else if (time && time.active) { // when time filter selected
      return this.filterEventsByTime(eventsBySections, time.value as number);
    } else {
        // filters were deactivated
        return eventsBySections;
    }
  }

  /**
   * Extracts time filters from sports config tabs by tab name
   * and forms an appropriate typed array including league filters
   * @param {string} tabName
   * @param {ISportConfigTab[]} tabs
   * @param {ICompetitionFilter[]} leagueFilters
   * @returns {ICompetitionFilter[]}
   */
  formTimeFilters(tabName: string, tabs: ISportConfigTab[], leagueFilters: ICompetitionFilter[] = []): ICompetitionFilter[] {
    const targetTab: ISportConfigTab = tabs.find((tab: ISportConfigTab) => tab.id.includes(tabName));
    const leagueFilterLength = leagueFilters.length;

    if (targetTab && targetTab.filters && targetTab.filters.time && targetTab.filters.time.length) {
      return leagueFilters.concat(targetTab.filters.time.map((time: number, index: number): ICompetitionFilter => {
        return {
          id: `${leagueFilterLength + index + 1}`,
          type: FILTER_TYPES.TIME,
          name: `${time}h`,
          value: time,
          active: false
        };
      }));
    } else {
      return leagueFilters;
    }
  }

  /**
   * Extracts league filters from sports config tabs by tab name
   * and forms an appropriate typed array
   * @param {string} tabName
   * @param {ISportConfigTab[]} tabs
   * @returns {ICompetitionFilter[]}
   */
  formLeagueFilters(tabName: string, tabs: ISportConfigTab[]): ICompetitionFilter[] {
    const targetTab: ISportConfigTab = tabs.find((tab: ISportConfigTab) => tab.id.includes(tabName));

    if (targetTab && targetTab.filters && targetTab.filters.league && targetTab.filters.league.length) {
      return targetTab.filters.league.map((league: ILeagueFilter, index: number): ICompetitionFilter => {
        return {
          id: `${index + 1}`,
          type: FILTER_TYPES.LEAGUE,
          name: league.leagueName,
          value: league.leagueIds,
          active: false
        };
      });
    } else {
      return [];
    }
  }

  /**
   * Get Sport Event Filters Availability via FeatureToggle from CMS Config
   */
  getSportEventFiltersAvailability(): Observable<boolean> {
    return this.cmsService.getSystemConfig()
      .pipe(
        map((config: ISystemConfig) => config.FeatureToggle && config.FeatureToggle[this.filtersKey])
      );
  }

  /**
   * Filter eventsBySections by hidden markets (BMA-57901)
   * @param {ITypeSegment[] | IGroupedByDateItem[]} eventsBySections
   * @returns {ITypeSegment[] | IGroupedByDateItem[]} eventsBySections
   */
  filterEventsByHiddenMarkets(eventsBySections: (ITypeSegment | IGroupedByDateItem)[]): ITypeSegment[] | IGroupedByDateItem[] {
    // because both ITypeSegment and IGroupedByDateItem contains events, we specify ITypeSegment as a type
    return (eventsBySections as ITypeSegment[]).filter((eventsBySection: ITypeSegment): boolean => {
      if (eventsBySection.groupedByDate && eventsBySection.groupedByDate.length) {  // mobile sorting case
        eventsBySection.groupedByDate = eventsBySection.groupedByDate.filter((group: IGroupedByDateItem): boolean => {
          group.events = this.filterByHiddenMarkets(group.events);

          return group.events.length > 0;
        });
      }

      if (eventsBySection.events && eventsBySection.events.length) {
        eventsBySection.events = this.filterByHiddenMarkets(eventsBySection.events);
      }

      return (eventsBySection.groupedByDate && eventsBySection.groupedByDate.length > 0) ||
        (eventsBySection.events && eventsBySection.events.length > 0);
    });
  }

  /**
   * Return event only if at least 1 market of its is not hidden (BMA-57901)
   * @param {ISportEvent[]} events
   * @private
   * @returns {ISportEvent[]} events
   */
  private filterByHiddenMarkets(events: ISportEvent[]): ISportEvent[] {
    const marketFilterList = this.selectedMarket ? this.selectedMarket.toLowerCase().split(',') : [];
    return !this.selectedMarket ? events : events.filter((event: ISportEvent) => {
      return event.markets.some((market: IMarket) => {
        return marketFilterList.indexOf(market.templateMarketName.toLowerCase()) !== -1 && !market.hidden;
      });
    });
  }

  /**
   * Filters given events within time range
   * @param {ITypeSegment[]} eventsBySections
   * @param {string} time
   * @returns {ITypeSegment[]} eventsBySections
   */
  private filterEventsByTime(eventsBySections: ITypeSegment[], time: number): ITypeSegment[] {
    const limit = new Date();
    const filterByTime = (events: ISportEvent[]): ISportEvent[] => {
      return events.filter((event: ISportEvent): boolean => {
        const startTime = new Date(event.startTime);

        return limit >= startTime;
      });
    };

    limit.setHours(limit.getHours() + time);

    return eventsBySections.filter((eventsBySection: ITypeSegment): boolean => {
      if (eventsBySection.groupedByDate && eventsBySection.groupedByDate.length) {  // mobile sorting case
        eventsBySection.groupedByDate = eventsBySection.groupedByDate.filter((group: IGroupedByDateItem): boolean => {
          group.events = this.filterByHiddenMarkets(filterByTime(group.events));

          return group.events.length > 0;
        });
      }

      if (eventsBySection.events && eventsBySection.events.length) {
        eventsBySection.events = this.filterByHiddenMarkets(filterByTime(eventsBySection.events));
      }

      return (eventsBySection.groupedByDate && eventsBySection.groupedByDate.length > 0) ||
        (eventsBySection.events && eventsBySection.events.length > 0);
    });
  }

  /**
   * Filters given events by selected category (league)
   * @param {ITypeSegment[]} eventsBySections
   * @param {string} league
   * @returns {ITypeSegment[]} eventsBySections
   */
  private filterEventsByLeague(eventsBySections: ITypeSegment[], league: number[]): ITypeSegment[] {
    return eventsBySections.filter((eventsBySection: ITypeSegment): boolean => league.includes(+eventsBySection.typeId));
  }
  /**
   * append url to all the eventsforschema
   * @param eventsForSchema 
   * @returns ISportEvent[]
   */
  getSeoSchemaEvents(eventsForSchema: ISportEvent[]):ISportEvent[] {
    eventsForSchema?.forEach((event) => {
      {
        const edpUrl: string = event && this.routingHelperService.formEdpUrl(event);
        event.url = edpUrl;
      }
    });
    return eventsForSchema;
  }
}

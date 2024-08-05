import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { YOURCALL_DATA_PROVIDER } from '@yourcall/constants/yourcall-data-provider';
import { TimeService } from '@core/services/time/time.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';

import { IBYBLeaguesPeriod } from '@yourcall/models/request-params.model';
import {
  IYourcallBYBEventResponse,
  IYourcallBYBLeagueEventsResponse
} from '@yourcall/models/byb-events-response.model';
import { IBybExtendedLeagueEvent } from '@yourcall/models/byb-extended-league-event.model';
import { YourCallLeague } from '@yourcall/models/yourcall-league';
import { IRoutingHelperEvent } from '@core/services/routingHelper/routing-helper.model';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class YourcallBybLeagueService {
  constructor(
    private yourcallProviderService: YourcallProviderService,
    private timeService: TimeService,
    private routingHelperService: RoutingHelperService,
    private filterService: FiltersService,
    private sportsConfigHelperService: SportsConfigHelperService
  ) {}

  /**
   * Get league events for specific time period
   * @param league
   * @param filter
   * @returns {Promise}
   */
  getLeagueEvents(league: YourCallLeague, filter: IBYBLeaguesPeriod): Promise<IYourcallBYBEventResponse[]> {
    return this.yourcallProviderService.useOnce(YOURCALL_DATA_PROVIDER.BYB).getLeagueEvents(league.obTypeId, filter)
      .then((response: IYourcallBYBLeagueEventsResponse) => {
        return response.data;
      }, error => {
        console.warn('BYB:getLeagueEvents error:', error);
        return [];
      });
  }

  /**
   * Prepare leagues data
   * @param eventsData
   * @returns {Array}
   */
  parse(eventsData: IYourcallBYBEventResponse[]): IBybExtendedLeagueEvent[] {
    return _.map(eventsData, (event: IYourcallBYBEventResponse) => {
      return _.extend(event, {
        id: event.obEventId,
        teamHome: this.getTeamName(event.title, 0) || event.homeTeam.title,
        teamAway: this.getTeamName(event.title, 1) || event.visitingTeam.title
      });
    });
  }

  /**
   * Get time range object for specific filter
   * @param filter
   * @returns {{dateFrom: (string|*), dateTo: (string|*)}}
   */
  getInterval(filter: string): IBYBLeaguesPeriod {
    return filter === 'today'
      ? {
        dateFrom: this.timeService.dateTimeOfDayInISO('today'),
        dateTo: this.timeService.dateTimeOfDayInISO('tomorrow')
      }
      : {
        dateFrom: this.timeService.dateTimeOfDayInISO('tomorrow'),
        dateTo: this.timeService.dateTimeOfDayInISO('6days')
      };
  }

  /**
   * Get url path for event
   * @param event
   * @param league
   * @returns {*}
   */
  getEventPath(event: IBybExtendedLeagueEvent, league: YourCallLeague): Observable<string> {
    return this.sportsConfigHelperService.getSportPathByCategoryId(league.categoryId)
      .pipe(
        map((sportPath: string) => {
          const eventEntity = {
            categoryId: league.categoryId,
            categoryName: sportPath,
            name: event.title,
            id: event.obEventId
          };

          return this.routingHelperService.formEdpUrl(eventEntity as IRoutingHelperEvent);
        })
      );
  }

  /**
   * Get particular team name from event title
   * @param eventTitle
   * @param index
   * @returns {string}
   */
  getTeamName(eventTitle: string, index: number): string {
    const title: string = this.filterService.clearEventName(eventTitle).replace(/\|/g, '');
    const splitter = /\sv\s|\svs\s/ig;
    const arr = title.match(splitter) && title.split(title.match(splitter)[0]);
    return arr && arr[index] ? arr[index] : '';
  }
}

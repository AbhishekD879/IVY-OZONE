import { Injectable } from '@angular/core';

import environment from '@environment/oxygenEnvConfig';

import { CmsService } from '@coreModule/services/cms/cms.service';

import {
  IBYBLeaguesPeriod,
  IBYBPostRequestData,
  IEmptyMethodResult,
  IGetMarketSelectionsParams,
  IYourcallAPIRequestData, IYourcalStatValuesParams, IYourcallPlayerStatisticParams
} from '@yourcall/models/request-params.model';
import { IBybMarket } from '@core/services/cms/models';
import { YourCallEvent } from '@yourcall/models/yourcall-event';
import { IOddsParams } from '@yourcall/models/odds-params.model';

@Injectable({ providedIn: 'root' })
export class BybApiService {
  uri: string = environment.BYB_CONFIG.uri;
  code: string = 'BYB';
  UPCOMING_LEAGUES_RANGE: number = 6;

  constructor(
    private cmsService: CmsService
  ) {
    this.getUri = this.getUri.bind(this);
    this.getUpcomingLeagues = this.getUpcomingLeagues.bind(this);
    this.getEDPMarkets = this.getEDPMarkets.bind(this);
  }

  /**
   * Extend request params is needed before calling resource
   * @param requestParams
   * @return {*}
   */
  extendParams(requestParams: any): any {
    return requestParams;
  }

  /**
   * Get full uri for BYB resources
   * @param request
   * @return {string}
   */
  getUri(request: IYourcallAPIRequestData): string {
    return `${this.uri}${request.path}`;
  }

  /**
   * GET BYB (Banach) list of available leagues
   * @return {{path: string}}
   */
  getLeagues(): IYourcallAPIRequestData {
    return this.getData('/v1/leagues');
  }

  /**
   * Get leagues for periods
   * @returns {{path: string, params: {days: number, tz: number}}}
   */
  getUpcomingLeagues(): IYourcallAPIRequestData {
    return {
      path: '/v1/leagues-upcoming',
      params: { days: this.UPCOMING_LEAGUES_RANGE, tz: -1 * (new Date().getTimezoneOffset() / 60) }
    };
  }

  /**
   * Get events
   * @returns {{ path: string }}
   */
  getLeagueEventsWithoutPeriod(): IYourcallAPIRequestData {
    return this.getData('/v1/events');
  }

  /**
   * Get events for particular league and period
   * @param leagueIds
   * @param period
   * @returns {{path: string, params: {leagueIds: *, dateFrom: *, dateTo: *}}}
   */
  getLeagueEvents(leagueIds: number | number[], period: IBYBLeaguesPeriod): IYourcallAPIRequestData {
    const { dateFrom, dateTo } = period;
    return this.getData('/v1/events', { leagueIds, dateFrom, dateTo });
  }

  /**
   * Get BYB (Banach) event data
   * @param obEventId
   * @return {{path: string}}
   */
  getGameInfo(obEventId: string): IYourcallAPIRequestData {
    return this.getData(`/v1/events/${obEventId}`);
  }

  /**
   * Load EDP market configuration
   * @returns {*}
   */
  getEDPMarkets(): Promise<IBybMarket[]> {
    return this.cmsService.getYourCallBybMarkets().toPromise();
  }

  /**
   * Get Grouped BYB markets
   * @param event
   * @returns {{path: string, params: {obEventId: (number|string|*)}}}
   */
  getMatchMarkets(event: YourCallEvent): IYourcallAPIRequestData {
    return this.getData('/v2/markets-grouped', { obEventId: event.obEventId });
  }

  /**
   * Get selections for specific market
   * @param params
   */
  getMarketSelections(params: IGetMarketSelectionsParams): IYourcallAPIRequestData {
    return this.getData('/v1/selections', params);
  }

  /**
   * Get list of players for an event
   * @param obEventId
   * @returns {{path: string, params: {obEventId: (number|string|*)}}}
   */
  getPlayers(obEventId: number): IYourcallAPIRequestData {
    return this.getData('/v1/players', { obEventId });
  }

  /**
   * Get list of available statistics
   * @param params
   * @return {{path: string, params: *}}
   */
  getStatistics(params: IYourcallPlayerStatisticParams): IYourcallAPIRequestData {
    return this.getData('/v1/player-statistics', params);
  }

  /**
   * Get values for BYB specific statistic
   * @param params
   * @return {{path: string, params: *}}
   */
  getStatValues(params: IYourcalStatValuesParams): IYourcallAPIRequestData {
    return this.getData('/v1/statistic-value-range', params);
  }

  /**
   * Calculate odds for DS selection in dashboard
   * @param params
   * @return {{path: string, params: *}}
   */
  calculateAccumulatorOdds(params: IOddsParams): IBYBPostRequestData {
    return {
      path: '/v1/price',
      method: 'POST',
      params
    };
  }

  // Moved From Base API
  // empty not implemented methods
  calculateOdds(params: any): IEmptyMethodResult {
    return { resolve: { data: {} } };
  }

  getBets(id: number): IEmptyMethodResult {
    return { resolve: { data: [] } };
  }

  getGames(typeIds: number[]): IEmptyMethodResult {
    return { resolve: { data: [] } };
  }

  getMaxExposure(params: any): IEmptyMethodResult {
    return { resolve: {} };
  }

  // private method to get data, and not duplicate code
  private getData(path: string, params?: any): IYourcallAPIRequestData {
    const data: IYourcallAPIRequestData = { path };

    if (params) {
      data.params = params;
    }

    return data;
  }
}

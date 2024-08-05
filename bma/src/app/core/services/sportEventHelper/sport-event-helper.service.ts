import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CoreToolsService } from '../coreTools/core-tools.service';
import { MEDIA_DRILL_DOWN_NAMES } from '@sb/sb.constant';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { IWidgetEventNames } from '@desktop/models/wigets.model';
import { ISportConfig } from '@app/core/services/cms/models';

@Injectable()
export class SportEventHelperService {

  constructor(
    private locale: LocaleService,
    private coreTools: CoreToolsService,
    private filterService: FiltersService
  ) {
  }
  /**
   * Checks if to show clock
   * @returns {boolean}
   */
  isClockAllowed(event: ISportEvent): boolean {
    return !!event.clock;
  }

  /**
   * Checks if match time is half time
   * @returns {boolean}
   * @private
   */
  isHalfTime(event: ISportEvent): boolean {
    const eventClock = event.clock;
    return !!eventClock && eventClock.matchTime === 'HT';
  }

  /**
   * Checks if match time is penalties
   * @returns {boolean}
   * @private
   */
  isPenalties(event: ISportEvent): boolean {
    const eventClock = event.clock;
    return !!eventClock && eventClock.matchTime === 'PENS';
  }

  /**
   * Checks if match time full time
   * @returns {boolean}
   */
  isFullTime(event: ISportEvent): boolean {
    const eventClock = event.clock;
    return !!eventClock && eventClock.matchTime === 'FT';
  }

  /**
   * Check if cashout is enabled for event
   * @param event
   * @returns {boolean}
   */

  isCashOutEnabled(event: ISportEvent): boolean {
    if (event.markets && event.markets.length) {
      return event.markets && event.markets[0] && event.markets[0].cashoutAvail === 'Y';
    }
    return event.cashoutAvail === 'Y';
  }

  /**
   * Check if event second name is available
   * @param event
   * @returns {boolean}
   */
  isEventSecondNameAvailable(event: ISportEvent): boolean {
    return !!this.getEventNames(event).eventSecondName;
  }

  /**
   * Parse event names from event
   * @param event
   * @returns {object}
   */

  getEventNames(event: ISportEvent): IWidgetEventNames {
    const eventName = event.nameOverride || event.name;
    const result: IWidgetEventNames = {
      eventFirstName: null,
      eventSecondName: null
    };
    if (eventName) {
      result.eventFirstName = this.filterService.getTeamName(eventName, 0);
      result.eventSecondName = this.filterService.getTeamName(eventName, 1);
    }
    return result;
  }

  /**
   * Get score for team
   * @param {String} teamType
   * @param {boolean} isPenalty
   * @return {number|*|string|string|string}
   */
  getOddsScore(event: ISportEvent, teamType, isPenalty = false) {
    const teams = {
      teamA: 'home',
      teamB: 'away'
    };
    const teamsUs = {
      teamA: 'away',
      teamB: 'home'
    };
    const scoreProp = isPenalty ? 'penaltyScore' : 'score';
    const isUS = event.isUS;
    const selectedTeam = isUS ? teamsUs[teamType] : teams[teamType];
    return event.comments.teams[selectedTeam][scoreProp];
  }

  /**
   * Check if event type is tennis
   * @param event
   * @returns {boolean}
   */
  isTennis(event: ISportEvent): boolean {
    return event.categoryName === 'Tennis';
  }

  /**
   * Check if event type is football
   * @param event
   * @returns {boolean}
   */
  isFootball(event: ISportEvent): boolean {
    return event.categoryName === 'Football';
  }

  /**
   * Check if event has current points
   * @param event
   * @returns {boolean}
   */
  isEventHasCurrentPoints(event: ISportEvent): boolean {
    return this.coreTools.hasOwnDeepProperty(event, 'comments.teams.home.currentPoints');
  }

  /**
   * Returns current points for team
   * @param event
   * @param teamType
   * @returns {number}
   */
  getEventCurrentPoints(event: ISportEvent, teamType: string) {
    const teams = {
      teamA: 'home',
      teamB: 'away'
    };
    const team = teams[teamType];
    return event.comments.teams[team].currentPoints;
  }

  /**
   * Check if odds scores are present
   * @param event
   * @returns {boolean}
   */
  isEventHasOddsScores(event: ISportEvent) {
    return this.coreTools.hasOwnDeepProperty(event, 'comments.teams.home');
  }

  /**
   * Returns tennis set scores
   * @param event
   * @returns {object}
   */
  getTennisSetScores(event: ISportEvent): { [key: string]: number; }[] {
    let setsScores = {} as { [key: string]: number }[];
    if (this.coreTools.hasOwnDeepProperty(event, 'comments.setsScores')) {
      setsScores = event.comments.setsScores;
    }
    return _.toArray(setsScores);
  }

  /**
   * Returns tennis score for player
   * @param event
   * @param playerType
   * @returns {string}
   */
  getTennisScoreForPlayer(event: ISportEvent, playerType) {
    const players = {
      playerA: 'player_1',
      playerB: 'player_2'
    };
    const player = players[playerType];
    return event.comments.teams[player].id;
  }

  /**
   * Check if event is live
   * @param event
   * @returns {boolean}
   */
  isLive(event: ISportEvent): boolean {
    return event.isStarted || event.eventIsLive;
  }

  /**
   * Checks if stream is available
   * @returns {boolean}
   */
  isStreamAvailable(event: ISportEvent): boolean {
    return event.liveStreamAvailable && this.showStreamIcon(event);
  }

  /**
   * Check if markets counter should be shown
   * @param event
   * @returns {boolean}
   */
  showMarketsCount(event: ISportEvent): boolean {
    return event.marketsCount > 1;
  }

  /**
   * Parse set index from event
   * @param event
   * @returns {string}
   */
  getTennisSetIndex(event: ISportEvent): string {
    let result = '';
    if (this.coreTools.hasOwnDeepProperty(event, 'comments.runningSetIndex')) {
      const runningSetIndex = event.comments.runningSetIndex;
      const numberSuffix = this.locale.getString(this.filterService.numberSuffix(runningSetIndex));
      result = `${runningSetIndex}${numberSuffix} ${this.locale.getString('sb.tennisSet')}`;
    }
    return result;
  }

  /**
   * Check if event type is home/draw/away
   * @param event
   * @param sportConfig
   * @returns {boolean}
   */
  isHomeDrawAwayType(event: ISportEvent, sportConfig: ISportConfig): boolean {
    const homeDrawAwayType = 'homeDrawAwayType';
    let oddsCardHeaderType, isHomeDrawAwayType;
    if (event.oddsCardHeaderType) {
      isHomeDrawAwayType = event.oddsCardHeaderType === homeDrawAwayType || event.oddsCardHeaderType === 'oneThreeType';
    } else {
      oddsCardHeaderType = sportConfig && sportConfig.config.oddsCardHeaderType;
      const outcomesTemplateType1 = _.isObject(oddsCardHeaderType) && oddsCardHeaderType.outcomesTemplateType1 === homeDrawAwayType;
      isHomeDrawAwayType = outcomesTemplateType1 || oddsCardHeaderType === homeDrawAwayType;
    }
    return isHomeDrawAwayType;
  }

  /**
   * Returns event markets count
   * @param event
   * @returns {number}
   */
  getMarketsCount(event: ISportEvent): number {
    let marketsCount = 0;
    if (_.isNumber(event.marketsCount)) {
      marketsCount = event.marketsCount - 1;
    }
    return marketsCount;
  }

  /**
   * Check if each way terms are available
   * @param market
   * @returns {Boolean}
   */
  isEachWayTermsAvailable(market: IMarket): boolean {
    return !!(market.eachWayPlaces && market.eachWayFactorDen && market.eachWayFactorNum);
  }

  /**
   * Check if cashout is available for event
   * @param event
   * @returns {boolean}
   */
  isCashoutAvailable(event: ISportEvent): boolean {
    return event.cashoutAvail === 'Y';
  }

  /**
   * Check if event is outright
   * @param event
   * @returns {boolean}
   */
  isOutrightEvent(event: ISportEvent): boolean {
    const eventSortCode = event && event.eventSortCode;
    if (!eventSortCode) {
      console.warn('Event sort code was not provided');
    }
    if (this.isOutrightSport(event.categoryCode)) {
      return OUTRIGHTS_CONFIG.outrightsSportSortCode.indexOf(eventSortCode) > -1;
    }

    return OUTRIGHTS_CONFIG.sportSortCode.indexOf(eventSortCode) > -1;
  }
  /**
   * Check if event is special
   * @param event {object}
   * @param checkMarkets {boolean} if true then check markets. If one of markets is special then event is special as well
   * @returns {boolean}
   */
  isSpecialEvent(event: ISportEvent, checkMarkets: boolean): boolean {
    const SP_EVENT_FLAG = 'EVFLAG_SP';
    let drilldownTagNames = '';
    let isSpecialEvent;
    if (!event.markets.length) {
      return false;
    }
    if (event && _.isString(event.drilldownTagNames)) {
      drilldownTagNames = event.drilldownTagNames;
    }
    isSpecialEvent = drilldownTagNames.includes(SP_EVENT_FLAG);

    if (!isSpecialEvent && checkMarkets) {
      const SP_MARKET_FLAG = 'MKTFLAG_SP';
      const marketWithDrilldownTags = _.filter(event.markets, market => {
        return market.drilldownTagNames && _.isString(market.drilldownTagNames);
      });
      isSpecialEvent = _.some(marketWithDrilldownTags, market => {
        return market.drilldownTagNames.includes(SP_MARKET_FLAG);
      });
    }
    return isSpecialEvent;
  }

  /**
   * Checks if in drilldownTagNames property of event are two or more providers
   * @returns {boolean}
   * @private
   */
  private showStreamIcon(event: ISportEvent): boolean {
    const eventDrilldownTagNames = event.drilldownTagNames ? event.drilldownTagNames.split(',') : [];
    return _.intersection(eventDrilldownTagNames, MEDIA_DRILL_DOWN_NAMES).length > 0;
  }

  /**
   * Check if event belongs to specific sports which has sortCode "MTCH" as outright
   * @param code
   */
  private isOutrightSport(code: string): boolean {
    return _.indexOf(OUTRIGHTS_CONFIG.outrightsSports, code) !== -1;
  }

}

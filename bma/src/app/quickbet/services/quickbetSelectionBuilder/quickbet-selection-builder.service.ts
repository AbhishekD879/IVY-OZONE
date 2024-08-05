import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { UserService } from '@core/services/user/user.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { quickbetConstants } from '@app/quickbet/constants/quickbet.constant';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';

import { IConstant } from '@core/services/models/constant.model';
import { IQuickbetStoredStateModel } from '@app/quickbet/models/quickbet-stored-state.model';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { IQuickbetCombainedModel } from '@app/quickbet/models/quickbet-combained.model';
import { IQuickbetEventModel } from '@app/quickbet/models/quickbet-event.model';
import { IQuickbetMarketModel, IQuickbetOutcomeModel } from '@app/quickbet/models/quickbet-market.model';
import { IQuickbetData } from '@app/quickbet/models/quickbet-restored-data.model';
import { TimeService } from '@core/services/time/time.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { UNNAMED_FAVOURITES } from '@core/services/raceOutcomeDetails/race-outcome.constant';
import { IQuickbetRequestModel } from '@app/quickbet/models/quickbet-selection-request.model';

@Injectable({ providedIn: 'root' })
export class QuickbetSelectionBuilder {
  private quickbetConstants: IConstant;
  private categoriesData: IConstant;

  constructor(
    private filtersService: FiltersService,
    private userService: UserService,
    private fracToDecService: FracToDecService,
    private localeService: LocaleService,
    private clientUserAgentService: ClientUserAgentService,
    private toolsService: CoreToolsService,
    private timeService: TimeService,
    private timeSyncService: TimeSyncService
  ) {
    this.categoriesData = environment.CATEGORIES_DATA;
    this.quickbetConstants = quickbetConstants;
  }

  /**
   * Builds quickbet selection model based on passed params.
   * @param {Object} options.event
   * @param {Object} options.request
   * @param {Object} options.selectionPrice
   * @return {Object}
   */
  build({ event, request, selectionPrice, oddsBoost, freebetList, maxPayout }: IQuickbetData,
    storedState: IQuickbetStoredStateModel): IQuickbetSelectionModel {
    const selectionType = request.selectionType,
      isScorecast = selectionType === this.quickbetConstants.SCORECAST_TYPE,
      eventMarkets = isScorecast ? this.normalizeEventMarkets(event, request) : event.markets,
      eventModel = this.parseEventData(event),
      selectionModel = isScorecast ? this.parseScorecastSelection(eventMarkets)
        : this.parseSimpleSelection(eventMarkets);
    const combinedModel = this.getCombinedModel(selectionModel, selectionPrice);

    if (!_.isUndefined(storedState && storedState.isLP) && combinedModel.hasSPLP) {
      combinedModel.isLP = storedState.isLP;
    } else {
      combinedModel.isLP = !!(combinedModel.hasSPLP || selectionModel.hasLP);
    }
    if (selectionPrice) {
      combinedModel.price = selectionPrice;

      // Add Handicap value to outcome name.
      if (selectionPrice.handicapValueDec) {
        const handicap = selectionPrice.handicapValueDec.replace(/,/, '');
        selectionModel.handicapValue = Number(handicap) < 0 ? handicap : `+${handicap}`;
        selectionModel.oldHandicapValue = selectionModel.handicapValue;
        selectionModel.outcomeName += this.filtersService.makeHandicapValue(handicap, eventMarkets[0].outcomes[0]);
      }
    }

    if (combinedModel.isUnnamedFavourite) {
      combinedModel.hasSP = true;
      combinedModel.hasSPLP = false;
      selectionModel.isEachWayAvailable = false;
      selectionModel.eachWayFactorNum = '';
      selectionModel.eachWayFactorDen = '';
    }

    return new IQuickbetSelectionModel(
      _.extend(eventModel, selectionModel, combinedModel, {
        selectionType,
        requestData: request,
        freebetList: freebetList,
        disabled: this.isSuspended([eventModel.eventStatusCode, selectionModel.marketStatusCode,
        selectionModel.outcomeStatusCode]),
        isBoostActive: storedState.isBoostActive,
        oddsBoost,
        maxPayout
      }),
      storedState,
      this.userService,
      this.fracToDecService,
      this.clientUserAgentService,
      this.toolsService,
      this.timeSyncService
    );
  }

  /**
   * Checks if passed category id is of racing type.
   * @param {string} categoryId
   * @return {boolean}
   * @private
   */
  private isRacing(categoryId: string): boolean {
    return [
      this.categoriesData.racing.greyhound.id,
      this.categoriesData.racing.horseracing.id
    ].includes(`${categoryId}`);
  }

  private isVirtual(categoryId: string): boolean {
    return `${categoryId}` === this.categoriesData.virtuals[0].id;
  }

  /**
   * Checks if outcome name is of Unnamed favourite type.
   * @param {string} outcomeName
   * @return {boolean}
   * @private
   */
  private isUnnamedFavourite(outcomeName: string): boolean {
    return UNNAMED_FAVOURITES.indexOf(outcomeName.toLowerCase()) >= 0;
  }

  /**
   * Checks if passed status code or list of status codes are of suspended type.
   * @param {string|Array} status
   * @return {boolean}
   * @private
   */
  private isSuspended(status: string | string[]): boolean {
    if (_.isArray(status)) {
      return _.contains(status, this.quickbetConstants.SUSPENDED_STATUS);
    }

    return status === this.quickbetConstants.SUSPENDED_STATUS;
  }


  /**
   * Sort event markets according to the order of outcomes in request.
   * Markets with non-matched outcome ids are moved in the end of the list, keeping relative order (fallback case).
   * Original event.markets object reference is preserved.
   * @param event
   * @param request
   */
  private normalizeEventMarkets(event: IQuickbetEventModel = {}, request: IQuickbetRequestModel): IQuickbetMarketModel[] {
    if (event.markets && request.outcomeIds) {
      const outcomeIds = request.outcomeIds.map(String),
        orderMap = event.markets.reduce((map: { [key: string]: number }, market: IQuickbetMarketModel, marketIndex: number) => {
          const outcomeIndex = outcomeIds.indexOf(market.outcomes[0].id.toString());
          map[market.id] = outcomeIndex >= 0 ? outcomeIndex : marketIndex + outcomeIds.length + event.markets.length;
          return map;
        }, {});

      event.markets.sort((m2: IQuickbetMarketModel, m1: IQuickbetMarketModel) => orderMap[m2.id] - orderMap[m1.id]);
    }

    return event.markets;
  }

  /**
   * Parses event level data.
   * @param {Object} event
   * @return {Object}
   * @private
   */
  private parseEventData(event: IQuickbetEventModel = {}): IQuickbetEventModel {
    const keys = ['isStarted', 'typeId', 'categoryName', 'classId', 'className',
      'eventStatusCode', 'startTime', 'drilldownTagNames', 'markets'],
      categoryId = event.categoryId,
      isRacingSport = this.isRacing(categoryId),
      isVirtualSport = this.isVirtual(categoryId);

    let eventName = isRacingSport ? event.name : this.filtersService.clearEventName(event.name);
    eventName = isVirtualSport ? `${this.timeService.formatByPattern(new Date(event.startTime), 'HH:mm')} ${eventName}` : eventName;

    return _.extend(_.pick(event, keys), {
      eventId: event.id,
      eventName: eventName,
      typeName: event.typeName,
      eventIsLive: event.isLiveNowEvent,
      categoryId,
      isRacingSport
    });
  }

  /**
   * Parses simple selection data.
   * @param {Array} markets
   * @return {Object}
   * @private
   */
  private parseSimpleSelection(markets: IQuickbetMarketModel[] = []): IQuickbetMarketModel {
    const market: IQuickbetMarketModel = markets[0] || {},
      outcome: IQuickbetOutcomeModel = _.isArray(market.outcomes) ? market.outcomes[0] : {},
      keys = ['marketStatusCode', 'isEachWayAvailable', 'eachWayFactorDen',
        'eachWayFactorNum', 'isMarketBetInRun', 'isSpAvailable', 'isLpAvailable'];

    return _.extend(_.pick(market, keys), {
      marketName: market.name,
      marketId: market.id,
      hasLP: market.isLpAvailable && !market.isSpAvailable,
      hasGP: market.isGpAvailable,
      outcomeId: outcome.id,
      outcomeName: outcome.name,
      outcomeStatusCode: outcome.outcomeStatusCode,
      outcomeMeaningMinorCode: outcome.outcomeMeaningMinorCode
    });
  }

  /**
   * Parses scorecast selection data.
   * @param {Array} markets
   * @return {Object}
   * @private
   */
  private parseScorecastSelection(markets: IQuickbetMarketModel[]): IQuickbetMarketModel {
    const outcomes = _.flatten(_.pluck(markets, 'outcomes')),
      correctScoreOutcome = _.findWhere(outcomes, {
        outcomeMeaningMajorCode: this.quickbetConstants.CORRECT_SCORE_MEANING_CODE
      }),
      scorerOutcome = _.find(outcomes, outcome => {
        return outcome.outcomeMeaningMajorCode !== this.quickbetConstants.CORRECT_SCORE_MEANING_CODE;
      });

    return {
      marketName: scorerOutcome ?
        this.localeService.getString(`quickbet.${scorerOutcome.outcomeMeaningMajorCode}`) : '',
      marketId: _.pluck(markets, 'id').join(','),
      marketStatusCode: this.isSuspended(_.pluck(markets, 'marketStatusCode'))
        ? this.quickbetConstants.SUSPENDED_STATUS : this.quickbetConstants.AVAILABLE_STATUS,
      isEachWayAvailable: false,
      eachWayFactorDen: '',
      eachWayFactorNum: '',
      hasLP: true,
      hasGP: false,
      isSpAvailable: false,
      outcomeId: _.pluck(outcomes, 'id').join(','),
      outcomeName: scorerOutcome ? `${scorerOutcome.name}, ${correctScoreOutcome.name}` : '',
      outcomeStatusCode: this.isSuspended(_.pluck(outcomes, 'outcomeStatusCode'))
        ? this.quickbetConstants.SUSPENDED_STATUS : this.quickbetConstants.AVAILABLE_STATUS
    };
  }

  private getCombinedModel(selectionModel, selectionPrice): IQuickbetCombainedModel {
    const { isLpAvailable, isSpAvailable, outcomeName} = selectionModel;

    return {
      hasSP: isSpAvailable && (!isLpAvailable || (isLpAvailable && !selectionPrice)),
      hasSPLP: isSpAvailable && isLpAvailable && !!selectionPrice,
      isUnnamedFavourite: this.isUnnamedFavourite(outcomeName)
    };
  }
}

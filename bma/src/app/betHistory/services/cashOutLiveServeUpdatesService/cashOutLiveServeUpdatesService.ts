import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { CommentsService } from '@core/services/comments/comments.service';
import { CashoutErrorMessageService } from '@app/betHistory/services/cashoutErrorMessageService/cashout-error-message.service';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';

import { cashoutConstants } from '../../constants/cashout.constant';

import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ICashOutBet, ICashOutBetLeg,
  ICashOutBetLegPart, ITypesAndIds } from '@app/betHistory/models/bet-history-cash-out.model';
import { ILiveServeUpd, IPayload } from '@core/models/live-serve-update.model';
import { CashOutBetsMap } from '../../betModels/cashOutBetsMap/cash-out-bets-map.class';
import { IBetDetailInitial } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ICashoutMapItem } from '@app/betHistory/models/cashout-map-item.model';
import { ISocketCashoutValueUpdate,ISocketEventFinshedUpdate,ISocketTwoUpUpdate } from '@app/betHistory/models/cashout-socket.model';
import { RegularBet } from '@app/betHistory/betModels/regularBet/regular-bet.class';
import { PlacedBet } from '@app/betHistory/betModels/placedBet/placed-bet.class';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { BetHistoryMainService } from '@app/betHistory/services/betHistoryMain/bet-history-main.service';
import { CASHOUT_SUSPENDED } from '@app/betHistory/components/cashOutMessaging/cash-out-message.constants';
import { IBetHistoryLeg } from '@app/betHistory/models/bet-history.model';
import environment from '@environment/oxygenEnvConfig';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';

enum PAYLOAD_STATUSES {
  YES = 'Y',
  ACTIVE = 'A'
}

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class CashOutLiveServeUpdatesService {

  betsMap: CashOutBetsMap | { [key: string ]: CashoutBet | RegularBet | PlacedBet } = {};

  private readonly CASH_OUT = cashoutConstants;
  private betsInLiveUpdateProgress: {} = {};
  private BIRMarketsEnabled: string[];

  constructor(
    private cashOutMapIndexService: CashoutMapIndexService,
    private cashoutErrorMessageService: CashoutErrorMessageService,
    private commentsService: CommentsService,
    private pubsubService: PubSubService,
    private scoreParser: ScoreParserService,
    private betHistoryMainService: BetHistoryMainService,
    private cmsService: CmsService
    ) {
      this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
        this.BIRMarketsEnabled = config?.HorseRacingBIR?.marketsEnabled;
      });
    }

  static get cashoutUpdateType(): {} {
    return {
      sSELCN: 'outcome',
      sPRICE: 'outcome',
      sEVENT: 'event',
      sEVMKT: 'market'
    };
  }
  set cashoutUpdateType(value:{}){}
  static get attributesUpdateOn(): {} {
    return {
      event: {
        propertyName: 'events',
        attributes: ['displayed', 'status']
      },
      market: {
        propertyName: 'markets',
        attributes: ['displayed', 'status']
      },
      outcome: {
        propertyName: 'outcomes',
        attributes: ['displayed', 'status', 'settled', 'lp_num', 'lp_den']
      }
    };
  }
  set attributesUpdateOn(value:{}){}
  /**
   * Gets new cash out value
   * @param {ILiveServeUpd} update
   */
  updateCashOutValue(update: ILiveServeUpd): void {
    const updatePayload: IPayload = update.payload;
    const channelType: string = update.type;
    const id: string = update.id.toString();
    const type: string = CashOutLiveServeUpdatesService.cashoutUpdateType[channelType];

    this.eventStartedUpdate(update);
    // updates for match scores and match time
    if (channelType === this.CASH_OUT.channelName.score ||
      channelType === this.CASH_OUT.channelName.clock) {
      this.updateEventEntity(channelType, update);
      return;
    } else if (channelType === this.CASH_OUT.channelName.event) {
      this.updateEventEntity(channelType, update);
    }

    if (!channelType || !update.id || !type) {
      return;
    }

    // update results
    if (updatePayload.result) {
      const result = updatePayload.result;
      this.updateLegPartResult(result, update);
    }

    // send request for updating only for that bets which are not in progress of resolving update promises
    // this approach will avoid duplicate requests for one bet
    const diff = _.difference(this.getCashOutIdForUpdate(type, id, updatePayload), _.keys(this.betsInLiveUpdateProgress));

    if (diff.length !== 0) {
      this.updatePlacedBetsStatuses(diff, id, type, updatePayload);
    } else {
      _.each(_.toArray(this.betsMap), (bet: ICashOutBet) => {
        if (_.contains(bet.event, id) || _.contains(bet.market, id) || _.contains(bet.outcome, id)) {
          this.updateBetAccordingToPush(bet, id, type, updatePayload);
        }
      });
    }
  }

  /**
   * Applies cashout value update message from cashout events stream MS.
   * @param {Object} updatePayload
   */
  applyCashoutValueUpdate(updatePayload: ISocketCashoutValueUpdate): void {
    const betToUpdate = this.betsMap[updatePayload.betId];

    if (betToUpdate && (!betToUpdate.cashoutStatus ||
      (updatePayload.shouldActivate && !betToUpdate.isCashedOut))) {
      const updatedCashoutValue = updatePayload.cashoutValue || 0;
      const isPartialCashoutLowStatus = !betToUpdate.partialCashoutStatus ||
          `${betToUpdate.partialCashoutStatus}`.indexOf(this.CASH_OUT.betLowCashout) > -1;

      const partialCashoutAvailable = (
        betToUpdate.partialCashoutAvailable === this.CASH_OUT.result.YES &&
        Number(updatedCashoutValue) >= this.CASH_OUT.minValueForPartial &&
        isPartialCashoutLowStatus
      ) ? this.CASH_OUT.result.YES : this.CASH_OUT.result.NO;

      const updatedBet = {
        cashoutValue: Number(updatedCashoutValue).toFixed(2),
        cashoutStatus: updatePayload.cashoutStatus,
        partialCashoutAvailable,
        partialCashoutStatus: betToUpdate.partialCashoutStatus,
        shouldActivate: updatePayload.shouldActivate
      } as ICashOutBet;

      this.updateBetFromProxyResponse(betToUpdate, updatedBet, true);
    }
  }

  /**
   * Updates bet details based on given updated bet payload from:
   * - betUpdate message from cashout events stream;
   * - getBetDetail response from BPP after LiveServe update.
   * @param {Object} updatedBet
   * @param {number} timestamp
   * @param {Function} updatePayloadFn
   */
  updateBetDetails(updatedBet: ICashOutBet, timestamp: number, updatePayloadFn?: Function, fromBetUpdate = false): void {
    const bet = this.betsMap[updatedBet.betId] || {};
    const prevCashoutStatus = bet.isCashOutUnavailable;
    // prevCashoutStatus - shows was cashout previously available or not (saves prev status)

    delete this.betsInLiveUpdateProgress[updatedBet.betId];

    if (bet.lastTimeUpdate < timestamp && bet.lastTimeUpdate !== timestamp) {
      bet.lastTimeUpdate = Date.now();

      this.updateDispResult(bet, updatedBet);

      if (_.isFunction(updatePayloadFn)) {
        updatePayloadFn(bet);
      }

      const shouldBetBeDeleted = updatedBet.cashoutStatus
        && updatedBet.cashoutStatus.length
        && !this.CASH_OUT.status.some(value => updatedBet.cashoutStatus.indexOf(value) > -1)
        && !_.contains(this.CASH_OUT.values, updatedBet.cashoutValue);

      if (!bet.isCashedOut || shouldBetBeDeleted) {
        this.updateBetFromProxyResponse(bet, updatedBet, fromBetUpdate);
      }

      if (shouldBetBeDeleted) {
        this.pubsubService.publish(this.pubsubService.API.LIVE_BET_UPDATE, {
          betId: updatedBet.betId,
          prevCashoutStatus
        });
      } else {
        bet.type = '';
      }
    }
  }
  public updateEventDetail(update: ISocketEventFinshedUpdate): void {
    if (update.eventId && update.vod) {
      this.pubsubService.publish('EVENT_FINSHED', update.eventId.toString());
    }
  }

  update2UpSelection(update: ISocketTwoUpUpdate): void {
    if (update) {
      this.pubsubService.publish('TWO_UP_UPDATE', update);
    }
  }
  /**
   * Update payout details
   * we receive a flat structure for payoutUpdate we need to emit the same response
   *
  */
  updatePayoutDetails(updatedReturns: any) {
    if(updatedReturns && updatedReturns.length > 0) {
      updatedReturns.forEach((bet) =>{
        this.betsMap[bet.betNo].potentialPayout = Number(bet.returns);
      });
      this.pubsubService.publish(this.pubsubService.API.PAYOUT_UPDATE, {updatedReturns});
    }
  }

  /**
   * Update initial data.
   * We have different structure of data when receive initial response from /bet-details
   * so we need to extend this data by adding missed properties.
   * This solution causes type inconsistency so we need to use type 'any'
   */
  updateBetDetailsInitial(bet: IBetDetailInitial, timestamp: number): void {
    const { potentialPayout, stake, betType, leg } = bet;

    bet.betId = bet.betId || bet.id;
    if (Array.isArray(potentialPayout)) {
      bet.potentialPayout = potentialPayout[0] && potentialPayout[0].value;
    }
    if (Array.isArray(leg)) {
      bet.legType = leg[0]
        && leg[0].legType
        && leg[0].legType.code;
    }
    if (typeof stake === 'object') {
      bet.currency = stake.currency;
      bet.stakePerLine = stake.stakePerLine;
      bet.tokenValue = stake.tokenValue;
      (bet.stake as any) = stake.value;
    }
    if (typeof betType === 'object') {
      (bet.betType as any) = betType.code;
    }

    this.updateBetDetails(bet as any, timestamp);
  }

  /**
   * Calculates each leg status
   * @param result {string}
   * @param eventStatusCode {string}
   * @param marketStatusCode {string}
   * @param selectionsStatusCodes {Array}
   * @returns {string}
   */
  private getLegStatus(result: string, eventStatusCode: string, marketStatusCode: string, selectionsStatusCodes: string[]): string {
    let status: string = this.CASH_OUT.resultCodes[result] || '';

    if (!status) {
      const isSomeSelectionSuspended: boolean = _.some(selectionsStatusCodes, (statusCode: string) => statusCode === 'S');
      const isSuspended: boolean = eventStatusCode === 'S' || marketStatusCode === 'S' || isSomeSelectionSuspended;
      const isSettled: boolean = result !== '-';

      if (isSuspended) {
        status = 'suspended';
      }

      if (!isSettled && !isSuspended) {
        status = 'open';
      }
    }

    return status;
  }

  /**
   * Return cash out bets which have event/market/outcome with this {id} and
   * filter out cash out bets which are being of cashed out
   * @param type {string} - 'outcome'
   * @param id {string} - '13245780'
   * @param updatePayload {object} - object received from push payload
   * @returns {Array}
   */
  private getCashOutIdForUpdate(type: string, id: string, updatePayload: IPayload) {
    const isBetsMapEmpty = this.betsMap
                       && (this.betsMap as CashOutBetsMap).mapState
                       && (this.betsMap as CashOutBetsMap).mapState.isEmpty;
    // if it is not cashout bets - return
    if (!this.betsMap || isBetsMapEmpty) {
      return [];
    }
    const bets: ICashOutBet[] = this.cashOutMapIndexService[type][id];
    const newBets = [];

    // get updated cash out bets
    _.each(bets, (betEntity: ICashOutBet) => {
      const bet = this.betsMap && this.betsMap[betEntity.id],
        attributeToUpdateOn = CashOutLiveServeUpdatesService.attributesUpdateOn[type],
        pushType = attributeToUpdateOn && attributeToUpdateOn.propertyName,
        updatedElement = bet && bet[pushType] ? (bet[pushType][id] || {}) : {};

      if (pushType && this.updatePredicate(betEntity.id, type, updatePayload, updatedElement)) {
        newBets.push(betEntity.id);
      }
    });

    return newBets;
  }

  /**
   * Update predicate
   * @param betId {string}
   * @param type {string}
   * @param pushInfo {IPayload}
   * @param updatedElement {IPayload}
   * @returns {boolean}
   */
  private updatePredicate(betId: string, type: string, pushInfo: IPayload, updatedElement: IPayload): boolean {
    const bet = this.betsMap && this.betsMap[betId],
      update = CashOutLiveServeUpdatesService.attributesUpdateOn[type];

    return bet && !bet.isToteBet && (!bet.isDisable || bet.inProgress) &&
      update && update.attributes.some(attr => updatedElement[attr] !== pushInfo[attr]);
  }

  /**
   * Updates bet object with params according to push type
   * @param bet
   * @param id
   * @param type
   * @param updatePayload
   * @returns {*}
   */
  private updateBetAccordingToPush(bet: ICashOutBet, id: string, type: string, updatePayload: IPayload): void {
    const updatedInfo = { [id]: {} },
      attributeToUpdateOn = CashOutLiveServeUpdatesService.attributesUpdateOn[type],
      propName = attributeToUpdateOn && attributeToUpdateOn.propertyName;

    if (attributeToUpdateOn) {
      attributeToUpdateOn.attributes.forEach(attr => {
        if (updatePayload.hasOwnProperty(attr)) {
          updatedInfo[id][attr] = updatePayload[attr];
        }
      });
    }

    // Update each leg status according to push type
    this.updateBetSelectionsStatuses(bet, id, type, updatePayload);

    if (!bet[propName] || !bet[propName][id]) {
      bet[propName] = { ...bet[propName], ...updatedInfo };
    } else {
      bet[propName][id] = { ...bet[propName][id], ...updatedInfo[id] };
    }

    this.pubsubService.publish(this.pubsubService.API.EMA_HANDLE_BET_LIVE_UPDATE, { id, type, updatePayload });
  }

  /**
   * Sets the status to leg
   * @param bet {object}
   * @param pushType {string}
   * @param pushPayload {object}
   * @param legItem {object}
   * @param market {object}
   * @param outcomes {Array}
   * @param ids {object}
   * @param updateId {string}
   * @private
   */
  private updateLegStatus({ bet, pushType, pushPayload, legItem, market, outcomes, ids, updateId }: {
    bet: ICashOutBet, pushType, pushPayload: IPayload, legItem: ICashOutBetLeg,
    market: IMarket, outcomes: IOutcome[], ids: ITypesAndIds, updateId: string
  }): void {
    if (!_.contains(ids[pushType], updateId.toString())) {
      return;
    }
    const leg = _.find(bet.leg, (item: ICashOutBetLeg) => item.part[0].eventId === legItem.eventEntity.id.toString()),
      statusUpdated = pushPayload.hasOwnProperty('status');
    let updatedPartResult = null;

    switch (pushType) {
      case this.CASH_OUT.keyProperties.event: {
        if (statusUpdated) {
          legItem.eventEntity.eventStatusCode = pushPayload.status;
        }
        break;
      }
      case this.CASH_OUT.keyProperties.market: {
        if (statusUpdated) {
          market.marketStatusCode = pushPayload.status;
        }
        break;
      }
      case this.CASH_OUT.keyProperties.outcome: {
        updatedPartResult = { outcomeId: updateId, result: pushPayload.result };
        const updatedOutcome = outcomes.find(outcome => +outcome.id === +updateId);
        if (updatedOutcome && statusUpdated) {
          updatedOutcome.outcomeStatusCode = pushPayload.status;
        }
        break;
      }
    }

    const resultValue = this.normalizeUpdatedPartResult(leg.part, updatedPartResult);
    const status = this.getLegStatus(
        resultValue,
        legItem.eventEntity.eventStatusCode,
        market.marketStatusCode,
        outcomes.map(outcome => outcome.outcomeStatusCode)
      );

    if (status || pushPayload.status) {
      legItem.status = status;
      this.betHistoryMainService.setBybLegStatus(bet, legItem);
    }
  }

  /**
   * After settled outcome result is updated, it should be compared to other leg parts for defining the combined leg result.
   * Otherwise, if outcome result hadn't been updated, the combined result is defined from existing part result codes.
   * @param parts
   * @param updatedPart
   * @returns string
   */
  private normalizeUpdatedPartResult(parts: ICashOutBetLegPart[], updatedPart: { outcomeId: string, result: string } | null): string {
    const getOutcomeId = part => part.outcomeId || part.outcome;
    const partResults = parts.map(part => {
      const result = updatedPart && updatedPart.result && updatedPart.outcomeId === getOutcomeId(part) ? updatedPart.result : part.result;
      return result === this.CASH_OUT.handicapResultCode ? part.dispResult : result;
    });

    return this.betHistoryMainService.getPartsResult(partResults);
  }

  /**
   * Updates statuses for each selection according to push value
   * @param bet {object}
   * @param updateId {string}
   * @param pushType {string}
   * @param pushPayload {object}
   */
  private updateBetSelectionsStatuses(bet: ICashOutBet, updateId: string, pushType: string, pushPayload: IPayload): void {
    _.each(bet.leg, (legItem: ICashOutBetLeg) => {
      const ids: ITypesAndIds = {
        event: [legItem.part[0].eventId]
      };
      if (legItem.eventEntity && legItem.eventEntity.id.toString() === ids.event[0]) {
        const market = _.find(legItem.eventEntity.markets, (item: IMarket) => _.contains(bet.market, item.id.toString()));
        if (!market) {
          return;
        }
        ids.market = [market.id];
        const outcomes = _.filter(market.outcomes, (item: IOutcome) => _.contains(bet.outcome, item.id.toString()));
        if (outcomes && outcomes.length) {
          ids.outcome = outcomes.map(outcome => outcome.id);
          this.updateLegStatus({ bet, pushType, pushPayload, legItem, market, outcomes, ids, updateId });
        }
      }
    });
  }

  /**
   * Updates bet from map with values returned from proxy
   * @param {CashoutBet} bet
   * @param {ICashOutBet} updatedBet
   * @private
   */
  private updateBetFromProxyResponse(bet: CashoutBet, updatedBet: ICashOutBet, fromBetUpdate = false): void {
    if (updatedBet.cashoutValue && !bet.inProgress) {
      bet.isConfirmed = false;

      if (Number(updatedBet.cashoutValue)) {
        bet.partialCashoutStatus = updatedBet.partialCashoutStatus;
        bet.isPartialCashOutAvailable = updatedBet.partialCashoutAvailable === this.CASH_OUT.result.YES &&
          Number(updatedBet.cashoutValue) >= this.CASH_OUT.minValueForPartial;

        if (updatedBet.shouldActivate) {
          bet.resetCashoutSuspendedState();
        }

        if (updatedBet.stake) {
          bet.stake = updatedBet.stake;
          bet.stakePerLine = updatedBet.stakePerLine;
          if(!fromBetUpdate){
            bet.potentialPayout = bet.betModelService.getPotentialPayout(updatedBet);
          }
        }
      } else {
        updatedBet.currencySymbol = bet.currencySymbol;
        bet.panelMsg = this.cashoutErrorMessageService.getErrorMessage(updatedBet);

        bet.isPartialCashOutAvailable = false;
        bet.cashoutStatus = updatedBet.cashoutStatus;
      }
      /**
       * if current status of isPartialActive is true then on update if isPartialCashOutAvailable === false then
       * partial cashOut Slider (isPartialActive) is not needed anymore
       */
      if (bet.isPartialActive) {
        bet.isPartialActive = bet.isPartialCashOutAvailable;
      }
      bet.cashoutValue = updatedBet.cashoutValue;
      bet.cashoutStatus = updatedBet.cashoutStatus;
      const hasCashOutStake = bet.cashoutValue && Number(bet.cashoutValue);
      bet.isCashOutUnavailable = !hasCashOutStake;
      if (hasCashOutStake && !updatedBet.shouldActivate && bet.legType === 'E' && bet.leg?.length > 0 && this.isLive(bet) && this.isHRCategory(bet.leg) && bet.leg[0].part && this.isEnabledBIRMarket(bet.leg)) {
        bet.panelMsg = {
          type: cashoutConstants.cashOutAttempt.SUSPENDED
        };
        bet.isPartialCashOutAvailable = false;
        bet.cashoutValue = CASHOUT_SUSPENDED;
        bet.isCashOutUnavailable = true;
      }
      if(bet.potentialPayout === 0){
        bet.potentialPayout = 'N/A';
      }
      this.pubsubService.publish(this.pubsubService.API.UPDATE_CASHOUT_BET, bet);
    }
  }

  /**
   * returns true if any one leg in bet is live
   * @param {CashoutBet} bet 
   * @returns boolean
   */
   private isLive(bet: CashoutBet): boolean {
    return bet.leg.some(leg => leg.is_off && leg.status === 'open');
  }

  /**
 * @param  {IBetHistoryLeg[]} legs
 * @returns boolean
 */
  private isHRCategory(legs: IBetHistoryLeg[]): boolean {
    return legs.every((leg: IBetHistoryLeg) => leg.eventEntity?.categoryId === environment.HORSE_RACING_CATEGORY_ID);
  }

  /**
   * @param  {IBetHistoryLeg[]} legs
   * @returns boolean
   */
  private isEnabledBIRMarket(legs: IBetHistoryLeg[]): boolean {
    return legs.every((leg: IBetHistoryLeg) => {
      return this.BIRMarketsEnabled?.some((market: string) =>
        leg.part && (leg.part[0]?.eventMarketDesc?.toLocaleLowerCase() === market.toLocaleLowerCase()));
    });
  }

  /**
   * Sets updated dispResult after getBetDetail
   * @param bet {ICashOutBet}
   * @param updatedBet {ICashOutBet}
   * @private
   */
  private updateDispResult(bet: ICashOutBet, updatedBet: ICashOutBet): void {
    _.each(bet.leg, (leg: ICashOutBetLeg, i): void => {
      if (updatedBet && updatedBet.leg &&
          updatedBet.leg[i] && updatedBet.leg[i].part &&
          updatedBet.leg[i].part[0] && updatedBet.leg[i].part[0].dispResult) {
        leg.part[0].dispResult = updatedBet.leg[i].part[0].dispResult;
      }
    });
  }

  /**
   * Updates each leg part result property
   * @param {ICashOutBet} result
   * @param {IPayload} update
   * @private
   */
  private updateLegPartResult(result: string, update: ILiveServeUpd): void {
    if (this.cashOutMapIndexService.event[update.id]) {
      _.each(this.cashOutMapIndexService.event[update.id], (item: ICashoutMapItem) => {
        _.each(this.betsMap[item.id].leg, (leg: ICashOutBetLeg) => {
          _.each(leg.part, (part: ICashOutBetLegPart) => {
            if (Number(part.outcomeId || part.outcome) === Number(update.id)) {
              part.result = result;
            }
          });
        });
      });
    }
  }

  /**
   * Updates each selection status for placed bets
   * @param {Array} betIds
   * @param {string} id
   * @param {string} type
   * @param {IPayload} updatePayload
   * @private
   */
  private updatePlacedBetsStatuses(betIds: string[], id: string, type: string, updatePayload: IPayload): void {
    _.each(betIds, (betId: string) => {
      const bet: ICashOutBet = this.betsMap[betId];

      if (bet && (_.contains(bet.event, id) || _.contains(bet.market, id) || _.contains(bet.outcome, id))) {
        this.updateBetAccordingToPush(bet, id, type, updatePayload);
      }
    });
  }

  /**
   * Updates Event Entity with scores or clock
   * @param {string} channelType
   * @param {ILiveServeUpd} update
   */
  private updateEventEntity(channelType: string, update: ILiveServeUpd): void {
    const payload: IPayload = update.payload;
    let updateFn;

    if (channelType === this.CASH_OUT.channelName.score) {
      updateFn = this.eventCommentsUpdate.bind(this);

      // TODO (BMA-40873): must be removed after refactoring services for live updates
      this.pubsubService.publish(this.pubsubService.API.CASHOUT_LIVE_SCORE_UPDATE, update);
    }

    if (channelType === this.CASH_OUT.channelName.clock) {
      updateFn = this.eventClockUpdate.bind(this);
    }

    if (this.betsMap && this.cashOutMapIndexService && this.cashOutMapIndexService.event[update.id]) {
      this.cashOutMapIndexService.event[update.id].forEach((item: { id: string }) => {
        if (!this.betsMap[item.id]) {
          return;
        }
        this.betsMap[item.id].leg.forEach((leg: ICashOutBetLeg) => {
          if (leg.eventEntity && update.id === leg.eventEntity.id) {
            if (channelType === this.CASH_OUT.channelName.event) {
              const scoreInfo = this.scoreParser.parseTypeAndScores(payload.names && payload.names.en, leg.eventEntity.categoryCode);
              payload.scores = scoreInfo && scoreInfo.score;
              payload.scoreType = scoreInfo && scoreInfo.scoreType;
              updateFn = this.updateScoresFromNames.bind(this);

              // TODO (BMA-40873): must be removed after refactoring services for live updates
              this.pubsubService.publish(this.pubsubService.API.CASHOUT_LIVE_SCORE_EVENT_UPDATE, update);
            }
            updateFn(payload, leg.eventEntity);
          }
        });
      });
    }
  }

  /**
   * Extend event(s) cache with updated data.
   *
   * @param {Object} payload - object with new comments data
   * @param {ISportEvent} obj - event which need to update
   */
  private eventCommentsUpdate(payload: IPayload, obj: ISportEvent): void {
    const methodName = `${obj.categoryCode.toLowerCase()}UpdateExtend`;
    const extender = this.commentsService[methodName];

    if (obj.comments && extender) {
      extender(obj.comments, payload);
      this.commentsService.extendWithScoreType(obj, obj.categoryCode);
    }
  }

  /**
   * Extend event(s) with updated scores.
   *
   * @param {Object} payload - object with new data
   * @param {ISportEvent} obj - object which need to update
   */
  private updateScoresFromNames(payload: IPayload, obj: ISportEvent): void {
    if (payload.scoreType) {
      obj.scoreType = payload.scoreType;
    }
    if (!payload.scores) {
      return;
    }
    if (obj.comments) {
      this.commentsService.sportUpdateExtend(obj.comments, payload.scores);
    } else {
      obj.comments = {
        teams: payload.scores
      };
    }
  }

  /**
   * Extend event(s) cache with updated clock.
   * @param {object} payload - object with new clock data
   * @param {object} obj - event which need to update
   */
  private eventClockUpdate(payload: IPayload, obj: ISportEvent): void {
    if (Number(payload.ev_id) === obj.id && obj.clock) {
      obj.clock.refresh(payload);
    }
  }

  /**
   * Fires event id if event has started
   * @param {ILiveServeUpd} update
   */
  private eventStartedUpdate(update: ILiveServeUpd): void {
    if(update.payload.started === PAYLOAD_STATUSES.YES && update.payload.status === PAYLOAD_STATUSES.ACTIVE) {
      this.pubsubService.publish(this.pubsubService.API.EVENT_STARTED, update.id.toString());
    }
    if(update.payload.is_off === 'Y') {
      this.pubsubService.publish('IS_LIVE', update.id.toString());
    }
  }
}

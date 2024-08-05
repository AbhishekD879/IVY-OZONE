import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { PlacedBet } from '../../betModels/placedBet/placed-bet.class';
import { RegularBet } from '../../betModels/regularBet/regular-bet.class';
import { CashoutBet } from '../../betModels/cashoutBet/cashout-bet.class';
import { CashoutErrorMessageService } from '../cashoutErrorMessageService/cashout-error-message.service';
import { cashoutConstants } from '../../constants/cashout.constant';

import { CashOutMapService } from '../cashOutMap/cash-out-map.service';
import { UserService } from '@core/services/user/user.service';
import { CashOutLiveServeUpdatesService } from '@app/betHistory/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import {
  CashOutLiveUpdatesSubscribeService
} from '@app/betHistory/services/cashOutLiveUpdatesSubscribeService/cashOutLiveUpdatesSubscribeService';
import { BetModelService } from '../betModelService/bet-model.service';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import { BetHistoryMainService } from '../betHistoryMain/bet-history-main.service';

import { IBetHistoryBet, IBetHistoryLeg, IMatchCmtryData } from '../../models/bet-history.model';
import { ICashOutData } from '../../models/cashout-section.model';
import { ITypesAndIds } from '@app/betHistory/models/bet-history-cash-out.model';
import { Observable } from 'rxjs';
import { RegularBetBase } from '@app/betHistory/betModels/regularBetBase/regular-bet-base.class';
import { LocaleService } from '@core/services/locale/locale.service';
import { ISystemConfig } from '@core/services/cms/models';
import { betLegConstants, MATCH_TIME_CONFIG, MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { HandleVarReasoningUpdatesService } from '@app/lazy-modules/bybHistory/services/handleVarReasonsUpdatesService/handle-var-reasoning-updates.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { StorageService } from '@core/services/storage/storage.service';
import { BetReceiptService } from '@betslip/services/betReceipt/bet-receipt.service';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class CashoutSectionService {

  readonly cashoutConstants = cashoutConstants;
  sortNotFilered: any;
  cashOutMapIndex: any;
  private freeBetMsg: string;
  private betTokenMsg: string;
  private liveServeSubscribers: string[] = [];
  private isMatchTime: boolean;

  constructor(
    private cashOutMapService: CashOutMapService,
    private userService: UserService,
    private cashOutLiveServeUpdatesService: CashOutLiveServeUpdatesService,
    private pubSubService: PubSubService,
    private cashOutLiveUpdatesSubscribeService: CashOutLiveUpdatesSubscribeService,
    private betModelService: BetModelService,
    private cashOutMapIndexService: CashoutMapIndexService,
    private betHistoryMainService: BetHistoryMainService,
    private cashOutErrorMessage: CashoutErrorMessageService,
    private locale: LocaleService,
    private windowRef: WindowRefService,
    private handleVarReasoningUpdatesService : HandleVarReasoningUpdatesService,
    private cmsService : CmsService,
    private storageService: StorageService,
    private betReceiptService: BetReceiptService
  ) {
    this.freeBetMsg = this.locale.getString('bethistory.cashoutBet.freeBetNotification');
    this.betTokenMsg = this.locale.getString('bethistory.cashoutBet.betTokenNotification');
  }

  /**
   * Generate bets object with appropriate properties
   */
  generateBetsMap(betsArray: { [key: string ]: CashoutBet | RegularBet | PlacedBet },
                  betLocation: string): { [key: string ]: CashoutBet | RegularBet | PlacedBet } {
    const betsMap = {};
    _.each(betsArray, item => {
      if (_.isEmpty(item)) {
        return;
      }
      if (betLocation === 'cashOutSection' && this.cashOutMapService.cashoutBetsMap[item.betId]) {
        this.setObjectProperty(betsMap, item.betId);
      } else if (item.betId) {
        betsMap[item.betId] = item;
      }
    });
    return betsMap;
  }

  /**
   * map bets array from bets data to represent them in view
   * in certain order
   */
  generateBetsArray(betsMap: { [key: string ]: CashoutBet | RegularBet | PlacedBet }, betLocation: string): ICashOutData[] {
    return this.sortBetsByTime(betsMap)
      .map(bet => {
        return { eventSource: bet, location: betLocation };
      });
  }

  /**
   * fire Connect callback for counter on Event detail page
   *
   */
  emitMyBetsCounterEvent(bets: ICashOutData[]): void {
    this.pubSubService.publish(this.pubSubService.API.EVENT_MY_BETS_COUNTER, bets.length);
  }

  getMyBetsIds(myBets: { [key: string]: PlacedBet | CashoutBet }): ITypesAndIds {
    const myBetsIds = { event: [], market: [], outcome: [] };

    _.forEach(myBets, (bet: PlacedBet | CashoutBet) => {
      myBetsIds.outcome = _.uniq(bet.outcome.concat(myBetsIds.outcome));
      myBetsIds.market = _.uniq(bet.market.concat(myBetsIds.market));
      myBetsIds.event = _.uniq(bet.event.concat(myBetsIds.event));
    });
    return myBetsIds;
  }

  /**
   * generate temp bets data for event detail page
   * (includes both cashout and placed bets)
   *
   */
  createTempDataForMyBets(cashoutIds: { id: number, isSettled?: boolean }[],
                          placedBets: IBetHistoryBet[]): { [key: string ]: PlacedBet | CashoutBet } {
    const tempData = {};

    if (cashoutIds) {
      cashoutIds.forEach(cashoutObj => {
        if (!cashoutObj.isSettled) {
          const cashoutBetMap = this.cashOutMapService.cashoutBetsMap[cashoutObj.id];
          if (cashoutBetMap) {
            tempData[cashoutObj.id] = cashoutBetMap;
          }
        }
      });
    }

    if (placedBets) {
      const { currency, currencySymbol } = this.userService;

      placedBets.forEach((item: IBetHistoryBet) => {
        const bet = new CashoutBet(item, this.betModelService, currency, currencySymbol,
          this.cashOutMapIndexService, this.cashOutErrorMessage);

        if (!tempData[bet.betId] && bet.cashoutStatus !== 'BET_CASHED_OUT' && bet.settled !== 'Y') {
          if (bet.isCashOutUnavailable) {
            bet.type = 'placedBetsWithoutCashoutPossibility';
          }
          tempData[bet.betId] = bet;
        }
      });

      const myBetsIds = this.getMyBetsIds(tempData);
      this.cashOutLiveUpdatesSubscribeService.addWatchForPlacedEventsOnly(tempData, myBetsIds);
    }
    return tempData;
  }

  /**x
   * generate bets data for open bets -> regular
   *
   */
  createDataForRegularBets(regularBets = []): { [key: string ]: RegularBet } {
    const tempData: { [key: string ]: RegularBet } = {};
    if (regularBets) {
      const { currency, currencySymbol } = this.userService;

      regularBets.forEach(item => {
        const bet: RegularBet = new RegularBet(
          item,
          this.betModelService,
          currency,
          currencySymbol,
          this.cashOutMapIndexService,
          this.betHistoryMainService,
          this.locale,
          this.cashOutErrorMessage,
          this.cashoutConstants,
        );
        tempData[bet.betId] = bet;
      });

      const myBetsIds = this.getMyBetsIds(tempData);
      this.cashOutLiveUpdatesSubscribeService.addWatchForRegularBets(tempData, myBetsIds);
    }
    return tempData;
  }

  /**
   * register directive's controller inside CashoutLiveServUpdateFactory
   *
   */
  registerController(controllerName: string): void {
    this.liveServeSubscribers.push(controllerName);
    this.pubSubService.publish(this.pubSubService.API.CASHOUT_CTRL_STATUS, { ctrlName: controllerName, isDestroyed: false });
  }

  /**
   * Removes bethistory item from list
   * in order to remove - cashout status (if given) should match
   */
  removeCashoutItemWithTimeout(data: { [key: string ]: RegularBet | CashoutBet }, options: { [key: string ]: any }): Observable<null> {
    return Observable.create((observer) => {
      this.sortNotFilered = setTimeout(() => {
        const betId = options.betId;
        const bet = data[betId];
        const isSettled = bet && (bet.cashoutStatus === 'BET_SETTLED' || bet.cashoutStatus === 'BET_CASHED_OUT');
        if (bet && (!options.isRegularBets || isSettled)) {
          this.unsubscribeFromDeletedBetUpdates(data, bet);
          delete data[betId];
          this.sortNotFilered = null;
        }
        observer.next(null);
        observer.complete();
      }, this.cashoutConstants.tooltipTime);
    });
  }

  /**
   * Hides cashout item's red error box on My Bets tab
   */
  removeErrorMessageWithTimeout(bets: ICashOutData[], options) {
    const bet = _.find(bets, item => {
      return item.eventSource.betId === options.betId;
    });

    if (bet) {
      bet.eventSource.isCashOutUnavailable = true;
      (bet.eventSource as CashoutBet).isPartialCashOutAvailable = false;

      // check cashout before update
      if (options.prevCashoutStatus && !this.sortNotFilered) {
        bet.eventSource.type = 'placedBetsWithoutCashoutPossibility';
      } else {
        this.sortNotFilered = setTimeout(() => {
          (bet.eventSource as CashoutBet).isCashOutBetError = false;
          bet.eventSource.type = 'placedBetsWithoutCashoutPossibility';
          this.sortNotFilered = null;
        }, this.cashoutConstants.tooltipTime);
      }
    }
  }

  /**
   * destroy syncs for certain controller
   * @param name {string}
   * @private
   *
   */
  removeListeners(name: string): void {
    this.liveServeSubscribers = this.liveServeSubscribers.filter((item: string) => item !== name);

    // Clear syncs added for both cashout and myBets controllers
    this.pubSubService.unsubscribe(name);

    // Clear all syncs for cashout functionality on event detail page
    if (name === this.cashoutConstants.controllers.MY_BETS_CTRL) {
      this.pubSubService.unsubscribe('eventPlacedBet');
    }

    if (!this.liveServeSubscribers.length) {
      this.pubSubService.publish(this.pubSubService.API.UNSUBSCRIBE_LS_UPDATES_MS);
      this.cashOutLiveServeUpdatesService.betsMap = {};
    }
  }

  /**
   * Update cashout bet(needed for my bets and cashout widget)
   * @param bet
   * @param bets
   */
  updateBet(bet: CashoutBet, bets: ICashOutData[]): void {
    const oldBet = _.find(bets, b => b.eventSource.betId === bet.betId);
    oldBet && _.extend(oldBet.eventSource, bet);
  }

  /**
   * Check if is cashout attempt error or cashout is unavailable
   * @param { RegularBetBase } bet - bet object
   * @returns {boolean}
   */
  isCashoutError(bet: RegularBetBase): boolean {
    return bet.isCashOutBetError || bet.isCashOutUnavailable || bet.hasFreeBet;
  }

  /**
   * Get cashout attempt error or unavailable message
   * @param {RegularBetBase} bet - bet object
   * @returns {string}
   */
  getCashoutError(bet: RegularBetBase): string {
    return (bet.attemptPanelMsg && bet.attemptPanelMsg.msg) ||
     (bet.panelMsg && bet.panelMsg.msg) ||
     (bet.tokenType?.replace(/ /g, '').toUpperCase() === this.locale.getString('bs.betTokenSp') && !bet.isCashOutUnavailable && this.betTokenMsg)|| 
      (bet.hasFreeBet && !bet.isCashOutUnavailable && this.freeBetMsg);
  }

  /**
   * To Get Leaderboard config
   * @param {ISystemConfig} config
   * @returns {boolean}
   */
  getLeaderBoardConfig(config: ISystemConfig): boolean {
    return config && config.myBetsSection;
  }
  /**
   * Defines certain object certain project
   */
  private setObjectProperty(obj: object, betId: string): void {
    Object.defineProperty(obj, betId,
      {
        enumerable: true,
        configurable: true,
        get: () => {
          return this.cashOutMapService.cashoutBetsMap[betId];
        }
      }
    );
  }

  /**
   * Sort Bets by creation date and by eventStartTimeStamp
   * if creation date is the same than by event start time
   * replace is needed to fix safari bug
   */
  private sortBetsByTime(betsData: { [key: string ]: CashoutBet | RegularBet | PlacedBet }): (CashoutBet | RegularBet | PlacedBet)[] {
    return _.chain(betsData)
      .compact()
      .filter(bet => {
        return bet instanceof CashoutBet || bet instanceof RegularBet || bet instanceof PlacedBet;
      })
      .sortBy('minEventStartTimeStemp')
      .sortBy(bet => {
        return -(new Date(bet.date.replace(/-/g, '/')).getTime());
      })
      .value();
  }

  /**
   * Get Entity(event/market/outcome) ids for which should unsubscribe from Live Updates
   * @param bets - all bets array
   * @param deletedBet - deleted bet
   * @param entityType - entity type (event, market or outcome)
   */
  private getIdsToUnsubscribe(bets: (RegularBet | CashoutBet)[], deletedBet: RegularBet | CashoutBet,  entityType: string)
    : { entitiesToUnsubscribe: string[], betsWithSameEntity: (RegularBet | CashoutBet)[] } {
    const entitiesToDelete = deletedBet[entityType].slice();
    const betsWithSameEntityMap = {};

    deletedBet[entityType].forEach((entityIdFromDeletedBet: string) => {
      bets.forEach(eachBet => {
        if (eachBet.betId === deletedBet.betId) {
          return;
        }
        const indexOfMatchedEntity = eachBet[entityType].indexOf(entityIdFromDeletedBet);
        if (indexOfMatchedEntity === -1) {
          return;
        }
        betsWithSameEntityMap[eachBet.betId] = eachBet;
        const indexToDelete = entitiesToDelete.indexOf(entityIdFromDeletedBet);
        if (indexToDelete === -1) {
          return;
        }
        entitiesToDelete.splice(indexToDelete, 1);
      });
    });

    return {
      entitiesToUnsubscribe: entitiesToDelete,
      betsWithSameEntity: Object.values(betsWithSameEntityMap)
    };
  }

  /**
   * Unsubscribe from events/markets/outcomes which belong deleted Bet only if they not included into other bets
   * @param betsMap
   * @param deletedBet
   */
  private unsubscribeFromDeletedBetUpdates(betsMap: { [key: string ]: RegularBet | CashoutBet },
                                           deletedBet: RegularBet | CashoutBet): void {
    const eventsToUnsubscribeInfo = this.getIdsToUnsubscribe(Object.values(betsMap), deletedBet, 'event'),
      marketsToUnsubscribeInfo = this.getIdsToUnsubscribe(eventsToUnsubscribeInfo.betsWithSameEntity, deletedBet, 'market'),
      outcomesToUnsubscribeInfo = this.getIdsToUnsubscribe(marketsToUnsubscribeInfo.betsWithSameEntity, deletedBet, 'outcome');

    const unsubscribeParams = {
      event: eventsToUnsubscribeInfo.entitiesToUnsubscribe,
      market: marketsToUnsubscribeInfo.entitiesToUnsubscribe,
      outcome: outcomesToUnsubscribeInfo.entitiesToUnsubscribe
    };

    const areItemsToUnsubscribe = !!(['event', 'market', 'outcome'].reduce(
      (currentValue: number, entityType: string) => currentValue + unsubscribeParams[entityType].length, 0));

    if (areItemsToUnsubscribe) {
      this.pubSubService.publish(this.pubSubService.API.UNSUBSCRIBE_LS_UPDATES_MS, unsubscribeParams);
    }
  }
  /**
   * Updates bet-leg with match-commentary data when ever available
   * @param bets 
   * @param matchCmtryDataUpdate 
   */
   matchCommentaryDataUpdate(bets: ICashOutData[], matchCmtryDataUpdate: IMatchCmtryData, section: MYBETS_AREAS = MYBETS_AREAS.WIDGET): void {
    bets && bets.forEach((bet: ICashOutData) => {
      if (bet?.eventSource?.event && bet.eventSource.event.includes(matchCmtryDataUpdate?.matchCmtryEventId)) {
        bet.eventSource.leg && bet.eventSource.leg.forEach((leg: IBetHistoryLeg) => {
          if (leg?.hasOwnProperty('eventEntity') && leg.eventEntity.id?.toString() == matchCmtryDataUpdate.matchCmtryEventId) {
            if (matchCmtryDataUpdate.varIconData != null) {
              leg.matchCmtryDataUpdate = {
                varIconData: {
                  svgId: matchCmtryDataUpdate.varIconData.svgId,
                  description: matchCmtryDataUpdate.varIconData.description
                },
                teamName: matchCmtryDataUpdate.teamName?.toUpperCase(),
                playerName: matchCmtryDataUpdate.playerName?.toUpperCase()
              };
            }
            else {
               leg.matchCmtryDataUpdate = matchCmtryDataUpdate && this.getMatchfactsUpdate(matchCmtryDataUpdate);
            }   
            if (leg.myBetsAreas && leg.myBetsAreas[section]) {
              leg.myBetsAreas[section].isMatchCmtryDataAvailable = true;
            }
            else if (leg.myBetsAreas) {
              leg.myBetsAreas[section] = { isMatchCmtryDataAvailable: true };
            }
            else {
              leg.myBetsAreas = { [section]: { isMatchCmtryDataAvailable: true } };
            }
            if (leg.matchCmtryTimeInterval && leg.myBetsAreas && leg.myBetsAreas[section] && leg.myBetsAreas[section].isMatchCmtryDataAvailable) {
              this.windowRef.nativeWindow.clearInterval(leg.matchCmtryTimeInterval);
            }
            this.isMatchTime = leg.matchCmtryDataUpdate.matchfact === MATCH_TIME_CONFIG.STOP_FIRST_HALF || leg.matchCmtryDataUpdate.matchfact === MATCH_TIME_CONFIG.STOP_FIRST_HALF_EXTRA_TIME ? true : false;
            leg.matchCmtryTimeInterval =  !this.isMatchTime && this.windowRef.nativeWindow.setTimeout(() => {
              for (section in leg.myBetsAreas) {
                leg.myBetsAreas[section].isMatchCmtryDataAvailable = false;
              }
              leg.matchCmtryTimeInterval = betLegConstants.matchCmtryTimeIdRefreshTime;
            }, betLegConstants.matchCmtryDisplaytime);
          }
        });
      }
    });
  }
  /**
   * Assigns data to leg.matchCmtryDataUpdate object
   * @param matchCmtryDataUpdate 
   * @returns object with teamName, matchfact and playerName
   */
  private getMatchfactsUpdate(matchCmtryDataUpdate: IMatchCmtryData): IMatchCmtryData {
    return {
      teamName: matchCmtryDataUpdate.teamName && this.transformMatchFact(matchCmtryDataUpdate.teamName),
      matchfact: this.transformMatchFact(matchCmtryDataUpdate.matchfact?.replace(betLegConstants.underScoreRegex, betLegConstants.replacedText)),
      playerName: matchCmtryDataUpdate.playerName ? this.transformMatchFact(matchCmtryDataUpdate.playerName) : null,
      playerOffName: matchCmtryDataUpdate.playerOffName ? this.transformMatchFact(matchCmtryDataUpdate.playerOffName) : null,
      playerOnName: matchCmtryDataUpdate.playerOnName ? this.transformMatchFact(matchCmtryDataUpdate.playerOnName) : null,
      clock: matchCmtryDataUpdate.clock ? matchCmtryDataUpdate.clock : null,
      minutes: matchCmtryDataUpdate.minutes ? (betLegConstants.plus + matchCmtryDataUpdate.minutes+ betLegConstants.replacedText +(matchCmtryDataUpdate.minutes==='1'? betLegConstants.min : betLegConstants.mins)) : null
    };
  }
  /**
   * transforms the text in lower case in sync with display of match facts in EDP
   * @param matchFact 
   * @returns transformedMatchfact
   */
  private transformMatchFact(matchFact: string): string {
    let transformedMatchfact: string = "";
    const splitedMatchFact: string[] = matchFact?.split(betLegConstants.replacedText);
    splitedMatchFact?.forEach((matchFactItem:string) => {
      transformedMatchfact += matchFactItem.charAt(0).toUpperCase() + matchFactItem.slice(1).toLowerCase() + betLegConstants.replacedText;
    });
    return transformedMatchfact.trimEnd();
  }
  /**
   * send the request for last match facts
   * @param bets 
   */
  sendRequestForLastMatchFact(bets: ICashOutData[]):string[] {
    const channels: string[] = [];
    this.cmsService.getSystemConfig().subscribe((sysConfig: ISystemConfig) => {
      if (sysConfig && sysConfig.MybetsMatchCommentary && sysConfig.MybetsMatchCommentary.enabled) {
        bets?.forEach((bet: ICashOutData) => {
          bet?.eventSource && bet.eventSource.settled !== 'Y' && bet.eventSource.leg?.forEach((legItem: IBetHistoryLeg) => {
            if (legItem?.part && legItem.part[0].outcome) {
              const eventId = legItem.part[0].outcome[0].event?.id?.toString();
              const isFootball = legItem.part[0].outcome[0].eventCategory?.id === betLegConstants.footballId;
              const isEventLive = legItem.part[0].outcome[0].event?.isOff === 'Y';
              if (isFootball && isEventLive) {
                !channels.includes(betLegConstants.mFACTS + eventId) && channels.push(betLegConstants.mFACTS + eventId);
              }
            }
          });
        });
        channels.length && this.handleVarReasoningUpdatesService.sendRequestForLastMatchFact(channels);
      }
    });
    return channels;
  }
  /**
   * remove all the handlers 
   * @param channels 
   */
  removeHandlers(channels: string[]): void {
    this.handleVarReasoningUpdatesService.removeHandlers(channels);
  }

  /**
 * set the tooltip view status
 */
  setToolTipStatus(): void {
    const tooltipData = this.storageService.get('tooltipsSeen') || {},
      toolTipKey = `receiptViewsCounter-${this.userService.username}`;
    const receiptViewsCounter = tooltipData[toolTipKey] || null;
    tooltipData[toolTipKey] = receiptViewsCounter === null ? 1 : receiptViewsCounter + 1;
    this.storageService.set('tooltipsSeen', tooltipData);
  }
  getInitialStake(bet: RegularBet | CashoutBet): string | number {
    const betTerm = (bet.betTermsChange || []).filter(betTermsChange => betTermsChange.reasonCode === "ORIGINAL_VALUES");
    return betTerm.length>0 && betTerm[0].stake && betTerm[0].stake.value ? betTerm[0].stake.value : (typeof bet.stake === 'object' ? bet.stake.value : bet.stake);
  }
  // Check for lucky bonus
  checkLuckyBonus(bets){
    if(['L15', 'L31', 'L63'].includes(bets.eventSource.betType) && bets.eventSource.availableBonuses){
      return this.betReceiptService.luckyAllWinnersBonus(bets);
    }
  }
  // Check SP selections for lucky bonus
  checkSPSelection(bets){
    if(['L15', 'L31', 'L63'].includes(bets.eventSource.betType) && bets.eventSource.availableBonuses){
      return bets.eventSource && bets.eventSource.leg && bets.eventSource.leg.filter((legItem: IBetHistoryLeg) => {
        return legItem.part && legItem.part.every((item: any) => (item.price) ? item.price[0].priceType.code === 'S': item.priceType === 'S');
      }).length !== 0;
    }
  }
// Check for lucky bonus
  checkLuckyType(bets){
    if(['L15', 'L31', 'L63'].includes(bets.eventSource.betType) && bets.eventSource.availableBonuses && this.betReceiptService.isAllWinnerOnlyApplicable(bets.eventSource)){
       return true;
    }
  }
}

import { of as observableOf,  Observable } from 'rxjs';

import { finalize, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { DeviceService } from '@core/services/device/device.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SiteServerEventToOutcomeService } from '@app/ss/services/site-server-event-to-outcome.service';
import { StorageService } from '@core/services/storage/storage.service';

import { IPoolBetPlacementRequest, IPoolBetPlacementResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IConstant } from '@core/services/models/constant.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IRacingEvent } from '@core/models/racing-event.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IStakeRestrictions, IToteBet, IToteLeg } from './tote-betslip.model';
import { ILiveUpdateResponseMessage } from '@betslip/services/betslipLiveUpdate/betslip-live-update.model';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { UserService } from '@core/services/user/user.service';
import { CurrencyCalculatorService } from '@core/services/currencyCalculatorService/currency-calculator.service';
import { CurrencyCalculator } from '@core/services/currencyCalculatorService/currency-calculator.class';
import { IFreebetsPopupDetails } from '@app/core/services/cms/models/system-config';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { AuthService } from '@app/auth/services/auth/auth.service';

@Injectable({ providedIn: BetslipApiModule })
export class ToteBetslipService {
  betName: string;
  betTitle: string;
  correctedDay: string;
  eventTitle: string;
  isPlaceBetPending: boolean = false;
  isPotBet: boolean;
  numberOfLines: number;
  orderedLegs: any[];
  orderedOutcomes: IOutcome[];
  poolName: string;
  stakeRestrictions: IStakeRestrictions;
  toteBet: IToteBet = this.storageService.get('toteBet') || null;
  toteError: string;
  totalStakeTitle: string;
  toteSuspensionError: string = 'Please beware some of your selections have been suspended';
  poolCurrencyCode: string;
  poolCurrencySymbol: string;
  userCurrencyCode: string;
  currencyCalculator: CurrencyCalculator;
  freeBetsConfigData: IFreebetsPopupDetails;
  tokenValue: string;
  freeBetText: string;

  constructor(
    private bppService: BppService,
    private commandService: CommandService,
    private deviceService: DeviceService,
    private filterService: FiltersService,
    private localeService: LocaleService,
    private pubSubService: PubSubService,
    private siteServerEventToOutcomeService: SiteServerEventToOutcomeService,
    private storageService: StorageService,
    private clientUserAgentService: ClientUserAgentService,
    private coreToolsService: CoreToolsService,
    private userService: UserService,
    private currencyCalculatorService: CurrencyCalculatorService,
    private freeBetsService: FreeBetsService,
    private authService: AuthService
  ) {
    this.userCurrencyCode = userService.currency;
    this.addListeners();
  }

  /**
   * Add tote bet to Betslip
   * @param data
   */
  addToteBet(data: IToteBet, poolData?: IToteBet): void {
    this.storageService.set('toteBet', poolData ? poolData: data);
    this.pubSubService.publish(this.pubSubService.API.BETSLIP_COUNTER_UPDATE, 1);
    this.freeBetsService.getFreeBets().subscribe((freeBet: IFreebetToken[]) => {
      let freeBetsStorage = this.storageService.get(`freeBets-${this.userService.username}`);
      if(_.isString(freeBetsStorage)) {
        freeBetsStorage = JSON.parse(freeBetsStorage);
      }
      const freebets = freeBetsStorage ? freeBetsStorage.filter(bet => {
        return (bet.tokenPossibleBetTags && bet.tokenPossibleBetTags.tagName) ? bet.tokenPossibleBetTags.tagName !== 'FRRIDE' : bet;
      }) : [];
      this.authService.drillDownToteFreebets(freebets);
    });
    this.initialize(data);
  }

  /**
   * Unsubscribe from live updates
   */
  clear(): void {
    if (!this.toteBet || !this.toteBet.channelIds) {
      return;
    }

    this.pubSubService.publish(this.pubSubService.API.BETSLIP_LIVEUPDATE_UNSUBSCRIBE, [this.toteBet.channelIds]);
  }

  /**
   * Get leg title
   * @param leg - tote bet let object
   * @returns {string}
   */
  getLegTitle(leg: IToteLeg): string {
    return `${leg.name}: ${leg.eventTitle}`;
  }

  /**
   * Get selection name
   * @param outcome
   * @returns {string}
   */
  getSelectionName(outcome: IOutcome): string {
    return !outcome.isFavourite ? `${outcome.runnerNumber}. ${outcome.name}` : outcome.name;
  }

  getTotalStake(val?:number): string {
    const totalStakeInPoolCurrency = this.getTotalStakeValue(val);
    let totalStakeInUserCurrency;
    if (this.poolCurrencyCode && this.userCurrencyCode
      &&  this.poolCurrencyCode === this.userCurrencyCode) {
      totalStakeInUserCurrency = totalStakeInPoolCurrency;
    } else {
      totalStakeInUserCurrency = totalStakeInPoolCurrency && this.currencyCalculator
        ? this.currencyCalculator.currencyExchange(this.poolCurrencyCode, this.userCurrencyCode,
          totalStakeInPoolCurrency) : null;
    }
    return totalStakeInUserCurrency && (+totalStakeInUserCurrency).toFixed(2);
  }

  handleErrors(betFailure): void {
    const errorKey = betFailure.betError[0].betFailureKey,
      errorDesc = betFailure.betError[0].betFailureDesc;

    if (errorKey === 'LARGE_STAKE' || errorKey === 'SMALL_STAKE' || errorKey === 'STAKE_INCREMENT') {
      this.generateToteStakeError(errorKey);
    } else {
      const errorMessage = this.localeService.getString(`bs.TOTE_BET_ERRORS.${errorDesc}`);
      this.toteError = errorMessage === 'KEY_NOT_FOUND' ? betFailure.betError[0].betFailureReason : errorMessage;
    }
  }

  /**
   * Checks if there are any tote bets in tote betslip
   * @returns {boolean}
   */
  isToteBetPresent(): boolean {
    return !!this.toteBet;
  }

  /**
   * Checks if tote bet is with proper stake
   * @returns {boolean}
   */
  isToteBetWithProperStake(): boolean {
    return !!this.getTotalStakeValue();
  }

  /**
   * Placing bet from this.toteBet class property by making request to bet placement proxy
   * @returns {Promise}
   */
  placeBet(val): Observable<IPoolBetPlacementResponse> {
    if (!this.toteBet) {
      return observableOf(<IPoolBetPlacementResponse>{});
    }

    this.isPlaceBetPending = true;
    this.toteError = undefined;

    return this.bppService.send('placePoolBet',
      this.getPlacePoolBetObj(val)).pipe(
      map((response: IPoolBetPlacementResponse): IPoolBetPlacementResponse => {
        if (response.betFailure) {
          this.handleErrors(response.betFailure[0]);
          return <IPoolBetPlacementResponse>response.betFailure[0];
        }
        return response;
      }), finalize(() => {
        this.isPlaceBetPending = false;
      }));
  }

  reload(): void {
    this.toteBet = this.storageService.get('toteBet') || null;
    if (this.toteBet) {
      this.initialize(this.toteBet);
    }
  }

  /**
   * Remove tote bet from betslip
   * @param {boolean} withRefresh
   * @param {boolean} receipt
   * @returns {string}
   */
  removeToteBet(withRefresh: boolean = true, receipt?: boolean): void {
    this.toteError = undefined;
    this.toteBet = null;
    this.storageService.remove('toteBet');
    this.storageService.remove('toteSuspended');
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_COUNTER_UPDATE, 0);
    if (withRefresh) {
      this.pubSubService.publish(this.pubSubService.API.REFRESH_BETSLIP);
    }
    // Do not close betslip if need to show receipt
    if (!receipt) {
      this.pubSubService.publish(this.pubSubService.API['show-slide-out-betslip'], false);
    }
  }

  setStakePerLine(): void {
    this.setTotalStakeTitle();
  }


  private betslipUpdated(): void {
    this.pubSubService.publish(this.pubSubService.API.TOTE_BETSLIP_UPDATED, this.getToteBetSuspendedError());
  }

  private generateToteStakeError(errorCode: string): void {
    const maxStakePerLine = this.stakeRestrictions.maxStakePerLine,
      maxTotalStake = this.stakeRestrictions.maxTotalStake,
      minStakePerLine = this.stakeRestrictions.minStakePerLine,
      minTotalStake = this.stakeRestrictions.minTotalStake,
      stakeIncrementFactor = this.stakeRestrictions.stakeIncrementFactor,
      errorCodeMapper = {
        STAKE_INCREMENT: () => this.localeService.getString(`bs.TOTE_BET_ERRORS.${errorCode}`, [stakeIncrementFactor]),
        LARGE_STAKE: () => this.localeService.getString(`bs.TOTE_BET_ERRORS.${errorCode}`,
          [maxStakePerLine, maxTotalStake, this.poolCurrencySymbol]),
        SMALL_STAKE: () => this.localeService.getString(`bs.TOTE_BET_ERRORS.${errorCode}`,
          [minStakePerLine, minTotalStake, this.poolCurrencySymbol])
      };

    this.toteError = errorCodeMapper[errorCode]();
  }

  /**
   * Calculate exacta/trifecta total stakes
   * @returns {number}
   */
  private getNotPotBetTotalStake(): number {
    const bet = this.toteBet.poolBet,
      length = bet.poolItem.length,
      isExactaBet = _.contains(['UEXA', 'EX'], bet.poolType),
      isTrifectaBet = _.contains(['UTRI', 'TR'], bet.poolType),
      calculateTotalStake = linesNumber => Number(this.toteBet.poolBet.stakePerLine * linesNumber) || 0,
      isWinOrPlaceBet = _.contains(['UWIN', 'UPLC', 'WN', 'PL'], bet.poolType),
      isStrightExactaOrTrifecta = _.contains([
        this.localeService.getString('uktote.strightExactaBet'),
        this.localeService.getString('uktote.strightTrifectaBet')
      ], this.betName);

    let combinationMultiplicator: number;

    // Stright Exacta or Trifecta bet case
    if (isStrightExactaOrTrifecta) {
      return calculateTotalStake(1);
    }

    // Win of Place bet case
    if (isWinOrPlaceBet) {
    return calculateTotalStake(length);
    }

    // Combination exacta bet case
    if (isExactaBet) {
      combinationMultiplicator = length * (length - 1);
      return calculateTotalStake(combinationMultiplicator);
    }

    // Combination trifecta bet case
    if (isTrifectaBet) {
      combinationMultiplicator = length * (length - 1) * (length - 2);
      return calculateTotalStake(combinationMultiplicator);
    }
    console.error('Missed formula for bet type ', bet.poolType);
  }

  /**
   * Extend bet object with user and device details
   * @private
   * @returns {Object}
   */
  private getPlacePoolBetObj(val): IPoolBetPlacementRequest {
    const totePoolBet = this.storageService.get('toteBet') || null;
    const poolBetObj = {...this.toteBet.poolBet};
    poolBetObj.stakePerLine = this.calculateStakePerLine(totePoolBet, val);
    if(totePoolBet && totePoolBet.poolBet.freebetTokenId) {
      poolBetObj.freebetTokenId = totePoolBet.poolBet.freebetTokenId;
    } else {
      if(poolBetObj.freebetTokenValue) {
        delete poolBetObj.freebetTokenValue;
      } 
      if(poolBetObj.freebetTokenId) {
        delete poolBetObj.freebetTokenId;
      }
     }
    return {
      channel: this.deviceService.channel.channelRef.id,
      clientUserAgent: this.clientUserAgentService.getId(),
      fullDetails: 'Y',
      poolBet: [poolBetObj]
    };
  }

  /**
   * Calculate stake per line
   * @returns {number}
   * @private
   */
  private calculateStakePerLine(totePoolBet, val='0.00'): number {
    let freeBetPerLine;
    if(totePoolBet.poolBet.freebetTokenValue) {
      freeBetPerLine = (Number(totePoolBet.poolBet.freebetTokenValue)/this.calculateNumOfLines(totePoolBet));
    }
    if(Number(this.toteBet.poolBet.stakePerLine <= 0) || this.toteBet.poolBet.stakePerLine === undefined || this.toteBet.poolBet.stakePerLine === null) {
      return this.getRoundedValue(freeBetPerLine);
    } else {
      if(totePoolBet.poolBet.freebetTokenValue) {
        const x = (Number(totePoolBet.poolBet.freebetTokenValue)+Number(val))/Number(this.calculateNumOfLines(totePoolBet));
        return this.getRoundedValue(x);
      } else {
        return this.getRoundedValue(this.toteBet.poolBet.stakePerLine)
      }
    }
  }

  calculateNumOfLines(totePoolBet): number {
    let numberOfLines;
    if(totePoolBet.poolBet.poolType === 'UTRI') {
      numberOfLines = Number(totePoolBet.toteBetDetails.betName.split(' ')[0]);
    } else if(totePoolBet.poolBet.poolType === 'UEXA') {
      if(totePoolBet.toteBetDetails.betName.split(' ')[0] === '1' && totePoolBet.toteBetDetails.betName.split(' ')[1] === 'REVERSE') {
        numberOfLines = 2;
      } else {
        numberOfLines = Number(totePoolBet.toteBetDetails.betName.split(' ')[0]);
      }
    } else {
      let orderedOutcomes = 0;
      if(this.toteBet.toteBetDetails && this.toteBet.toteBetDetails.orderedOutcomes){
        orderedOutcomes = this.toteBet.toteBetDetails.orderedOutcomes.length;
      }
      numberOfLines = (this.toteBet.toteBetDetails && this.toteBet.toteBetDetails.numberOfLines) ? this.toteBet.toteBetDetails.numberOfLines : orderedOutcomes;
    }
    return numberOfLines;
  }

  /**
   * Calculate total stake value
   * @returns {number}
   * @private
   */
  private getTotalStakeValue(val?: number): number {
    if (!this.toteBet || !this.toteBet.poolBet || !this.toteBet.poolBet.stakePerLine) {
      return 0;
    }
    /**
     * Placepot, Jackpot etc
     */
    if (this.isPotBet) {
      if(val) {
        return (Number(this.toteBet.poolBet.stakePerLine) * this.numberOfLines) - val;
      } else {
        return Number(this.toteBet.poolBet.stakePerLine) * this.numberOfLines;
      }
    }
    /**
     * Exacta, Trifecta etc
     */
    return this.getNotPotBetTotalStake() === 0 ? this.getNotPotBetTotalStake() : (this.getNotPotBetTotalStake() - (val||0));
}

  /**
   * Check if TOTE bet is suspended
   * @returns {string}
   */
  private getToteBetSuspendedError(): string {
    const toteEvents: IRacingEvent[] = this.toteBet && this.toteBet.events,
      selectedOutcomes = this.toteBet ? _.pluck(this.toteBet.outcomes, 'id') : [],
      isSuspendedMap: IConstant = {},
      suspentionPriority = ['EVENT', 'MARKET', 'OUTCOME'];
    if (!toteEvents) {
      return '';
    }
    const toteMarkets = _.compact(
      _.flatten(
        _.pluck(toteEvents, 'markets')
      )
    );
    const toteOutcomes = _.chain(toteMarkets)
      .pluck('outcomes')
      .compact()
      .flatten()
      .filter(outcome => _.contains(selectedOutcomes, outcome.id.toString()))
      .value();

    isSuspendedMap.EVENT = _.some(toteEvents, toteEvent => toteEvent.eventStatusCode === 'S');
    isSuspendedMap.MARKET = _.some(toteMarkets, toteMarket => toteMarket.marketStatusCode === 'S');
    isSuspendedMap.OUTCOME = _.some(toteOutcomes, toteOutcome => toteOutcome.outcomeStatusCode === 'S');
    const suspendedItemsTypes = _.filter(suspentionPriority, itemType => isSuspendedMap[itemType]);

    return suspendedItemsTypes.length ? this.localeService.getString(`bs.${suspendedItemsTypes[0]}_SUSPENDED`) : '';
  }

  /**
   * Provide initialization with provided data
   * @param data
   * @private
   */
  private initialize(data: IToteBet): void {
    this.toteBet = data;
    this.betName = data.toteBetDetails.betName;
    this.eventTitle = data.toteBetDetails.eventTitle;
    this.correctedDay = data.toteBetDetails.correctedDay;
    this.orderedOutcomes = data.toteBetDetails.orderedOutcomes;
    this.poolName = data.toteBetDetails.poolName;
    this.orderedLegs = data.toteBetDetails.orderedLegs;
    this.isPotBet = !!data.toteBetDetails.orderedLegs;
    this.numberOfLines = data.toteBetDetails.numberOfLines ? data.toteBetDetails.numberOfLines : data.toteBetDetails.orderedOutcomes?.length;
    this.stakeRestrictions = data.toteBetDetails.stakeRestrictions;
    this.poolCurrencyCode = this.toteBet && this.toteBet.poolCurrencyCode;
    this.poolCurrencySymbol = this.coreToolsService.getCurrencySymbolFromISO(this.poolCurrencyCode);

    this.setBetTitle();
    this.setTotalStakeTitle();

    // Get currency exchange calculator instance
    this.currencyCalculatorService.getCurrencyCalculator()
      .subscribe(calculator => {
        this.currencyCalculator = calculator;
      });

    this.loadFixedOddsEvents()
      .then((fixedOddsEvents: ISportEvent[]) => {
        this.updateToteEventsStatuses(fixedOddsEvents);
        this.betslipUpdated();
        this.subscribeForUpdates();
      });
  }

  /**
   * Live updates handler function, updates TOTE events with live udpates received
   * for linked fixed odds events
   * @param liveUpdate {Object} - live update received from server
   * @private
   */
  private liveUpdateHandler(liveUpdate: ILiveUpdateResponseMessage): void {
    const eventId = liveUpdate && liveUpdate.event && liveUpdate.event.id,
      toteEvents = this.toteBet && this.toteBet.events;

    if (!eventId || !toteEvents) {
      return;
    }
    const changedEvent = _.find(toteEvents, (toteEvent: IRacingEvent) => toteEvent.linkedEventId === eventId);
    const { type, id } = liveUpdate.channel,
      payload = liveUpdate.message;
    const updateObject = { payload, type, id };

    this.commandService.executeAsync(this.commandService.API.UK_TOTE_UPDATE_EVENT_WITH_LIVEUPDATE,
      [changedEvent, updateObject])
      .then(() => this.betslipUpdated());
  }

  /**
   * Load fixed odds events
   * @private
   */
  private loadFixedOddsEvents(): Promise<ISportEvent[]> {
    const outcomeIds = _.compact(
      _.map(this.toteBet && this.toteBet.outcomes, (outcome: IOutcome) => +outcome.linkedOutcomeId)
    );
    return this.siteServerEventToOutcomeService.getEventToOutcomeForOutcome(outcomeIds);
  }
  /**
   * Set title of Tote bet
   * @private
   */
  private setBetTitle(): void {
    if (this.isPotBet) {
      this.betTitle = this.localeService.getString('bs.potBetTitle', [this.numberOfLines]);
    } else {
      this.betTitle = this.betName;
    }
  }

  /**
   * Set total stake title
   * @private
   */
  private setTotalStakeTitle(): void {
    let value;
    if (this.toteBet && this.toteBet.poolBet) {
      value = +this.toteBet.poolBet.stakePerLine;
    } else {
      value = 0;
    }
    const formattedValue = this.filterService.numberWithCurrency(value, '£');
    this.totalStakeTitle = this.localeService.getString('bs.totalStakeTitle', { value: formattedValue });
  }

  /**
   * Subscribe for live updates
   * @private
   */
  private subscribeForUpdates(): void {
    if (!this.toteBet || !this.toteBet.channelIds) {
      return;
    }
    this.pubSubService.publish(this.pubSubService.API.BETSLIP_LIVEUPDATE_SUBSCRIBE_FOR_TOTE_BETS,
      [this.toteBet.channelIds, (liveUpdate: ILiveUpdateResponseMessage): void => { this.liveUpdateHandler(liveUpdate); }]);
  }

  /**
   * update TOTE event status with fixed odds event status
   * @param linkedToteEvent {Object} - linked TOTE event
   * @param fixedOddsEvent {Object} - fixed odds event
   * @private
   */
  private updateLinkedEvent(linkedToteEvent: IRacingEvent, fixedOddsEvent: ISportEvent): void {
    if (!linkedToteEvent || !fixedOddsEvent) {
      return;
    }
    linkedToteEvent.eventStatusCode = fixedOddsEvent.eventStatusCode;
    this.updateLinkedMarket(linkedToteEvent, fixedOddsEvent);
  }

  /**
   * update linked TOTE outcomes statuses with fixed odds outcome statuses
   * @param linkedMarket {Object} - tote event market
   * @param fixedOddsMarket {Object} - fixed odds event market
   * @private
   */
  private updateLinkedOutcome(linkedMarket: IMarket, fixedOddsMarket: IMarket) {
    if (!fixedOddsMarket.outcomes || !linkedMarket.outcomes) {
      return;
    }
    _.forEach(fixedOddsMarket.outcomes, fixedOddsOutcome => {
      const linkedOutcome = _.find(linkedMarket.outcomes,
        (toteOutcome: IOutcome) => +toteOutcome.linkedOutcomeId === +fixedOddsOutcome.id);
      if (!linkedOutcome) {
        return;
      }
      linkedOutcome.outcomeStatusCode = fixedOddsOutcome.outcomeStatusCode;
    });
  }

  /**
   * update TOTE market status with fixed odds market status
   * @param linkedToteEvent {Object} - TOTE event
   * @param fixedOddsEvent {Object} - fixed odds event
   * @private
   */
  private updateLinkedMarket(linkedToteEvent: IRacingEvent, fixedOddsEvent: ISportEvent) {
    if (!fixedOddsEvent.markets || !linkedToteEvent.markets) {
      return;
    }
    const fixedOddsMarket = fixedOddsEvent.markets[0],
      linkedMarket = linkedToteEvent.markets[0];
    linkedMarket.marketStatusCode = fixedOddsMarket.marketStatusCode;
    this.updateLinkedOutcome(linkedMarket, fixedOddsMarket);
  }

  /**
   * Update statuses of TOTE events/markets/outcomes with statuses of linked
   * fixed odds events/markets/outcomes
   * @param fixedOddsEvents {Array} - fixed odds events
   * @private
   */
  private updateToteEventsStatuses(fixedOddsEvents: ISportEvent[]): void {
    const toteEvents = this.toteBet && this.toteBet.events;
    _.forEach(fixedOddsEvents, (fixedOddsEvent: ISportEvent) => {
      const linkedToteEvent = _.find(toteEvents, (toteEvent: IRacingEvent) => toteEvent.linkedEventId === fixedOddsEvent.id);
      this.updateLinkedEvent(linkedToteEvent, fixedOddsEvent);
    });
  }

  /**
   * Add login/logout listeners to update currency
   */
  private addListeners(): void {
    this.pubSubService.subscribe('ToteBetslipService',
      [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
        this.userCurrencyCode = this.userService.currency;
      });
  }

  setFreeBetsConfig(data): any {
    this.freeBetsConfigData = data;
  }

  getFreeBetsConfig(): any{
    return this.freeBetsConfigData;
  }

  /**
   * sets selected tote token value 
   * @returns {void}
   */
  setTokenValue(tokenValue): void {
    this.tokenValue = tokenValue;
  }
  
  /**
   * gets selected tote token value 
   * @returns {string}
   */
  getTokenValue(): string {
    return this.tokenValue;
  }

  /**
   * round off to 2 decimal points
   * @returns {number}
   * @public
   */
  public getRoundedValue(value: string| number): number {
    return Number((value).toString().match(/^-?\d+(?:\.\d{0,2})?/)[0]);
  }

  setToteFreeBetText(text): void {
    this.freeBetText = text;
  }

  getToteFreeBetText(): any {
    return this.freeBetText;
  }
}


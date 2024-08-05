import { Component, Input, OnDestroy, OnInit } from '@angular/core';

import { IPanelStateConfig } from '@app/betHistory/models/cashout-panel.model';
import { ICashOutData } from '@app/betHistory/models/cashout-section.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { TimeService } from '@core/services/time/time.service';
import { CashoutPanelService } from './cashout-panel.service';
import { CashoutBet } from '@app/betHistory/betModels/cashoutBet/cashout-bet.class';
import { ICountDownTimer } from '@core/services/time/time-service.model';
import { IBetHistoryLeg } from '@app/betHistory/models/bet-history.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ICashout, ICashoutMarketEvent, ILSUpdate } from '@app/betHistory/components/cashoutPanel/cashout-panel.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@app/core/models/market.model';
import { CASHOUT_SUSPENDED_WS, CASHOUT_FLAGS,
   CASHOUT_SUSPENDED } from '@app/betHistory/components/cashOutMessaging/cash-out-message.constants';
import environment from '@environment/oxygenEnvConfig';
import { cashoutConstants } from '@app/betHistory/constants/cashout.constant';

@Component({
  selector: 'cashout-panel',
  templateUrl: 'cashout-panel.component.html',
  styleUrls: ['cashout-panel.component.scss']
})
export class CashoutPanelComponent implements OnDestroy, OnInit {
  @Input() data: ICashOutData[];
  @Input() betLocation: string;
  @Input() bet: { eventSource: CashoutBet; location: string; };
  eventIsLive: boolean = false;
  countDownTimer: ICountDownTimer;
  subscriberName: string;
  enableCashOut: boolean;
  isMarketLevelDisabled: boolean;
  isEventLevelDisabled: boolean;
  componentId: string;
  isShow: boolean = false;
  cashoutSuspended: string = CASHOUT_SUSPENDED_WS;
  gaTrackDetails = new Set<string>();
  allEventsAndMarkets = new Map<string, ICashoutMarketEvent>();
  isCoral: boolean;

  private _isPartialCashOutAvailable: boolean;
  private isFirstInit: boolean = true;
  private subscriberNameEW: string;
  private BIRMarketsEnabled: string[];

  constructor(
    private cashoutPanelService: CashoutPanelService,
    private pubSubService: PubSubService,
    private timeService: TimeService,
    private cmsService: CmsService
  ) {
    this.cmsService.getSystemConfig().subscribe((config) => {
      if (config && config.cashOutMessaging) {
        this.enableCashOut = config.cashOutMessaging.enable;
      }
      this.BIRMarketsEnabled = config?.HorseRacingBIR?.marketsEnabled;
    });
  }

  @Input() set isPartialCashOutAvailable(value: boolean) {
    if (this.isFirstInit) {
      this.isFirstInit = false;
      this._isPartialCashOutAvailable = value;
      return;
    }
    if (this._isPartialCashOutAvailable !== value && value === false) {
      this.cashoutPanelService.setPartialState(this.bet.eventSource, false);
    }
  }

  /**
   * to initiate the logic on component initialisation
   * @returns {void}
   */
  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.componentId= this.bet.eventSource.betId;
    this.isShowCashoutMessaging();
    this.pubSubService.subscribe(this.componentId, this.pubSubService.API.EMA_HANDLE_BET_LIVE_UPDATE, (update: ILSUpdate) => {
      this.updateEventAndMarketFlags(update);
    });
    this.subscriberNameEW = `${this.bet.location}-${this.componentId}`;
    this.pubSubService.subscribe(this.subscriberNameEW, this.pubSubService.API.IS_LIVE, (updateEventId: string) => {
      if (this.bet.eventSource.event?.length > 0 && this.bet.eventSource.event.includes(updateEventId?.toString())) {
        this.isEWBetSuspend(this.bet.eventSource);
      }
    });

    this.isEWBetSuspend(this.bet.eventSource);
  }

  /**
   * user in HR EDP markets tab - and EW bet is live - then suspend cashout in mybets tab
   * @param { CashoutBet } bet 
   */
  private isEWBetSuspend(bet: CashoutBet): void {
    if (bet.legType === 'E' && bet.leg?.length > 0 && this.isHRCategory(bet.leg) && bet.leg[0].part && this.isEnabledBIRMarket(bet.leg) && this.isLive(bet)) {
      bet.panelMsg = {
        type: cashoutConstants.cashOutAttempt.SUSPENDED
      };
      bet.isPartialCashOutAvailable = false;
      bet.cashoutValue = CASHOUT_SUSPENDED;
      bet.isCashOutUnavailable = true;
      bet.isEWCashoutSuspend = true;
      this.pubSubService.publish(this.pubSubService.API.UPDATE_CASHOUT_BET, bet);
    }
  }

  /**
   * @param  {IBetHistoryLeg[]} legs
   * @returns boolean
   */
  private isHRCategory(legs: IBetHistoryLeg[]): boolean {
    return legs.every((leg: IBetHistoryLeg) => leg.eventEntity?.categoryId === environment.HORSE_RACING_CATEGORY_ID);
  }

    /**
  * returns true if any one leg in bet is live
  * @param {CashoutBet} bet 
  * @returns boolean
  */
  private isLive(bet: CashoutBet): boolean {
    return bet.leg.some(leg => (leg.is_off || leg.eventEntity?.rawIsOffCode === 'Y') && leg.status === 'open');
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

  ngOnDestroy(): void {
    this.subscriberName && this.pubSubService.unsubscribe(this.subscriberName);
    this.subscriberNameEW && this.pubSubService.unsubscribe(this.subscriberNameEW);
    this.countDownTimer && this.countDownTimer.stop && this.countDownTimer.stop();
    this.pubSubService.unsubscribe(this.componentId);
  }

  /**
   * @param  {ILSUpdate} update
   * @returns void
   */
  updateEventAndMarketFlags(update: ILSUpdate): void {
    if (update && update.updatePayload) {
      const updatedEntity = this.allEventsAndMarkets.get(update.id);
      if(!updatedEntity) {
        return;
      }
      updatedEntity.cashoutMessagingFlags.isDisplayed = update.updatePayload.displayed === CASHOUT_FLAGS.NO ? false : true;
      updatedEntity.cashoutMessagingFlags.isActive = update.updatePayload.status === CASHOUT_FLAGS.SUSP ? false : true;
      if (update.type === CASHOUT_FLAGS.EVENT) {
        updatedEntity.cashoutMessagingFlags.rawIsOffCode = update.updatePayload.is_off;
      }
      this.updateInit();
    }
  }

  /**
   * to update the event or market flags
   * @returns {void}
   */
  updateInit(): void {
    this.allEventsAndMarkets.forEach(evtOrMktEntity => {
      if (evtOrMktEntity.type === CASHOUT_FLAGS.MARKET) {
        const isEventLevelActiveForMarket: boolean = this.isEventActiveForMarket(evtOrMktEntity.event_id);
        if (isEventLevelActiveForMarket || evtOrMktEntity.cashoutMessagingFlags.isCashoutMessagingEnabled) {
          this.isMarketLevelCashoutMessagingEnabled(evtOrMktEntity.cashoutMessagingFlags, isEventLevelActiveForMarket);
        }
      } else {
        this.isEventActive(evtOrMktEntity.cashoutMessagingFlags);
      }
    });
    this.enableAllFlags();
  }

  /**
   * to check if a event flags are proper
   * @param eventId {string}
   * @returns {void}
   */
  isEventActiveForMarket(eventId: string): boolean {
    const flagCheck = this.allEventsAndMarkets.get(eventId).cashoutMessagingFlags;
    return (flagCheck.cashoutAvail === CASHOUT_FLAGS.YES && flagCheck.isActive.toString() === CASHOUT_FLAGS.TRUE &&
      flagCheck.isDisplayed.toString() === CASHOUT_FLAGS.TRUE && flagCheck.rawIsOffCode === CASHOUT_FLAGS.YES);
  }

  /**
   * to check if a market flags are proper
   * @param marketCashoutisEventLevelActive {ICashout}
   * @param isEventLevelActive {boolean}
   * @returns {void}
   */
  isMarketLevelCashoutMessagingEnabled(marketCashout: ICashout, isEventLevelActive: boolean): void {
    if (!marketCashout.isActive && !marketCashout.isDisplayed && isEventLevelActive) {
      marketCashout.isCashoutMessagingEnabled = true;
    } else {
      marketCashout.isCashoutMessagingEnabled = false;
    }
  }

  /**
   * to enable isCashoutMessagingEnabled flags for every market and event
   * @param eventCashout {ICashout}
   * @returns {void}
   */
  isEventActive(eventCashout: ICashout): void {
    if (!eventCashout.isActive && !eventCashout.isDisplayed && eventCashout.rawIsOffCode === CASHOUT_FLAGS.NO) {
      eventCashout.isCashoutMessagingEnabled = true;
    } else {
      eventCashout.isCashoutMessagingEnabled = false;
    }
  }

  /**
   * to enable event and market level cashout enabled flags
   * @returns {void}
   */
  enableAllFlags(): void {
    const marketFlags = [...this.allEventsAndMarkets.values()].filter(market => market.type === CASHOUT_FLAGS.MARKET
      && market.cashoutMessagingFlags.isCashoutMessagingEnabled === true);
    const eventFlags = [...this.allEventsAndMarkets.values()].filter(event => event.type === CASHOUT_FLAGS.EVENT
      && event.cashoutMessagingFlags.isCashoutMessagingEnabled === true);
    this.setGAstatus([...marketFlags, ...eventFlags]);
    this.isEventLevelDisabled = eventFlags.length ? true : false;
    this.isMarketLevelDisabled = marketFlags.length ? true : false;
    this.isShow = (this.isEventLevelDisabled || this.isMarketLevelDisabled) && this.isCashoutSuspended();
  }

  /**
   * to set ga tracking array details
   * @param allCashOutDisabledlEvents {ICashoutMarketEvent[]}
   * @returns {void}
   */
  setGAstatus(allCashOutDisabledlEvents: ICashoutMarketEvent[]): void {
    allCashOutDisabledlEvents.forEach((cashoutMessagingEnabledEvent: ICashoutMarketEvent) => {
      this.gaTrackDetails.add(cashoutMessagingEnabledEvent.event_name);
    });
  }

  /**
   * to check if cashout event state is changed
   * @returns {boolean}
   */
  isCashoutSuspended(): boolean {
    return this.bet.eventSource.cashoutStatus === CASHOUT_SUSPENDED || this.bet.eventSource.cashoutStatus === CASHOUT_SUSPENDED_WS;
  }

  get isButtonShown(): boolean {
    return this.cashoutPanelService.isButtonShown((this.bet.eventSource), this.betLocation);
  }
  set isButtonShown(value:boolean) {}

  get isPartialAvailable(): boolean {
    return this.cashoutPanelService.isPartialAvailable(this.bet.eventSource);
  }
  set isPartialAvailable(value:boolean) {}

  get buttonState(): string {
    return this.cashoutPanelService.getButtonState(this.bet.eventSource);
  }
  set buttonState(value:string) {}
  
  get stateConfig(): IPanelStateConfig {
    return this.cashoutPanelService.getStateConfig(this.bet.eventSource);
  }
  set stateConfig(value:IPanelStateConfig) {}
  /**
   * Cashout buttons handler
   *
   * @param {string} type? - type of the cashOut, is 'undefined' for "confirm" action
   */
  doCashOut(type?: string): void {
    !type && this.iniTimer();
    this.cashoutPanelService.doCashOut(this.data, this.bet.location, this.bet.eventSource, type);
    this.eventIsLive = this.bet.eventSource.leg.filter((item: IBetHistoryLeg) => item.eventEntity.eventIsLive).length > 0;
    this.pubSubService.publish(this.pubSubService.API.UPDATE_CASHOUT_BET, this.bet.eventSource);
  }

  partialPercentageChange(updatedPercentage: number): void {
    this.bet.eventSource.partialCashOutPercentage = updatedPercentage;
  }

  /**
   * to initialise the map for events
   * @returns {boolean}
   */
  isShowCashoutMessaging(): boolean {
    if (!this.bet.eventSource.leg || this.allEventsAndMarkets.size) {
      return false;
    }
    this.bet.eventSource.leg.forEach((betEventEntity: IBetHistoryLeg) => {
      if (!betEventEntity.eventEntity) {
        return false;
      }
      const betLegEntity = betEventEntity.eventEntity;
      this.allEventsAndMarkets.set(betLegEntity.id?.toString(),{
        name: betLegEntity.name, event_name: betLegEntity.name, event_id: betLegEntity.id?.toString(), type: CASHOUT_FLAGS.EVENT,
        cashoutMessagingFlags: {
          isDisplayed: betLegEntity.isDisplayed ? betLegEntity.isDisplayed : false,
          isActive:  betLegEntity.eventStatusCode === CASHOUT_FLAGS.SUSP ? false : true,
          rawIsOffCode:  betLegEntity.rawIsOffCode, cashoutAvail:  betLegEntity.cashoutAvail, isCashoutMessagingEnabled: false
        }
      });
      this.enableMarketLevelFlags(betLegEntity);
    });
    this.updateInit();
    return this.isShow;
  }

  /**
   * to initialise the map for markets
   * @param  {ISportEvent} betLegEntity
   */
  enableMarketLevelFlags(betLegEntity: ISportEvent) {
    if (betLegEntity.markets?.length > 0) {
      betLegEntity.markets.forEach((market: IMarket) => {
        this.allEventsAndMarkets.set(market.id,{
          name: market.name, event_name: betLegEntity.name, event_id: betLegEntity.id?.toString(), type: CASHOUT_FLAGS.MARKET,
          cashoutMessagingFlags: {
            isDisplayed: market.isDisplayed ? market.isDisplayed : false,
            isActive: market.marketStatusCode === CASHOUT_FLAGS.SUSP ? false : true,
            rawIsOffCode:  betLegEntity.rawIsOffCode,
            cashoutAvail:  market.cashoutAvail,
            isCashoutMessagingEnabled: false
          }
        });
      });
    }
  }

  /**
   * Add one-off subscription for countdown timer,
   * start timer only if pending state with given delay.
   */
  private iniTimer(): void {
    this.subscriberName = `CashoutPanelComponent-${this.bet.eventSource.betId}${this.bet.eventSource.receipt}`;
    this.pubSubService.subscribe(this.subscriberName, this.pubSubService.API.CASHOUT_COUNTDOWN_TIMER, (time?: number) => {
      if (time) {
        this.countDownTimer = this.timeService.countDownTimer(time);
      }

      this.pubSubService.unsubscribe(this.subscriberName);
      this.subscriberName = null;
    });
  }
}

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { IOutcome, IOutcomeDetails } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { CommandService } from '@core/services/communication/command/command.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UserService } from '@core/services/user/user.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { LocaleService } from '@core/services/locale/locale.service';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';
@Component({
  selector: 'price-odds-button',
  templateUrl: './price-odds-button.component.html',
})
export class PriceOddsButtonComponent implements OnInit, OnDestroy {
  @Input() event: ISportEvent;
  @Input() market: IMarket;
  @Input() outcome: IOutcome;
  @Input() goToBetslip?: boolean;
  @Input() cssClass: string;
  @Input() head: string;
  @Input() isShowHistoricPrices: boolean = true;
  @Input() hasWasLabel: boolean = false;
  @Input() gtmModuleTitle?: string;
  @Input() gtmPlacedLocation?: string;
  @Input() nonRunner: boolean;
  @Input() handicapVal?: string;
  @Input() isRacing?: boolean;
  @Input() sbPosition?: number;
  @Input() correctName?: string;
  @Input() overUnderTag?: string;
  @Input() eventQuickSwitch: boolean;

  oddsPrice: string;
  showHandicapValue: boolean = false;
  showSuspendValue: boolean = false;
  showCorrectScore: boolean = false;
  private env = environment;

  constructor(
    private userService: UserService,
    private gtmService: GtmService,
    private pubsubService: PubSubService,
    private commandService: CommandService,
    private betSlipSelectionsData: BetslipSelectionsDataService,
    private routingState: RoutingState,
    private gtmTrackingService: GtmTrackingService,
    private sportEventHelperService: SportEventHelperService,
    protected locale: LocaleService,
    protected scorecastDataService: ScorecastDataService
  ) {
  }

  ngOnInit(): void {
    if (this.handicapVal) {
      this.showHandicapValue = true;
      this.handicapVal = this.handicapVal.replace(/,/g, '');
    }
    if (this.correctName){
      this.showCorrectScore = true;
    }

    this.pubsubService.subscribe(`priceOddsButton_${this.outcome.id}`, `SELECTION_PRICE_UPDATE_${this.outcome.id}`, (price) => {
      if (this.outcome.prices && this.outcome.prices[0]) {
        this.outcome.prices[0].priceDen = price.priceDen;
        this.outcome.prices[0].priceNum = price.priceNum;
      }
    });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(`priceOddsButton_${this.outcome.id}`);
  }

  showOddsPriceValue(showVal: boolean) {
    this.showSuspendValue = showVal;
  }

  /**
   *
   * Common Handler for button click
   *
   * @param {object} $event
   */
  onPriceOddsButtonClick($event: Event): void {
    $event.stopPropagation();
    this.scorecastDataService.setScorecastData({});
    this.commandService.executeAsync(this.commandService.API.IS_ADDTOBETSLIP_IN_PROCESS).then((inProgress: boolean) => {
      if (!inProgress) {
        this.addToBetSlip($event);
      }
    });
    
  }

  /**
   * Adding to BetSlip.
   * Placing bet for 'SP' button, we send priceNum, priceDen as undefined.
   * @private
   * @param {object} event
   */
  private addToBetSlip(event: Event): void {
    const segment: string = this.routingState.getCurrentSegment();
    this.outcome.prices = this.outcome.prices || [];
    const tracking = this.gtmTrackingService.detectTracking(this.gtmModuleTitle, segment, this.event, this.market, this.gtmPlacedLocation);
    if(this.eventQuickSwitch && tracking.location) {
      tracking.location = 'events switcher-'+tracking.location.toLowerCase();
    }
    const priceType = this.outcome.prices && this.outcome.prices[0] ? this.outcome.prices[0].priceType : 'SP';
    const price = _.extend({}, this.outcome.prices[0], priceType && { priceType });
    const isRacing: boolean = this.event.categoryId === '19' || this.event.categoryId === '21';

    if (isRacing) {
      price.priceType = this.getCorrectPriceType();
    }

    const handicap = this.market.rawHandicapValue && {
      type: this.outcome.outcomeMeaningMajorCode,
      raw: this.outcome.prices[0].handicapValueDec.replace(/,/g, '')
    };

    const isBuildYourBet = this.isByB();

    const GTMObject = {
      categoryID: this.event && String(this.event.categoryId),
      typeID: this.event && String(this.event.typeId),
      eventID: this.event && String(this.event.id),
      selectionID: this.outcome && String(this.outcome.id)
    };

    if (tracking) {
      GTMObject['tracking'] = tracking;
      GTMObject['betData'] = {
        name: this.event.originalName || this.event.name,
        category: String(this.event.categoryId),
        variant: String(this.event.typeId),
        brand: this.market.marketName || this.market.name,
        dimension60: String(this.event.id),
        dimension61: this.outcome.id,
        dimension62: this.event.eventIsLive ? 1 : 0,
        dimension63: isBuildYourBet ? 1 : 0,
        dimension64: tracking.location,
        dimension65: tracking.module,
        dimension177: this.market.isSCAvailable ? 'show': 'No show',
        dimension180: tracking.module === 'next races' && this.event.categoryId == '39' ? 'virtual' : 'normal'

      };
      if(this.sbPosition) { // on surfacebet odds click provides the item position 
        Object.assign(GTMObject['betData'], {dimension94: this.sbPosition});
      }
    }

    const details: Partial<IOutcomeDetails> = BetslipBetDataUtils.outcomeDetails(this.event, this.market, this.outcome);

    const addToBetSlipObject = {
      eventIsLive: this.event.eventIsLive,  // solution for indicate in-play event
      outcomes: [this.outcome],
      typeName: this.event.typeName,
      price,
      handicap,
      goToBetslip: !!this.goToBetslip && this.betSlipSelectionsData.count() === 0,
      modifiedPrice: this.outcome.modifiedPrice,
      eventId: this.event.id,
      isOutright: this.sportEventHelperService.isOutrightEvent(this.event),
      isSpecial: this.sportEventHelperService.isSpecialEvent(this.event, true),
      GTMObject,
      details,
      eventName : this.event.originalName || this.event.name 
    };

    // send data customer places a bet and betslip opens
    if (addToBetSlipObject.goToBetslip && !this.userService.quickBetNotification) {
      this.gtmService.push('trackPageview', { virtualUrl: '/betslip-receipt' });
    }

    this.pubsubService.publishSync(this.pubsubService.API.ADD_TO_BETSLIP_BY_SELECTION, [addToBetSlipObject]);
  }

  private getCorrectPriceType(): string {
    return (this.market.isLpAvailable && this.outcome.prices.length && !this.outcome.isFavourite) ?
      'LP' : 'SP';
  }

  private isByB(): boolean {
    return this.event && this.env && this.env.BYB_CONFIG
      && String(this.env.BYB_CONFIG.HR_YC_EVENT_TYPE_ID) === String(this.event.typeId);
  }
}

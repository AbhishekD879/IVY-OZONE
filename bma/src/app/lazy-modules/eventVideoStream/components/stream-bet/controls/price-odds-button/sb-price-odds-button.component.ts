import { Component, Input, Output, EventEmitter, ElementRef } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { LocaleService } from '@core/services/locale/locale.service';

import {  OnDestroy, OnInit } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import * as _ from 'underscore';
import { CommandService } from '@core/services/communication/command/command.service';
import { IOutcome, IOutcomeDetails } from '@core/models/outcome.model';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'sb-price-odds-button',
  templateUrl: './sb-price-odds-button.component.html',
  styleUrls: ['./sb-price-odds-button.component.scss']
})
export class SbPriceOddsButtonComponent implements OnInit, OnDestroy {
 
  @Input() event: ISportEvent;
  @Input() market: IMarket;
  @Input() outcome: IOutcome;
  @Input() goToBetslip?: boolean;
  @Input() cssClass: string;
  @Input() head: string;
  @Input() isShowHistoricPrices: boolean = true;
  @Input() hasWasLabel: boolean = false;
  @Input() gtmModuleTitle?: string;
  @Input() nonRunner: boolean;
  @Input() handicapVal?: string;
  @Input() isRacing?: boolean;
  @Input() sbPosition?: number;
  @Input() correctName?: string;
  @Input() isStreamAndBet?: boolean = false;

  @Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();

  oddsPrice: string;
  showHandicapValue: boolean;
  showSuspendValue: boolean;
  showCorrectScore: boolean;
  isActive: boolean = false;
  isBrandLadbrokes: boolean;

  constructor(
    private pubsubService: PubSubService,
    protected locale: LocaleService,
    private commandService: CommandService,
    private sportEventHelperService: SportEventHelperService,
    private elementRef: ElementRef,
    private gtmTrackingService: GtmTrackingService,
    private routingState: RoutingState,
  ) {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
  }

  ngOnInit(): void {
    if (this.handicapVal) {
      this.showHandicapValue = true;
      this.handicapVal = this.handicapVal.replace(/,/g, '');
    }
    if (this.correctName){
      this.showCorrectScore = true;
    }

    this.pubsubService.subscribe(`sbPriceOddsButton_${this.outcome.id}`, `SELECTION_PRICE_UPDATE_${this.outcome.id}`, (price) => {
      if (this.outcome.prices && this.outcome.prices[0]) {
        this.outcome.prices[0].priceDen = price.priceDen;
        this.outcome.prices[0].priceNum = price.priceNum;
      }
    });
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
    // ToDO: SnB - try to move below line to scss file  
    this.elementRef.nativeElement.parentNode.style.backgroundColor = "#78b200";
     
    this.isActive = true;
    $event.stopPropagation();

    if (this.isStreamAndBet) {
      this.selectionClickEmit.emit(this.market);
    }

    this.commandService.executeAsync(this.commandService.API.IS_ADDTOBETSLIP_IN_PROCESS).then((inProgress: boolean) => {
      if (!inProgress) {
        this.formSelectionData();
      }
    });
  }

  formSelectionData() {
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

    const GTMObject = {
      categoryID: this.event && String(this.event.categoryId),
      typeID: this.event && String(this.event.typeId),
      eventID: this.event && String(this.event.id),
      selectionID: this.outcome && String(this.outcome.id)
    };

    const details: Partial<IOutcomeDetails> = BetslipBetDataUtils.outcomeDetails(this.event, this.market, this.outcome);

    const segment: string = this.routingState.getCurrentSegment();
    const tracking = this.gtmTrackingService.detectTracking(this.gtmModuleTitle, segment, this.event, this.market);
    
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
        dimension63: 0,
        dimension64: tracking.location,
        dimension65: tracking.module,
        dimension177: this.market.isSCAvailable ? 'show': 'No show',
        dimension180: tracking.module === 'next races' && this.event.categoryId == '39' ? 'virtual' : 'normal'

      };
      if(this.sbPosition) { // on surfacebet odds click provides the item position 
        Object.assign(GTMObject['betData'], {dimension94: this.sbPosition});
      }
    }
    const selectionData = {
      eventIsLive: this.event.eventIsLive,  // solution for indicate in-play event
      outcomes: [this.outcome],
      typeName: this.event.typeName,
      price,
      handicap,
      goToBetslip: false,
      modifiedPrice: this.outcome.modifiedPrice,
      eventId: this.event.id,
      isOutright: this.sportEventHelperService.isOutrightEvent(this.event),
      isSpecial: this.sportEventHelperService.isSpecialEvent(this.event, true),
      GTMObject,
      details,
      eventName : this.event.originalName || this.event.name,
      isStreamBet: true
    };

    this.pubsubService.publishSync(this.pubsubService.API.ADD_TO_QUICKBET_BMA_STREAM_BET, [selectionData]);
  }

  private getCorrectPriceType(): string {
    return (this.market.isLpAvailable && this.outcome.prices.length && !this.outcome.isFavourite) ?
      'LP' : 'SP';
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(`sbPriceOddsButton_${this.outcome.id}`);
  }
}

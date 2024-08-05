import { Component, OnInit, Input, ChangeDetectionStrategy,
  ChangeDetectorRef, OnChanges, SimpleChanges, OnDestroy } from '@angular/core';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@app/core/models/market.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { marketDescriptionConstants } from '@app/lazy-modules/racingConstants/racing.constants';

@Component({
  selector: 'market-description',
  templateUrl: './market-description.component.html',
  styleUrls: ['./market-description.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MarketDescriptionComponent implements OnInit, OnChanges, OnDestroy {
  @Input() selectedMarket: string;
  @Input() eventEntity: ISportEvent;
  marketData: IMarket;
  isValidRaceEvent: boolean;
  isEventLive: boolean = false;
  isHrEvent: boolean = false;
  isEventBIR: boolean = false;
  constructor(protected changeDetectorRef: ChangeDetectorRef,
    protected pubSubService: PubSubService) { }

  ngOnInit() {
    this.setMarketDescription();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.selectedMarket) {
      this.setMarketDescription();
    }
  }
  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(marketDescriptionConstants.marketDescription + this.eventEntity.id);
  }
  /**
   * Sets market description based on market selected
   */
  private setMarketDescription(): void {
    this.marketData = null;
    this.isValidRaceEvent = false;
    const hasSortedMarkets = this.eventEntity && this.eventEntity.sortedMarkets
      && this.eventEntity.sortedMarkets.length;
    if (hasSortedMarkets) {
      this.marketData = this.eventEntity.sortedMarkets.find((market: IMarket) => {
        return market.label === this.selectedMarket;
      });
      this.isValidRaceEvent = this.isHorseRacingOrGreyHound();
      if (this.marketData.birDescription) {
        this.setBirDescription();
      }
    }
    this.changeDetectorRef.markForCheck();
  }


  /**
   * To Verify type of racing event
   */
  private isHorseRacingOrGreyHound(): boolean {
    const response = this.eventEntity && this.marketData && (this.eventEntity.categoryId === environment.HORSE_RACING_CATEGORY_ID &&
      this.marketData.isHR) || (this.eventEntity.categoryId !== environment.HORSE_RACING_CATEGORY_ID &&
        this.marketData.isGH);
    this.pubSubService.publish(this.pubSubService.API.HAS_MARKET_DESCRIPTION, response);
    return response;
  }
  /**
   * sets all the flags required to the birDescription
   */
  private setBirDescription(): void {
    this.isEventBIR = this.eventEntity.drilldownTagNames && this.eventEntity.drilldownTagNames.includes(marketDescriptionConstants.EVFLAG_IHR);
    this.isHrEvent = this.eventEntity.categoryId === environment.HORSE_RACING_CATEGORY_ID;
    this.isEventLive = (this.eventEntity.isStarted || this.eventEntity.eventIsLive || this.eventEntity.rawIsOffCode === 'Y') 
                        && !this.eventEntity.isResulted;
    this.pubSubService.subscribe(marketDescriptionConstants.marketDescription+this.eventEntity.id, this.pubSubService.API.EXTRA_PLACE_RACE_OFF, (updateEventId: number) => {
      if (updateEventId === this.eventEntity.id) {
        this.eventEntity.rawIsOffCode = 'Y';
        this.isEventLive = true;
        this.changeDetectorRef.detectChanges();
      }
    });
  }
  /**
   *  To verify and show Description
   * @returns true if all the flags are satisfied to show description
   */
  showDescription(): boolean {
    return this.marketData?.description && this.isValidRaceEvent && (!this.isEventBIR || !this.isEventLive || this.isEventLive && !this.marketData.birDescription);
  }
  /**
   * To verify and show birDescription
   * @returns true if all the flags are satisfied to show birDescription
   */
   showBIRDescription(): boolean {
    return this.marketData?.birDescription && this.isValidRaceEvent && this.isHrEvent && (this.isEventLive || this.eventEntity.rawIsOffCode === 'Y') && this.isEventBIR;
  }
}

import { Component, Input, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';

import { ISportEvent, IEventData } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { TemplateService } from '@shared/services/template/template.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { SportService } from '@core/services/sport/sport.service';
import { ISportServiceConfig } from '@core/models/sport-service-config.model';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';

@Component({
  selector: 'event-markets',
  templateUrl: './event-markets.html',
  styleUrls: ['./event-markets.scss']
})
export class EventMarketsComponent implements OnInit, OnDestroy {
  @Input() eventId: string;
  @Input() eventEntity: ISportEvent;
  @Input() sportConfig: ISportServiceConfig;
  @Input() panelType: string;
  @Input() isFeaturedMarkets?: boolean;
  // for featured module. amount of selections above "see more/show.scss" button.
  @Input() selectionsLimit?: number = -1;
  @Input() isLuckyDipMarketAvailable?: boolean;
  @Input() fetchOutcomes?: boolean;

  // Open first 2 market tabs(0,1)
  openMarketTabs: number = 1;
  showTerms: boolean = false;
  isEachWayAvailable: boolean;

  isShowAllActive: boolean = false;
  allShown: boolean = false;
  limit: number;
  private readonly tagName: string = 'EventMarketsComponent';

  constructor(
    private templateService: TemplateService,
    private pubSubService: PubSubService,
    protected routingHelperService: RoutingHelperService,
    protected seoDataService: SeoDataService,
    private sportService: SportService,
    protected changeDetectorRef: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    if(this.fetchOutcomes){
      this.sportService.setConfig(this.sportConfig)
        .getById(this.eventId, false, true)
        .subscribe((data: IEventData) => {
          const event = (data.event && data.event[0]) || data[0];
          if(this.isLuckyDipMarketAvailable) {
            event.markets.forEach(market => {
              market.isLuckyDip = market && market.drilldownTagNames && market.drilldownTagNames.indexOf(LUCKY_DIP_CONSTANTS.MKTFLAG_LD) != -1;
           });
          }
          this.eventEntity = event;
          this.init();
      });
    }
    else if(this.eventEntity) {
      this.init();
    }
  }

  private init(): void{
    if (this.isLuckyDipMarketAvailable) {
      if(this.fetchOutcomes) {
        this.eventEntity.markets.forEach(market => {
          market.isLuckyDip = market && market.drilldownTagNames && market.drilldownTagNames.indexOf(LUCKY_DIP_CONSTANTS.MKTFLAG_LD) != -1;
       });
      }
      this.changeDetectorRef.detectChanges();
    }
    const outcomesLength = this.eventEntity.markets[0]?.outcomes?.length ?? 0;
    this.sortMarkets();
    this.goToSeo(this.eventEntity);
    this.pubSubService.publish(this.pubSubService.API.QUICKBET_EXTRAPLACE_SELECTION, this.eventEntity);
    // show all button and limit only for featured module
    this.limit = this.isFeaturedMarkets ? this.selectionsLimit : undefined;
    this.isShowAllActive = this.isFeaturedMarkets && outcomesLength > 0 && outcomesLength > this.selectionsLimit;

    if (this.panelType === 'outright') {
      this.getTerms(this.eventEntity);
      this.showTerms = true;
    }
    
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.OUTCOME_UPDATED, () => {
      this.sortMarkets();
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.WS_EVENT_UPDATE, () => {
      this.changeDetectorRef.detectChanges();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.tagName);
  }

  toggleShow(): void {
    this.allShown = !this.allShown;

    if (this.allShown) {
      this.limit = undefined;
    } else {
      this.limit = this.selectionsLimit;
    }
  }

  goToSeo(eventEntity: ISportEvent): void {
    const edpUrl: string = this.routingHelperService.formEdpUrl(eventEntity);
    this.seoDataService.eventPageSeo(eventEntity, edpUrl);
  }

  trackByIndex(index): number {
    return index;
  }

  /**
   * Sort markets by displayOrder,
   *      outcomes by displayOrder or price and name
   */
  private sortMarkets(): void {
    this.eventEntity.markets = [...this.eventEntity.markets].sort((a: IMarket, b: IMarket) => (a.displayOrder - b.displayOrder));
    this.eventEntity.markets.forEach((market: IMarket) => {
      market.outcomes = [...market.outcomes].sort((a: IOutcome, b: IOutcome) => {
        if (a.displayOrder > b.displayOrder) { return 1; }

        if (a.displayOrder === b.displayOrder) {
          const
            aPrice = a.prices && a.prices[0] && a.prices[0].priceDec,
            bPrice = b.prices && b.prices[0] && b.prices[0].priceDec;

          if (!aPrice) {
            return -1;
          }
          if (aPrice > bPrice || (aPrice === bPrice && a.name > b.name)) {
            return 1;
          }
        }

        return -1;
      });
    });
  }

  /**
   * Generates "Each Way" text string with info about odds and win places.
   * @param {Object} event
   */
  private getTerms(event: ISportEvent): void {
    _.each(event.markets, market => {
      market.terms = this.templateService.genTerms(market);
    });
  }
}

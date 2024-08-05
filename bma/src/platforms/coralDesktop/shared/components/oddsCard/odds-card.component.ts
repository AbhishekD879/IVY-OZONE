import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';

import { IMarket } from '@core/models/market.model';
import { IOutputModule } from '@featured/models/output-module.model';

import { OddsCardComponent as AppOddsCardComponent } from '@shared/components/oddsCard/odds-card.component';

@Component({
  selector: 'odds-card-component',
  templateUrl: 'odds-card.component.html',
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class OddsCardComponent extends AppOddsCardComponent implements OnInit {
  @Input() featuredModule: IOutputModule;
  @Input() isActiveLiveStream: boolean;
  @Input() isLiveStreamTab: boolean;
  @Input() gtmDataLayer:  { eventAction: string, eventLabel: string };

  isFeaturedOffer: boolean;
  extensionName: string;

  ngOnInit() {
    super.ngOnInit();
    this.isFeaturedOffer = this.featuredModule && (this.featuredModule.isEnhanced || this.featuredModule.isSpecial);
    this.isEnhancedMultiplesCard = (this.template.name === 'Enhanced Multiples') &&
      !this.event.hideEvent && this.isEnhancedMultiples && !this.isFeaturedOffer;
    this.isSpecialCard = this.eventType === 'specials' && !this.isEnhancedMultiples && !this.isFeaturedOffer;
  }

  /**
   * Checks if odds card is sport one
   * @param {IMarket} market
   * @returns {boolean}
   */
  isSportCard(market: IMarket): boolean {
    return (this.isSelectedMarket(market) &&
      !this.isEnhancedMultiplesCard &&
      !(this.template.name === 'Outrights') && !this.isSpecialCard) &&
      !this.isFeaturedOffer;
  }
}

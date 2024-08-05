import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';

import { IMarket } from '@core/models/market.model';
import { IOutputModule } from '@featured/models/output-module.model';

import { OddsCardComponent } from '@shared/components/oddsCard/odds-card.component';

@Component({
  selector: 'odds-card-component',
  templateUrl: 'odds-card.component.html',
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class DesktopOddsCardComponent extends OddsCardComponent implements OnInit {
  @Input() featuredModule: IOutputModule;
  @Input() isActiveLiveStream: boolean;
  @Input() isLiveStreamTab: boolean;
  @Input() gtmDataLayer:  { eventAction: string, eventLabel: string };
  @Input() gtmModuleTitle?: string;

  isFeaturedOffer: boolean;

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
    return ((this.selectedMarket === market.name || this.selectedMarket === market.templateMarketName || !this.selectedMarket) &&
      !this.isEnhancedMultiplesCard &&
      !(this.template.name === 'Outrights') && !this.isSpecialCard) &&
      !this.isFeaturedOffer;
  }
}

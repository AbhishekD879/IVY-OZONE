import { Component, Input } from '@angular/core';

import {
  OddsCardSportComponent as LMOddsCardSportComponent
} from '@ladbrokesMobile/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';

@Component({
  selector: 'odds-card-sport',
  styleUrls: ['odds-card-sport.component.scss'],
  templateUrl: 'odds-card-sport.component.html'
})
export class OddsCardSportComponent extends LMOddsCardSportComponent {
  @Input() gtmDataLayer:  { eventAction: string, eventLabel: string };
  @Input() gtmModuleTitle?: string;

  /**
   * Check if time should be shown
   * @returns {boolean}
   */
  isTimeShown(): boolean {
    return !this.isLive;
  }

  /**
   * Builds markets amount string
   * @param isInline
   * @returns {string}
   */
  buildMarketsCountString(isInline?: boolean | string): string {
    let marketsCountString = `+${this.event.marketsCount - 1}`;
    if (isInline) {
      marketsCountString = `${marketsCountString} ${this.locale.getString('sbdesktop.markets')}`;
    }
    return marketsCountString;
  }

  sendToGTM(): void {
    if (this.gtmDataLayer) {
      this.gtmService.push('trackEvent', {
        eventCategory: 'home',
        eventAction: this.gtmDataLayer.eventAction,
        eventLabel: this.gtmDataLayer.eventLabel
      });
    }
  }
}

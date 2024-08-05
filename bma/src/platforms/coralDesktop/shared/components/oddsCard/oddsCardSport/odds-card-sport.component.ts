import { Component, Input } from '@angular/core';

import { OddsCardSportComponent as AppOddsCardSportComponent } from '@shared/components/oddsCard/oddsCardSport/odds-card-sport.component';

@Component({
  selector: 'odds-card-sport',
  templateUrl: 'odds-card-sport.component.html'
})

export class OddsCardSportComponent extends AppOddsCardSportComponent {
  @Input() gtmDataLayer: { eventAction: string, eventLabel: string };
  @Input() gtmModuleTitle?: string;
  //added isActiveLiveStream and isLiveStreamTab properties for strict mode issue fix
  @Input() isActiveLiveStream: boolean;
  @Input() isLiveStreamTab: boolean;
  @Input() eventQuickSwitch: boolean;

  /**
   * Check if time should be shown
   * @returns {boolean}
   */
  isTimeShown(): boolean {
    return !this.isLive;
  }

  /**
   * Returns label for odds
   * @returns {String}
   */
  getOddsLabel(): string {
    this.liveLabelText = this.locale.getString('sb.live');
    // for live featured selection - show live label
    if (this.isLiveFeaturedSelection()) {
      return this.liveLabelText;
    }

    // show tennis set
    if (this.event.comments && this.event.comments.runningSetIndex) {
      const runningSetIndex = this.event.comments.runningSetIndex;
      const numberSuffix = this.locale.getString(this.filtersService.numberSuffix(runningSetIndex));
      return `${runningSetIndex}${numberSuffix} ${this.locale.getString('sb.tennisSet')}`;
    }

    // if clock is available - no label
    if (this.isMatchClock) {
      return '';
    }

    // show live label
    if (this.isLive && !this.isHalfOrFullTime) {
      return this.liveLabelText;
    }

    // show half or full time
    if (this.isHalfOrFullTime) {
      return this.event.clock.matchTime;
    }

    // show event time
    if (!this.isEventStartedOrLive) {
      return this.eventTime;
    }

    return '';
  }

  /**
   * Builds markets amount string
   * @param isInline
   * @returns {string}
   */
  buildMarketsCountString(isInline?: boolean): string {
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

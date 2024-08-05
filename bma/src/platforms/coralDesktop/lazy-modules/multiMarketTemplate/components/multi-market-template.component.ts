import { Component, Input } from '@angular/core';
import {
  MultiMarketTemplateComponent
} from '@app/lazy-modules/multiMarketTemplate/components/multi-market-template.component';
@Component({
  selector: 'multi-market-template',
  templateUrl: 'multi-market-template.component.html',
  styleUrls: ['multi-market-template.component.scss']
})
export class CoralMultiMarketTemplateComponent extends MultiMarketTemplateComponent {
  @Input() gtmDataLayer: { eventAction: string, eventLabel: string };
  @Input() gtmModuleTitle?: string;
  //added isActiveLiveStream and isLiveStreamTab properties for strict mode issue fix
  @Input() isActiveLiveStream: boolean;
  @Input() isLiveStreamTab: boolean;
  twoEvents = ['1', '2'];
  threeEvents = ['1', '2', '3'];
  
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
    return '';
  }
  /**
   * Builds markets amount string
   * @param isInline
   * @returns {string}
   */
  buildMarketsCountString(isInline?: boolean): string {
    let marketsCountString = `+${this.getMarketsCount(this.event) - 1}`;
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
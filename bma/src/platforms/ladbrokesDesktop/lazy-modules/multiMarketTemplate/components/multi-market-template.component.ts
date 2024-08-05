import { Component, Input, SimpleChanges } from '@angular/core';
import {
  LadsMobileMultiMarketTemplateComponent
} from '@ladbrokesMobile/lazy-modules/multiMarketTemplate/components/multi-market-template.component';
@Component({
  selector: 'multi-market-template',
  templateUrl: 'multi-market-template.component.html',
  styleUrls: ['multi-market-template.component.scss']
})
export class LadsDesktopMultiMarketTemplateComponent extends LadsMobileMultiMarketTemplateComponent {
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
  ngOnChanges(changes: SimpleChanges): void {
    super.ngOnChanges(changes);
    if (!this.isEventStartedOrLive && this.oddsLabel) {
      this.oddsLabel = this.oddsLabel.replace(',', '');
    }
  }
}
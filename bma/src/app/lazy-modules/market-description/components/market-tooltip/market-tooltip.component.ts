import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { LocaleService } from '@app/core/services/locale/locale.service';

@Component({
  selector: 'market-tooltip',
  templateUrl: './market-tooltip.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MarketTooltipComponent {
  @Input() toolTipArgs: { [key: string]: string; };
  @Input() marketContainer: HTMLElement;
  @Input() toolTipTitle: string;
  @Input() sportName: string;
  private readonly VIEW_ACTION: string = 'view';

  constructor(private gtmService: GtmService,
    private localeService: LocaleService) {
  }

  /**
   * To trigger tooltip event
   * @param {boolean} isTooltipSeen
   */
  setTooltipEvent(isTooltipSeen: boolean): void {
    if (isTooltipSeen) {
      this.gtmService.push('trackEvent', {
        eventCategory: this.sportName,
        eventAction: this.VIEW_ACTION,
        eventLabel: this.localeService.getString(`racing.showTooltip`)
      });
    }
  }

}

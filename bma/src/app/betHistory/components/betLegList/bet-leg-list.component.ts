import { Component, Input } from '@angular/core';

import { IBetHistoryBet, IBetHistoryLeg } from '../../models/bet-history.model';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';
import environment from '@environment/oxygenEnvConfig';
import { IBetHistoryPart } from '@app/betHistory/models/bet-history.model';
import { IPrice } from '@app/bpp/services/bppProviders/bpp-providers.model';
@Component({
  selector: 'bet-leg-list',
  templateUrl: './bet-leg-list.component.html',
  styleUrls: ['./bet-leg-list.component.scss']
})
export class BetLegListComponent extends UsedFromWidgetAbstractComponent {

  @Input() bet: { eventSource: IBetHistoryBet, location: string};
  @Input() betLocation: string;
  @Input() removeBogAndLabel: boolean;
  @Input() section: string;
  @Input() isLastBet: boolean;
  @Input() origin: string;
  @Input() tabName: string;
  @Input() isSportIconEnabled: boolean;
  isCoral: boolean;
  @Input() estimatedReturns: string;
  @Input() editAccaHistory: boolean;
  @Input() showDHmessage: boolean;

  constructor() {
    super();
    this.isCoral = environment && environment.brand === 'bma';
  }
  
  /**
 * Show BOG icon if Best Odds guarantied for horse racing events.
 * Best odds are guarantied when priceType.code is GP (for Ladbrokes brand) or G (for Coral)
 * @return {IBetHistoryLeg}
 */
  updateLeg(leg: IBetHistoryLeg): IBetHistoryLeg {
    leg.part.forEach((part: IBetHistoryPart) => {
      part.isBog = part.price ? part.price.some((price: IPrice) => {
        const priceTypeCode = price && price.priceType && price.priceType.code;
        return (priceTypeCode === 'G' || priceTypeCode === 'GP');
      }) : false;
    });
    return leg;
  }

  trackByLeg(index: number, leg: IBetHistoryLeg): string {
    return `${index}${leg.status}`;
  }
}

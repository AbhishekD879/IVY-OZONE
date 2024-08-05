import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { STATUSES } from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';

@Component({
  selector: 'bet-status-indicator',
  templateUrl: 'bet-status-indicator.component.html',
  styleUrls: ['./bet-status-indicator.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class BetStatusIndicatorComponent {
  @Input() status: string;

  constructor() {}

  get iconStatusName(): string {
    switch (this.status) {
      case STATUSES.WON:
        return '#bet-status-won';
      case STATUSES.LOSE:
        return '#bet-status-lose';
      case STATUSES.WINNING:
        return '#bet-status-arrow-up';
      case STATUSES.LOSING:
        return '#bet-status-arrow-down';
      default:
        return '';
    }
  }

  set iconStatusName(value: string){}
}

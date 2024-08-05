import { Component, Input } from '@angular/core';

import { ICashOutData } from '../../models/cashout-section.model';
import { RegularBet } from '../../betModels/regularBet/regular-bet.class';

@Component({
  selector: 'edit-my-acca-history-list',
  templateUrl: './edit-my-acca-history-list.component.html',
  styleUrls: ['./edit-my-acca-history-list.component.scss']
})
export class EditMyAccaHistoryListComponent {
  @Input() bets: ICashOutData[];

  expandBet(bet: ICashOutData): void {
    const accaHistory = (bet.eventSource as RegularBet).accaHistory;
    accaHistory.isExpanded = !accaHistory.isExpanded;
  }

  trackBet(index: number, bet: ICashOutData): string {
    return bet.eventSource.id;
  }
}

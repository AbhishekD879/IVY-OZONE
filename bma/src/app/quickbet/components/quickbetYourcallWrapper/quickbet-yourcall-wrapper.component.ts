import {
  Component,
  Input,
  Output,
  EventEmitter
} from '@angular/core';

import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { DSBet } from '@yourcall/models/bet/ds-bet';
import { BYBBet } from '@yourcall/models/bet/byb-bet';

@Component({
  selector: 'quickbet-yourcall-wrapper',
  templateUrl: 'quickbet-yourcall-wrapper.component.html'
})
export class QuickbetYourcallWrapperComponent {
  @Input() title: string;
  @Input() selection: DSBet | BYBBet;
  @Input() leftBtnLocale?: string;
  @Input() ycOddsValue?: Function;
  @Input() isFiveASideBet?: boolean;
  @Input() bodyClass: string;
  @Input() betslipType: string;

  @Output() readonly placeBetFn: EventEmitter<void> = new EventEmitter();
  @Output() readonly closePanelFn: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly reuseSelectionFn: EventEmitter<void> = new EventEmitter();

  placeBet(): void {
    this.placeBetFn.emit();
  }

  closePanel(isBetReceipt: boolean): void {
    this.closePanelFn.emit(isBetReceipt);
  }

  reuseSelection(): void {
    this.reuseSelectionFn.emit();
  }

  trackById(index: number, selection: IBetSelection): string {
    return `${selection.id} ${index}`;
  }
}

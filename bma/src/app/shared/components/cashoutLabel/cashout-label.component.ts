import {
  ChangeDetectionStrategy,
  Component, Input
} from '@angular/core';

@Component({
  selector: 'cashout-label',
  templateUrl: 'cashout-label.component.html',
  styleUrls: ['cashout-label.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CashoutLabelComponent {
  @Input() mode: string;

  get isBigMode() {
    return !this.mode || this.mode === 'big';
  }
  set isBigMode(value:any){}
}

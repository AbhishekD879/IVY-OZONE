import { Component, Input } from '@angular/core';
@Component({
  selector: 'cashout-error-message',
  templateUrl: './cashout-error-message.component.html',
  styleUrls: ['./cashout-error-message.component.scss']
})
export class CashoutErrorMessageComponent {
  @Input() message: string;
}

import { Component } from '@angular/core';
import { CashoutErrorMessageComponent as AppCashoutErrorMessageComponent} from '@app/betHistory/components/cashoutErrorMessage/cashout-error-message.component';

@Component({
  selector: 'cashout-error-message',
  templateUrl: '../../../../../app/betHistory/components/cashoutErrorMessage/cashout-error-message.component.html',
  styleUrls: ['../../../../../app/betHistory/components/cashoutErrorMessage/cashout-error-message.component.scss', 
  'cashout-error-message.component.scss']
})
export class CashoutErrorMessageComponent extends  AppCashoutErrorMessageComponent{}
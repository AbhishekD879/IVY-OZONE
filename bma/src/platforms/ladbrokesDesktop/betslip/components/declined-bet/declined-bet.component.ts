import { ChangeDetectionStrategy, Component } from '@angular/core';
import { DeclinedBetComponent as AppDeclinedBetComponent } from '@betslip/components/declinedBet/declined-bet.component';

@Component({
  selector: 'declined-bet',
  templateUrl: '../../../../../app/betslip/components/declinedBet/declined-bet.component.html',
  styleUrls: ['./declined-bet.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DeclinedBetComponent extends AppDeclinedBetComponent {}

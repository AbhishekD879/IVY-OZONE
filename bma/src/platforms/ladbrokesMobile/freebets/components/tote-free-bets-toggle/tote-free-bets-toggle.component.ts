import { Component } from '@angular/core';
import { ToteFreeBetsToggleComponent as AppToteFreeBetsToggleComponent} from '@freebets/components/tote-free-bets-toggle/tote-free-bets-toggle.component';
import { ToteFreeBetSelectDialogComponent } from '../tote-free-bet-select-dialog/tote-free-bet-select-dialog.component';


@Component({
  selector: 'tote-free-bets-toggle',
  templateUrl: '../../../../../app/freebets/components/tote-free-bets-toggle/tote-free-bets-toggle.component.html',
  styleUrls: ['./tote-free-bets-toggle.component.scss']
})
export class ToteFreeBetsToggleComponent extends AppToteFreeBetsToggleComponent {
  
 get dialogComponent() {
    return ToteFreeBetSelectDialogComponent;
  }
  set dialogComponent(value:any){}
}

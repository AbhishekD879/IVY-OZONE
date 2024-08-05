import { Component } from '@angular/core';

import { FreeBetToggleComponent as AppFreeBetToggleComponent} from '@freebets/components/freeBetToggle/free-bet-toggle.component';
import { FreeBetSelectDialogComponent } from '../freeBetSelectDialog/free-bet-select-dialog.component';

@Component({
  selector: 'free-bet-toggle',
  templateUrl: '../../../../../app/freebets/components/freeBetToggle/free-bet-toggle.component.html',
  styleUrls: ['./free-bet-toggle.component.scss']
})
export class FreeBetToggleComponent extends AppFreeBetToggleComponent {
  get dialogComponent() {
    return FreeBetSelectDialogComponent;
  }
  set dialogComponent(value:any){}
}

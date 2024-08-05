import { Component, ChangeDetectionStrategy } from '@angular/core';

import {
  FreeBetSelectDialogComponent as AppFreeBetSelectDialogComponent
} from '@freebets/components/freeBetSelectDialog/free-bet-select-dialog.component';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'free-bet-select-dialog',
  templateUrl: '../../../../../app/freebets/components/freeBetSelectDialog/free-bet-select-dialog.component.html',
  styleUrls: ['../../../../../app/freebets/components/freeBetSelectDialog/free-bet-select-dialog.component.scss', 'free-bet-select-dialog.component.scss']
})
export class FreeBetSelectDialogComponent extends AppFreeBetSelectDialogComponent {}

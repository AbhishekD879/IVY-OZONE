import { Component, ChangeDetectionStrategy } from '@angular/core';

import {
  ToteFreeBetSelectDialogComponent as AppToteFreeBetSelectDialogComponent
} from '@freebets/components/tote-free-bet-select-dialog/tote-free-bet-select-dialog.component';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'tote-free-bet-select-dialog',
  templateUrl: '../../../../../app/freebets/components/tote-free-bet-select-dialog/tote-free-bet-select-dialog.component.html',
  styleUrls: ['./tote-free-bet-select-dialog.component.scss']
})
export class ToteFreeBetSelectDialogComponent extends AppToteFreeBetSelectDialogComponent {}

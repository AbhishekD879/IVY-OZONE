import { Component, ViewChild } from '@angular/core';

import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { ICashOutData } from '../../models/cashout-section.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'edit-my-acca-history-dialog',
  templateUrl: './edit-my-acca-history-dialog.component.html',
  styleUrls: ['./edit-my-acca-history-dialog.component.scss']
})
export class EditMyAccaHistoryDialogComponent extends AbstractDialogComponent {
  @ViewChild('emaDialog', {static: true}) dialog;

  loading: boolean;
  bets: ICashOutData[];

  constructor(
    device: DeviceService, windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }

  open(): void {
    super.open();
    this.params.open(this);
  }
}

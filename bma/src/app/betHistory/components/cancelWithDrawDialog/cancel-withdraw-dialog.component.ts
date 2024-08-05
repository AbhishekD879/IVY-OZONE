import { Component, ViewChild } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'cancel-withdraw-dialog',
  templateUrl: './cancel-withdraw-dialog.component.html'
})
export class CancelWithDrawDialogComponent extends AbstractDialogComponent {

  @ViewChild('cancelWithDrawDialog',{static: true}) dialog;

  constructor(
    device: DeviceService, windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }
}

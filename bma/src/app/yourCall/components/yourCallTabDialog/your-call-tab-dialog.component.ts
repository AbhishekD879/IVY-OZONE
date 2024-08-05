import { Component, ViewChild } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'your-call-dialog',
  templateUrl: './your-call-tab-dialog.component.html'
})
export class YourCallTabDialogComponent extends AbstractDialogComponent {

  @ViewChild('yourCallTabDialog', { static: true }) dialog;

  constructor(
    device: DeviceService, windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }
}

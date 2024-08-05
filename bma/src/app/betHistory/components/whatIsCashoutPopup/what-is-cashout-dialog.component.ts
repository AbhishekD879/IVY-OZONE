import { Component, ViewChild } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'what-is-cashout-dialog',
  templateUrl: './what-is-cashout-dialog.component.html'
})
export class WhatIsCashOutDialogComponent extends AbstractDialogComponent {

  @ViewChild('whatIsCashOutDialog', { static: true }) dialog;

  constructor(
    device: DeviceService, windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }
}

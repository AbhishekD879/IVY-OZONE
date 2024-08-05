import { Component, ViewChild } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'over-ask-notification-dialog',
  templateUrl: 'over-ask-notification-dialog.component.html'
})
export class OverAskNotificationDialogComponent extends AbstractDialogComponent {
  @ViewChild('overAskNotificationDialog', { static: true }) dialog;

  constructor(device: DeviceService, windowRef: WindowRefService) {
    super(device, windowRef);
  }
}

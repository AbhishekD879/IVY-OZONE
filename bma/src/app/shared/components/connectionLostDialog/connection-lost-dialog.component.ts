import { Component, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '../oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'connection-lost-dialog',
  templateUrl: 'connection-lost-dialog.component.html',
  styleUrls: ['connection-lost-dialog.component.scss']
})
export class ConnectionLostDialogComponent extends AbstractDialogComponent {

  @ViewChild('connectionLostDialog', { static: true }) dialog;

  constructor(
    device: DeviceService, windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }
}

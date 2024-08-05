import { Component, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '../oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'bpp-error-dialog',
  templateUrl: './bpp-error-dialog.component.html'
})
export class BppErrorDialogComponent extends AbstractDialogComponent {
  @ViewChild('bppErrorDialog', { static: true }) dialog;

  constructor(
    device: DeviceService,
    windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }
  getHeaderTitle() {
    return `bpp.${this.params.error}Header`;
  }

  getBodyMessage() {
    return `bpp.${this.params.error}Message`;
  }
}

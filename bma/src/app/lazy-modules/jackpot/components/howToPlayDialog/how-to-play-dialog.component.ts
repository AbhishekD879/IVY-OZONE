import { Component, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'how-to-play-dialog',
  templateUrl: './how-to-play-dialog.component.html'
})
export class HowToPlayDialogComponent extends AbstractDialogComponent {

  @ViewChild('howToPlayDialog', { static: true }) dialog;
  params: { dialogClass: string };

  constructor(
    device: DeviceService, windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }
}

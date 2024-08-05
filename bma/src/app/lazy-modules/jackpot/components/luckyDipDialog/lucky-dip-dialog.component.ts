import { Component, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'lucky-dip-dialog',
  templateUrl: './lucky-dip-dialog.component.html'
})
export class LuckyDipDialogComponent extends AbstractDialogComponent {

  @ViewChild('luckyDipDialog', { static: true }) dialog;
  params: { makeLuckyDip: Function };

  constructor(
    device: DeviceService, windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }

  makeLuckyDip(): void {
    this.params.makeLuckyDip();
    this.closeDialog();
  }
}

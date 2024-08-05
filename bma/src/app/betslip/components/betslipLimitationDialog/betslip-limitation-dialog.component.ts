import { Component, ViewChild } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'betslip-limitation-dialog',
  templateUrl: 'betslip-limitation-dialog.component.html'
})
export class BetslipLimitationDialogComponent extends AbstractDialogComponent {
  @ViewChild('betslipLimitationDialog', { static: true }) dialog;

  constructor(device: DeviceService, windowRef: WindowRefService) {
    super(device, windowRef);
  }
}

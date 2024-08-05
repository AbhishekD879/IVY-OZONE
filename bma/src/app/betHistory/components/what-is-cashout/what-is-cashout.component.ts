import { Component, ComponentFactoryResolver } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import {
  WhatIsCashOutDialogComponent
} from '@betHistoryModule/components/whatIsCashoutPopup/what-is-cashout-dialog.component';

@Component({
  selector: 'what-is-cashout',
  templateUrl: './what-is-cashout.component.html'
})
export class WhatIsCashoutComponent {

  constructor(
    private device: DeviceService,
    private infoDialog: InfoDialogService,
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver
  ) { }

  openWhatIsCashOut(): void {
    if (!this.device.isOnline()) {
      this.infoDialog.openConnectionLostPopup();
    } else {
      this.dialogService.openDialog(
        DialogService.API.whatIsCashOutDialog,
        this.componentFactoryResolver.resolveComponentFactory(WhatIsCashOutDialogComponent),
        true
      );
    }
  }

}

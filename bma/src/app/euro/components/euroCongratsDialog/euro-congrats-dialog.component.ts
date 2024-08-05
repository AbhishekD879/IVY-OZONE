import { Component, Inject, ViewChild } from '@angular/core';
import { PlatformLocation } from '@angular/common';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { Router } from '@angular/router';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA } from '@angular/material/legacy-dialog';

@Component({
  selector: 'euro-congrats-dialog',
  templateUrl: 'euro-congrats-dialog.component.html',
  styleUrls: ['euro-congrats-dialog.component.scss']
})

export class EuroCongratsDialogComponent extends AbstractDialogComponent {
  @ViewChild('dialog', { static: true }) dialog: any;
  @Inject(MAT_DIALOG_DATA) public data: any;
  public freeTokenMessage: string[];

  constructor(protected router: Router, device: DeviceService, windowRef: WindowRefService, private loc: PlatformLocation) {
    super(device, windowRef);
    // closes modal when back button is clicked
    loc.onPopState(() => super.closeDialog());
  }

  /**
   * to open dialog box of congrats message
   * @returns {void}
   */
  public open(): void {
    super.open();
    if (this.params && this.params.data && this.params.data.freeTokenMessage) {
      this.freeTokenMessage = this.params.data.freeTokenMessage;
    }
  }

}

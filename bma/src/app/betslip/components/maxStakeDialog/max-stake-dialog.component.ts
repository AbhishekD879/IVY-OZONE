import { Component, OnInit, ViewChild } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'max-stake-dialog',
  templateUrl: 'max-stake-dialog.component.html'
})
export class MaxStakeDialogComponent extends AbstractDialogComponent implements OnInit {
  @ViewChild('maxStakeDialog', {static: true}) dialog;

  text: number;

  constructor(device: DeviceService, windowRef: WindowRefService) {
    super(device, windowRef);
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.text = this.params.text;
  }
}

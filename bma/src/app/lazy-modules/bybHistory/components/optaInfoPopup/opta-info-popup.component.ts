import { Component, ViewChild, ViewEncapsulation, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';

import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';


@Component({
  selector: 'opta-info-popup',
  templateUrl: './opta-info-popup.component.html',
  styleUrls: ['./opta-info-popup.component.scss'],
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OptaInfoPopupComponent extends AbstractDialogComponent {

  @ViewChild('optaInfoPopup') dialog;

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    super(device, windowRef);
  }

  open(): void {
    this.changeDetectorRef.detectChanges();
    super.open();
    this.changeDetectorRef.markForCheck();
  }
}

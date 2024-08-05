import { Component, ViewChild } from '@angular/core';
import { DeviceService } from '@app/core/services/device/device.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { NETWORK_CONSTANTS } from '@app/lazy-modules/networkIndicator/components/network-indicator/network-indicator.constants';

@Component({
  selector: 'connection-interruption-dialog',
  templateUrl: './connection-interruption-dialog.component.html',
  styleUrls: ['./connection-interruption-dialog.component.scss']
})
export class ConnectionInterruptionDialogComponent extends AbstractDialogComponent {

  @ViewChild('connectionInterruptionDialog', { static: true }) dialog;

  constructor(
    device: DeviceService, windowRef: WindowRefService, private gtmService: GtmService
  ) {
    super(device, windowRef);
  }

  closeInterruptionPopup() : void {
    this.gtmService.push(NETWORK_CONSTANTS.GA_TAGS.EVENT_TRACKING, [{
      ...NETWORK_CONSTANTS.GA_STATIC_FIELDS,
      'component.ActionEvent': NETWORK_CONSTANTS.GA_TAGS.CLICK,
      'component.PositionEvent': NETWORK_CONSTANTS.GA_TAGS.TOP,
      'component.LocationEvent': NETWORK_CONSTANTS.GA_TAGS.NA,
      'component.EventDetails': NETWORK_CONSTANTS.GA_TAGS.OK_CTA,
    }]);
    super.closeDialog();
  }
}

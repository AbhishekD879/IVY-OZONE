import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { AbstractDialogComponent } from '../oxygenDialogs/abstract-dialog';
import { StorageService } from '@core/services/storage/storage.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'session-logout-dialog',
  templateUrl: './session-logout-dialog.component.html',
  styleUrls: ['session-logout-dialog.component.scss','./session-logout-dialog.scss'],
  encapsulation: ViewEncapsulation.None
})
export class SessionLogoutDialogComponent extends AbstractDialogComponent implements OnInit {
  @ViewChild('sessionLogoutDialog', { static: true }) dialog;
  errorMsg: string;
  commonError: boolean;

  constructor(
    device: DeviceService,
    private storage: StorageService,
    private locale: LocaleService,
    private pubSubService: PubSubService,
    windowRef: WindowRefService
  ) {
    super(device, windowRef);
  }

  open(): void {
    super.open();

    const limitsData: { sessionLimitLogout?: boolean; sessionLimit?: number } = this.storage.get('sessionLimitLogout') || {};

    this.commonError = !limitsData.sessionLimitLogout;
    this.errorMsg = limitsData.sessionLimitLogout ?
      this.locale.getString('bma.loggedOutTittleSessionLimit', [limitsData.sessionLimit]) :
      this.locale.getString('bma.loggedOutTittle');
  }

  openLoginDialog(): void {
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { placeBet: false, moduleName: 'logout' });
  }
}

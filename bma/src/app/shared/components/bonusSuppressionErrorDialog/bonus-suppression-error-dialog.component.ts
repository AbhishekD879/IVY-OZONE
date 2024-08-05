import { Component, ViewChild } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { CmsService } from '@core/services/cms/cms.service';
import { AbstractDialogComponent } from '../oxygenDialogs/abstract-dialog';
import { ISystemConfig } from '@core/services/cms/models';
import environment from '@environment/oxygenEnvConfig';
import { REDIRECTION_URLS } from './bonus-suppression-error-dialog.constants';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';

@Component({
  selector: 'bonus-suppression-error-dialog',
  templateUrl: './bonus-suppression-error-dialog.component.html',
  styleUrls: ['./bonus-suppression-error-dialog.component.scss']
})
export class BonusSuppressionErrorDialogComponent extends AbstractDialogComponent {

  @ViewChild('bonusSuppresionErrorDialog', { static: true }) dialog;
  bonusSuppresionErrorMessage: string = '';
  errorMsg: string = rgyellow.ERROR_MSG;

  constructor(
    device: DeviceService, windowRef: WindowRefService,
    private cmsService: CmsService
  ) {
    super(device, windowRef);
    this.getErrorMessage();
  }

  getErrorMessage() {
    this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        this.bonusSuppresionErrorMessage = config.BonusSupErrorMsg ? config.BonusSupErrorMsg.errorMsg : this.errorMsg
      });
  }

  /**
  * Handles click on "Chat" button. redirects to chat and help page
  */
  goToChatPage() {
    if (environment.brand === 'ladbrokes') {
      this.windowRef.nativeWindow.open(REDIRECTION_URLS.ladbrokes);
    } else {
      this.windowRef.nativeWindow.open(REDIRECTION_URLS.coral);
    }
  }

}

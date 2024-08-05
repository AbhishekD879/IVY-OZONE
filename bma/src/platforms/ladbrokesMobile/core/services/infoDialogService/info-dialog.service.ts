import { Injectable } from '@angular/core';
import { InfoDialogService as AppInfoDialogService } from '@core/services/infoDialogService/info-dialog.service';

@Injectable()
export class InfoDialogService extends AppInfoDialogService {

  // Don't show logged out popup
  openLogoutPopup(): void {}
}

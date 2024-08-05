import { Injectable } from '@angular/core';

import { CommandService } from '@core/services/communication/command/command.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { QuickbetNotificationService } from '@app/quickbet/services/quickbetNotificationService/quickbet-notification.service';

@Injectable({ providedIn: 'root' })
export class QuickbetRunService {

  constructor(private command: CommandService,
              private quickbetService: QuickbetService,
              private quickbetNotificationService: QuickbetNotificationService) {}

  // TODO: after command will use Observable remove Promise
  init(): void {
    this.command.register(this.command.API.SHOW_QUICKBET, (selection, dynamicGtmObj) => {
      this.quickbetService.showQuickbet(selection, dynamicGtmObj);
      return Promise.resolve();
    });
    this.command.register(this.command.API.QUICKBET_RESTORE, (...args) => {
      this.quickbetService.restoreSelection(...args);
      return Promise.resolve();
    });
    this.command.register(this.command.API.QUICKBET_SHOW_ERROR, (message, type) => {
      this.quickbetNotificationService.saveErrorMessage(message, type);
      return Promise.resolve();
    });
    this.command.register(this.command.API.QUICKBET_CLEAR_ERROR, () => {
      this.quickbetNotificationService.clear();
      return Promise.resolve();
    });
  }
}

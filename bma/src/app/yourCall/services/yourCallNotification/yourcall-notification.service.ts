/**
 * @class notification service for yourcall betslip
 */
import { Injectable } from '@angular/core';
import { CommandService } from '@core/services/communication/command/command.service';

@Injectable({ providedIn: 'root' })
export class YourCallNotificationService {
  constructor(
    private commandService: CommandService
  ) {}

  saveErrorMessage(message: string, type: string): Promise<void> {
    return this.commandService.executeAsync(this.commandService.API.QUICKBET_SHOW_ERROR, [message, type]);
  }

  clear(): Promise<void> {
    return this.commandService.executeAsync(this.commandService.API.QUICKBET_CLEAR_ERROR, []);
  }
}

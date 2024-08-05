import { Injectable } from '@angular/core';

import { UserService } from '@core/services/user/user.service';
import { StorageService } from '../storage/storage.service';
import { CommandService } from '../communication/command/command.service';
import { PubSubService } from '../communication/pubsub/pubsub.service';

@Injectable()
export class DigitalSportBetsService {
  constructor(
    private userService: UserService,
    private storage: StorageService,
    private command: CommandService,
    private pubsub: PubSubService,
  ) {

  }

  sendOddsToDS(dsTempToken: string, myBetsIframe: HTMLIFrameElement): void {
    if (dsTempToken && myBetsIframe) {
      myBetsIframe.contentWindow.postMessage(`ds:odds:${this.userService.oddsFormat}`, '*');
    }
  }

  getDSBetslipCounter(callback: Function): void {
    // TODO: should be removed after yourcall full integration
    if (this.storage.get('dsBetslip')) {
      this.command.executeAsync(this.command.API.DS_READY, undefined, 0)
        .then(count => {
          callback(count);
        });
    }

    this.pubsub.subscribe('digitalSportBetsFactory', this.pubsub.API.DS_BETSLIP_COUNTER_UPDATE, callback);
  }
}

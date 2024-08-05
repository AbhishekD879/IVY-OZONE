import { Injectable } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LiveServIframeService } from '@core/services/liveServ/live-serv-iframe.service';

@Injectable()
export class BmaRunService {

  constructor(
    private pubsub: PubSubService,
    private liveServIframeService: LiveServIframeService
  ) { }

  init(): void {
    this.pubsub.subscribe('bma', this.pubsub.API.APP_IS_LOADED, () => {
      this.liveServIframeService.initIframe();
    });
  }
}

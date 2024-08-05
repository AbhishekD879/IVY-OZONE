import { Injectable, NgZone } from '@angular/core';
import { WindowRefService } from '../windowRef/window-ref.service';
import { DeviceService } from '../device/device.service';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { IConstant } from '../models/constant.model';
import { WsConnector } from './ws-connector';
@Injectable()
export class WsConnectorService {
  constructor(public windowRef: WindowRefService, public device: DeviceService, public pubsub: PubSubService,
              private ngZone: NgZone) {}
  create(endpoint: string, options: IConstant, moduleName?: string): WsConnector {
    return new WsConnector(endpoint, options, moduleName, this.windowRef, this.device, this.pubsub, this.ngZone);
  }
}
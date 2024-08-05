import { Injectable } from '@angular/core';

import * as io from 'socket.io-client';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';

@Injectable({
  providedIn: 'root'
})
export class WindowRefService {

  constructor(private pubsub: PubSubService, private command: CommandService) {
    this.nativeWindow.io = io;
    this.nativeWindow.ps = {
      subscribe: pubsub.subscribe.bind(this.pubsub),
      unsubscribe: pubsub.unsubscribe.bind(this.pubsub),
      publish: pubsub.publish.bind(this.pubsub)
    };
    this.nativeWindow.command = {
      execute: command.execute.bind(this.command),
      executeAsync: command.executeAsync.bind(this.command),
    };
  }

  get document(): HTMLDocument {
    return this.nativeWindow.document;
  }
  set document(value:HTMLDocument){}
  get nativeWindow(): { [name: string]: any } {
    return window;
  }
  set nativeWindow(value:{ [name: string]: any }){}
}

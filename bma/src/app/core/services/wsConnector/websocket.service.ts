import { webSocket, WebSocketSubject, WebSocketSubjectConfig } from "rxjs/webSocket";
import { interval, Observable, retry, Subject, Subscription } from 'rxjs';
import { Injectable, NgZone } from '@angular/core';

import { SocketSettings } from "./websocket.model";
import { SOCKETCODES } from "@core/constants/websocket-events.constant";
@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private readonly ioSettings: SocketSettings;
  socket;
  callbacks: any;
  private pingSubscription: Subscription;
  connection: Subject<any>;
  websocketConfig: WebSocketSubjectConfig<any>;
  constructor(
    private ngZone: NgZone
  ) {
    this.connection = new Subject();
    this.ioSettings = {
      reconnectionDelay: 1000,
      timeout: 10000,
      reconnectionAttempts: 15,
      pingDelay: 25000
    };
    this.websocketConfig = {
      url: '',
      deserializer: function (e) { return e.data },
      serializer: (msg: string) => msg,
      openObserver: {
        next: () => this.onConnect()
      },
      closeObserver: {
        next: () => { }
      }
    };
  }
  /**
    * initiates the heartbeat after connection is established
    * emits a message to the connection subscriber
    */
  onConnect(): void {
    this.pingpong();
    this.connection.next(true);
  }

  pingpong(): void {
    this.pingSubscription = interval(this.ioSettings.pingDelay).subscribe(n => {
      !this.isConnected() ? this.pingSubscription.unsubscribe() : this.sendMessage(SOCKETCODES.SOCKET_PING);
    });
  }
  /**
   * Remove event listener from connection
   * @param {String} event
   * @param {Function} handler
   */
  removeEventListener(event: string, handler: Function): void {
    const callback = this.callbacks[event];
    if (!callback) {
      return;
    }
    delete this.callbacks[event];
  }

  /**
   * Remove all connection listeners
   * @param events {Array}
   */
  removeAllListeners(events: string[]): void {
    if (!!this.callbacks)
      events.forEach(event => {
        if (this.callbacks[event]) {
          delete this.callbacks[event];
        }
      })
  }
  /**
   * establish websocket connection
   */
  establishConnection(endpoint: string): void {
    this.websocketConfig.url = endpoint;
    this.ngZone.runOutsideAngular(() => {
      this.socket = this.getSocket(this.websocketConfig);
    });
    this.socketListener();
  }
  /**
     * emits data to server 
  */
  sendMessage(msg: any): void {
    if (this.socket) {
      this.socket.next(msg);
    }
  }

  /**
   * Add event listener to connection
   * @param {String} event
   * @param {Function} cb
   */
  addEventListener(event: string, cb: Function): void {
    this.callbacks = this.callbacks || {};
    (this.callbacks[event] = this.callbacks[event] || []).push(cb);
  }
  /**
  * sends disconnect message to server
  * clears the subscriptions, callback events
  */
  disconnect(): void {
    this.sendMessage(SOCKETCODES.SOCKET_DISCONNECT);
    if (this.socket) {
      this.socket.complete();
    }
    if (this.pingSubscription) {
      this.pingSubscription.unsubscribe();
    }
    this.socket = undefined;
    this.callbacks = undefined;
    this.connection = new Subject();
  }
  /**
    * Listens WebSocket subject which reconnects after failure
    */
  socketListener(): Observable<any> {
    return this.socket.pipe(
      retry({ count: this.ioSettings.reconnectionAttempts, delay: this.ioSettings.reconnectionDelay }))
      .subscribe(item => {
        this.callBacks(item);
      });
  }

  clearCallbacks(): void {
    this.callbacks = {};      
  }

  /**
    * registers all the listners
    * @param item
    */
  callBacks(item: any): void {
    if (!!item) {
      const index = item.indexOf(',');
      if (index != -1) {
        if (item.charAt(0) !== '0') {
          const response = JSON.parse(item.substr(index + 1));
          if (!!response[0]) {
            const callBack = this.callbacks[response[0]];
            if (!!callBack) {
              for (let i = 0, len = callBack.length; i < len; ++i) {
                callBack[i].apply(this, [response[1]]);
              }
            }
          }
        }
      }
    }
  }
  /**
   * Check if websocket subject connected
   */
  public isConnected(): boolean {
    return (this.socket && !this.socket.closed);
  }
  /**
   * Return a custom WebSocket subject
   */
  public getSocket<T>(socketConfig: string | WebSocketSubjectConfig<T>): WebSocketSubject<T> {
    return webSocket<T>(socketConfig);
  }
}


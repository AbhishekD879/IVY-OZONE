import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { ISocketIO } from '@core/services/liveServ/live-serv-connection.model';
import { LiveServConnectionService } from '@app/core/services/liveServ/live-serv-connection.service';
import { ICallBack } from '@app/fiveASideShowDown/models/call-back';

@Injectable({
  providedIn: 'root'
})
export class FiveASideLiveServeHandlerService {
  private callbacks: { channel: string, handler: Function, emitKey: string }[] = [];
  private connection: any;
  private eventsHandlers: { [key: string]: Function } = {};

  constructor(
    private liveServConnectionService: LiveServConnectionService
  ) {
    this.disconnectHandler = this.disconnectHandler.bind(this);
  }
  /**
   * SHOWDOWN SUBSCRIPTION
   * @param  {string} channel
   * @param  {Function} onUpdateCallback
   * @param  {string} emitKey
   * @returns {void}
   */
  showDownSubscribe(channel: string, onUpdateCallback: Function, emitKey?: string): void {
    const updatesHandler = update => {
      if (_.isFunction(onUpdateCallback)) {
        onUpdateCallback(update);
      }
    };
    this.callbacks.push({ channel, handler: updatesHandler, emitKey });
    this.liveServConnectionService.connect().subscribe(connection => {
      this.liveServConnectionService.subscribeToShowdown(channel, updatesHandler, emitKey);
      this.updateConnection(connection);
    });
  }
  /**
   * To Add event Listener
   * @param  {string[]} channels
   * @param  {Function} onUpdateCallback
   * @returns {void}
   */
  addEventListner(channels: string[], onUpdateCallback: Function): void {
    channels.forEach((channel: string) => {
      this.showDownSubscribe(channel, onUpdateCallback, 'subscribeshowdown');
    });
  }
  /**
   * Remove Listner
   * @param  {string} channel
   * @returns {void}
   */
  removeEventListner(channel: string): void {
    if (this.eventsHandlers[channel]) {
      this.liveServConnectionService.removeEventListner(channel, this.eventsHandlers[channel]);
      delete this.eventsHandlers[channel];
    }
  }
  /**
   * Remove Listners
   * @param  {string[]} channels
   * @returns {void}
   */
  removeEventAllListner(channels: string[]): void {
    this.liveServConnectionService.removeAllEventListner(channels);
  }
  /**
   * Remove all subscription after failed connection and re-init again
   * @returns {void}
   */
  reconnect(): void {
    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      const uniqueCallBacks: ICallBack[] = this.getUniqueCallBacks(this.callbacks);

      this.callbacks.forEach((callback: { channel: string, handler: Function, emitKey: string }) => {
        this.unsubscribe([callback.channel], callback.handler);
      });
      uniqueCallBacks.forEach(callBack => {
        this.showDownSubscribe(callBack.channel, callBack.handler, callBack.emitKey);
      });
      this.updateConnection(connection);
    });
  }

  /**
   * Unsibscribe from list of channels
   * @param {Array} channels - array of channels
   * @returns {void}
   */
  unsubscribe(channels: string[], handler: Function): void {
    if (channels && channels.length) {
      channels.forEach((channel: string) => {
        const callBacks = this.callbacks.filter((callBack) => callBack.channel === channel);
        if (callBacks && callBacks.length) {
          this.unsubscribeChannels(callBacks, handler);
          this.callbacks = this.callbacks.filter((callBack) => callBack.channel !== channel);
        }
      });
    }
  }

  /**
   * To Get Unique call backs
   * @param {ICallBack[]} callBacks
   * @returns {ICallBack[]}
   */
  private getUniqueCallBacks(callBacks: ICallBack[]): ICallBack[] {
    const uniqueCallBacks: ICallBack[] = callBacks.reduce((previous, current) => {
      const unique = previous.find((callBack: ICallBack) => callBack.channel === current.channel);
      if (!unique) {
        return previous.concat([current]);
      } else {
        return previous;
      }
    }, []);
    return uniqueCallBacks;
  }

  /**
   * To Unsubscribe all channels
   * @param {ICallBack[]} callBacks
   * @param {Function} handler
   * @returns {void}
   */
  private unsubscribeChannels(callBacks: ICallBack[], handler: Function): void {
    callBacks.forEach((callBack: ICallBack) => this.liveServConnectionService.unsubscribeFromShowdown([callBack.channel], handler));
  }

  /**
   * To Update connection
   * @param {Object} connection - socket connenction to LS MS
   * @returns {void}
   */
  private updateConnection(connection: ISocketIO): void {
    if (this.isConnectionValid(connection)) {
      this.connection = connection;
      this.setDisconnectHandler();
    }
  }

  /**
   * Check if connenction is connencted and not dublicated
   * @param {ISocketIO} connection
   * @return {boolean}
   */
  private isConnectionValid(connection: ISocketIO): boolean {
    return connection && connection.connected && (!this.connection || this.connection.id !== connection.id);
  }

  /**
   * Handle server disconnect and then reestablish connection
   * @returns {void}
   */
  private disconnectHandler(error: string): void {
    if (this.liveServConnectionService.isDisconnected(error)) {
      this.reconnect();
    }
  }
  /**
   * Set disconnect listener only for new or re-established socket connections
   * @returns {void}
   */
  private setDisconnectHandler(): void {
    this.liveServConnectionService.onDisconnect(this.disconnectHandler);
  }

}

import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { ISocketIO } from '@core/services/liveServ/live-serv-connection.model';

@Injectable({
  providedIn: 'root'
})
export class HandleLiveServeUpdatesService {
  private callbacks: any;
  private connection: any;

  constructor(
    private liveServConnectionService: LiveServConnectionService
  ) {
    this.disconnectHandler = this.disconnectHandler.bind(this);
  }

  /**
   * Subscribe to list of channels
   * @param {Array} channels - array of channels
   * @param {Function} onUpdateCallback - on update callback
   */
  subscribe(channels: string[], onUpdateCallback: Function, isForShowdown?: boolean) {
    const updatesHandler = update => {
      if (update.type === 'MESSAGE') {
        const { type, id } = update.channel,
          payload = update.message;
        const updateObject = { payload, type, id };
        if (_.isFunction(onUpdateCallback)) {
          onUpdateCallback(updateObject);
        }
      }
    };
    this.callbacks = { channels, handler: updatesHandler };
    this.liveServConnectionService.connect().subscribe(connection => {
      this.liveServConnectionService.subscribe(this.callbacks.channels, this.callbacks.handler, isForShowdown);

      this.updateConnection(connection);
    });
  }

  /**
   * Remove all subscription after failed connection and re-init again
   */
  reconnect(): void {
    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      this.unsubscribe(this.callbacks.channels);
      this.liveServConnectionService.subscribe(this.callbacks.channels, this.callbacks.handler);

      this.updateConnection(connection);
    });
  }

  /**
   * Unsibscribe from list of channels
   * @param {Array} channels - array of channels
   */
  unsubscribe(channels: string[]): void {
    if (channels && channels.length) {
      this.liveServConnectionService.unsubscribe(channels, this.callbacks.handler);
    }
  }

  /**
   *
   * @param {Object} connection - socket connenction to LS MS
   * @private
   */
  private updateConnection(connection: ISocketIO): void {
    if (this.isConnectionValid(connection)) {
      this.connection = connection;
      this.setDisconnectHandler();
    }
  }

  /**
   * Check if connenction is connencted and not dublicated
   * @param {Object} connection
   * @return {boolean}
   * @private
   */
  private isConnectionValid(connection: ISocketIO): boolean {
    return connection && connection.connected && (!this.connection || this.connection.id !== connection.id);
  }

  /**
   * Set disconnect listener only for new or re-established socket connections
   */
  private setDisconnectHandler(): void {
    this.liveServConnectionService.onDisconnect(this.disconnectHandler);
  }

  /**
   * Handle server disconnect and then reestablish connection
   */
  private disconnectHandler(error: string): void {
    if (this.liveServConnectionService.isDisconnected(error)) {
      this.reconnect();
    }
  }
}

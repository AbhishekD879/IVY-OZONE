import { Injectable } from '@angular/core';
import { ReplaySubject } from 'rxjs';

import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { ISocketIO } from '@core/services/liveServ/live-serv-connection.model';
import { IScoreboardStatsUpdate } from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Injectable({ providedIn: 'root' })
export class HandleScoreboardsStatsUpdatesService {
  private callbacks: { handler: Function };
  private channels: string[] = [];
  private connection: ISocketIO;
  private statsStore: Map<string , IScoreboardStatsUpdate> = new Map();
  private $statisticsEventIds: ReplaySubject<string> = new ReplaySubject();

  constructor(
    private liveServConnectionService: LiveServConnectionService,
    private coreToolsService: CoreToolsService,
    private pubSubService: PubSubService
  ) {
    this.disconnectHandler = this.disconnectHandler.bind(this);
  }

  getStatisticsEventIds(): ReplaySubject<string> {
    return this.$statisticsEventIds;
  }

  /**
   * Subscribe to channel to get scoreboard stats
   * @param channel - chanel(eventID)
   */
  subscribeForUpdates(channel: string) {
    const updatesHandler = (update: IScoreboardStatsUpdate) => {
      if (this.statsStore.has(update.obEventId)) {
        const oldUpdate = this.statsStore.get(update.obEventId);
        const extendedUpdate = this.coreToolsService.deepMerge(oldUpdate, update);
        this.statsStore.set(update.obEventId, extendedUpdate);
      } else {
        this.statsStore.set(update.obEventId, update);
        this.$statisticsEventIds.next(update.obEventId);
      }
      this.pubSubService.publish(this.pubSubService.API.UPDATE_BYB_BET, this.statsStore.get(update.obEventId));
    };
    if (this.statsStore.has(channel)) {
      this.pubSubService.publish(this.pubSubService.API.UPDATE_BYB_BET, this.statsStore.get(channel));
    }

    this.channels.push(channel);
    this.callbacks = { handler: updatesHandler };
    this.liveServConnectionService.connect().subscribe(connection => {
      this.liveServConnectionService.subscribeToScoreboards(channel, this.callbacks.handler);

      this.updateConnection(connection);
    });
  }

  /**
   * Remove all subscription after failed connection and re-init again
   */
  reconnect(): void {
    this.liveServConnectionService.connect().subscribe((connection: ISocketIO) => {
      const uniqueChannels: string[] = this.channels.filter((channel, index) => this.channels.indexOf(channel) === index);
      this.channels.forEach(ch => this.unsubscribe(ch));
      // this.channels = []; Commented to fix BMA-59513
      uniqueChannels.forEach(channel => {
        this.statsStore.delete(channel);
        this.liveServConnectionService.subscribeToScoreboards(channel, this.callbacks.handler);
      });
      this.updateConnection(connection);
    });
  }

  /**
   * Unsubscribe from list of channels(updates with scoreboard stats)
   * @param channel - eventId
   */
  unsubscribe(channel: string): void {
    this.liveServConnectionService.unsubscribeFromScoreboards(channel, this.callbacks.handler);
  }

  /**
   *
   * @param {Object} connection - socket connection to LS MS
   * @private
   */
  private updateConnection(connection: ISocketIO): void {
    if (this.isConnectionValid(connection)) {
      this.connection = connection;
      this.setDisconnectHandler();
    }
  }

  /**
   * Check if connection is connected and not duplicated
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

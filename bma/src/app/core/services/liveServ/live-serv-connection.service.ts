import { of as observableOf, Observable, Subject } from 'rxjs';
import { Injectable, NgZone } from '@angular/core';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { EVENTS, MatchCmtryConstants } from '@core/constants/websocket-events.constant';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { SubscriptionsManagerService } from '@core/services/subscriptionsManager/subscriptions-manager.service';
import { ISocketIO } from '@core/services/liveServ/live-serv-connection.model';

@Injectable()
export class LiveServConnectionService {
  connection: ISocketIO = null;

  protected moduleName = 'liveServe';

  protected connectionObserver: Subject<ISocketIO>;

  protected subscriptionsManager: any;
  protected readonly SUBSCRIBE_SHOWDOWN_CHANNEL = 'subscribeshowdown';

  constructor(protected windowRef: WindowRefService,
    protected deviceService: DeviceService,
    protected pubsub: PubSubService,
    protected subscriptionsManagerService: SubscriptionsManagerService,
    protected ngZone: NgZone) {

    this.subscriptionsManager = this.subscriptionsManagerService.create();
  }

  /**
   * Provides web socket connection: returns observable of either currently connected,
   * or a new one (creates connection if not already pending for it).
   * @returns {Observable<ISocketIO>}
   */
  connect(): Observable<ISocketIO> {
    if (this.isConnected()) {
      return observableOf(this.connection);
    }

    if (!this.connectionObserver || this.connectionObserver.isStopped) {
      this.connectionObserver = new Subject<ISocketIO>();

      if (this.connection) {
        this.connection.close();
      }

      this.connection = this.createConnection();
      this.addConnectionCallbacks();
    }

    return this.connectionObserver as Observable<ISocketIO>;
  }

  closeConnection(): void {
    this.connection.close();
    this.connectionObserver.complete();
  }

  /**
   * Adds listeners to array of channels
   * if the channel has already any listener,
   * the new one is added,
   * otherwise, subscription is emitted
   * @param channels {Array}
   * @param handler
   */
  subscribe(channels: string[], handler: Function, isForShowdown?: boolean): void {
    if (_.isArray(channels) && channels.length) {
      const channelsToEmit = this.subscriptionsManager.checkForSubscribe(channels);

      _.each(channels, ch => {
        this.connection.on(ch, handler);
      });

      // Emit "subscribe" only for channels that do not have other subscribers
      if (channelsToEmit.length) {
        this.connection.emit(isForShowdown ? this.SUBSCRIBE_SHOWDOWN_CHANNEL : 'subscribe', channelsToEmit);
      }
    } else {
      console.warn('Array of channels is expected but not found');
    }
  }

  /**
   * Adds listeners to  betpacks
   * if the channel has already any listener,
   * the new one is added,
   * otherwise, subscription is emitted
   * @param channels [Array]
   * @param handler
   */
  subscribeBP(channels: string[], handler: Function): void {
    if (_.isArray(channels) && channels.length) {
      const channelsToEmit = this.subscriptionsManager.checkForSubscribe(channels);

      _.each(channels, ch => {
        this.connection.on(ch, handler);
      });

      if (channelsToEmit.length) {
        this.connection.emit('bet-pack-subscribe', channelsToEmit);
      }
    } else {
      console.warn('Array of channels is expected but not found');
    }
  }

    /**
   * Unsubscribe for betpack
   * @param channels [Array]
   * @param handler
   */
  unsubscribeBP(channels: string[], handler: Function): void {
    if (_.isArray(channels) && channels.length) {
      const channelsToEmit = this.subscriptionsManager.checkForUnsubscribe(channels);

      _.each(channels, ch => {
        this.connection.removeAllListeners(ch);
      });

      // Emit "unsubscribe" only for channels that do not have other subscribers
      if (channelsToEmit.length) {
        this.connection.emit('bet-pack-unsubscribe', channelsToEmit);
      }
    } else {
      console.warn('Array of channels is expected but not found');
    }
  }

  /**
   * To Add Event Listener
   * @param  {string[]} channels
   * @param  {Function} handler
   * @returns {void}
   */
  addEventListner(channels: string[], handler: Function): void {
    channels.forEach((channel: string) => {
      this.subscribeToShowdown(channel, handler, this.SUBSCRIBE_SHOWDOWN_CHANNEL);
    });
  }

  /**
   * To Remove Event Listener
   * @param  {string} channel
   * @param  {Function} handler
   * @returns {void}
   */
  removeEventListner(channel: string, handler: Function): void {
    this.connection.removeListener(channel, handler);
  }

  /**
   * To Remove All event Listeners
   * @param  {string[]} channels
   * @returns {void}
   */
  removeAllEventListner(channels: string[]): void {
    this.connection.removeAllListeners(channels);
  }

  /**
   * Adds listeners channel(which is event ID)
   * To get scoreboard statistics
   * @param channel
   * @param handler
   */
  subscribeToScoreboards(channel: string, handler: Function): void {
    const channelsToEmit = this.subscriptionsManager.checkForSubscribe([channel]);
    this.connection.on(channel, handler);

    // Emit "scoreboard" only for channels that do not have other subscribers
    if (channelsToEmit.length) {
      this.connection.emit('scoreboard', channelsToEmit[0]);
    }
  }
  /**
   * Adds listeners channel(which is event ID)
   * To get match-commentary updates
   * @param channel
   * @param handler
   */
  subscribeToMatchCommentary(channel: string, handler: Function): void {
    const channelsToEmit = this.subscriptionsManager.checkForSubscribe([channel]);
    if (channelsToEmit?.length) {
      this.connection.on(channel, handler);
      this.connection.emit(MatchCmtryConstants.subMatchCmtry, channel);
    }
  }
  /**
   * Adds listeners channel(which is event ID)
   * To get match-commentary updates
   * @param channels
   * @param handler
   */
  sendRequestForLastMatchFact(channels: string[], handler: Function): void {
    channels.forEach((channel:string) => {
      this.connection?.on(channel, handler);
    });
    this.connection?.connected && this.connection.emit(MatchCmtryConstants.subLastMatchCode, channels);
  }

  /**
   * Subscribe For ShowDown
   * @param  {string} channel
   * @param  {Function} handler
   * @returns {void}
   */
  subscribeToShowdown(channel: string, handler: Function, keyEmit: string): void {
    const channelsToEmit = this.subscriptionsManager.checkForSubscribe([channel]);
    this.connection.on(channel, handler);
    const isSubscribeToShowDown: boolean = keyEmit === this.SUBSCRIBE_SHOWDOWN_CHANNEL;
    if (channelsToEmit.length) {
      if(isSubscribeToShowDown) {
        this.connection.emit(keyEmit, [channelsToEmit[0]]);
      } else {
        this.connection.emit(keyEmit, channelsToEmit[0]);
      }
    }
  }

  /**
   * Unsubscribe for Showdown
   * @param  {string} channel
   * @param  {Function} handler
   * @returns {void}
   */
  unsubscribeFromShowdown(channels: Array<string>, handler: Function): void {
    if (channels.length) {
      const channelsToEmit = this.subscriptionsManager.checkForUnsubscribe(channels);

      channels.forEach((ch: string) => {
        this.connection.removeAllListeners(ch);
      });

      // Emit "unsubscribe" only for channels that do not have other subscribers
      if (channelsToEmit.length) {
        this.connection.emit('unsubscribeshowdown', channelsToEmit);
      }
    } else {
      console.warn('Array of channels is expected but not found');
    }
  }

  /**
   * Remove listeners from channel(which is event ID)
   * @param channel
   * @param handler
   */
  unsubscribeFromScoreboards(channel: string, handler: Function): void {
    const channelsToEmit = this.subscriptionsManager.checkForUnsubscribe([channel]);

    this.connection.removeListener(channel, handler);

    // Emit "unsubscribeScoreboard" only for channels that do not have other subscribers
    if (channelsToEmit.length) {
      this.connection.emit('unsubscribeScoreboard', channelsToEmit[0]);
    }
  }
   /**
   * Unsubscribe for match-commentary
   * @param channel
   * @param handler
   */
  unsubscribeFromMatchCommentary(channel: string, handler: Function): void {
    const channelsToEmit = this.subscriptionsManager.checkForUnsubscribe([channel]);
    if (channelsToEmit?.length) {
      this.connection.removeAllListeners([channel]);
      this.connection.emit(MatchCmtryConstants.unsubMatchCmtry, channel);
    }
  }

  /**
   * Removes listeners from specific channel
   * if the channel has the only one listener and it is removed,
   * unsubscription is emitted
   * @param channels {Array}
   * @param handler
   */
  unsubscribe(channels: string[], handler: Function): void {
    if (_.isArray(channels) && channels.length) {
      const channelsToEmit = this.subscriptionsManager.checkForUnsubscribe(channels);

      _.each(channels, ch => {
        this.connection.removeListener(ch, handler);
      });

      // Emit "unsubscribe" only for channels that do not have other subscribers
      if (channelsToEmit.length) {
        this.connection.emit('unsubscribe', channelsToEmit);
      }
    } else {
      console.warn('Array of channels is expected but not found');
    }
  }

  /**
   * Shared handler to handle properly disconnect event outside service
   */
  onDisconnect(callback: Function): void {
    this.connection.removeListener('disconnect', callback);
    this.connection.on('disconnect', callback);
  }

  disconnect(): void {
    if (this.connection) {
      this.connection.io.disconnect();
    }
  }

  /**
   * Check if connection is disconnected
   * @param {string} error - error code from live serve WS
   * @returns {boolean}
   */
  isDisconnected(error: string): boolean {
    return ['transport close', 'ping timeout', 'transport error'].includes(error);
  }

  /**
   * Checks if connection to web socket is established
   * @returns {boolean}
   * @private
   */
  isConnected(): boolean {
    return this.connection && this.connection.connected;
  }

  /**
   * Create Ms webSocket connection.
   */
  private createConnection(): ISocketIO {
    const ioSettings = {
      path: this.getPath(),
      transports: this.getTransports(),
      upgrade: false,
      reconnectionDelay: 2000,
      forceNew: true,
      timeout: 10000,
      reconnectionAttempts: 10
    };

    const url = this.isPooling() ? `${environment.LIVESERVEMS}:444` : environment.LIVESERVEMS;
    return this.ngZone.runOutsideAngular(() => this.windowRef.nativeWindow.io(url, ioSettings));
  }

  /**
   * Register socket handlers
   * @private
   * @return {BehaviorSubject<io>}
   */
  private addConnectionCallbacks(): void {
    this.connection.on('connect', () => this.connectHandler());
    this.connection.on('connect_error', (error: string) => this.connectErrorHandler(error));

    if (!this.deviceService.isSafari) {
      this.connection.on('disconnect', (error: string) => this.disconnectHandler(error));
    }
  }

  private connectHandler(): void {
    console.warn('liveServe WS connect');
    this.connectionObserver.next(this.connection);
    this.connectionObserver.complete();
    this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_CONNECT_SUCCESS}`, this.connection);
  }

  private connectErrorHandler(error: string): void {
    console.warn('LS MS connect error', error);
    this.connectionObserver.complete();
  }

  private disconnectHandler(error: string): void {
    console.warn('LS MS disconnect', error);
    this.connectionObserver = new Subject<ISocketIO>();
    this.connection.on('reconnect', () => this.reconnectHandler());
    this.connection.on('reconnect_failed', (err: string) => this.reconnectErrorHandler(err));
  }

  private reconnectHandler(): void {
    console.warn('liveServe WS reconnect');
    if (this.isConnected()) {
      this.connectionObserver.next(this.connection);
      this.connectionObserver.complete();
    }
    this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_RECONNECT_SUCCESS}`);
  }

  private reconnectErrorHandler(error: string): void {
    console.warn('liveServe WS reconnect_failed', error);
    this.connectionObserver.complete();
  }

  /**
   * Gets transports
   * @returns {Array}
   * @private
   */
  private getTransports(): string[] {
    return [this.isPooling() ? 'polling' : 'websocket'];
  }

  /**
   * Gets path
   * @returns {string}
   * @private
   */
  private getPath(): string {
    return `/${this.isPooling() ? 'polling' : 'websocket'}`;
  }

  /**
   * Checks if pooling is necessary,
   * as not all devices support web sockets
   * @returns {boolean}
   * @private
   */
  private isPooling(): boolean {
    return this.deviceService.osVersion === '4.3' && this.deviceService.isNativeAndroid;
  }
}

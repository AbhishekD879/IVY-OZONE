import { throwError, of as observableOf,  Observable ,  Subject } from 'rxjs';
import * as _ from 'underscore';
import { WindowRefService } from '../windowRef/window-ref.service';
import { DeviceService } from '../device/device.service';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { EVENTS } from '../../constants/websocket-events.constant';
import { IConstant } from '../models/constant.model';
import { ISocketConnection } from '../../models/socket-connection.model';
import { NgZone } from '@angular/core';
export class WsConnector {
  public connection: ISocketConnection;
  public state$: Subject<string>;
  private isConnecting: boolean;
  private anyMessageHandler: Function;
  private connect$: Subject<ISocketConnection>;
  private reconnect$: Subject<ISocketConnection>;
  constructor(private endpoint: string, private options: IConstant, public moduleName: string,
    public windowRef: WindowRefService, public device: DeviceService, public pubsub: PubSubService,
    private ngZone: NgZone) {
    const defaultOptions: IConstant = {
      path: '/websocket',
      transports: ['websocket'],
      upgrade: false,
      forceNew: true,
      autoConnect: true,
      timeout: options.timeout || 2200,
      reconnectionDelay: options.reconnectionDelay || 500,
      reconnectionAttempts: options.reconnectionAttempts || 5
    };
    this.isConnecting = false;
    this.endpoint = endpoint;
    this.options = _.extend(defaultOptions, options);
    this.connection = null;
    this.anyMessageHandler = null;
    this.state$ = new Subject();
    this.state$.subscribe(state => state && console.warn(`${this.moduleName} ${state}`, this.connection));
  }
  /**
   * Connects to web socket
   * @returns Observable<ISocketConnection>
   */
  connect(): Observable<ISocketConnection> {
    if (!this.windowRef.nativeWindow.io) {
      return throwError('no socket-io lib loaded');
    }
    // create observable if no one
    if (!this.connect$ || this.connect$.isStopped) {
      this.connect$ = new Subject();
      this.connect$.subscribe();
    }
    // return reconnect observable if was disconnect and reconnect started
    if (this.reconnect$ && !this.reconnect$.isStopped) {
      return this.reconnect$;
    }
    // return connect observable if current connection in progress
    if (this.isConnecting) {
      return this.connect$;
    }
    // complete current observable if websocket is connnected
    if (this.isConnected()) {
      this.connect$.complete();
      return observableOf(this.connection);
    }
    // add flag for starting connection
    this.isConnecting = true;
    this.ngZone.runOutsideAngular(() => {
      this.connection = this.windowRef.nativeWindow.io(this.endpoint, this.options);
    });
    this.decorateEventIncomeMessage();
    this.addCallbacks();
    return this.connect$;
  }
  /**
   * Reconnects to web socket
   * Promise is returned in order to have possibility
   * to check if other requests may be sent
   * @returns Observable<ISocketConnection>
   */
  reconnect(): Observable<ISocketConnection> {
    // resolve with current connection if it's connected
    if (this.isConnected()) {
      return observableOf(this.connection);
    }
    // if all reconnect attempts failed init new connection
    if (!this.reconnect$ || this.reconnect$.isStopped) {
      if (this.connection) {
        this.connection.close();
      }
      return this.connect();
    }
    return this.reconnect$;
  }
  /**
   * Adds listener handler for given event.
   * @param {string} event
   * @param {Function} handler
   */
  addEventListener(event: string, handler: Function): void {
    if (this.connection) {
      this.connection.on(event, handler);
    }
  }
  /**
   * Adds listener handler for given event.
   * @param {string} event
   * @param {Function} handler
   */
  addOnceEventListener(event: string, handler: Function): void {
    if (this.connection) {
      this.connection.once(event, handler);
    }
  }
  /**
   * Removes listener handler for given event.
   * @param {string} event
   * @param {Function} handler
   */
  removeEventListener(event: string, handler: Function | Function[]): void {
    if (this.connection) {
      if (Array.isArray(handler)) {
        handler.forEach((fn: Function) => {
          this.connection.off(event, fn);
        });
      } else {
        this.connection.off(event, handler);
      }
    }
  }
  /**
   * Emits an event with variable data.
   * @param {string} event
   * @param {*} data
   */
  emit(event: string, data: any): Observable<any> {
    const result = new Subject();
    if (this.isConnected()) {
      this.connection.emit(event, data);
      result.next(true);
      result.complete();
    } else {
      this.connect().subscribe(() => {
          this.connection.emit(event, data);
          result.next(true);
          result.complete();
        });
    }
    return result;
  }
  /**
   * Disconnects the socket manually.
   */
  disconnect(): void {
    if (this.connection) {
      this.connection.close();
      this.isConnecting = false;
      this.connect$ = null;
      this.reconnect$ = null;
    }
  }
  /**
   * Adds global handler for all WS messages.
   * @param {Function} handler
   */
  addAnyMessagesHandler(handler: Function): void {
    this.anyMessageHandler = handler;
  }
  /**
   * Updates options for WS connection.
   * @param {Object} options
   */
  updateOptions(options: IConstant): void {
    this.options = _.extend(this.options, options);
  }
  /**
   * Removes option by given key in WS connection parameters.
   * @param {string} key
   */
  removeOption(key: string): void {
    delete this.options[key];
  }
  /**
   * Checks if connection to web socket is established
   * @returns {boolean}
   */
  isConnected(): boolean {
    return !!(this.connection && this.connection.connected);
  }
  /**
   * Handler for event fired upon a connection including a successful reconnection.
   * @private
   */
  private onConnect(): void {
    this.state$.next('connect');
    this.isConnecting = false;
    this.connect$.next(this.connection);
    this.connect$.complete();
    if (this.reconnect$ && !this.reconnect$.isStopped) {
      this.reconnect$.next(this.connection);
      this.reconnect$.complete();
    }
    if (this.moduleName) {
      this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_CONNECT_SUCCESS}`);
    }
  }
  /**
   * Handler for event fired upon a connection error.
   * @private
   */
  private onConnectError(error: any): void {
    this.state$.next('connect_error');
    console.warn(`${this.moduleName} ${error}`);
    this.isConnecting = false;
    if (this.connect$ && !this.connect$.isStopped) {
      this.connect$.error(error);
    }
    if (this.moduleName) {
      this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_CONNECT_ERROR}`);
    }
  }
  /**
   * Handler for event fired upon a successful reconnection.
   * @private
   */
  private onReconnect(): void {
    this.state$.next('reconnect');
    if (!this.connect$ || this.connect$.isStopped) {
      this.connect$ = new Subject();
    }
    if (this.isConnected() && this.reconnect$ && !this.reconnect$.isStopped) {
      this.reconnect$.next(this.connection);
      this.reconnect$.complete();
    }
    if (this.moduleName) {
      this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_RECONNECT_SUCCESS}`);
    }
  }
  /**
   * Handler for event fired upon an attempt to reconnect.
   * @private
   */
  private onReconnectAttempt(): void {
    this.state$.next('reconnect_attempt');
    if (this.moduleName) {
      this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_RECONNECT_ATTEMPT}`);
    }
  }
  /**
   * Handler for event fired when couldn't reconnect within reconnectionAttempts.
   * @private
   */
  private onReconnectFailed(): void {
    this.state$.next('reconnect_failed');
    this.isConnecting = false;
    if (this.reconnect$ && !this.reconnect$.isStopped) {
      this.reconnect$.error('reconnect failed');
    }
    if (this.moduleName) {
      this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`);
    }
  }
  /**
   * Handler for event fired upon a disconnection.
   * @private
   */
  private onDisconnect(error): void {
    console.warn(`${this.moduleName} ${error}`);
    this.state$.next('disconnect');
    this.isConnecting = false;
    if (!this.reconnect$ || this.reconnect$.isStopped) {
      this.reconnect$ = new Subject();
    }
    if (this.moduleName) {
      this.pubsub.publish(`${this.moduleName}.${EVENTS.SOCKET_DISCONNECT}`);
    }
  }
  /**
   * Register socket handlers
   * @private
   */
  private addCallbacks(): void {
    this.connection.on('connect', this.onConnect.bind(this));
    this.connection.on('connect_error', this.onConnectError.bind(this));
    this.connection.on('reconnect', this.onReconnect.bind(this));
    this.connection.on('reconnect_attempt', this.onReconnectAttempt.bind(this));
    this.connection.on('reconnect_failed', this.onReconnectFailed.bind(this));
    this.connection.on('disconnect', this.onDisconnect.bind(this));
  }
  /**
   * As socket.io doesnt have posibility to subscribe to all messages
   * we decorate socket.io "onevent" function to listen all websockets events
   * @private
   */
  private decorateEventIncomeMessage() {
    if (_.isFunction(this.anyMessageHandler)) {
      const context = this;
      this.connection.on('connect', () => {
        this.connection.onevent = (function (fn) {
          return function (message) {
            const {data = []} = message || {};
            context.anyMessageHandler(...data);
            // eslint-disable-next-line prefer-rest-params
            return fn.apply(this, arguments);
          };
        })(this.connection.onevent);
      });
    }
  }
}
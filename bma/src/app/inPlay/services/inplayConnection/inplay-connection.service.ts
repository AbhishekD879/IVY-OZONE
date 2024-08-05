import { Injectable } from '@angular/core';
import { WsConnectorService } from '@core/services/wsConnector/ws-connector.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { inplayConfig } from '@app/inPlay/constants/config';
import { IInplayConnectionState } from '@app/inPlay/models/connection.model';
import { IWSLiveUpdate } from '@app/inPlay/models/liveUpdates/live-updates.model';
import { WsConnector } from '@core/services/wsConnector/ws-connector';
import { EVENTS } from '@core/constants/websocket-events.constant';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';
import { Observable, of, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable({
  providedIn: InplayApiModule
})
export class InplayConnectionService {
  connection: WsConnector = null;
  /**
   * timeout to revent multiple quick ws reconnection during navigating site
   * @type {number}
   */
  websocketDisconnectionTimeout: number = 5000;

  /**
   * timeout to disconnect ws connection after all connected components are destroyed
   * @type {TimeoutId|null}
   */
  disconnectComponentTimeout: number = null;

  // TODO refactor this old logic to use wsConnector connection state
  status: IInplayConnectionState = {
    reconnectFailed: false
  };

  constructor(
    private wsConnectorService: WsConnectorService,
    private pubSubService: PubSubService,
    private windowRef: WindowRefService,
    private awsService: AWSFirehoseService
  ) {
    this.listenForAllWebsocketMessages = this.listenForAllWebsocketMessages.bind(this);
  }

  setConnectionErrorState(state) {
    this.status = {
      reconnectFailed : state
    };
  }

  /**
   * Add websockets events listeners
   */
  addWsEventsListeners(): void {
    this.pubSubService.subscribe('inplayService', `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_ERROR}`, () => {
      this.setConnectionErrorState(true);
    });

    this.pubSubService.subscribe('inplayService', `${inplayConfig.moduleName}.${EVENTS.SOCKET_RECONNECT_SUCCESS}`, () => {
      this.setConnectionErrorState(false);

      this.pubSubService.publish(this.pubSubService.API.RELOAD_IN_PLAY);
    });

    this.pubSubService.subscribe('inplayService', this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.disconnectSocket();
      this.createConnection();

      this.startConnection().subscribe(() => {
        this.setConnectionErrorState(false);
        this.pubSubService.publish(this.pubSubService.API.RELOAD_IN_PLAY);
      });
    });
  }

  /**
   * Component ws connection handler
   */
  connectComponent(): Observable<WsConnector> {
    // connect once for multiple component instances on page
    if (!this.connection) {
      this.createConnection();
    } else if (this.disconnectComponentTimeout) {
      clearTimeout(this.disconnectComponentTimeout);
      this.disconnectComponentTimeout = null;
    }

    if (this.connection.isConnected()) {
      return of(this.connection);
    }

    return this.startConnection();
  }

  /**
   * Component disconnection handler.
   * called when component being destroyed
   */
  disconnectComponent(): void {
    if (!this.disconnectComponentTimeout) {
      // plan to disconnect websockets, when the last connected module destroyed
      this.disconnectComponentTimeout = this.windowRef.nativeWindow.setTimeout(() => {
        this.disconnectSocket();
      }, this.websocketDisconnectionTimeout);
    }
  }

  createConnection() {
    this.connection = this.wsConnectorService.create(environment.INPLAYMS, {
      timeout: 10000,
      reconnectionAttempts: 15,
      reconnectionDelay: 1000
    }, inplayConfig.moduleName);

    this.connection.state$.subscribe((state: string) => {
      if (state === 'connect') {
        this.awsService.addAction(this.awsService.API.INPLAY_WS_CONNECTION_SUCCESS);
      }
    });

    this.connection.addAnyMessagesHandler(this.listenForAllWebsocketMessages.bind(this));
  }

  addAwsEventListeners(): void {
    const connection = this.connection && this.connection.connection;
    if (!connection) { return; }

    connection.on('connect_error', error => {
      this.awsService.addAction(this.awsService.API.INPLAY_WS_CONNECTION_FAILED, {
        error
      });
    });
    connection.on('reconnect', (attemp: number) => {
      this.awsService.addAction(this.awsService.API.INPLAY_WS_RECONNECTION_SUCCESS, {
        attemp
      });
    });
    connection.on('reconnect_failed', () => {
      this.awsService.addAction(this.awsService.API.INPLAY_WS_RECONNECTION_FAILED);
    });
    connection.on('reconnect_attempt', (attemp: number) => {
      this.awsService.addAction(this.awsService.API.INPLAY_WS_RECONNECTION_ATTEMP, {
        attemp
      });
    });
    connection.on('INPLAY_STRUCTURE', (structure) => {
      this.awsService.addAction(this.awsService.API.INPLAY_WS_STRUCTURE_RECEIVED, {
        payloadSize: JSON.stringify(structure).length
      });
    });
  }

  /**
   * Start in play WS connection.
   */
  startConnection(): Observable<WsConnector> {
    this.setConnectionErrorState(false);

    if (this.connection.isConnected()) {
      return of(this.connection);
    }

    return this.connection.connect()
      .pipe(map(() => {
        this.addAwsEventListeners();
        this.addWsEventsListeners();
        return this.connection;
      }), catchError((error) => {
        this.awsService.addAction(this.awsService.API.INPLAY_WS_CONNECTION_FAILED, {
          error
        });
        this.addWsEventsListeners();
        return throwError(error);
      }));
  }

  /**
   * Listen for all events to handle live event updates. Possible event types:
   */
  listenForAllWebsocketMessages(updatedItemId: number, messageBody: IWSLiveUpdate): void {
    const isLiveUpdateMessage = !isNaN(updatedItemId);

    if (isLiveUpdateMessage) {
      this.pubSubService.publish(this.pubSubService.API.WS_EVENT_LIVE_UPDATE, [updatedItemId, messageBody]);
    }
  }

  /**
   * Ws disconnect
   * remove all listeners for all data messsages.
   */
  disconnectSocket(): void {
    if (this.connection) {
      this.connection.disconnect();
      this.connection = null;
      this.disconnectComponentTimeout = null;
    }
  }

  /**
   * Register a new handler for the given event.
   *
   * @param {string} eventName
   * @param {Function} callBack
   * @param {boolean} bindOnceFlag
   */
  addEventListener(eventName: string, callBack: Function, bindOnceFlag?: boolean) {
    if (!this.connection) {
      this.createConnection();
    }

    this.startConnection().subscribe(() => {
      if (bindOnceFlag) {
        this.connection.addOnceEventListener(eventName, callBack);
      } else {
        this.connection.addEventListener(eventName, callBack);
      }
    }, () => {
      console.warn(`in play app, addEventListener (${eventName}) - failed`);
    });
  }

  removeEventListener(eventName: string, handler?: Function | Function[]): void {
    this.connection.removeEventListener(eventName, handler);
  }

  /**
   * Emits an event to the socket identified by the string name.
   * All serializable data structure are supported.
   *
   * @param {string} eventEmit - ws eventName
   * @param {any} data - any WS Data.
   */
  emitSocket(eventEmit: string, data: any): void {
    if (this.connection) {
      this.connection.emit(eventEmit, data);
    }
  }
}

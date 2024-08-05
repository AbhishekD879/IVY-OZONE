import { Injectable } from '@angular/core';
import { WsConnectorService } from '@core/services/wsConnector/ws-connector.service';
import { WsConnector } from '@core/services/wsConnector/ws-connector';
import { Observable, of, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { catchError, map } from 'rxjs/operators';
import { timelineConfig } from '@lazy-modules/timeline/constants/timeline.constant';
import { IConstant } from '@core/services/models/constant.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable()
export class TimelineService {
  socket: WsConnector = null;

  constructor(
    private wsConnectorService: WsConnectorService,
    private awsService: AWSFirehoseService,
    private gtmService: GtmService
  ) {
  }

  /**
   * create web socket
   */
  createSocket(): Observable<WsConnector> {
    if (!this.socket) {
      this.socket = this.wsConnectorService.create(
        environment.TIMELINE_MS, {
          path: '/socket.io',
          timeout: 10000,
          reconnectionAttempts: 5,
          reconnectionDelay: 1000
        }, timelineConfig.moduleName);
    }

    return of(this.socket);
  }

  /**
   * Component disconnection handler.
   * called when component being destroyed
   */
  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  /**
   * Start in play WS connection.
   */
  connect(): Observable<WsConnector> {
    return this.socket.connect()
      .pipe(map(() => {
        this.addAwsEventListeners();
        return this.socket;
      }), catchError((error) => {
        this.awsService.addAction(this.awsService.API.TIMELINE_WS_CONNECTION_FAILED, {
          error
        });
        return throwError(error);
      }));
  }

  reconnect(): void {
    this.disconnect();
    this.createSocket();
    this.connect();
  }

  /**
   * Add event listener to connection
   * @param {String} event
   * @param {Function} cb
   */
  addListener(eventName: string, callBack: Function): void {
    this.socket && this.socket.addEventListener(eventName, callBack);
  }

  /**
   * Remove listener for event
   * @param eventName - event name
   * @param handler - event handler function
   */
  removeListener(eventName: string, handler?: Function | Function[]): void {
    this.socket && this.socket.removeEventListener(eventName, handler);
  }

  /**
   * Emits an event to the socket identified by the string name.
   *
   * @param {string} eventEmit - web socket eventName
   * @param {any} data - any WS Data to send
   */
  emit(eventEmit: string, data: any): void {
    this.socket && this.socket.emit(eventEmit, data);
  }

  gtm(eventAction: string, analyticParams: { [key: string]: string }, eventCategory: string): void {
    this.gtmService.push('trackEvent', Object.assign({
      eventAction,
      eventCategory: eventCategory
    }, analyticParams));
  }

  /**
   * Add listeners for AWS Firehose events
   */
  private addAwsEventListeners(): void {
    const connection = this.socket && this.socket.connection;

    if (!connection) {
      return;
    }

    connection.on('connect', () => {
      this.awsService.addAction(this.awsService.API.TIMELINE_WS_CONNECTION_SUCCESS);
    });

    connection.on('connect_error', (error: IConstant) => {
      this.awsService.addAction(this.awsService.API.TIMELINE_WS_CONNECTION_FAILED, {
        error
      });
    });

    connection.on('reconnect', (attemp: number) => {
      this.awsService.addAction(this.awsService.API.TIMELINE_WS_RECONNECTION_SUCCESS, {
        attemp
      });
    });

    connection.on('reconnect_failed', () => {
      this.awsService.addAction(this.awsService.API.TIMELINE_WS_RECONNECTION_FAILED);
    });

    connection.on('reconnect_attempt', (attemp: number) => {
      this.awsService.addAction(this.awsService.API.TIMELINE_WS_RECONNECTION_ATTEMP, {
        attemp
      });
    });
  }
}

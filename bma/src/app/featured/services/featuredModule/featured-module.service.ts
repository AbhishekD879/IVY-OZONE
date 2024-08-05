import { CommentsService } from '@core/services/comments/comments.service';
import { IFeaturedModel } from './../../models/featured.model';
import environment from '@environment/oxygenEnvConfig';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { ISportEvent } from '@core/models/sport-event.model';
import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IConstant } from '@app/core/services/models/constant.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { SegmentEventManagerService } from '@app/lazy-modules/segmentEventManager/service/segment-event-manager.service';
import { UserService } from '@app/core/services/user/user.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { IOutputModule } from '../../models/output-module.model';
import { WebSocketService } from '@core/services/wsConnector/websocket.service';
import { SOCKETCODES } from '@core/constants/websocket-events.constant';


@Injectable({
  providedIn: 'root'
})
export class FeaturedModuleService {
  private readonly moduleStates: Map<string, boolean>;
  private subscribedFeaturedTabModules: string[];
  private currentSport: number;
  private currentPageType: string;
  socket;
  constructor(
    private cacheEventsService: CacheEventsService,
    private commentsService: CommentsService,
    private timeSyncService: TimeSyncService,
    private liveEventClockProviderService: LiveEventClockProviderService,
    private pubSubService: PubSubService,
    private awsService: AWSFirehoseService,
    private segmentEventManagerService: SegmentEventManagerService,
    private userService: UserService,
    private device: DeviceService,
    private webSocketService: WebSocketService
  ) {

    this.moduleStates = new Map();
    this.subscribedFeaturedTabModules = [];
    this.segmentedSubscription();
    this.pubSubService.subscribe('featuredModule', this.pubSubService.API.RELOAD_COMPONENTS, () => {
      if (!this.webSocketService.isConnected()) {
        this.reconnect();
      }
    });
  }

  /**
   * Subscription to SEGMENT_RECEIVED
   */
  segmentedSubscription(): void {
    this.pubSubService.subscribe('featuredModule', this.pubSubService.API.SEGMENT_RECEIVED, () => {
      this.segmentReceivedListner();
    });
  }

  get tabModuleStates(): Map<string, boolean> {
    return this.moduleStates;
  }
  set tabModuleStates(value: Map<string, boolean>) { }
  /**
   * Get subscribed modules
   * @returns {Array}
   */
  getSubscribedFeaturedTabModules(): string[] {
    return this.subscribedFeaturedTabModules;
  }

  /**
   * Add module to subscribed modules
   * @param {String} id
   */
  addModuleToSubscribedFeaturedTabModules(id: string): void {
    if (this.subscribedFeaturedTabModules.indexOf(id) === -1) {
      this.subscribedFeaturedTabModules.push(id);
    }
  }

  /**
   * based on SEGMENT_RECEIVED will subscribe to Featured MS to 
   * get the segmented details
   */
  segmentReceivedListner(): void {
    const segment = this.segmentEventManagerService.getSegmentDetails()
    if (this.webSocketService.isConnected() && this.checkForValidEmit(segment)) {
      this.emit('login', segment);
    }
  }

  checkForValidEmit(segment: string): boolean {
    return this.device.requestPlatform === 'mobile'
      && this.userService.username
      && segment
      && this.segmentEventManagerService.chkModuleForSegmentation(false)
  }

  checkEventModuleAndReturnValue(module: IOutputModule) {
    let moduleId = module._id;
    const segment = this.segmentEventManagerService.getSegmentDetails();
    if (segment && this.userService.username && this.device.isMobile && module['@type'] === 'EventsModule') {
      moduleId = moduleId + `#${segment}`;
    }
    return moduleId;
  }

  /**
   * Clear subscribed modules
   */
  clearSubscribedFeaturedTabModules(): void {
    this.subscribedFeaturedTabModules = [];
  }
  /**
   * Reconnect
   */
  reconnect(): void {
    if (this.webSocketService.isConnected()) {
      this.webSocketService.disconnect();
    }
    this.startConnection(this.currentSport, this.currentPageType);
  }

  /**
   * Emit connection event
   * @param {String} event
   * @param {*} data
   */
  emit(event: string, data: string | string[]): void {
    this.webSocketService.sendMessage(`${SOCKETCODES.SOCKET_MESSAGE_EVENT}/${this.currentPageType === 'eventhub'?'h':''}${this.currentSport},` + JSON.stringify([event, data]));
  }
  /**
     * Remove event listener from connection
     * @param {String} event
     * @param {Function} handler
     */
  removeEventListener(event: string, handler: Function): void {
    this.webSocketService.removeEventListener(event, handler);
  }

  /**
   * Remove all connection listeners
   * @param events {Array}
   */
  removeAllListeners(events: string[]): void {
    this.webSocketService.removeAllListeners(events);
  }
  /**
   * Add event listener to connection
   * @param {String} event
   * @param {Function} cb
   */
  addEventListener(event: string, cb: Function): void {
    this.webSocketService.addEventListener(event, cb);
  }
  /**
   * Start MS connection
   * @param sportId - sportId or event hub index
   * @param pageType - 'sport' or 'eventhub'
   */
  startConnection(sportId: number, pageType: string): void {
    this.currentSport = sportId;
    this.currentPageType = pageType;
    this.webSocketService.establishConnection(`${environment.FEATURED_SPORTS}/socket.io/?EIO=3&transport=websocket`);
    this.socketListener();
    this.webSocketService.addEventListener('connect_error', (error: IConstant) => {
      this.awsService.addAction(this.awsService.API.FEATURED_WS_CONNECTION_FAILED, {
        error
      });
    });
    this.webSocketService.addEventListener('error', (error) => this.errorsMessagesHandler(error));
    this.onConnect();
  }

  onConnect(): void {
    this.webSocketService.connection.subscribe(isConnected => {
      if (isConnected) {     
        this.awsService.addAction(this.awsService.API.FEATURED_WS_CONNECTION_SUCCESS);
        this.webSocketService.sendMessage(`${SOCKETCODES.SOCKET_MESSAGE_CONNECT}/${this.currentPageType === 'eventhub'?'h':''}${this.currentSport}`);
        this.pubSubService.publishSync(this.pubSubService.API.FEATURED_CONNECT_STATUS, true);
      }
    });
  }

  disconnect(): void {
    this.webSocketService.disconnect();
  }

  socketListener() {
    return this.webSocketService.socket.subscribe(item => {
      if (item === 'Invalid namespace') {
        this.errorsMessagesHandler(item);
        return;
      }
    },
      err => {
        this.onReconnectionFailed();
      },
      () => {
        //logic after connection complete
      });
  }

  onReconnectionFailed() {
    this.pubSubService.publishSync(this.pubSubService.API.FEATURED_CONNECT_STATUS, false);
    this.awsService.addAction(this.awsService.API.FEATURED_WS_RECONNECTION_FAILED);
  }

  /**
   * Connection error handler
   * @param {Function} cb
   */
  onError(cb: Function): void {
    const connectionErrorHandler = isBooted => {
      if (isBooted) {
        return;
      }
      this.reconnect();
      cb();
    };
    this.addEventListener('error', connectionErrorHandler);
    this.addEventListener('disconnect', connectionErrorHandler);
  }

  /**
   * Handler for microservice error messages
   * @param error
   */
  errorsMessagesHandler(error: string): void {
    if (error === 'Invalid namespace') {
      this.pubSubService.publish(this.pubSubService.API.NAMESPACE_ERROR);
    }
  }

  /**
   * Cache events
   * @param {Object} data
   */
  cacheEvents(data: IFeaturedModel): void {
    if (!data) {
      return;
    }
    this.cacheEventsService.store('ribbonEvents', data);
  }

  /**
   * Add clock data to events
   * @param {Array} events
   * @returns {Array}
   */
  addClock(events: ISportEvent[]): ISportEvent[] {
    const serverTimeDelta = this.timeSyncService.getTimeDelta();

    events.forEach(event => {
      if (!event.comments || !event.comments.latestPeriod) {
        return;
      }

      // TODO move this initialisation to liveClock directive
      const clockInitialData = this.commentsService.getCLockData(_.extend(
        {
          startTime: event.comments.latestPeriod.startTime,
          responseCreationTime: event.responseCreationTime,
          sport: event.categoryCode.toLowerCase(),
          ev_id: event.comments.latestPeriod.eventId,
        },
        event.comments.latestPeriod
      ));

      // ToDo import after migration
      event.clock = this.liveEventClockProviderService.create(
        serverTimeDelta,
        clockInitialData
      );
    });

    return events;
  }

  trackDataReceived(data: IConstant, message: string): void {
    this.awsService.addAction(this.awsService.API.FEATURED_WS_STRUCTURE_RECEIVED, {
      message,
      payloadSize: JSON.stringify(data).length
    });
  }
}


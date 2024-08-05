import { Injectable } from '@angular/core';

import { SubscriptionsManager } from '@core/services/subscriptionsManager/subscriptions-manager';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SubscriptionsManagerService } from '@core/services/subscriptionsManager/subscriptions-manager.service';
import { InplayConnectionService } from '@app/inPlay/services/inplayConnection/inplay-connection.service';
import { InPlayStorageService } from '@inplayModule/services/inplayStorage/in-play-storage.service';

import { inplayConfig } from '@app/inPlay/constants/config';

import { EVENTS } from '@core/constants/websocket-events.constant';
import { SUBSCRIBE_MESSAGES } from '@app/inPlay/constants/messages';

import { IRibbonData, IVirtualRibbonItem } from '@app/inPlay/models/ribbon.model';
import { IStructureCache } from '@app/inPlay/models/structure.model';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';


@Injectable({
  providedIn: InplayApiModule
})
export class InplaySubscriptionManagerService {
  wsEventsHandlers: { [key: string]: Function[] } = {};
  subscriptionsManager: SubscriptionsManager;

  constructor(
    private pubSubService: PubSubService,
    private subscriptionsManagerService: SubscriptionsManagerService,
    private inPlayConnectionService: InplayConnectionService,
    private inPlayStorageService: InPlayStorageService
  ) {
    this.subscriptionsManager = this.subscriptionsManagerService.create();

    this.addEventListeners();
  }

  /**
   * Add websockets events listeners
   * events are triggered in WSConnector
   */
  addEventListeners(): void {
    this.pubSubService.subscribe('inplaySubscription', `${inplayConfig.moduleName}.${EVENTS.SOCKET_DISCONNECT}`,
      () => {
        this.clearAllListeners();
      });
  }

  /**
   * Performs subscription for live updates for given event ids.
   * @param {Array} eventsIds
   */
  subscribeForLiveUpdates(eventsIds: number[]): void {
    const eventsToSubscribe = this.subscriptionsManager.checkForSubscribe(eventsIds);

    if (eventsToSubscribe.length > 0) {
      this.inPlayConnectionService.emitSocket(SUBSCRIBE_MESSAGES.SUBSCRIBE, eventsToSubscribe);
    }
  }

  /**
   * Performs unsubscription for live updates for given event ids.
   * @param {Array} eventsIds
   */
  unsubscribeForLiveUpdates(eventsIds: number[]): void {
    const eventsToUnsubscribe = this.subscriptionsManager.checkForUnsubscribe(eventsIds);

    if (eventsToUnsubscribe.length > 0) {
      this.inPlayConnectionService.emitSocket(SUBSCRIBE_MESSAGES.UNSUBSCRIBE, eventsToUnsubscribe);
    }
  }

  /**
   * subscribes for RibbonUpdates
   * @private
   */
  subscribe4RibbonUpdates(): void {
    const isSubscribedToRibbonUpdates: boolean = this.wsEventsHandlers[SUBSCRIBE_MESSAGES.RIBBON_CHANGE]
      && this.wsEventsHandlers[SUBSCRIBE_MESSAGES.RIBBON_CHANGE].length > 0;
    if (!isSubscribedToRibbonUpdates) {
      this.subscribe(SUBSCRIBE_MESSAGES.RIBBON_CHANGE,
        (data: IRibbonData) => this.inPlayStorageService.onRibbonUpdate(data));
    }
  }


  /**
   * subscribes for virtuals event updates
   * @returns void
   */
  subscribe4VirtualsUpdates(): void {
    this.virtualSportsListener = this.virtualSportsListener.bind(this);
    this.inPlayConnectionService.addEventListener(SUBSCRIBE_MESSAGES.VIRTUALS_RESPONSE_CHANGE, this.virtualSportsListener);
      this.subscribe(SUBSCRIBE_MESSAGES.VIRTUALS_CHANGE,
        (data: IVirtualRibbonItem[]) => this.inPlayStorageService.onVirtualsUpdate(data));
  }

  virtualSportsListener(data: IVirtualRibbonItem[]): void {
    this.inPlayStorageService.onVirtualsUpdate(data);
  }

  subscribeForStructureUpdates(liveStream: boolean = false): void {
    const subscrMsg: string = liveStream ? SUBSCRIBE_MESSAGES.LS_STRUCTURE_CHANGE : SUBSCRIBE_MESSAGES.STRUCTURE_CHANGE;

    this.subscribe(subscrMsg, (structureData: IStructureCache) => this.inPlayStorageService.onStructureUpdate(structureData));
  }

  /**
   * subscription to remove/add competition from sport
   * when the last event undisplayed, or first event added.
   */
  subscribeForSportCompetitionChanges(sportId: string, topLevelType: string, marketSelector: string, callback: Function): void {
    let subscribeMessage = `${SUBSCRIBE_MESSAGES.COMPETITION_CHANGE}::${sportId}::${topLevelType}`;

    if (marketSelector) {
      subscribeMessage = `${subscribeMessage}::${marketSelector}`;
    }

    this.subscribe(subscribeMessage, data => callback(data));
  }

  /**
   * unsubscribe to remove/add competition from sport
   */
  unsubscribeForSportCompetitionChanges(sportId: string, topLevelType: string, marketSelector?: string): void {
    let unsubscribeMessage = `${SUBSCRIBE_MESSAGES.COMPETITION_CHANGE}::${sportId}::${topLevelType}`;

    if (marketSelector) {
      unsubscribeMessage = `${unsubscribeMessage}::${marketSelector}`;
    }

    this.unSubscribe(unsubscribeMessage);
  }

  /**
   * Unsubscribes for RibbonUpdates.
   * @private
   */
  unsubscribe4RibbonUpdates(): void {
    this.unSubscribe(SUBSCRIBE_MESSAGES.RIBBON_CHANGE);
  }

  /**
   * Unsubscribes for structure updates.
   * @private
   */
  unsubscribeForStructureUpdates(): void {
    this.unSubscribe(SUBSCRIBE_MESSAGES.STRUCTURE_CHANGE);
  }

  /**
   * Unsubscribes for VR LiveEvent Updates.
   * @private
   */

  unsubscribe4VRLiveEventUpdates(): void {
    this.unSubscribe(SUBSCRIBE_MESSAGES.VIRTUALS_CHANGE);
  }
  /**
   * Subscribe data from WS related to event.
   * Callback will be called (each time) as soon as the data coming from the server.
   * Callback approach.
   *
   * @param eventName {string}
   * @param handlerFunction {function}
   */
  subscribe(eventName: string, handlerFunction: Function): void {
    if (this.wsEventsHandlers[eventName] === undefined) {
      this.wsEventsHandlers[eventName] = [];
    }

    this.wsEventsHandlers[eventName].push(handlerFunction);

    this.inPlayConnectionService.addEventListener(eventName, handlerFunction);
    this.inPlayConnectionService.emitSocket(SUBSCRIBE_MESSAGES.SUBSCRIBE, eventName);
  }

  /**
   * UnSubscribe data from WS related to event.
   * @param eventName {string}
   */
  unSubscribe(eventName: string): void {
    if (this.wsEventsHandlers[eventName]) {
      this.inPlayConnectionService.removeEventListener(eventName, this.wsEventsHandlers[eventName]);
      this.inPlayConnectionService.emitSocket(SUBSCRIBE_MESSAGES.UNSUBSCRIBE, eventName);

      delete this.wsEventsHandlers[eventName];
    }
  }

  /**
   * Ws disconnect
   * remove all listeners for all data messsages.
   */
  clearAllListeners(): void {
    this.wsEventsHandlers = {};
  }
}

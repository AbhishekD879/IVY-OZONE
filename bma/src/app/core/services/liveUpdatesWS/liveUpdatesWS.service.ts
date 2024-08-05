import { Injectable } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { ILiveUpdate } from '@core/models/private-markets.model';

interface IChannelsMap {
  [key: string]: string[];
}

@Injectable()
export class LiveUpdatesWSService {
  private subscribersMap: IChannelsMap = {};  // Current active subscriptions
  private subscribeMapQueue: IChannelsMap = {};
  private unsubscribeMapQueue: IChannelsMap = {};

  constructor(
    private pubSubService: PubSubService,
    private liveServConnectionService: LiveServConnectionService
  ) {
    this.liveServeUpdateHandler = this.liveServeUpdateHandler.bind(this);
    this.connectHandler = this.connectHandler.bind(this);
    this.disconnectHandler = this.disconnectHandler.bind(this);
  }

  /**
   * Add items to Subscription queue and fetch updates to LS
   */
  subscribe(channelsArray: Array<string>, moduleName?: string): string {
    const channelsId = moduleName || `${channelsArray.toString()}-${Date.now()}`;
    this.subscribeMapQueue[channelsId] = channelsArray;
    this.fetchSubscriptions();
    return channelsId;
  }

  /**
   * Add items to Unsubscription queue (also remove from Subscription queue) and fetch updates to LS
   */
  unsubscribe(channelsId: string): void {
    delete this.subscribeMapQueue[channelsId]; // to avoid unnecessary subscription if it is still in pending queue
    if (this.subscribersMap[channelsId]) {
      this.unsubscribeMapQueue[channelsId] = this.subscribersMap[channelsId];
      this.fetchSubscriptions();
    }
  }

  /**
   * Execute update actions as soon as proper connection to LS is available
   */
  private fetchSubscriptions(): void {
    this.liveServConnectionService.connect().subscribe(this.connectHandler);
  }

  /**
   * Update subscriptions based on current queues state, replace previous assignment of disconnect handler
   */
  private connectHandler(): void {
    this.updateSubscriptions();
    this.liveServConnectionService.onDisconnect(this.disconnectHandler);
  }

  /**
   * Unsubscribe/subscribe updates for channels stored in queues.
   */
  private updateSubscriptions(): void {
    const unsubscribeChannelsList = this.getChannelsList(this.unsubscribeMapQueue);
    if (unsubscribeChannelsList.length) {
      Object.keys(this.unsubscribeMapQueue).forEach((key: string) => delete this.subscribersMap[key]);
      this.unsubscribeMapQueue = {};
      this.liveServConnectionService.unsubscribe(unsubscribeChannelsList, this.liveServeUpdateHandler);
    }

    const subscribeChannelsList = this.getChannelsList(this.subscribeMapQueue);
    if (subscribeChannelsList.length) {
      Object.keys(this.subscribeMapQueue).forEach((key: string) => this.subscribersMap[key] = this.subscribeMapQueue[key]);
      this.subscribeMapQueue = {};
      this.liveServConnectionService.subscribe(subscribeChannelsList, this.liveServeUpdateHandler);
    }
  }

  /**
   * Extract channel ids from ChannelsMap
   */
  private getChannelsList(map: IChannelsMap): string[] {
    return Object.keys(map).reduce((arr, key) => arr.concat(map[key]), []);
  }

  /**
   * Handler for live serve updates
   * @param {Object} update
   * @private
   */
  private liveServeUpdateHandler(update: ILiveUpdate): void {
    if (update.type === 'MESSAGE') {
      const payload = update.message,
        channel = update.channel.name,
        updatedObject = { channel,
          channel_number: update.event.id,
          payload,
          subject_number: update.subChannel.id,
          subject_type: update.subChannel.type
        };

      this.pubSubService.publish(this.pubSubService.API.LIVE_SERVE_MS_UPDATE, [updatedObject]);
    }
  }

  /**
   * Handle server disconnect and then reestablish connection with complete re(un)subscribing
   */
  private disconnectHandler(error: string): void {
    if (this.liveServConnectionService.isDisconnected(error)) {
      this.unsubscribeMapQueue = {...this.subscribersMap};
      this.subscribeMapQueue = {...this.subscribersMap};
      this.fetchSubscriptions();
    }
  }
}

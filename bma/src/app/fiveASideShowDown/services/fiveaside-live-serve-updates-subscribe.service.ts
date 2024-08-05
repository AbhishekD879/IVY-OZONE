import { Injectable } from '@angular/core';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { HandleLiveServeUpdatesService } from '@app/core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { ChannelService } from '@app/core/services/liveServ/channel.service';
import { IShowdownLobbyContest } from '@app/fiveASideShowDown/models/showdown-lobby-contest.model';
import { IShowdownCard } from '@app/fiveASideShowDown/models/showdown-card.model';
import { LIVE_SERV_CHANNELS, PUBSUB_API, SHOWDOWN_CHANNELS, SHOWDOWN_LS_CHANNELS } from '@app/fiveASideShowDown/constants/constants';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { FiveASideLiveServeHandlerService } from '@app/fiveASideShowDown/services/fiveaside-liveserve-handler';

/**
 * Service to handle LiveServe connections, channels and update handler
 */
@Injectable({
  providedIn: FiveASideShowDownApiModule
})
export class FiveAsideLiveServeUpdatesSubscribeService {
  eventIds;
  channels: string[] = [];
  channelsList: string[] = [];
  constructor(
    private channelService: ChannelService,
    private pubsubService: PubSubService,
    private showDownLiveServeHandleUpdatesService: HandleLiveServeUpdatesService,
    private handledShowDownService: FiveASideLiveServeHandlerService
  ) { }

  /**
   * Open LiveServe connection by passing channels list
   * @param  {string[]=[]} channels
   * @returns void
   */
  openLiveServeConnectionForUpdates(channels: string[]): void {
    channels.forEach((channel: string) => {
      this.channelsList.push(channel);
    });
    this.showDownLiveServeHandleUpdatesService
      .subscribe(channels, this.liveServeShowdownUpdatesListener.bind(this), true);
  }

  /**
   * My Entry Iniital Data
   * @param  {string} userId
   * @param  {string} contestId
   * @returns {void}
   */
  openLiveServeInitialDataEntryInformation(channel: string, handler: Function, emitKey: string): void {
    this.handledShowDownService
      .showDownSubscribe(channel, handler, emitKey);
  }

  /**
   * Initial Legs
   * @param  {string} entryId
   * @returns {void}
   */
  getInitialLegs(channel: string, handler: Function, emitKey: string): void {
    this.handledShowDownService.showDownSubscribe(channel, handler, emitKey);
  }
  /**
   * @param  {Array<string>} outcomeIds
   * @param  {Function} handler
   * @returns {void}
   */
  legsUpdateSubscribe(outcomeIds: Array<string>, handler: Function): void {
    this.handledShowDownService.addEventListner(outcomeIds, handler);
  }
  /**
   * User Entry Updates
   * @param  {string} channel
   * @param  {Function} handler
   * @param  {string} emitKey
   * @returns {void}
   */
  userEntryUpdates(channel: string, handler: Function, emitKey: string): void {
    this.handledShowDownService.showDownSubscribe(channel, handler, emitKey);
  }
  /**
   * Un Subscription for ShowDown Channels
   * @param  {string[]=[]} channels
   * @param  {Function} handler
   * @returns {void}
   */
  unSubscribeShowDownChannels(channels: string[], handler: Function): void {
    this.handledShowDownService.unsubscribe(channels, handler);
  }
  /**
   * RemoveAllEvent Listners
   * @param  {string[]=[]} channels
   * @returns {void}
   */
  removeAllEventListneres(channels: string[]): void {
    this.handledShowDownService.removeEventAllListner(channels);
  }
  /**
   * Add Event Listners
   * @param  {string[]=[]} channels
   * @param  {Function} handle
   * @returns {void}
   */
  addEventListneres(channels: string[], handle: Function): void {
    this.handledShowDownService.addEventListner(channels, handle);
  }
  /**
   * Unsubscribing channels from LiveServe connection
   * @param  {string[]=[]} channels
   * @returns void
   */
  unSubscribeLiveServeConnection(channels: string[]): void {
    const filteredChannels: string[] = [];
    channels.forEach((item: string) => {
      const duplicateChannels = this.channelsList.filter(channel => channel === item);
      this.channelsList = this.channelsList.filter((channel) => channel !== item);
      filteredChannels.push(...duplicateChannels);
    });
    this.showDownLiveServeHandleUpdatesService
      .unsubscribe(filteredChannels);
  }

  /**
   * Listens to the updates of subscribed LiveServe channels
   * @param  {{payload} update
   * @param  {} type
   * @param  {} id}
   * @returns void
   */
  liveServeShowdownUpdatesListener(update: { payload, type, id }): void {
    const channelType = update.type;
    switch (channelType) {
      case SHOWDOWN_CHANNELS.CLOCK:
        this.pubsubService.publish(PUBSUB_API.SHOWDOWN_LIVE_CLOCK_UPDATE, update);
        break;
      case SHOWDOWN_CHANNELS.SCORE:
        this.pubsubService.publish(PUBSUB_API.SHOWDOWN_LIVE_SCORE_UPDATE, update);
        break;
      case SHOWDOWN_CHANNELS.EVENT:
        this.pubsubService.publish(PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE, update);
        this.publishEventStarted(update);
        break;
      case LIVE_SERV_CHANNELS.MARKET:
        this.publishEventStarted(update);
        break;
      default:
        break;
    }
  }

  /**
   * Returns list of channels from contests
   * @param  {IShowdownLobbyContest[]} contests
   * @returns Array
   */
  createLiveServeChannels(contests: IShowdownLobbyContest[]): Array<string> {
    const channelsList: string[] = [];
    const eventIds = this.getEventIdsToBeSubscribed(contests);
    if (eventIds.length) {
      channelsList.push(
        ...this.getChannels(eventIds, SHOWDOWN_LS_CHANNELS.CLOCK),
        ...this.getChannels(eventIds, SHOWDOWN_LS_CHANNELS.SCORE),
        ...this.getChannels(eventIds, SHOWDOWN_LS_CHANNELS.EVENT)
      );
    }
    return channelsList;
  }


  /**
   * create channels for events
   * @param  {string[]} events
   * @returns string
   */
  createChannels(events: string[]): string[] {
    this.channels = [
      ...this.getChannels(events, SHOWDOWN_LS_CHANNELS.EVENT),
      ...this.getChannels(events, SHOWDOWN_LS_CHANNELS.SCORE),
      ...this.getChannels(events, SHOWDOWN_LS_CHANNELS.CLOCK),
    ];
    return this.channels;
  }

  /**
   * Publish event started message by PubSub
   * @param  {{payload} update
   * @param  {} type
   * @param  {} id}
   * @returns void
   */
  private publishEventStarted(update: { payload, type, id }): void {
    if (update && update.payload && update.payload.started) {
      this.pubsubService.publish(PUBSUB_API.SHOWDOWN_EVENT_STARTED, update.id.toString());
    }
  }

  /**
   * Return channel names list based on event ids and type
   * @param  {string[]} arrayIds
   * @param  {string} type
   * @returns string[]
   */
  private getChannels(arrayIds: string[], type: string): string[] {
    return arrayIds.map((id: string) => {
      return `${type}${id}`;
    });
  }

  /**
   * Return Event Ids to be subscribed by passsng contests
   * @param  {IShowdownLobbyContest[]} contests
   * @returns string[]
   */
  private getEventIdsToBeSubscribed(contests: IShowdownLobbyContest[]): string[] {
    const eventIds: string[] = [];
    if (contests) {
      contests.forEach((category: IShowdownLobbyContest) => {
        eventIds.push(...this.filterOnlyLiveEvents(category.contests));
      });
    }
    return eventIds;
  }

  /**
   * Return list of event ids by passing contests
   * @param  {IShowdownCard[]} contests
   * @returns string[]
   */
  private filterOnlyLiveEvents(contests: IShowdownCard[]): string[] {
    return contests.filter((contest: IShowdownCard) => {
      if (contest && contest.eventDetails && contest.showRoleContest) {
        const event = contest.eventDetails;
        if (event && !event.regularTimeFinished) {
          return event.id;
        }
      }
    }).map((contest: IShowdownCard) => {
      const event = contest.eventDetails;
      return event.id.toString();
    });
  }
}

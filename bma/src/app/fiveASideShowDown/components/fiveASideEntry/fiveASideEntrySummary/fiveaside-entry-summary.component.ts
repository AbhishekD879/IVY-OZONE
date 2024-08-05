import { Component, Input, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { IEntrySummaryInfo, IOutCome } from '@app/fiveASideShowDown/models/entry-information';
import {
  ENTRYINFO,
  GTM_EVENTS,
  LIVESERVELISTNERS,
  PUBSUB_API
} from '@app/fiveASideShowDown/constants/constants';
import { FiveAsideLiveServeUpdatesSubscribeService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { UserService } from '@app/core/services/user/user.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';

@Component({
  selector: 'fiveaside-entry-summary',
  template: ``
})
export class FiveASideEntrySummaryComponent implements OnInit, OnDestroy {
  public origin: string = ENTRYINFO.SUMMARY;
  public channel: string;
  public emitKey: string = 'entrylegsinfo';
  public listeners = LIVESERVELISTNERS;
  public unsubscribechannel: Array<string>;
  componentId: string;
  legDetails: Array<IOutCome>;
  readonly MAX_LIMIT = 9999;
  outcomeIds: Array<string> = [];
  @Input() entryInfo: IEntrySummaryInfo;
  @Input() eventEntity: ISportEvent;
  @Input() index: number;
  @Input() entryIdList?: string[];
  isActiveUser: boolean = false;
  @Input() isOverlay: boolean = false;
  @Input() eventStatus?: string = 'live';
  @Input() prizePoolData: IEntrySummaryInfo;
  @Input() isLeaderboard: boolean;
  @Input() isTopEntry: boolean = false;
  @Input() teamColors: ITeamColor[];
  readonly MAXVALUE = 100.0;
  @Input() hasTeamImage: boolean;
  constructor(protected fiveAsideLiveServeUpdatesSubscribeService: FiveAsideLiveServeUpdatesSubscribeService,
    protected pubSubService: PubSubService,
    protected coreToolsService: CoreToolsService, protected changeDetectorRef: ChangeDetectorRef,
    protected fiveasideLeaderBoardService: FiveasideLeaderBoardService,
    protected gtmService: GtmService, public userService: UserService) { }

  ngOnDestroy(): void {
    if (this.eventStatus === 'live') {
      this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.legsInitialHandlers);
    }
    this.pubSubService.unsubscribe(this.componentId);
    this.legDetails = [];
    this.outcomeIds = [];
    this.entryInfo.isOverlayOpend = false;
    this.entryInfo.isOpened = false;
  }

  /**
   * To mask user name with *** at the end
   * @param entry {string}
   * @returns
   */
  getuserNameMask(userId: string): string {
    if (userId && userId.length >= 8) {
      return `${userId.slice(0, 5)}***`;
    } else {
      return userId ? `${userId.slice(0, -3)}***` : '';
    }
  }

  ngOnInit() {
    this.componentId = this.coreToolsService.uuid();
    this.pubSubService.subscribe(this.componentId, PUBSUB_API.PUBLISH_LEADERBOARD, this.checkActiveUser.bind(this));
    this.checkActiveUser();
    this.pubSubService.subscribe(this.componentId,
      PUBSUB_API.CLOSE_EVERY_ENTRY_DETAILS, this.closeAllEntryDetails.bind(this));
    if (!this.isOverlay) {
      this.pubSubService.subscribe(this.componentId, PUBSUB_API.CLOSE_ALL_ENTRIES, this.openCloseHandler.bind(this));
    } else {
      this.pubSubService.subscribe(this.componentId,
        PUBSUB_API.CLOSE_ALL_ENTRIES_OVERLAY, this.openCloseHandleOverlay.bind(this));
    }
    if (this.eventStatus === 'live' && !this.isLeaderboard) {
      this.myEntryUpdate();
    }
  }
  /**
   * @param  {{componentId:string} entryInfo
   * @param  {string} entryId
   * @param  {boolean}} auto?
   * @returns void
   */
  openCloseHandleOverlay(entryInfo: { componentId: string, entryId: string, auto?: boolean }): void {
    this.channel = `${this.listeners.ENTRYINFO}::${this.entryInfo.id}`;
    if (entryInfo.entryId === this.entryInfo.id && entryInfo.componentId === this.componentId) {
      if ((entryInfo.auto && this.index === 0) || !entryInfo.auto) { 
        this.entryInfo.isOverlayOpend = !this.entryInfo.isOverlayOpend;
       }
      if (!this.entryInfo.isOverlayOpend) {
        this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.legsInitialHandlers);
      } else {
        this.fiveAsideLiveServeUpdatesSubscribeService.getInitialLegs(this.channel, this.legsInitialHandlers.bind(this), this.emitKey);
        this.entryOpenCloseTrack();
      }
    } else {
      this.entryInfo.isOverlayOpend = false;
      this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.legsInitialHandlers);
    }
  }

  /**
   * @param  {{componentId:string} entryInfo
   * @param  {string} entryId
   * @param  {boolean}} auto?
   * @returns void
   */
  openCloseHandler(entryInfo: { componentId: string, entryId: string, auto?: boolean }): void {
    this.channel = `${this.listeners.ENTRYINFO}::${this.entryInfo.id}`;
    if (this.eventStatus === 'live') {
      if (entryInfo.entryId === this.entryInfo.id && entryInfo.componentId === this.componentId) {
        if (!this.isLeaderboard && !this.entryInfo.isOpened) {
          this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.legsInitialHandlers.bind(this));
        }
        if (!entryInfo.auto) { this.entryInfo.isOpened = !this.entryInfo.isOpened; }
        if (!this.entryInfo.isOpened) {
          this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.legsInitialHandlers.bind(this));
        } else {
          this.fiveAsideLiveServeUpdatesSubscribeService.getInitialLegs(this.channel, this.legsInitialHandlers.bind(this), this.emitKey);
          this.entryOpenCloseTrack();
        }
      }
    } else {
      if (entryInfo.entryId === this.entryInfo.id && entryInfo.componentId === this.componentId) {
        this.entryInfo.isOpened = !this.entryInfo.isOpened;
      } else {
        this.entryInfo.isOpened = false;
      }
    }
  }
  /**
   * @returns void
   */
  myEntryUpdate(): void {
    const myEntryindex = this.index;
    this.pubSubService.subscribe(this.componentId,
      PUBSUB_API.MY_ENTRY_UPDATE, (myEntries: { update: Array<IEntrySummaryInfo> }) => {
        if((this.entryInfo.isOverlayOpend || this.entryInfo.isOpened) && (this.isOverlay || this.index === 0) && !this.isLeaderboard){
          this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.legsInitialHandlers.bind(this));
          this.entryInfo.isOverlayOpend = false;
          this.entryInfo.isOpened = false;
        }
        myEntries.update.forEach((entry, updateindex) => {
          if (myEntryindex === updateindex) {
            this.handleEntryUpdate(entry, 'isOpened', PUBSUB_API.CLOSE_ALL_ENTRIES);
            this.entryInfo = entry;
            this.prizePoolData = entry;
          }
          this.entryInfo.userEntry = true;
        });
        this.changeDetectorRef.markForCheck();
      });
  }

  /**
   * To Open the leg details of the Bet
   * @param  {number} index
   * @returns void
   */
  public onClick(): void {
    if (!this.isOverlay) {
      this.pubSubService.publish(PUBSUB_API.CLOSE_EVERY_ENTRY_DETAILS, this.componentId);
      this.pubSubService.publish(PUBSUB_API.CLOSE_ALL_ENTRIES, { componentId: this.componentId, entryId: this.entryInfo.id });
    } else {
      this.pubSubService.publish(PUBSUB_API.CLOSE_ALL_ENTRIES_OVERLAY,
        { componentId: this.componentId, entryId: this.entryInfo.id });
    }
  }

  /**
   * get legs infornation for each entry when clicked on the entry on post match leaderboard
   * @returns void
   */
  public postOnClick(): void {
    if (!this.isOverlay) {
      const outcomeIds = this.entryInfo.outcomeIds;
      const outcomeIdsList = outcomeIds.join();
      this.fiveasideLeaderBoardService.getLegsForEntryId(outcomeIdsList).subscribe((response: Array<IOutCome>) => {
        this.legsInitialHandlers(response);
        this.entryInfo.legs = response;
        this.handleEntryUpdate(this.entryInfo, 'isOpened', PUBSUB_API.CLOSE_ALL_ENTRIES);
      });
    }
  }

  /**
   * LegsUpdateHandler
   * @param  {Array<IOutCome>} legs
   * @returns void
   */
  legsInitialHandlers(legs: Array<IOutCome>): void {
    this.legDetails = legs;
    this.changeDetectorRef.detectChanges();
  }
  /**
   * Close All Entrie Details When
   * @returns void
   */
  closeAllEntryDetails(componentId: string): void {
    if (this.entryInfo.isOpened || this.entryInfo.isOverlayOpend) {
      this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels([this.channel], this.legsInitialHandlers);
    }
    
    if (componentId === this.componentId) {
      const isOpened = this.entryInfo.isOpened;
      this.entryInfo.isOpened = isOpened;
    } else {
      this.entryInfo.isOpened = false;
    }
    
    this.entryInfo.isOverlayOpend = false;
  }

  /**
   * To Get Rank class based on the length
   * @returns {string}
   */
   getClass(): string {
    return this.fiveasideLeaderBoardService.getDynamicClass(this.entryInfo.rank as string);
  }

  /**
   * GA Tracking expand collapse actions
   * @returns void
   */
  private entryOpenCloseTrack(): void {
    const trackingObj = {
      eventCategory: GTM_EVENTS.OPENENTRY.category,
      eventAction: GTM_EVENTS.OPENENTRY.action,
      eventLabel: this.isLeaderboard ? ENTRYINFO.MAIN_LEADERBOARD :ENTRYINFO.MY_ENTRIES,
      entryId: this.entryInfo.id
    };
    this.gtmService.push('trackEvent', trackingObj);
  }

  /**
   * Publish CLOSE_ALL message based on entries open/close state
   * @param  {IEntrySummaryInfo} entry
   * @param  {string} state
   * @param  {string} channel
   * @returns void
   */
  private handleEntryUpdate(entry: IEntrySummaryInfo, state: string, channel: string): void {
    if (this.entryInfo[state]) {
      entry[state] = this.entryInfo[state];
      if (entry.previousIndex !== this.entryInfo.currentIndex) {
        this.pubSubService.publish(channel,
          { componentId: this.componentId, entryId: entry.id, auto: true });
        this.pubSubService.publish(PUBSUB_API.OUTCOME_CHANGES,
          { previous: this.entryInfo.outcomeIds, current: entry.outcomeIds });
      }
    }
  }

  /**
   * checkActiveUser used to check for active user entry and check that the event is live.
   * @returns boolean
   */
  private checkActiveUser() {
    try {
      const entryIds = this.entryIdList;
      this.isActiveUser = (this.userService.username === this.entryInfo.userId || entryIds.includes(this.entryInfo.id)) &&
        this.eventStatus === 'live';
    } catch(e) {
      console.warn('Error in check for active user entry and check that the event is live',e);
     }
  }
}

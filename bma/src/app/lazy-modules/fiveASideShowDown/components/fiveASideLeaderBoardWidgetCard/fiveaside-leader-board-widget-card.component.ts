import { Component, Input, OnInit, OnDestroy, ChangeDetectionStrategy,
ChangeDetectorRef } from '@angular/core';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { ILeaderBoardWidget } from '@lazy-modules/fiveASideShowDown/models/leader-board-widget';
import { FiveasideWidgetService } from '@lazy-modules/fiveASideShowDown/services/fiveaside-widget.service';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FiveAsideLiveServeUpdatesService } from '@app/fiveASideShowDown//services/fiveaside-live-serve-updates.service';
import { IEventDetails, IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { IEntrySummaryInfo } from '@app/fiveASideShowDown/models/entry-information';
import { FiveASideEntryInfoService } from '@app/fiveASideShowDown/services/fiveaside-entryInfo-handler.service';
import { UserService } from '@core/services/user/user.service';
import { FiveAsideLiveServeUpdatesSubscribeService
} from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { GTM_EVENTS, LEADERBOARD_WIDGET, LIVE_SERVE_KEY, PRIZE_TYPES, PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { Router } from '@angular/router';
import { FiveasideRulesEntryAreaService
} from '@app/fiveASideShowDown/services/fiveaside-rules-entry-area.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { CmsService } from '@core/services/cms/cms.service';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import environment from '@environment/oxygenEnvConfig';
import { AWSFirehoseService } from '@app/lazy-modules/awsFirehose/service/aws-firehose.service';
import { ILeaderboardData } from '@app/fiveASideShowDown/models/leader-board';
import { IShowdownOptaUpdate } from '@app/fiveASideShowDown/models/IShowdownOptaUpdate.model';

@Component({
  selector: 'fiveaside-leader-board-widget-card',
  template: ``,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveasideLeaderBoardWidgetCardComponent implements OnInit, OnDestroy {
  @Input() widgetData: IShowDown;
  @Input() eventEntity: IEventDetails;
  @Input() leaderBoards: IShowDown[];
  public entryDetails: IEntrySummaryInfo;
  public leaderBoardWidget: ILeaderBoardWidget;
  public teamColors: ITeamColor[] = [];
  public hasTeamImage: boolean;
  public readonly prizeTypes: {[key: string]: string} = PRIZE_TYPES;
  public readonly signPostingLogoUrl: string =
    environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  private subscriber: string;
  private entryChannel: string;
  private entryUpdateChannel: string;
  private readonly WIDGET_COMPONENT = `LeaderBoardWidget`;
  private readonly FOOTBALL_MATCHES_TAB: string = '/sport/football/matches';
  private isComponentDestroyed: boolean = false;
  constructor(private coreToolsService: CoreToolsService,
    private widgetService: FiveasideWidgetService,
    private lobbyService: FiveASideShowDownLobbyService,
    private pubSub: PubSubService,
    private entryService: FiveASideEntryInfoService,
    private liveServeUpdateService: FiveAsideLiveServeUpdatesService,
    private userService: UserService,
    private subscriberService: FiveAsideLiveServeUpdatesSubscribeService,
    private rulesEntryService: FiveasideRulesEntryAreaService,
    private router: Router,
    private cmsService: CmsService,
    private leaderBoardService: FiveasideLeaderBoardService,
    private changeDetectorRef: ChangeDetectorRef,
    private awsService: AWSFirehoseService) { }

  ngOnInit(): void {
    this.leaderBoardWidget = {} as ILeaderBoardWidget;
    if (this.widgetData && this.eventEntity) {
      this.initEntryDetails();
      this.initWidgetDetails();
      this.subscribeForLiveUpdates();
    }
  }

  ngOnDestroy(): void {
    this.isComponentDestroyed = true;
    this.pubSub.unsubscribe(this.subscriber);
    this.subscriberService.unSubscribeShowDownChannels([this.entryUpdateChannel], this.userEntryHandler.bind(this));
  }

  /**
   * Triggered when widget is clicked
   * @returns {void}
   */
  onWidgetClick(): void {
    this.router.navigate([LEADERBOARD_WIDGET.LEADERBOARD_URL, this.widgetData.id]);
    if (this.isMatchesURL()) {
      this.rulesEntryService.trackGTMEvent(GTM_EVENTS.FOOTBALL_WIDGET.category,
        GTM_EVENTS.FOOTBALL_WIDGET.action, GTM_EVENTS.FOOTBALL_WIDGET.label);
    } else {
      this.rulesEntryService.trackGTMEvent(GTM_EVENTS.HOME_WIDGET.category,
        GTM_EVENTS.HOME_WIDGET.action, GTM_EVENTS.HOME_WIDGET.label);
    }
  }

  /**
   * To Set Masked name based on length
   * @param userName {string}
   * @returns {string}
   */
  setMaskedName(userName: string): string {
    if (userName) {
      if (userName.length >= 8) {
        return `${userName.slice(0, 5)}***`;
      } else {
        return `${userName.slice(0, -3)}***`;
      }
    }
    return '';
  }

  /**
   * To Get Rank class based on the length
   * @returns {string}
   */
  getClass(): string {
    return this.leaderBoardService.getDynamicClass(this.entryDetails.rank);
  }

  /**
   * To Get signposting url
   * @param {string} fileName
   * @returns {string}
   */
    getSignpostingUrl(fileName: string): string {
    return `${this.signPostingLogoUrl}${fileName}`;
  }

  /**
  * To limit the decimal length
  * @param {string} value
  * @returns {string}
  */
  public fixedDecimals(value: string): string {
    const decimalValues = value.toString().split('.')[1];
    if (Number(decimalValues) > 0) {
      return Number(value).toFixed(2).toString();
    } else {
      return Math.round(Number(value)).toString();
    }
  }

    /**
    * To verify if it is Matches URL
    * @returns {boolean}
    */
    private isMatchesURL(): boolean {
      const currentURL: string = this.router.url.replace('?q=1', '');
      return currentURL === this.FOOTBALL_MATCHES_TAB;
    }

  /**
   * To Initialize top entry details
   * @returns {void}
   */
  private initEntryDetails(): void {
    this.entryUpdateChannel = `${LIVE_SERVE_KEY.LDRBRD}::${this.widgetData.id}::${this.userService.username ? `${this.userService.username}::${this.userService.bppToken}` : 0}`;
    this.subscriberService.unSubscribeShowDownChannels([this.entryUpdateChannel], this.userEntryHandler.bind(this));
    this.subscribeToEntries();
  }

  /**
   * To subscribe to entries
   * @returns {void}
   */
  private subscribeToEntries(): void {
    this.subscriberService.userEntryUpdates(this.entryUpdateChannel, this.userEntryHandler.bind(this), 'subscribeshowdown');
  }

  /**
   * Handler for entry update
   * @param {IEntrySummaryInfo[]} entryList
   * @returns {void}
   */
  private userEntryHandler(entryList: ILeaderboardData): void {
    const [topEntry] = entryList && entryList.myEntries ? entryList.myEntries : [];
    if (topEntry && topEntry.contestId === this.widgetData.id && !this.isComponentDestroyed) {
      [this.entryDetails] = this.entryService.entriesCreation([topEntry]);
      this.changeDetectorRef.detectChanges();
      this.awsService.addAction('LEADERBOARD_WIDGET=>TOP_ENTRY', { topEntry });
    }
  }

  /**
   * To Update Entry when updates are available
   * @param {IEntrySummaryInfo[]} entryList
   * @returns {void}
   */
  private entryUpdateHandler(entryList: IEntrySummaryInfo[]): void {
    const [topEntry] = entryList;
    if (topEntry && topEntry.contestId === this.widgetData.id && !this.isComponentDestroyed) {
      [this.entryDetails] = this.entryService.entriesCreation([topEntry]);
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * To Initialize widget details with score and clock
   * @returns {void}
   */
  private initWidgetDetails(): void {
    this.subscriber = `${this.WIDGET_COMPONENT}_${this.coreToolsService.uuid()}`;
    this.widgetService.getEventLiveStatus(this.eventEntity, this.leaderBoardWidget);
    this.lobbyService.setEventStateByStartDate(this.eventEntity);
    this.widgetService.setScoresFromEventComments(this.eventEntity, this.leaderBoardWidget);
    this.getTeamsColors();
  }

  /**
   * To Subscribe for pubsub events published in liveserve
   * @returns {void}
   */
  private subscribeForLiveUpdates(): void {
    this.createEventHanler(PUBSUB_API.SHOWDOWN_LIVE_SCORE_UPDATE, 'updateEventComments', 'setScoresFromOptaUpdate');
    this.createEventHanler(PUBSUB_API.SHOWDOWN_LIVE_CLOCK_UPDATE, 'updateClock', 'clockUpdate');
    this.createEventHanler(PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE, 'updateEventLiveData', 'getEventLiveStatus');
  }

  /**
   * To create handler for all the scenarios
   * @param {string} channelName
   * @param {string} liveServeFunc
   * @param {string} widgetFunc
   * @returns {void}
   */
  private createEventHanler(channelName: string, liveServeFunc: string,
    widgetFunc: string): void {
    this.pubSub.subscribe(this.subscriber, channelName, (update: IShowdownOptaUpdate) => {
      if (update && Number(this.eventEntity.id) === update.id && update.payload) {
        this.liveServeUpdateService[liveServeFunc](this.eventEntity, update);
        if (widgetFunc) {
          this.widgetService[widgetFunc](this.eventEntity, this.leaderBoardWidget, update);
        }
      }
    });
  }

  /**
   * To fetch team colors from asset manager
   * @returns {void}
   */
  private getTeamsColors(): void {
    this.cmsService.getTeamsColors([this.leaderBoardWidget.homeTeam, this.leaderBoardWidget.awayTeam], '16')
    .subscribe((response: ITeamColor[]) => {
      this.teamColors = response;
      this.hasTeamImage = this.leaderBoardService.hasImageForHomeAway(this.teamColors);
      this.teamColors = this.leaderBoardService.setDefaultTeamColors(this.teamColors,
        [this.leaderBoardWidget.homeTeam, this.leaderBoardWidget.awayTeam]);
      this.changeDetectorRef.markForCheck();
    });
  }
}

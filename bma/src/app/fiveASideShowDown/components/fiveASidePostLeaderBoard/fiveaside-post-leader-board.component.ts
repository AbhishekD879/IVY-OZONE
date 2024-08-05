import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '@app/core/services/user/user.service';
import { IEventDetails, IShowDown, IShowDownResponse } from '@app/fiveASideShowDown/models/show-down';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { IPageYOffset, LIVE_EVENT_VALUE } from '@app/fiveASideShowDown/constants/enums';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { IEntrySummaryInfo, IHeaderArea } from '@app/fiveASideShowDown/models/entry-information';
import { Subscription } from 'rxjs';
import { CmsService } from '@core/services/cms/cms.service';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { EVENTSTATUS, GTM_RULES_DATA, LEADERBOARD_WIDGET } from '@app/fiveASideShowDown/constants/constants';
import { IPrize } from '@app/fiveASideShowDown/models/IPrize';
import { DeviceService } from '@core/services/device/device.service';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { NavigationService } from '@core/services/navigation/navigation.service';

@Component({
  selector: 'fiveaside-post-leader-board',
  templateUrl: './fiveaside-post-leader-board.component.html'
})
export class FiveASidePostLeaderBoardComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() leaderboardData: IShowDown;
  public showOverlay: boolean;
  public postcontestInfo: IShowDown;
  public event: IEventDetails;
  myEntriesList: Array<IEntrySummaryInfo> = [];
  teamColors: any[];
  hasTeamImage: boolean;
  leaderboardEntires: Array<IEntrySummaryInfo> = [];
  prize: IPrize;
  readonly eventStatus: string = EVENTSTATUS.POST;
  public isNoCommentaryAvailable: boolean = false;
  public headerAreaInfo: IHeaderArea;
  public offSetPValue:number = IPageYOffset.offSetPValue;
  public offSetValue:number = IPageYOffset.offSetValue;
  public slideContent: HTMLElement;
  public showLeaderBoardTop: string;
  public initialRecordsCopy: Array<IEntrySummaryInfo> = [];
  public entryIdList: string[];
  public dataLoading: boolean = true;
  public showServiceMessage: boolean = false;
  public leaderboardVal: string = '';
  private events: IEventDetails;
  private routeSubscriber: Subscription;
  private contestId: string;
  private readonly leaderBoardTop: string = 'Leaderboard Top';
  private initialAllRecords: Array<IEntrySummaryInfo> = [];
  private timeOutListener: number;
  private readonly title = 'FiveASidePostLeaderBoard';

  constructor(
    private windowRefService: WindowRefService,
    private route: ActivatedRoute,
    private userService: UserService,
    private showDownService: FiveasideLeaderBoardService,
    private fiveASideShowDownLobbyService: FiveASideShowDownLobbyService,
    private rendererService: RendererService,
    private cmsService: CmsService,
    private deviceService: DeviceService,
    private gtmService: GtmService,
    private pubSubService: PubSubService,
    private navigationService: NavigationService
     ) {
       super();
     }

  ngOnInit(): void {
    this.headerAreaInfo = {} as IHeaderArea;
    this.contestId = this.route.snapshot.params.id;
    this.setScrollListeners();
    this.decodeInitialData();
    // this.fetchInitialDataOfEvent();
    // this.prizePool();
    this.postLoginTrigger();
  }

  ngOnDestroy(): void {
    this.removeScrollListeners();
    this.routeSubscriber && this.routeSubscriber.unsubscribe();
    this.pubSubService.unsubscribe(this.title);
  }

  /**
   * showOverlay on clicking Rules button and Ga track
   * @returns {void}
   */
  showOverlayFunction(): void {
    this.showOverlay = true;
    const gtmData = GTM_RULES_DATA;
    this.gtmService.push('trackEvent', gtmData);
  }

  /**
   * gets the prize pool information to know the total prizes
   * @returns void
   */
  prizePool(): void {
    this.showDownService.getContestPrizeById(this.contestId).subscribe((prize: IPrize) => {
      this.prize = prize;
    });
  }

  /**
   * initial scores and clock updates form the event comments
   * @returns {void}
   */
  initScoresFromEventComments(): void {
    if (this.event && this.event.scores) {
      this.headerAreaInfo.homeName = this.event.scores.home.name;
      this.headerAreaInfo.awayName = this.event.scores.away.name;
      this.headerAreaInfo.homeScore = this.event.scores.home.score;
      this.headerAreaInfo.awayScore = this.event.scores.away.score;
    }
    this.isMatchCompletedAndResulted();
    if (this.event.name) {
      const eventName: string = this.event.name.replace(/[|,]/g, '');
      [this.headerAreaInfo.homeName, this.headerAreaInfo.awayName] = eventName.split(/ v | vs | - /);
    }
    this.headerAreaInfo.flagHomeIcon = this.showDownService.formFlagName(this.headerAreaInfo.homeName);
    this.headerAreaInfo.flagAwayIcon = this.showDownService.formFlagName(this.headerAreaInfo.awayName);
    this.headerAreaInfo.isScoresAvailable = this.isTeamScoresAvailable();
  }

  /**
   * check if Match is Completed And Resulted
   * @returns {boolean}
   */
  isMatchCompletedAndResulted(): boolean {
    return this.event.isResulted && this.event.regularTimeFinished;
  }

  /**
   * is Team Scores Available
   * @returns {boolean}
   */
  isTeamScoresAvailable(): boolean {
    return !!(this.headerAreaInfo.homeScore && this.headerAreaInfo.awayScore);
  }

  /**
   * initialLbrEntries is used to set initial data live for leader board
   * @param  { IEntrySummaryInfo } initialData
   * @returns void
   */
  initialLbrEntries(initialData: Array<IEntrySummaryInfo>): void {
    this.initialAllRecords = initialData;
    this.showLeaderBoardTop = `${this.leaderBoardTop} ${this.initialAllRecords.length}`;
    if (this.leaderboardEntires.length !== LIVE_EVENT_VALUE.INITIAL_COUNT) {
      this.entryIdList = this.leaderboardEntires.map(({id}) => id); // To Filter out as array of id from leaderboardEntires
    }
    this.timeOutListener = this.windowRefService.nativeWindow.setInterval(() => {
      const count:number = this.initialRecordsCopy.length;
      for (let index=count; index< count+LIVE_EVENT_VALUE.UPDATE_COUNT; index++) {
        if (this.initialAllRecords[index] && this.initialAllRecords) {
          this.initialRecordsCopy.push(this.initialAllRecords[index]);
          this.dataLoading = false;
          if (this.initialRecordsCopy.length === this.initialAllRecords.length) {
            this.windowRefService.nativeWindow.clearInterval(this.timeOutListener);
          }
        }
      }
      this.leaderboardVal = this.validateLeaderBoardRecords(this.initialAllRecords.length);
    }, LIVE_EVENT_VALUE.UPDATE_COUNT);
  }

  /**
   * Scenario: When User Logged in first time to refresh the Data
   * @returns void
   */
  private postLoginTrigger(): void {
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.fetchInitialDataOfEvent();
    });
  }

  /**
   * To decode initial contest information received from leaderboard component
   * @returns {void}
   */
  private decodeInitialData() {
    this.postcontestInfo = this.leaderboardData;
    this.prize = this.leaderboardData.prizeMap;
    if (!this.postcontestInfo.display) {
      this.navigationService.openRouterUrl(LEADERBOARD_WIDGET.LOBYY_URL, true);
    }
    this.showServiceMessage = this.postcontestInfo.enableServiceMsg;
    this.myEntriesList = this.postcontestInfo.myEntries;
    this.leaderboardEntires = this.postcontestInfo.leaderBoardEntries;
    this.initialLbrEntries(this.leaderboardEntires);
    this.initContestDetails();
    this.cmsService.getTeamsColors([this.headerAreaInfo.homeName, this.headerAreaInfo.awayName], '16').subscribe((response: ITeamColor[]) => {
        this.teamColors = response;
        this.hasTeamImage = this.showDownService.hasImageForHomeAway(this.teamColors);
        this.teamColors = this.showDownService.setDefaultTeamColors(this.teamColors,
          [this.headerAreaInfo.homeName, this.headerAreaInfo.awayName]);
        this.hideSpinner();
      },
      () => {
        this.showError();
        this.navigationService.openRouterUrl(LEADERBOARD_WIDGET.LOBYY_URL, true);
      });
  }

  /**
   *  fetch initial data for event
   * @returns void
   */
  private fetchInitialDataOfEvent(): void {
    this.showSpinner();
    const username: string = this.userService.username;
    const bppToken: string = this.userService.bppToken;
    this.showDownService.getContestInformationById(this.contestId, username, bppToken)
    .subscribe((response: IShowDownResponse) => {
      this.leaderboardData = response.contest;
      this.decodeInitialData();
    });
  }

  /**
   * to get the initial contest Details for the entry
   * @returns {void}
   */
  private initContestDetails(): void {
    this.events = this.postcontestInfo.eventDetails;
    this.event = this.events as any;
    this.initScoresFromEventComments();
  }

  /**
   * scrollHandler for animation expand and collapse the header area
   * @returns {void}
   */
  private scrollHandler(): void {
    if (this.deviceService.isMobile) {
    const headerAreaScroll: HTMLElement = this.windowRefService.document.querySelector('.header-area-scroll');
    this.slideContent = this.windowRefService.document.querySelector('.over-all-height');
    if (headerAreaScroll && this.windowRefService.nativeWindow.pageYOffset > this.offSetPValue) {
      const diff =
        (this.windowRefService.nativeWindow.pageYOffset - this.offSetPValue) > this.offSetValue ?
          this.offSetValue : (this.windowRefService.nativeWindow.pageYOffset - this.offSetPValue);
      this.rendererService.renderer.setStyle(headerAreaScroll, 'display', 'initial');
      this.rendererService.renderer.setStyle(headerAreaScroll, 'top', `${diff}px`);
      this.rendererService.renderer.setStyle(headerAreaScroll, 'position', 'fixed');
    }
    if (headerAreaScroll && this.windowRefService.nativeWindow.pageYOffset <= this.offSetPValue) {
      this.rendererService.renderer.setStyle(headerAreaScroll, 'top', '-38px');
      this.rendererService.renderer.setStyle(headerAreaScroll, 'display', 'none');
    }
    if (this.slideContent && this.windowRefService.nativeWindow.pageYOffset > (this.slideContent.offsetHeight - this.offSetPValue)) {
      this.rendererService.renderer.setStyle(headerAreaScroll, 'display', 'none');
    }
  }
  }

  /**
   * check Commentary to be called for Event
   * @param  {ISportEvent} event
   * @returns {boolean}
   */
  private checkCommentaryToBeCalledForEvent(event: IEventDetails): boolean {
    return !(event.clock || event.comments) && !this.isNoCommentaryAvailable;
  }

  /**
   * set scroll Listeners
   * @returns {void}
   */
  private setScrollListeners(): void {
    this.windowRefService.nativeWindow.document.addEventListener('scroll', this.scrollHandler.bind(this));
  }

  /**
   * remove scroll Listeners
   * @returns {void}
   */
  private removeScrollListeners(): void {
    this.windowRefService.nativeWindow.document.removeEventListener('scroll', this.scrollHandler.bind(this));
  }
  private validateLeaderBoardRecords(length: number): string {
    return length < 100 ? `${length}` : '100';
  }
}

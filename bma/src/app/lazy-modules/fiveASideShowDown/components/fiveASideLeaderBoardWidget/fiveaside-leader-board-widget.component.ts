import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  Input,
  OnDestroy
} from '@angular/core';
import { Router } from '@angular/router';
import { IShowDown } from '@app/fiveASideShowDown/models/show-down';
import { FiveasideLeaderBoardService
} from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';
import { UserService } from '@core/services/user/user.service';
import { FiveasideWidgetService } from '@lazy-modules/fiveASideShowDown/services/fiveaside-widget.service';
import { FiveAsideLiveServeUpdatesSubscribeService
} from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { Subscription } from 'rxjs';
import { PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';

@Component({
  selector: 'fiveaside-leader-board-widget',
  template: ``,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveasideLeaderBoardWidgetComponent implements OnDestroy {
  showDownData: IShowDown[] = [];
  carouselName: string = 'leader-board-widget-carousel';
  public activeSlideIndex: number = 0;
  protected navigationServiceSubscription: Subscription;
  private eventIds: string[] = [];
  private channelsList: string[] = [];
  private masterShowDownData: IShowDown[] = [];
  private readonly WIDGET_COMPONET = 'FiveasideLeaderBoardWidgetComponent';
  private readonly FOOTBALL_MATCHES_TAB: string = '/sport/football/matches';
  private _showLeaderboard: boolean;
  @Input()
  get showLeaderboard(): boolean {
    return this._showLeaderboard;
  }
  set showLeaderboard(value: boolean) {
    this._showLeaderboard = value;
    this.init();
  }

  /**
   * To Check If it has One card
   * @returns {boolean}
   */
  public get isOneCard(): boolean {
    return this.showDownData.length === 1;
  }

  public set isOneCard(value: boolean) {}

  constructor(private leaderBoardService: FiveasideLeaderBoardService,
    private userService: UserService,
    private widgetService: FiveasideWidgetService,
    private liveServeSubscriberService: FiveAsideLiveServeUpdatesSubscribeService,
    private changeDetectorRef: ChangeDetectorRef,
    private carouselService: CarouselService,
    private pubsub: PubSubService,
    private navigationService: NavigationService,
    private router: Router
  ) { }

  ngOnDestroy(): void {
    this.unsubscribeChannels();
    this.pubsub.unsubscribe(this.WIDGET_COMPONET);
    this.navigationServiceSubscription && this.navigationServiceSubscription.unsubscribe();
  }

  /**
   * To Navigate to specific slide
   * @param {number} indexOf
   * @returns {void}
   */
  goToSlide(index: number): void {
    this.bannersCarousel.toIndex(index);
    this.handleActiveShowdown(index);
  }

  /**
   * To Handle Active Slide
   * @param {number} slideIndex
   * @returns {void}
   */
  handleActiveSlide(slideIndex: number): void {
    if (!Number.isInteger(slideIndex)) {
      return;
    }
    const index:number = slideIndex - 1;
    this.handleActiveShowdown(index);
  }

  /**
   * should trigger whenever there is a change in input property
   */
  private init(): void {
    if (!this.isMatchesURL()) {
      this.getLeaderboardData();
    }
    this.checkDataLoad();
    this.postLoginTrigger();
  }

  /**
   * To Check if data is loaded in sports page
   */
  private checkDataLoad(): void {
    this.navigationServiceSubscription = this.navigationService.changeEmittedFromChild.subscribe(loaded => {
      if (loaded && !this.showDownData.length && this.isMatchesURL()) {
        this.getLeaderboardData();
      }
    });
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
   * Scenario: When User Logged in first time to refresh the Data
   * @returns {void}
   */
  private postLoginTrigger(): void {
    this.pubsub.subscribe(this.WIDGET_COMPONET, this.pubsub.API.SUCCESSFUL_LOGIN, () => {
      this.getLeaderboardData();
    });
  }

  /**
   * To Handle Active Showdown
   * @param {number} index
   * @returns {void}
   */
  private handleActiveShowdown(index: number): void {
    if (this.showDownData[index]) {
      this.showDownData[this.activeSlideIndex].active = false;
      this.showDownData[index].active = true;
      this.activeSlideIndex = index;
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * To Get Banners Carousel
   * @returns {Carousel}
   */
  private get bannersCarousel(): Carousel {
    return this.carouselService.get(this.carouselName);
  }

  private set bannersCarousel(value: Carousel) {}

  /**
   * To unsubscribe to channels
   * @returns {void}
   */
  private unsubscribeChannels(): void {
    this.channelsList = this.liveServeSubscriberService.createChannels(this.eventIds.slice());
    this.liveServeSubscriberService.unSubscribeLiveServeConnection(this.channelsList);
  }

  /**
   * To Fetch Initial Leaderboard information
   * @returns {void}
   */
  private getLeaderboardData(): void {
    if (this.userService.username) {
      const userName = this.userService.username;
      const bppToken: string = this.userService.bppToken;
      this.leaderBoardService.getLeaderBoardInformation(userName, bppToken)
        .subscribe((response: { contests: IShowDown[] }) => {
          if (response && response.contests && response.contests.length) {
            this.showDownData = response.contests;
            this.masterShowDownData = response.contests;
            this.initLeaderBoardData();
            this.hidePreEventContests();
            this.setActiveWidgetSlide();
            this.changeDetectorRef.detectChanges();
          }
        }, (error) => {
          console.warn(error);
        });
    }
  }

  /**
   * Set showdown slide card as active for first card
   * @returns void
   */
  private setActiveWidgetSlide(): void {
    if (this.showDownData) {
      const [showdownContest] = this.showDownData;
      if (showdownContest && showdownContest.eventDetails) {
        showdownContest.active = true;
      }
    }
  }

  /**
   * To Initialize leaderboard data
   * @returns {void}
   */
  private initLeaderBoardData(): void {
    this.widgetService.buildLeaderBoardData(this.showDownData, this.eventIds);
    this.unsubscribeChannels();
    this.openLiveServeConnection();
    this.pubsub.subscribe(this.WIDGET_COMPONET, PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED, this.handleResultedEvent.bind(this));
    this.pubsub.subscribe(this.WIDGET_COMPONET, PUBSUB_API.SHOWDOWN_EVENT_STARTED, this.handleStartedEvent.bind(this));
  }

  /**
   * To Open Live Servce Connection
   * @returns {void}
   */
  private openLiveServeConnection(): void {
    this.channelsList = this.liveServeSubscriberService.createChannels(this.eventIds.slice());
    this.liveServeSubscriberService.openLiveServeConnectionForUpdates(this.channelsList);
  }

  /**
   * To Handle Resulted Event
   * @param {string} eventId
   * @returns {void}
   */
  private handleResultedEvent(eventId: string): void {
    this.showDownData = this.showDownData.filter((showDown: IShowDown) => {
      return showDown.event !== eventId;
    });
    this.changeDetectorRef.markForCheck();
  }

  /**
   * To handle the event which just started
   * @param  {string} eventId
   * @returns void
   */
  private handleStartedEvent(eventId: string): void {
    const contestTobeAdded = this.masterShowDownData.find((contest: IShowDown) => contest.event === eventId);
    if (contestTobeAdded && contestTobeAdded.eventDetails) {
      const contestEvent = contestTobeAdded.eventDetails;
      if (contestEvent) {
        contestEvent.started = true;
        contestEvent.scores = { home: { score: 0 }, away: { score: 0 } };
      }
      if (!this.checkEventAlreadyExists(eventId)) {
        this.showDownData.unshift(contestTobeAdded);
      }
    }
    this.changeDetectorRef.markForCheck();
  }

  /**
   * To check if event is already added to widget
   * @param  {string} eventId
   * @returns boolean
   */
  private checkEventAlreadyExists(eventId: string): boolean {
    return this.showDownData.some(contest => contest.event === eventId);
  }

  /**
   * Hide pre event contests
   * @returns void
   */
  private hidePreEventContests(): void {
    this.showDownData = this.showDownData.filter((showDown: IShowDown) => {
      const showDownEvent = showDown.eventDetails;
      if (showDownEvent) {
        return showDownEvent.started;
      }
      return false;
    });
    this.changeDetectorRef.markForCheck();
  }
}

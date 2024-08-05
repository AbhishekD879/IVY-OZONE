import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';

import { filter, mergeMap } from 'rxjs/operators';
import { Subscription } from 'rxjs';

import { WsConnector } from '@core/services/wsConnector/ws-connector';
import { TimelineService } from '@lazy-modules/timeline/services/timeline.service';
import { CmsService } from '@core/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { AsyncScriptLoaderService } from '@app/core/services/asyncScriptLoader/async-script-loader.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { UserService } from '@core/services/user/user.service';
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@core/services/locale/locale.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';

import { ITimelineSettings } from '@core/services/cms/models/timeline-settings.model';
import { IPost, ITimelineConfig } from '@lazy-modules/timeline/models/timeline-post.model';
import { SPRITE_PATH } from '@app/bma/constants/image-manager.constant';
import { TIMELINE_EVENTS, timelineConfig } from '@lazy-modules/timeline/constants/timeline.constant';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { ISystemConfig } from '@core/services/cms/models';

@Component({
  selector: 'timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TimelineComponent implements OnInit, OnDestroy {
  public showSkeleton: boolean = false;
  public isReconectedFailedMsg: boolean = false;
  public posts: IPost[] = [];
  public lastPost: IPost;
  public socket: WsConnector;
  public isTimelineAvailable: boolean = false;
  public isNewPostIconDisplayed: boolean = false;
  public timelineOpened: boolean = false;
  public timelineSettings: ITimelineSettings;
  public timelineIcons: string;
  public bybShown: boolean = false;
  public allPostsLoaded: boolean = false;
  public tutorialReady: boolean = false;
  public priceButtonClasses: { [key: string]: string } = {};
  public isBrandLadbrokes: boolean;
  public gtmModuleBrandName: string;
  public totalPoststoDisplay: number;
  private timelineSettingSub: Subscription;
  private timelineServiceSub: Subscription;
  private timelinePostsCountSub: Subscription;
  private createSocketSub: Subscription;
  private routeChangeSub: Subscription;
  private BODY_CLASS: string = 'timeline-opened';
  private readonly title: string = 'timeline';
  private readonly removePriceUpdateClassTime = 2000;
  private socketStates = ['reconnect_attempt', 'reconnect', 'connect_error'];
  private availableRoutes: string[];

  constructor(
    protected timelineService: TimelineService,
    protected cms: CmsService,
    protected router: Router,
    private changeDetectorRef: ChangeDetectorRef,
    private asyncScriptLoaderService: AsyncScriptLoaderService,
    private pubSubService: PubSubService,
    private windowRefService: WindowRefService,
    private rendererService: RendererService,
    private userService: UserService,
    private locale: LocaleService
  ) {
    this.handleTimeline = this.handleTimeline.bind(this);
    this.loadTimelineIcons();
  }

  ngOnInit(): void {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    this.gtmModuleBrandName = this.isBrandLadbrokes? timelineConfig.gtmModuleLadbrokesTitle : timelineConfig.gtmModuleCoralTitle;

    this.timelineSettingSub = this.cms.getTimelineSetting()
      .subscribe((settings: ITimelineSettings) => {
        this.timelineSettings = settings;
        this.availableRoutes = settings.pageUrls && settings.pageUrls.split(',') || [''];
      });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.LOGIN_POPUPS_END, () => {
      this.tutorialReady = true;
      this.changeDetectorRef.detectChanges();
    });

    this.timelinePostsCountSub = this.cms.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.totalPoststoDisplay = config.Timeline && config.Timeline.totalPostsCount;
    });

    if (this.userService.status) {
      this.tutorialReady = true;
      if (!this.timelineService.socket || !this.timelineService.socket.isConnected()) {
        this.openTimeline();
      }
    } else {
      this.closeTimeline();
    }

    this.pubSubService.subscribe(this.title, [
        this.pubSubService.API.TIMELINE_SETTINGS_CHANGE,
        this.pubSubService.API.SESSION_LOGOUT,
        this.pubSubService.API.SUCCESSFUL_LOGIN
      ], this.handleTimeline
    );

    this.pubSubService.subscribe(this.title, this.pubSubService.API.BYB_SHOWN, (bybShown: boolean) => {
      this.bybShown = bybShown;
      this.changeDetectorRef.markForCheck();
    });
    this.pubSubService.subscribe(this.title, this.pubSubService.API.TOTEPOOL_SHOWN, (totepoolShown: boolean) => {
      this.bybShown = totepoolShown;
      this.changeDetectorRef.markForCheck();
    });

    this.subscribeToRouteEvents();
    this.handleTimeline();

    this.changeDetectorRef.markForCheck();
  }

  ngOnDestroy(): void {
    this.closeTimeline();
    this.routeChangeSub && this.routeChangeSub.unsubscribe();
    this.timelineSettingSub && this.timelineSettingSub.unsubscribe();
    this.timelineServiceSub && this.timelineServiceSub.unsubscribe();
    this.timelinePostsCountSub && this.timelinePostsCountSub.unsubscribe();
    this.createSocketSub && this.createSocketSub.unsubscribe();
    this.pubSubService.unsubscribe(this.title);
  }

  handleTimeline(): void {
    if (this.timelineSettings && this.timelineSettings.enabled) {
      const endDate = new Date(this.timelineSettings.liveCampaignDisplayTo).getTime();
      this.isTimelineAvailable = this.isUrlAvailable(this.availableRoutes, this.router.url) &&
        this.userService.status && this.userService.timeline;
      this.timelineOpened = false;

      this.pubSubService.publish(this.pubSubService.API.TIMELINE_SHOWN, this.isTimelineAvailable);

      if (this.isTimelineAvailable && (endDate > Date.now())) {
        this.timelineService.gtm('rendered', {
          eventLabel: this.timelineSettings.liveCampaignName
        }, this.gtmModuleBrandName);
        this.tutorialReady && this.windowRefService.nativeWindow.setTimeout(() => {
          this.pubSubService.publish(this.pubSubService.API.SHOW_TIMELINE_TUTORIAL);
        });
        if (!this.timelineService.socket || !this.timelineService.socket.isConnected()) {
          this.openTimeline();
        }
      }
      if (!this.userService.status) {
        this.closeTimeline();
      }

      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Change state of timeline
   *
   * @param state - state
   */
  onStateChange(state: boolean): void {
    this.timelineOpened = state;
    this.timelineService.gtm(`${state ? 'open': 'close'}`, {
      eventLabel: this.timelineSettings.liveCampaignName
    }, this.gtmModuleBrandName);
    this.toggleBodyScroll(state);

    if (state) {
      this.isNewPostIconDisplayed = false;
      this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', true);
    } else {
      this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', false);
    }

    this.changeDetectorRef.detectChanges();
  }

  onTimelineReload(state: boolean): void {
    if (state) {
      this.closeTimeline();
      this.openTimeline();
      this.changeDetectorRef.detectChanges();
    }
  }

  openTimeline(): void {
    this.subscribeToTimelineUpdates();
    this.pubSubService.subscribe(this.title, this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.subscribeToTimelineUpdates(true);
    });
  }

  closeTimeline(): void {
    if (this.timelineService) {
      this.timelineService.removeListener(TIMELINE_EVENTS.CAMPAIGN_CLOSED);
      this.timelineService.removeListener(TIMELINE_EVENTS.POST_CHANGED);
      this.timelineService.removeListener(TIMELINE_EVENTS.POST_REMOVED);
      this.timelineService.removeListener(TIMELINE_EVENTS.POST_PAGE);
      this.timelineService.removeListener(TIMELINE_EVENTS.POST);
      this.timelineService.removeListener(TIMELINE_EVENTS.TIMELINE_CONFIG);

      this.timelineServiceSub && this.timelineServiceSub.unsubscribe();
      this.createSocketSub && this.createSocketSub.unsubscribe();
      this.timelineService.disconnect();
    }

    this.posts = [];
    this.changeDetectorRef.detectChanges();
  }

  loadMore(): void {
    if (this.posts.length < this.totalPoststoDisplay) {
      this.showSkeleton = true;
      this.timelineService.emit(TIMELINE_EVENTS.LOAD_POST_PAGE, {
        from: {
          id: this.lastPost.id,
          timestamp: this.lastPost.createdDate
        }
      });
      this.changeDetectorRef.detectChanges();
    }
  }

  private trackSocketState(state: string): void {
    if (state && this.socketStates.includes(state)) {
      this.showSkeleton = true;
      this.isReconectedFailedMsg = false;
    } else if (state === 'reconnect_failed') {
      this.showSkeleton = false;
      this.isReconectedFailedMsg = true;
    } else {
      this.showSkeleton = false;
      this.isReconectedFailedMsg = false;
    }
    this.changeDetectorRef.detectChanges();
  }

  private subscribeToTimelineUpdates(resetTimelinePosts: boolean = false): void {
    let resetPosts = resetTimelinePosts;
    this.createSocketSub = this.timelineService.createSocket()
      .pipe(mergeMap(webSocket => webSocket.state$))
      .subscribe((state) => {
        this.trackSocketState(state);
      });

    this.timelineServiceSub = this.timelineService.connect().subscribe(() => {
      this.timelineService.addListener(TIMELINE_EVENTS.POST_PAGE, ((postsPage: any) => {

        let posts = postsPage && postsPage.page;
        const count = postsPage && postsPage.count;

        setTimeout(() => {
          if (posts && posts.length) {
            this.lastPost = posts[posts.length - 1];
            if (resetPosts) {
              this.posts = [...posts];
            } else {
              posts = posts.filter((post: IPost) => !this.posts.find((oldPost: IPost) => oldPost.id === post.id));
              this.posts = [...this.posts, ...posts];
            }
            this.validateTotalPostsDisplay();
            this.allPostsLoaded = count === this.posts.length;
            resetPosts = false;
          }
          this.showSkeleton = false;
          this.changeDetectorRef.detectChanges();
        }, 300);
      }));

      this.timelineService.addListener(TIMELINE_EVENTS.POST, (post: IPost) => {
        if (!this.posts.find((oldPost: IPost) => oldPost.id === post.id)) {
          this.posts = [post, ...this.posts];
        }
        this.validateTotalPostsDisplay();
        if (!this.timelineOpened) {
          this.isNewPostIconDisplayed = true;
        }
        this.lastPost = this.posts[this.posts.length - 1];
        this.changeDetectorRef.detectChanges();
      });

      this.timelineService.addListener(TIMELINE_EVENTS.POST_CHANGED, (action) => {
        const post = action.data || action[0];
        const postToUpdate = this.posts.find((p: IPost) => post.id === p.id);
        this.handlePriceChange(post, postToUpdate);
        this.posts = this.posts.reduce((posts: IPost[], currentPost: IPost) => {
          return currentPost.id === post.id ? [...posts, post] : [...posts, currentPost];
        }, []);

        this.changeDetectorRef.detectChanges();
      });

      this.timelineService.addListener(TIMELINE_EVENTS.POST_REMOVED, (action) => {
        this.posts = this.posts.filter((post: IPost) => post.id !== action.affectedMessageId);
        this.changeDetectorRef.detectChanges();
      });

      this.timelineService.addListener(TIMELINE_EVENTS.CAMPAIGN_CLOSED, () => {
        this.posts = [];
        this.changeDetectorRef.detectChanges();
      });

      this.timelineService.addListener(TIMELINE_EVENTS.TIMELINE_CONFIG, (timelineFlag: ITimelineConfig) => {
        if (this.timelineSettings) {
          this.timelineSettings.enabled = timelineFlag.enabled;
          if (this.timelineSettings.enabled) {
            this.handleTimeline();
          } else {
            this.isTimelineAvailable = this.timelineSettings.enabled;
          }
        }
        this.changeDetectorRef.markForCheck();
      });
    });
  }

  /**
   * Valdate the total post limit is reached or not.
   * If reached, pop the old post
   */
  private validateTotalPostsDisplay(): void {
    if (this.posts.length > this.totalPoststoDisplay) {
      let extraPostsCount = this.posts.length - this.totalPoststoDisplay;
      while (extraPostsCount) {
        this.posts.pop();
        extraPostsCount--;
      }
    }
  }

  private handlePriceChange(post: IPost, updatedPost: IPost): void {
    if (post.selectionEvent) {
      const prices = post.selectionEvent.obEvent.markets[0].outcomes[0].prices[0];
      const updatedPrices = updatedPost?.selectionEvent?.obEvent.markets[0].outcomes[0].prices[0];
      const buttonClass = this.getClassForPriceUpdate(prices, updatedPrices);
      this.updateButtonClass(post.id, buttonClass);
    }
  }

  private getClassForPriceUpdate(currentPrices: IOutcomePrice, updatedPrices: IOutcomePrice): string {
    if (!currentPrices || !updatedPrices) {
      return '';
    }
    let buttonClass = '';
    if ((currentPrices.priceNum / currentPrices.priceDen) > (updatedPrices.priceNum / updatedPrices.priceDen)) {
      buttonClass = 'bet-up';
    } else if ((currentPrices.priceNum / currentPrices.priceDen) < (updatedPrices.priceNum / updatedPrices.priceDen)) {
      buttonClass = 'bet-down';
    }
    return buttonClass;
  }

  private updateButtonClass(postId: string, buttonClass: string): void {
    if (buttonClass) {
      this.priceButtonClasses = {...this.priceButtonClasses, [postId]: buttonClass };
      setTimeout(() => {
        this.priceButtonClasses = {...this.priceButtonClasses, [postId]: '' };
        this.changeDetectorRef.markForCheck();
      }, this.removePriceUpdateClassTime);
    }
  }

  /**
   * Check if timeline is available for current url
   * @param availableRoutes {Array} - urls where popup is enabled
   * @param currentUrl {string} - current url
   *
   * Examples of page url rules:
   *  /, /horse-racing/, /live-stream - only for root page, /horse-racing/ page and /live-stream page
   *  /horse-racing/* - category horse-racing and all its child (for example /horse-racing/live-stream)
   */
  private isUrlAvailable(availableRoutes: string[], currentUrl: string): boolean {
    return availableRoutes.some((url: string): boolean => {
      url = url.trim();
      let isEnabled = url === currentUrl;

      if (url[url.length - 1] === '*') {
        const result = currentUrl.match(url);
        isEnabled = result && (result.index === 0);
      }

      return isEnabled;
    });
  }

  /**
   * Toggles class to body element to enable/disable scrolling depending on passed state.
   * @param {boolean} state
   * @private
   */
  private toggleBodyScroll(state: boolean): void {
    const body = this.windowRefService.document.body;
    if (state) {
      this.rendererService.renderer.addClass(body, this.BODY_CLASS);
    } else {
      this.rendererService.renderer.removeClass(body, this.BODY_CLASS);
    }
  }

  private loadTimelineIcons(): void {
    this.asyncScriptLoaderService.getSvgSprite(SPRITE_PATH.timeline).subscribe((icons: string) => this.timelineIcons = icons);
  }

  private subscribeToRouteEvents(): void {
    this.routeChangeSub = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        const isUrlConfigured = this.isUrlAvailable(this.availableRoutes, this.router.url);
        if (isUrlConfigured) {
          this.handleTimeline();
        } else {
          this.isTimelineAvailable = isUrlConfigured;
          if (!this.timelineService.socket || !this.timelineService.socket.isConnected()) {
            this.openTimeline();
          }
        }
        this.changeDetectorRef.markForCheck();
      });
  }
}

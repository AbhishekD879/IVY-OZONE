import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { UserService } from '@app/core/services/user/user.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import {
    FiveAsideLiveServeUpdatesSubscribeService
} from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { LAZY_LOAD_ROUTE_PATHS } from '@bma/constants/lazyload-route-paths.constant';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { IShowdownLobbyContest, IShowdownLobbyResponse, ITransition } from '@app/fiveASideShowDown/models/showdown-lobby-contest.model';
import { TimeService } from '@app/core/services/time/time.service';
import environment from '@environment/oxygenEnvConfig';
import { ENTRY_CONFIRMATION,TIME_OUTS, SHOWDOWN_CARDS, PUBSUB_API, LOBBY_OVERLAY } from '@app/fiveASideShowDown/constants/constants';
import { IShowdownCard } from '@app/fiveASideShowDown/models/showdown-card.model';
import { ITermsAndConditions } from '@app/core/services/cms/models/terms-and-conditions';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { IContest } from '@app/core/services/cms/models/contest';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import { DeviceService } from '@app/core/services/device/device.service';
import { FiveASideCmsService } from '@app/fiveASideShowDown/services/fiveaside-cms.service';
import { LiveServConnectionService } from '@app/core/services/liveServ/live-serv-connection.service';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
@Component({
    selector: 'fiveaside-show-down-lobby',
    template: ``
})
export class FiveASideShowDownLobbyComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
    public channelsList: string[] = [];
    public displayContests: IShowdownLobbyContest[];
    public linkToEventPage: string | boolean;
    public showDownHome: string = LAZY_LOAD_ROUTE_PATHS.showDownHome;
    public visible: boolean = false;
    public progress: number; // to show the progress bar loading
    public termsConditions: ITermsAndConditions;
    public title: string = SHOWDOWN_CARDS.TITLE;
    public showOverlay: boolean = false;
    public showTutorialIndex: number;
    public lobbyManualTutorial = false;
    public welcomeCard: IWelcomeOverlay;
    public welcomeOverlaySeen: boolean = false;
    public isLobbyOverlaySeen: boolean = false;
    public isAnimationLoaded: boolean = false;
    public isDesktop: boolean;
    private moduleName = rgyellow.FIVE_A_SIDE;

    constructor(
        protected fiveASideShowDownLobbyService: FiveASideShowDownLobbyService,
        protected fiveAsideLiveServeUpdatesSubscribeService: FiveAsideLiveServeUpdatesSubscribeService,
        protected userService: UserService,
        protected gtmService: GtmService,
        protected windowRefService: WindowRefService,
        protected changeDetectorRef: ChangeDetectorRef,
        protected timeService: TimeService,
        protected cmsService: FiveASideCmsService,
        protected pubSubService: PubSubService,
        protected device: DeviceService,
        protected liveServConnectionService: LiveServConnectionService,
        private bonusSuppression: BonusSuppressionService
    ) {
        super();
    }
    /**
     * Init method for Showdown lobby
     * @returns void
     */
    ngOnInit(): void {
        this.isDesktop = this.device.isDesktop;
        this.postUserLoginTrigger();
        this.cmsService.getTermsAndConditions().subscribe((response: ITermsAndConditions) => {
            this.termsConditions = response;
        });
        this.welcomeOverlaySeen = JSON.parse(this.windowRefService.nativeWindow.localStorage.getItem('showdownOverlay'));
        this.isLobbyOverlaySeen = JSON.parse(this.windowRefService.nativeWindow.localStorage.getItem('lobbyOverlay'));
        this.fetchAllShowdownContests();
        this.removeResultedContestByEventId();
        this.reloadComponentListener();
    }

    get loadAnimation() {
        return this.fiveASideShowDownLobbyService.loadAnimation;
    }

    set loadAnimation(value: boolean) {}

    /**
     * Destroy method for component
     * @returns void
     */
    ngOnDestroy(): void {
        this.unSubscribeLiveServConnection();
        this.pubSubService.unsubscribe(this.title);
        this.displayContests = [];
    }

    footerGATrack(): void {
        const footerGA = {
            eventCategory: '5-A-Side Showdown',
            eventAction: 'click',
            eventLabel: 'T&C',
            location: 'showDownLobby',
        };
        this.gtmService.push('trackEvent', footerGA);
    }

    /**
     * 2s for the first transition time to load progress bar
     * after completing first transition we are triggering the next transition
     * which is after 1s we are triggering the overlay transistion
     * @param {ITransition} event
     */
     captureLeftSlideDoneEvent(event: ITransition): void {
        this.windowRefService.nativeWindow.setTimeout(() => {
            this.visible = true;
            this.fiveASideShowDownLobbyService.loadAnimation = true;
        }, TIME_OUTS.progressbar);
        this.loadOverlay(event, this.visible);
    }

    /**
     * Manual trigger for Lobby tutorial
     * @returns void
     */
    triggerLobbyTutorial(): void {
        const trackingObj = SHOWDOWN_CARDS.TUTORIAL_GA_TRACKING;
        this.gtmService.push('trackEvent', trackingObj);
        this.lobbyManualTutorial = true;
        this.showOverlay = false;
        this.changeDetectorRef.detectChanges();
        this.showOverlay = true;
    }

    /**
     * Get welcome overlay data from CMS
     * @returns void
     */
     getWelcomeOverlayData(): void {
         this.cmsService.getWelcomeOverlay().subscribe((response: IWelcomeOverlay) => {
             this.welcomeCard = response;
             this.initWelcomeOverlay(this.welcomeCard.overlayEnabled);
         }, (error) => {
             console.warn(error);
         });
    }

    /**
     * Init Welcome overlay and check for required conditions
     * @param  {boolean} overlayEnabled
     * @returns void
     */
    initWelcomeOverlay(overlayEnabled: boolean): void {
        if ((this.isDesktop || this.isAnimationLoaded) && this.displayContests && this.displayContests.length && overlayEnabled) {
            if (this.welcomeOverlaySeen && !this.isLobbyOverlaySeen) {
                this.lobbyManualTutorial = false;
                this.showOverlay = true;
            } else if (!this.welcomeOverlaySeen) {
                this.showOverlay = true;
            }
        }
    }

    /**
     * Show the contest based on role
     * If the contest is mapped to test accounts only test users can able to view it
     * logged in usercannot able to view it if he is a real user
     * If the contest is mapped to real users or both real users and test users
     * every logged in user can able to view it
     * @param contest {IShowdownLobbyContest}
     * @returns { boolean }
     */
    public showRoleBasedContests(contest: IContest): boolean {
        const userRole = this.isTestOrRealUser(this.userService.email);
        let showContest: boolean = true;
        if( contest.testAccount && !contest.realAccount && userRole === ENTRY_CONFIRMATION.realUser ) {
            showContest = false;
        }
        return showContest;
    }

    private loadOverlay(event: ITransition, visible: boolean): void {
        this.windowRefService.nativeWindow.setTimeout(() => {
            if (event.toState && visible) {
                this.isAnimationLoaded = true;
                this.getWelcomeOverlayData();
            }
        }, TIME_OUTS.showOverlay);
    }

    /**
     * Check if the logged in user is a test user
     * @param email { string }
     * @returns { string }
     */
    private isTestOrRealUser(email: string): string {
        return new RegExp(ENTRY_CONFIRMATION.testAccountTokens.join('|')).test(
        email
        ) ? ENTRY_CONFIRMATION.testUser : ENTRY_CONFIRMATION.realUser;
    }

    /**
     * Method for opening for Open Live serv connection
     * @returns void
     */
    private openLiveServConnection(): void {
        this.channelsList = this.fiveAsideLiveServeUpdatesSubscribeService.createLiveServeChannels(this.displayContests);
        this.fiveAsideLiveServeUpdatesSubscribeService.openLiveServeConnectionForUpdates(this.channelsList);
    }

    /**
     * Method for unsubscribing for Open Live serv connection
     * @returns void
     */
    private unSubscribeLiveServConnection(): void {
        this.channelsList = this.fiveAsideLiveServeUpdatesSubscribeService.createLiveServeChannels(this.displayContests);
        this.fiveAsideLiveServeUpdatesSubscribeService.unSubscribeLiveServeConnection(this.channelsList);
    }

    /**
     * Fetch All Showdown Contests
     * @returns void
     */
    private fetchAllShowdownContests(): void {
        this.showSpinner();
        const userName = this.userService.username;
        const bppToken: string = this.userService.bppToken;
        this.fiveASideShowDownLobbyService.getAllShowdownContests(environment.brand, userName, bppToken)
            .subscribe((data: IShowdownLobbyResponse) => {
                this.getWelcomeOverlayData();
                this.displayContests = data?.showdownCards;
                if (this.displayContests) {
                    this.initShowdownContestData();
                }
                this.hideSpinner();
            }, () => {
                this.showError();
            });
    }

    /**
     * Init and add clock and scores data to events
     * @returns void
     */
    private initShowdownContestData(): void {
        this.displayContests.forEach((contest: IShowdownLobbyContest, index: number) => {
            const contestEvents = contest.contests;
            if (contestEvents && contestEvents.length) {
                contestEvents.forEach((contestDetails: IShowdownCard) => {
                    contestDetails.showRoleContest = this.showRoleBasedContests(contestDetails);
                });
            }
            contest.displayCount = this.getRoleBasedContestsSize(contestEvents);
            this.setTutorialPosition(contest.displayCount, index);
            this.setLobbyCategoryNames(contest);
            this.progress = 100;
            this.changeDetectorRef.markForCheck();
            if (index === this.displayContests.length -1) {
                this.pubSubService.publish(LOBBY_OVERLAY.LOBBY_DATA_RELOADED_COMPLETED, true);
            }
        });
        this.openLiveServConnection();
    }

    /**
     * Set Tutorial button position for categories which has data
     * @param  {number} displayCount
     * @param  {number} index
     * @returns void
     */
    private setTutorialPosition(displayCount: number, index: number): void {
        if (displayCount) {
            this.setLobbyTutorialIndex(index);
        }
    }

    /**
     * Method to define the Tutorial button index
     * @param  {number} index
     * @returns void
     */
    private setLobbyTutorialIndex(index: number): void {
        if (this.showTutorialIndex === undefined) {
            this.showTutorialIndex = index;
        }
    }

    /**
     * Returns size of displayable contests
     * @param  {IShowdownCard[]} contestEvents
     * @returns number
     */
    private getRoleBasedContestsSize(contestEvents: IShowdownCard[]): number {
        return contestEvents.filter((contestCard: IShowdownCard) => contestCard.showRoleContest).length;
    }

    /**
     * Set Lobby Category Names
     * @param  {IShowdownLobbyContest} contest
     * @returns void
     */
    private setLobbyCategoryNames(contest: IShowdownLobbyContest): void {
        const isTodayorTomorrow = this.checkDateIsTodayOrTomorrow(contest.category);
        if (contest.category === SHOWDOWN_CARDS.MYSHOWDOWNS) {
            contest.categoryName = `${SHOWDOWN_CARDS.MY_LEADERBOARDS}${contest.displayCount}${')'}`;
        } else if (contest.category === SHOWDOWN_CARDS.LAST7DAYS) {
            contest.categoryName = SHOWDOWN_CARDS.LAST_7_DAYS;
        } else if (isTodayorTomorrow) {
            contest.categoryName = SHOWDOWN_CARDS.DAYS[isTodayorTomorrow];
        } else if (this.toCheckCategoryOrValidDate(contest.category)) {
            contest.categoryName = this.timeService.getFullDateFormatSuffixWithDay(new Date(contest.category));
        }
    }

    /**
     * To Check contest category has Valid date or contest
     * @param  {string} date
     * @returns boolean
     */
    private toCheckCategoryOrValidDate(date: string): boolean {
        const dateObj = new Date(date);
        return dateObj instanceof Date && !isNaN(dateObj.valueOf());
    }

    /**
     * To Check contest date is today or tomorrow
     * @param  {string} date
     * @returns string
     */
    private checkDateIsTodayOrTomorrow(date: string): string {
        if (this.toCheckCategoryOrValidDate(date)) {
            const day = this.timeService.determineDay(date, false);
            const todayOrTomorrow = SHOWDOWN_CARDS.DAY_CATEGORIES.includes(day);
            return todayOrTomorrow ? day : null;
        }
        return null;
    }

    /**
     * Listens to the post user login event
     * @returns void
     */
    private postUserLoginTrigger(): void {
        this.pubSubService.subscribe(this.title, [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], () => {
                if (!this.bonusSuppression.checkIfYellowFlagDisabled(this.moduleName)) {
                    this.bonusSuppression.navigateAwayForRGYellowCustomer();
                }
            this.showTutorialIndex = undefined;
            this.fetchAllShowdownContests();
        });
    }

    /**
     * Remove resulted contests fromm My Showdowns
     * @returns void
     */
    private removeResultedContestByEventId(): void {
        this.pubSubService.subscribe(this.title, PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED, (eventId: number) => {
            this.fiveASideShowDownLobbyService.removeResultedContestsFromCategory(this.displayContests, eventId);
        });
    }

    /**
     * Reloads the component when connection is lost and reconnected
     * @returns void
     */
    private reloadComponentListener(): void {
        this.pubSubService.subscribe(this.title, this.pubSubService.API.RELOAD_COMPONENTS, () => {
            this.liveServConnectionService.connect()
                .subscribe(() => {
                    this.showSpinner();
                    this.ngOnDestroy();
                    this.ngOnInit();
                });
        });
    }
}

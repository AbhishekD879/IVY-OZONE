import { Component, OnDestroy, OnInit, ChangeDetectorRef, Input } from '@angular/core';
import { Router, Event, NavigationEnd } from '@angular/router';
import { Subscription, Observable, from, of } from 'rxjs';
import { switchMap, mergeMap } from 'rxjs/operators';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { DeviceService } from '@core/services/device/device.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ServingService } from '@core/services/serving/serving.service';
import { BetslipTabsService } from '@core/services/betslipTabs/betslip-tabs.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CommandService } from '@core/services/communication/command/command.service';

import { IFooterMenu } from '@core/services/cms/models/menu/footer-menu.model';
import { ISystemConfig } from '@core/services/cms/models';
import { IOpenBetsCount } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import environment from '@environment/oxygenEnvConfig';
import { FiltersService } from '@core/services/filters/filters.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { MENU_ICONS_STATE } from '@app/lazy-modules/carouselMenu/components/carousel-menu.constant';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'footer-menu',
  templateUrl: 'footer-menu.component.html',
  styleUrls: ['footer-menu.component.scss'],
})

export class FooterMenuComponent implements OnInit, OnDestroy {
  @Input() showFooterMenu?: string;
  @Input() footerMenuVisible?: string;
  // Config object for currently selected betslip tab.
  betSlipActiveTab: { name: string } = { name: '' };
  // The list of all footer menu links.
  // The list of filtered footer menu links.
  footerLinks: IFooterMenu[];
  routeChangeSuccessHandler: Subscription;
  unsubscribeBetsCounter: Subscription;
  environments:any;
  animate: boolean = false;
  animateOpenBetsCounter: number = 0;
  moreThanTwenty: boolean = false;
  openBetsCounter: number = 0;

  private readonly title = 'footerMenu';
  onBoardingData:any;

  constructor(
    private cmsService: CmsService,
    private userService: UserService,
    private casinoLinkService: CasinoLinkService,
    private pubSubService: PubSubService,
    private betslipTabsService: BetslipTabsService,
    private deviceService: DeviceService,
    private gtmService: GtmService,
    private servingService: ServingService,
    private router: Router,
    private navigationService: NavigationService,
    private commandService: CommandService,
    private cd: ChangeDetectorRef,
    private storageService: StorageService,
    private sessionStorageService: SessionStorageService,
    private filtersService: FiltersService,
    public windowRef: WindowRefService,
    private bonusSuppressionService: BonusSuppressionService
  ) { }

  ngOnInit(): void {
    this.environments=environment.brand;
    this.getLinks();
    this.pubSubService.subscribe(
        this.title, this.pubSubService.API.SESSION_LOGOUT, () => {
          this.getLinks();
      }
    );
    this.pubSubService.publishSync(this.pubSubService.API.FOOTER_MENU_READY);

    this.pubSubService.subscribe(
      this.title, [this.pubSubService.API.SESSION_LOGIN,
      this.pubSubService.API.SEGMENTED_INIT_FE_REFRESH], () => {
          this.getLinks();

        this.handleMyBetsCount(); // load myBets count information after login
      }
    );
    this.pubSubService.subscribe(this.title, this.pubSubService.API.DEVICE_VIEW_TYPE_CHANGED_NEW, () => this.updateLinksState());
    this.pubSubService.subscribe(this.title, this.pubSubService.API.APP_BUILD_VERSION, (appBuildVersion: string) => {
      this.getLinks(appBuildVersion);
    });
    this.pubSubService.subscribe(this.title, this.pubSubService.API.FIRST_BET, () => {
      this.onBoardingData.tutorialEnabled = false;
    });
    /**
     * Clears active state for bottom button which has redirect to betSlip if location changed,
     *   because focus on betslip is missed.
     */
    this.routeChangeSuccessHandler = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        if (this.betSlipActiveTab.name) {
          this.betSlipActiveTab.name = '';
        }

        this.updateLinksState();
      }
    });

    if (this.userService.status) {
      this.handleMyBetsCount(); // load myBets count information after login
    }

    if(this.sessionStorageService.get('firstBetTutorialAvailable')) {
      this.setOnboardingData();
    }
    
    this.pubSubService.subscribe('onBoardingFirstBet', this.pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL, (onBoarding:{step: string, tutorialEnabled: boolean}) => {
      onBoarding.step === 'pickYourBet' ? this.setOnboardingData() : this.onBoardingData = onBoarding;
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);

    if (this.routeChangeSuccessHandler) {
      this.routeChangeSuccessHandler.unsubscribe();
    }

    this.commandService.executeAsync(this.commandService.API.UNSUBSCRIBE_OPEN_BETS_COUNT);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Performs navigation to specific place in betSlip widget
   *
   * @param {MouseEvent} $event
   * @param {Object} link
   */
  customRedirect($event: MouseEvent, link: IFooterMenu): void {
    $event.preventDefault();

    if (link.redirectUrl) {
      this.navigationService.openUrl(link.redirectUrl, true);
    }

    this.navigationTracking(link.linkTitle);
    // Send cookies if link is external TODO seems no longer required
    this.servingService.sendExternalCookies(link.relUri);
    // get link to redirect in betSlip
    this.betSlipActiveTab.name = this.betslipTabsService.redirectToBetSlipTab(link.linkTitle);
    // Update state of bottom links.
    this.updateLinksState();
  }

  private setOnboardingData(): void {
    if (this.sessionStorageService.get('betPlaced')) {
      return;
    }
    const betsPlaced = this.storageService.get("betSelections");
    const stepSelection = betsPlaced && betsPlaced.length ? 'addSelection' : 'pickYourBet';
    this.onBoardingData = {step: stepSelection, tutorialEnabled: this.sessionStorageService.get('firstBetTutorialAvailable')};
  }


/**
 * to add class for icon at pressed state
 * @param link 
 */
  iconPressedState(link) {
    this.addClass(link.linkTitle, MENU_ICONS_STATE.ICON_PRESSED);
    this.addClass(link.id, MENU_ICONS_STATE.ICON_PRESSED_STATE);
    this.removeClass(link.id, MENU_ICONS_STATE.ICON_DEFAULT_STATE);
  }

  /**
   * to add class for icon at default state
   * @param link 
   */
  iconDefaultState(link) {
    this.addClass(link.linkTitle, MENU_ICONS_STATE.ICON_DEFAULT);
    this.addClass(link.id, MENU_ICONS_STATE.ICON_DEFAULT_STATE);
    this.removeClass(link.id, MENU_ICONS_STATE.ICON_PRESSED_STATE);
  }

  /**
   * add class by id for svg icon at pressed state
   * @param link 
   * @param event 
   */
  addClass(link: string, event: string) {
    this.windowRef.document.getElementById(link).classList.add(event);
  }

  /**
   * remove class by id for svg icon at default state
   * @param link 
   * @param event 
   */
  removeClass(link: string, event: string) {
    this.windowRef.document.getElementById(link).classList.remove(event);
  }

  /**
   * Checks if given link is currently active based on current location and selected tab in
   *   betslip widget.
   * @param {Object} link
   * @return {boolean}
   */
  private isActiveLink(link: IFooterMenu): boolean {
    if (this.betSlipActiveTab.name) {
      return this.betSlipActiveTab.name === link.linkTitle;
    }

    return this.servingService.getClass(link.targetUri);
  }

  /**
   * Updates redirection url and "active" class for the list of links.
   * @param {Array=} links
   */
  private updateLinksState(links: IFooterMenu[] = this.footerLinks): void {
    const pagesWithLinks = ['My Bets', 'Cash Out'],
      isMobile = this.deviceService.isMobile || this.deviceService.isTablet;

    _.each(links, (link: IFooterMenu) => {
      link.redirectUrl = !isMobile && _.contains(pagesWithLinks, link.linkTitle) ? '' : link.targetUri;
      if(link.targetUri.includes('racingsuperseries')){
        this.filtersService.filterLinkforRSS(link.targetUri).subscribe(data =>{
          link.targetUri = data;
        })
       }
      link.isActive = this.isActiveLink(link);
    });

    this.cd.detectChanges();
  }

  /**
   * Tracking - Navigation of footer menu
   * @param {string} linkTitle
   */
  private navigationTracking(linkTitle: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'navigation',
      eventAction: 'footer',
      eventLabel: linkTitle
    });
  }

  /**
   * Retrieves footer menu links from CMS.
   * @private
   * @args appbuildVersion is sent for ioS devices
   */
  private getLinks(appBuildVersion?: string): void {
    this.cmsService.getFooterMenu(appBuildVersion).subscribe((data: IFooterMenu[]) => {
      // #remove-hash code above should be removed after CMS remove #.
      _.each(data, (link: IFooterMenu) => {
        link.targetUri = link.targetUri.replace('#/', '/');
      });
      const status = !this.userService.status ? 'loggedIn' : 'loggedOut';
      const footerLinks = _.difference(data, _.where(data, { showItemFor: status }));

      // Find link to mcasino in Menu elements and add custom parameter 'deliveryPlatform' depending on
      // whether user using Wrapper or HTML5 app in browser
      this.footerLinks = _.map(footerLinks, link => {
        link.targetUri = this.casinoLinkService.uriDecoration(link.targetUri);
        return link;
      });
      this.cd.detectChanges();
      this.userService.status && this.filterFooterBasedOnRgyellow();
      this.updateLinksState(this.footerLinks);
    });
  }

  private handleMyBetsCount(): void {
    this.cmsService.getSystemConfig()
      .pipe(mergeMap((config: ISystemConfig): Observable<IOpenBetsCount | {}> => {
        if (config.BetsCounter && config.BetsCounter.enabled) {
          return this.getOpenBetsCount();
        } else {
          return of({});
        }
      }))
      .subscribe((val: IOpenBetsCount) => {
        this.animateOpenBetsCount(val);
      }
    );
  }

  private getOpenBetsCount(): Observable<IOpenBetsCount> {
    const observableFromPromise = from(this.commandService.executeAsync(this.commandService.API.GET_OPEN_BETS_COUNT));

    return observableFromPromise.pipe(switchMap((value: Observable<IOpenBetsCount>) => value));
  }

  private animateOpenBetsCount(value: IOpenBetsCount): void {
    if (value && (this.animateOpenBetsCounter !== value.count || value.count === 20)) {
      this.animate = false;
      this.cd.detectChanges();
      requestAnimationFrame(() => {
        this.moreThanTwenty = value.moreThanTwenty;
        this.animate = true;
        this.animateOpenBetsCounter = value.count;
        this.openBetsCounter = value.moreThanTwenty ? 20 : value.count || 0;
        this.cd.detectChanges();
      });
    }
  }

  /**
 * Filter set correct links
 */
  filterFooterBasedOnRgyellow(): void {
    this.footerLinks = this.footerLinks.filter((link: IFooterMenu) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(link.linkTitle);
    })
  }
}

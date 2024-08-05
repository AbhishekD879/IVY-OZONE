import { Component, OnInit, OnDestroy, ComponentFactoryResolver, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { RetailPageComponent as OxygenRetailPageComponent } from '@app/retail/components/retailPage/retail-page.component';
import { UserService } from '@core/services/user/user.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { IStaticBlock, ISystemConfig } from '@app/core/services/cms/models';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { FOOTBALL_FILTER_CONFIRM, GRID_GA_TRACKING } from '@app/retail/constants/retail.constant';
import { DialogService } from '@core/services/dialogService/dialog.service';
import {
  FootballFilterConfirmDialogComponent
} from '@app/retail/components/footballFilterConfirmDialog/football-filter-confirm-dialog.component';
import { BetFilterParamsService } from '@app/retail/services/betFilterParams/bet-filter-params.service';
import { IBetFilterParams } from '@app/retail/services/betFilterParams/bet-filter-params.model';
import { NavigationService } from '@app/core/services/navigation/navigation.service';
import { forkJoin, Subscription } from 'rxjs';
import { UPGRADE_ACCOUNT_DIALOG, LINK_TITLE, RETAIL_PAGE } from '@ladbrokesMobile/retail/constants/retail.constant';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
@Component({
  selector: 'retail-page',
  templateUrl: 'retail-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class RetailPageComponent extends OxygenRetailPageComponent implements OnInit, OnDestroy {
  readonly RETAIL_CONST = RETAIL_PAGE;
  readonly INSHOP: string = 'inshop';
  readonly FOOTBALL_BET_FILTER_INSHOP: string = '/bet-filter';
  readonly FOOTBALL_BET_FILTER_ONLINE: string = '/bet-filter/filter/your-teams?';
  readonly SERVICE_NAME: string = 'userLoginOnHub';
  upgradeButtonContent: SafeHtml;
  showUpgradeButton: boolean;
  isUpgradeEnable: boolean;
  showRetailHeader: boolean;
  disableDefaultNavigation: boolean = true;
  footBallContentOnline: SafeHtml = null;
  footBallContentInshop: SafeHtml = null;
  linkTitle: string = null;
  private subscription: Subscription;
  private upgradeSubscription: Subscription;
  private staticBlockSubscription: Subscription;

  constructor(
    private userService: UserService,
    private localeService: LocaleService,
    private cmsService: CmsService,
    private domSanitizer: DomSanitizer,
    private pubSubService: PubSubService,
    private navigationService: NavigationService,
    private dialogService: DialogService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private betFilterParamsService: BetFilterParamsService,
    private gtmService: GtmService,
    private changeDetectorRef: ChangeDetectorRef,
    private windowRef: WindowRefService
  ) {
    super();
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.configUpgradeButton();
    this.pubSubService.subscribe(this.SERVICE_NAME,
    [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
      this.configUpgradeButton();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.SERVICE_NAME);
    this.subscription && this.subscription.unsubscribe();
    this.upgradeSubscription && this.upgradeSubscription.unsubscribe();
    this.staticBlockSubscription && this.staticBlockSubscription.unsubscribe();
  }

  /**
   * Showing Football Betfiler Confirm popup
   */
  showFootballFilterConfirmDialog() {
    this.subscription = forkJoin([
      this.cmsService.getStaticBlock(FOOTBALL_FILTER_CONFIRM.CONFIRM_ONLINE, null),
      this.cmsService.getStaticBlock(FOOTBALL_FILTER_CONFIRM.CONFIRM_INSHOP, null)
    ]).subscribe(results => {
      this.footBallContentOnline = this.domSanitizer.bypassSecurityTrustHtml(results[0].htmlMarkup);
      this.footBallContentInshop = this.domSanitizer.bypassSecurityTrustHtml(results[1].htmlMarkup);
      this.dialogService.openDialog(
        'RetailFootballFilterConfirmation',
        this.componentFactoryResolver.resolveComponentFactory(FootballFilterConfirmDialogComponent),
        true, {
        inshopCouponText: this.footBallContentInshop,
        onlineCouponText: this.footBallContentOnline,
        footBallBetFilter: FOOTBALL_FILTER_CONFIRM.DEFAULT_RADIO_BUTTON,
        buttons: [{
          handler: this.handleAccaMoreClick.bind(this)
        }]
      });
    });
  }

  /**
   * Handling popup button actions
   * @return {void}
   */
  handleAccaMoreClick(footBallBetFilterType: 'online' | 'inshop'): void {
    const params: IBetFilterParams = {};
    this.dialogService.closeDialogs();
    params.mode = footBallBetFilterType;
    params.pathname = this.windowRef.nativeWindow.location.pathname;
    if (footBallBetFilterType === this.INSHOP) {
      this.betFilterParamsService.betFilterParams = params;
      this.navigationService.openUrl(this.FOOTBALL_BET_FILTER_INSHOP);
    } else {
      this.betFilterParamsService.betFilterParams = params;
      this.navigationService.openUrl(this.FOOTBALL_BET_FILTER_ONLINE);
    }
  }

  /**
   * @param {string} linkTitle
   * @return {boolean} - returns true value.
   */
  trackUpgradeNavigation(linkTitle: string): boolean {
    GRID_GA_TRACKING.eventLabel = linkTitle;
    GRID_GA_TRACKING.eventAction = 'Menu';
    this.gtmService.push('trackEvent', GRID_GA_TRACKING);
    return true;
  }

  private configUpgradeButton(): void {
    this.upgradeSubscription = this.cmsService.getSystemConfig().subscribe((data: ISystemConfig) => {
      this.isUpgradeEnable = data.Connect && data.Connect.upgrade; // TODO: rename to retail after changes in cms.
      this.showUpgradeButton = (this.userService.status && !this.userService.isMultiChannelUser()) && this.isUpgradeEnable;

      if (this.userService.isInShopUser() && this.showUpgradeButton) {
        this.linkTitle = LINK_TITLE.useGridOnline;
        this.getUpgradeButtonStaticBlock(UPGRADE_ACCOUNT_DIALOG.inshopUpgrade.dialogButton);
      } else if (!this.userService.isRetailUser() && this.showUpgradeButton) {
        this.linkTitle = LINK_TITLE.activateCard;
        this.getUpgradeButtonStaticBlock(UPGRADE_ACCOUNT_DIALOG.onlineUpgrade.dialogButton);
      }
    });
  }

  private getUpgradeButtonStaticBlock(blockName: string): void {
    this.staticBlockSubscription = this.cmsService.getStaticBlock(blockName, this.localeService.getLocale().toLowerCase())
      .subscribe((cmsContent: IStaticBlock) => {
        this.upgradeButtonContent = this.domSanitizer.bypassSecurityTrustHtml(cmsContent.htmlMarkup);
        this.changeDetectorRef.markForCheck();
      }, err => {
        console.warn('An error occured when loading button content from CMS', err);
    });
  }
}

import { map, concatMap } from 'rxjs/operators';
import {
  Component,
  ElementRef,
  HostListener,
  OnDestroy,
  OnInit,
  ViewEncapsulation,
  ChangeDetectorRef,
  Output,
  EventEmitter,
  ComponentFactoryResolver
} from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { ILeaderBoard, INavigationGroup, INavItem, IPromotionsSiteCoreBanner, ISpPromotion } from '@promotions/models/sp-promotion.model';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { NgInfoPanelComponent } from '@shared/components/infoPanel/ng-info-panel.component';
import { DynamicComponentsService } from '@core/services/dynamicComponents/dynamic-components.service';
import { IDynamicComponent } from '@core/services/dynamicComponents/dynamic-components.model';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ICheckStatusResponse } from '@promotions/models/response.model';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { SiteServerService } from '@app/core/services/siteServer/site-server.service';
import { ISelectionType } from '@app/core/models/selectiontype.model';
import { PROMOTION, GREYHOUND_RACING, HORSE_RACING } from '@app/promotions/constants/promotion-description';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@app/core/models/market.model';
import { IOutcome } from '@app/core/models/outcome.model';
import { IFilterType } from '@app/core/models/filter-type.model';
import { ChannelService } from '@app/core/services/liveServ/channel.service';
import { CacheEventsService } from '@app/core/services/cacheEvents/cache-events.service';
import { UpdateEventService } from '@app/core/services/updateEvent/update-event.service';
import {ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { PromotionsNavigationService } from '@promotions/services/promotions/promotions-navigation.service';
import { PromotionConfirmDialogComponent } from '@app/promotions/components/promotionConfirmDialog/promotion-confirm-dialog.component';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UserService } from '@core/services/user/user.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { rgyellow } from '@bma/constants/rg-yellow.constant';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';
import { SafeHtml } from '@angular/platform-browser';
import { LEADERBOARD_CONSTANTS } from '@lazy-modules/promoLeaderBoard/constants/leaderboard-constants';
import environment from '@environment/oxygenEnvConfig';import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { IBppResponse, IFreebetOffer } from '@app/bpp/services/bppProviders/bpp-providers.model';

@Component({
  selector: 'promotion-details',
  templateUrl: './promotion-details.component.html',
  styleUrls: ['../../assets/styles/main.scss', './promotion-details.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class PromotionDetailsComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  sysConfig: ISystemConfig;
  promotion: ISpPromotion;
  validPromotion: ISpPromotion;
  isExpanded: boolean[] = [true, true];
  promoDescriptionContentArr: ISelectionType[] = [];
  selectionIds: string[] = [];
  freeRideFlag: boolean;
  freeRideErrorFlag: boolean;
  notAvailable: string = PROMOTION.notAvailable;
  @Output() readonly customPromotion: EventEmitter<string> = new EventEmitter<string>();
  siteCorePromotions: ISiteCoreTeaserFromServer[];
  navGroups: INavigationGroup[] = [];
  navGroupItem: INavItem[] = [];
  leaderBoardList: ILeaderBoard[] = [];
  lbConfigData: ILeaderBoard;
  leaderBoardConfigId: string;
  descriptionTxt: SafeHtml;
  isLeaderBoard: boolean = false;
  activeNav: string;
  isCoral: boolean;
  readonly BRAND: string = this.cmsService.brand;

  private readonly COMPONENT_NAME: string = 'PromotionDetailsComponent';

  private timeoutInstance: any = null;
  private optInButton: HTMLElement = null;
  private optInButtonClicked: boolean = false;
  private infoPanelComponent: IDynamicComponent = null;
  private lastLoginStatus: boolean;
  private COMPILATION_DELAY: number = 300;
  private eventListeners: Function[] = [];
  private optInButtonListeners: Function[] = [];
  private readonly moduleName: string = rgyellow.PROMOTIONS;

  constructor(
    public userService: UserService,
    private promotionsService: PromotionsService,
    private promotionsNavigationService: PromotionsNavigationService,
    private pubSubService: PubSubService,
    private rendererService: RendererService,
    private elementRef: ElementRef,
    private domToolsService: DomToolsService,
    private cmsService: CmsService,
    private dynamicComponentsService: DynamicComponentsService,
    private router: Router,
    private route: ActivatedRoute,
    private changeDetectorRef: ChangeDetectorRef,
    private siteServerService: SiteServerService,
    private channelService: ChannelService,
    private cacheEventsService: CacheEventsService,
    private updateEventService: UpdateEventService,
    public dialogService: DialogService,
    public freeRideHelperService: FreeRideHelperService,
    public device: DeviceService,
    public componentFactoryResolver: ComponentFactoryResolver,
    private gtmService: GtmService,
    protected bonusSuppressionService: BonusSuppressionService,
    private bppService:BppService
  ) {
    super();

    this.optInButtonHandler = this.optInButtonHandler.bind(this);
    this.promoFired = this.promoFired.bind(this);
    this.promoNotFired = this.promoNotFired.bind(this);
    this.sendGTM = this.sendGTM.bind(this);
  }

  ngOnInit(): void {
    // GetPromotions from sitecore
    this.isCoral = environment && environment.brand === 'bma';
    this.promotionsService.getPromotionsFromSiteCore().subscribe((response: IPromotionsSiteCoreBanner[]) => {
      this.siteCorePromotions = response.length > 0 ? response[0].teasers : [];
      this.initPromo();
    });
    this.route.params.pipe(concatMap((params: Params) => {
      this.showSpinner();
      return this.cmsService.getSystemConfig().pipe(
        map((systemConfig: ISystemConfig) => {
          this.sysConfig = systemConfig;
          return params.promoKey;
        }));
    }),
      concatMap((promoKey: string) => {
        return this.promotionsService.promotionData(promoKey);
      }))
      .subscribe((promotionData: ISpPromotion) => {
        this.promotion = promotionData;
        this.checkPromotionType();
        this.init();
        this.hideSpinner();
      }, () => {
        this.showError();
        this.hideSpinner();
      });

      this.pubSubService.subscribe(this.COMPONENT_NAME, this.pubSubService.API.SESSION_LOGIN, () => {
          if (!this.bonusSuppressionService.checkIfYellowFlagDisabled(this.moduleName)) {
            this.bonusSuppressionService.navigateAwayForRGYellowCustomer();
          }
      });
  }

  ngOnDestroy(): void {
    this.timeoutInstance && clearTimeout(this.timeoutInstance);
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'dynamic-promotion');
    this.pubSubService.unsubscribe(this.COMPONENT_NAME);
    this.cacheEventsService.clearByName('event');
    // remove all renderer.listen listeners
    _.each(this.eventListeners, removeEventListener => {
      removeEventListener();
    });
  }

  changeAccordionState(index: number, value: boolean): void {
    this.isExpanded[index] = value;
    this.changeDetectorRef.detectChanges();
  }

  @HostListener('click', ['$event'])
  checkRedirect(event: MouseEvent): void {
    const redirectUrl: string = (<HTMLElement>event.target).dataset.routerlink;
    try {
      this.handleGtmTracking(event);
    } catch (e) {
      console.warn(e);
    }
    if (redirectUrl) {
      this.router.navigateByUrl(redirectUrl);
    }
  }

  /**
   * get PromotionConfirmDialogComponent
   */
  get dialogComponent() {
    return PromotionConfirmDialogComponent;
  }

  /**
   * check to display historic prices only for GH and HR
   */
  public isRacingEvent(event: ISportEvent): boolean {
    return (event.categoryId === GREYHOUND_RACING || event.categoryId === HORSE_RACING) ? true : false;
  }

  /**
   * checks for freeRide
   */
  public checkFreeRide() {
    this.freeRideErrorFlag = false;
    this.freeRideHelperService.showFreeRide() ? this.freeRideFlag = true : this.freeRideErrorFlag = true;
  }

  private init(): void {
    this.lastLoginStatus = this.promotionsService.isUserLoggedIn();

    // Waits for login state change (like login process started and login process finished)
    this.pubSubService.subscribe(this.COMPONENT_NAME, this.pubSubService.API.LOGIN_PENDING, status => {
      if (status && this.validPromotion && this.optInButton) {
        this.disableOptInButton();
      }
    });

    // Waits for login failed
    this.pubSubService.subscribe(this.COMPONENT_NAME, this.pubSubService.API.SET_LOGOUT_STATUS, () => {
      if (this.validPromotion && this.optInButton) {
        this.enableOptInButton();
      }
    });

    /*
     * Waits for login process (have to wait until login and vip statuses will be refreshed to be able to
     * filter promotions corresponding to user's vip level) to be completed and make auto startOptIn or
     * manual by user's click
     */
    this.pubSubService.subscribe(this.COMPONENT_NAME, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.lastLoginStatus = this.promotionsService.isUserLoggedIn();
      if (this.validPromotion && this.optInButton) {
        this.enableOptInButton();        
        this.getOptInStatus(this.validPromotion.requestId);
      }
    });

    // Waits for logout - here is the main case - server unexpectedly log out User from App
    this.pubSubService.subscribe(this.COMPONENT_NAME, [this.pubSubService.API.SESSION_LOGOUT], () => {
      if (this.lastLoginStatus !== this.promotionsService.isUserLoggedIn()) {
        this.initPromo();
      }
    });

    this.initPromo();
  }

  /**
   * Array of selection IDs are sliced to use it in api call
   */
  private getChannels(data: ISelectionType[]): string[] {
    const channelIds = [];
    data.forEach((outcome: ISelectionType) => {
      if (!!outcome.eventInfo) {
        channelIds.push(outcome.eventInfo.outcome.liveServChannels.slice(0, -1));
        channelIds.push(outcome.eventInfo.market.liveServChannels.slice(0, -1));
        channelIds.push(outcome.eventInfo.event.liveServChannels.slice(0, -1));
      }
    });
    return channelIds;
  }

  private optInButtonHandler(e: MouseEvent): void {
    e.preventDefault();
    e.stopPropagation();

    this.infoPanelComponent && this.infoPanelComponent.instance.hideInfoPanel();
    this.optInButtonClicked = true;
    if (!this.promotionsService.isUserLoggedIn()) {
      this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'optin' });
      return;
    }
    this.disableOptInButton();
    this.startOptIn();
  }

  private initPromo(): void {
    if (this.promotion) {
      const promotions = this.promotionsService.preparePromotions([this.promotion], this.siteCorePromotions);

      /*
       * Find link to mcasino in html source and add custom parameter 'deliveryPlatform' depending on
       * whether user using Wrapper or HTML5 app in browser
       */
      this.validPromotion = promotions.length && promotions[0];
      if (this.validPromotion) {
        if (this.promoDescriptionContentArr.length !== 0) {
          return;
        }
        this.populatePromoData(this.validPromotion.description);
        if (this.validPromotion.navigationGroupId) {
          this.promotionsNavigationService.isNavGroup.subscribe({
            next: (response: INavigationGroup[]) => {
              this.navGroups = response;
              this.getLeaderBoards();
              this.navGroupItem = (this.getNavGroup(this.validPromotion.navigationGroupId).length > 0) ? this.getNavGroup(this.validPromotion.navigationGroupId)[0].navItems : [];
            }

          });
          if (this.navGroups.length == 0) {
            this.promotionsNavigationService.getNavigationGroups().subscribe((navData: INavigationGroup[]) => {
              this.promotionsNavigationService.setNavGroupData(navData);        
            });
          }
        }
        this.validPromotion.safeDescription = this.promotionsService.decorateLinkAndTrust(this.validPromotion.description);
        this.validPromotion.safeHtmlMarkup = this.promotionsService.decorateLinkAndTrust(this.validPromotion.htmlMarkup);

        if (this.validPromotion.requestId) {
          this.initPromotionButton();
        }
      }
    }
  }

  /**
   * finds the nav group with provided id
   * @param {string} id
   * @returns INavigationGroup
   */
  private getNavGroup(id: string): INavigationGroup[] {
    return this.navGroups.filter((nav: INavigationGroup) => nav.id == id);
  }

  /**
   * HTML content is added into an array and separates all the buttons as separate element of an array
   * after checking if its a button tag or normal button string
   */
  private populatePromoData(promoDescription: string): void {
    const promoData: string = promoDescription.replace(/contenteditable="true"/g, 'contenteditable="false"').
      replace(/<button/g, '@splitButton<button').replace(/<\/button>/g, '</button>@splitButton');
    const parsedPromoDataArr: string[] = promoData.split('@splitButton');
    this.populatePromoDescContentArr(parsedPromoDataArr);
  }

  /**
   * selection ids are identified from the dynamic buttons id and betPackBtn
   */
  private populatePromoDescContentArr(parsedPromoDataArr: string[]): void {
    parsedPromoDataArr.forEach((parsedPromoData: string) => {
      const dynamicBtnIdIndex = parsedPromoData.search('dynamicbtn');
      const betPackBtn = parsedPromoData.search('bet-pack-btn');

      if (betPackBtn !== -1) {
        this.initBetpack();
      }

      if (dynamicBtnIdIndex !== -1) {
        this.promoDescriptionContentArr.push({
          isSelectionIdAvailable: true,
          selection: parsedPromoData.substr(dynamicBtnIdIndex + 11).split('\"')[0],
          eventInfo: null
        });
        this.selectionIds.push(parsedPromoData.substr(dynamicBtnIdIndex + 11).split('\"')[0]);
      } else {
        this.promoDescriptionContentArr.push({
          isSelectionIdAvailable: false,
          htmlCont: this.promotionsService.decorateLinkAndTrust(parsedPromoData)
        });
      }
    });
    this.getDynamicButtonDetails(this.selectionIds);
  }

  /**
   * Enable button, add and remember listeners
   */
  private enableOptInButton(): void {
    if (!this.optInButton || !this.optInButtonHandler) { return; }

    this.optInButtonListeners.push(
      this.promotionsService.enableOptInButton(this.optInButton, this.optInButtonHandler)
    );
  }

  /**
   * Disable button, cancel added listeners
   */
  private disableOptInButton(): void {
    if (!this.optInButton) { return; }

    this.promotionsService.disableOptInButton(this.optInButton, this.optInButtonListeners);
  }

  /**
   * initializing Promotion Buttons GTM tracking functionality
   */
  private handleGtmTracking(event): void {
    const promoDescriptionId: string = 'promo-descr'; // all promo links
    const termsAndConditions: string = 'terms-and-cond'; // all T&C links
    const idPath: string = event.path.map(node => node.id).toString();

    if (!event.target || event.target.nodeName !== 'A') {
      return;
    }

    if (idPath.indexOf(promoDescriptionId) > -1 || idPath.indexOf(termsAndConditions) > -1) {
      this.sendGTM(event);
    }
  }

  private sendGTM(event: MouseEvent): void {
    this.promotionsService.sendGTM(this.validPromotion, event, true);
  }

  /**
   * initializing Promotion Button functionality
   */
  private initPromotionButton(): void {
    this.timeoutInstance && clearTimeout(this.timeoutInstance);

    this.timeoutInstance = setTimeout(() => {
      this.optInButton = this.elementRef.nativeElement.querySelector('.handle-opt-in');

      if (this.optInButton) {
        this.domToolsService.removeClass(
          this.optInButton,
          'hidden'
        );

        // add click listener for Opt in Button
        const listener = this.rendererService.renderer.listen(this.optInButton, 'click', this.optInButtonHandler);
        this.eventListeners.push(listener);
        this.optInButtonListeners.push(listener);
      }
      if(this.promotionsService.isUserLoggedIn()){       
         this.getOptInStatus(this.validPromotion.requestId);
      }
    }, this.COMPILATION_DELAY);
  }
     /**
   * checks optin status 'accountOffers' and 'accountFreebetsWithNoLimits' calls
   * @param tirggerId
   */
  private getOptInStatus(tirggerId: string) {   
      this.disableOptInButton(); 
      this.bppService.send('accountOffers').subscribe((res: IBppResponse) => {
        res['response'].model.freebetOffer ? this.checkOptinTrigger(res['response'].model.freebetOffer, tirggerId) : this.CheckInClaimedOffers(tirggerId);
      });    
  }
   /**
   * checks optin status 'accountOffers' call and disable the optin button
   * @param IFreebetOffer
   * @param tirggerId
   */
  private checkOptinTrigger(offers, tirggerId: string) {
    const status = offers.some((offer: IFreebetOffer) => offer.freebetTrigger && offer.freebetTrigger.some(triggerData => triggerData.freebetTriggerId === tirggerId && triggerData.freebetTriggeredDate));
    !status && this.CheckInClaimedOffers(tirggerId);
    status&&this.changeOptinText()
}
/**
   * checks optin status 'accountFreebetsWithNoLimits' call and disable the optin button
   * @param IFreebetOffer
   * @param tirggerId
   */
  private CheckInClaimedOffers(tirggerId: string) {
    this.bppService.send('accountFreebetsWithNoLimits').subscribe((offers: any) => {
    const offerStatus = offers.response.model.freebetOffer?offers.response.model.freebetOffer.some(offer => offer.freebetTrigger && offer.freebetTrigger.some(triggerData => triggerData.freebetTriggerId === tirggerId)):this.enableOptInButton();
    !offerStatus && this.enableOptInButton();
    offerStatus&&this.changeOptinText()
    })
  }
    /**
   * change the optin text
   */
  private changeOptinText() {
    this.promotionsService.changeBtnLabel(this.sysConfig.OptInMessagging.alreadyOptedInMessage, this.optInButton);
  }
  /**
   * checks Promotion Status and call needed callback
   * @param firedCallBack
   * @param notFiredCallBack
   */
  private checkPromotionStatus(firedCallBack: Function, notFiredCallBack: Function): void {
    this.promotionsService.checkStatus(this.validPromotion.requestId)
      .subscribe((response: ICheckStatusResponse) => {
        if (response.fired) {
          firedCallBack();
        } else {
          notFiredCallBack();
        }
      }, () => {
        console.warn('checkPromotionStatus failed');
        notFiredCallBack();
      });
  }
 
  /**
   * behavior for fired promotion
   */
  private promoFired(): void {
    this.promotionsService.changeBtnLabel(this.sysConfig.OptInMessagging.alreadyOptedInMessage, this.optInButton);
  }

  /**
   * behavior for not fired promotion
   */
  private promoNotFired(): void {
    if (this.optInButtonClicked) {
      this.optInButtonClicked = false;
      this.startOptIn();
    } else {
      this.enableOptInButton();
    }
  }

  /**
   * Start the Opt In functionality.
   */
  private startOptIn(): void {
    this.promotionsService.storeId(this.validPromotion.requestId)
      .subscribe(storeResponse => {
        if (storeResponse.fired) {
          this.promotionsService.changeBtnLabel(this.sysConfig.OptInMessagging.successMessage, this.optInButton);
        } else {
          this.infoPanelWarningMessage();
          this.enableOptInButton();
        }
      }, () => {
        this.infoPanelWarningMessage();
        this.enableOptInButton();
      });
  }

  /**
   * data is fetched and added to local obj to render in template
   */
  private getDynamicButtonDetails(selectionIdList: string[]): void {
    const selectedPromoContentArr: ISelectionType[] = this.promoDescriptionContentArr;
    const filters: IFilterType = {
      includeUndisplayed: true,
      priceHistory: true,
      outcomesIds: selectionIdList
    };
    this.siteServerService.getEventsByOutcomeIds(filters, true)
      .then((eventDataResponse: ISportEvent[]) => {
        const allmarkets: IMarket[] = eventDataResponse.reduce(
          (marketAccumulator: IMarket[], eventItem: ISportEvent) => [...marketAccumulator, ...eventItem.markets], []);
        const allOutcomes: IOutcome[] = allmarkets.reduce(
          (outcomeAccumulator: IOutcome[], marketItem) => [...outcomeAccumulator, ...marketItem.outcomes], []);
        allOutcomes.forEach((outcome: IOutcome) => {
          if (filters.outcomesIds.includes(outcome.id)) {
            const selectedOutcomeIndex = selectedPromoContentArr.findIndex(selectedOutcome => (selectedOutcome.selection === outcome.id));
            const marketId = allOutcomes.find((outcomeItem: IOutcome) => outcomeItem.id === outcome.id).marketId;
            const eventId = allmarkets.find((marketItem: IMarket) => marketItem.id === marketId).eventId;
            selectedPromoContentArr[selectedOutcomeIndex].eventInfo = {
              'id': outcome.id,
              'event': eventDataResponse.find((eventItem: ISportEvent) => eventItem.id.toString() === eventId),
              'market': allmarkets.find((marketItem: IMarket) => marketItem.id === marketId),
              'outcome': outcome
            };
          }
        });
        this.liveConnection();
      });
  }

  /**
   * handler is called whenever data is received
   */
  private liveConnection(): void {
    this.cacheEventsService.store('event', 'dynamic-button', this.eventsArr());
    this.updateEventService.init();
    const channel = this.channelService.getLSChannelsFromArray(this.eventsArr());
    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'dynamic-promotion'
    });
  }

  private eventsArr() {
    const eventsArr: any = [];
    this.promoDescriptionContentArr.
      forEach((outcome: ISelectionType) => {
        if (outcome.eventInfo && outcome.eventInfo.event) {
          eventsArr.push(outcome.eventInfo.event);
        }
      });
    return eventsArr;
  }

  /**
   * Adds/shows ng-info-panel component and shows Warning Message
   */
  private infoPanelWarningMessage(): void {
    const message = this.sysConfig.OptInMessagging.errorMessage,
      type = 'warning',
      align = 'center';

    if (!this.infoPanelComponent) {
      this.infoPanelComponent = this.dynamicComponentsService.addComponent(
        NgInfoPanelComponent,
        { type, message, align },
        this.optInButton.parentNode,
        this.optInButton
      );
    } else {
      this.infoPanelComponent.instance.showInfoPanel(message, type);
    }
  }

  /**
   * Emits the promotion name based on the conditions
   */
  private checkPromotionType(): void {
    if (this.promotion.useCustomPromotionName && this.promotion.customPromotionName) {
      this.customPromotion.emit(this.promotion.customPromotionName);
    }
  }

  /**
   *  add click listener for Bet pack in Button
   */
  private initBetpack(): void {
    this.timeoutInstance && clearTimeout(this.timeoutInstance);
    this.timeoutInstance = setTimeout(() => {
      const el = this.elementRef.nativeElement.querySelector('.bet-pack-btn');
      if (el) {
        el.addEventListener('click', this.onClick.bind(this));
      }
    }, this.COMPILATION_DELAY);
  }

  /**
   * on event listener click
   */
  private onClick(e: MouseEvent): void {
    e.preventDefault();
    e.stopPropagation();
    this.callDialog();
    const buttonElement = e.target as HTMLElement;
    const gtmBtnClick = {
      event: 'trackEvent',
      eventAction: 'link click',
      eventCategory: 'promotions',
      eventLabel: this.validPromotion.title,
      vipLevel: this.userService.vipLevel,
      promoAction: buttonElement.innerHTML,
      promoType: 'Bet Pack – ' + this.validPromotion.betPack.offerId
    };
    this.gtmService.push('trackEvent', gtmBtnClick);
  }

  /**
   * open Login Dialog
   */
  private openLoginDialog() {
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'header' });
  }

  /**
   * Adds/shows promotion-confirm-dialog.component and pass betpack info
   */
  private callDialog(): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.dialogService.openDialog(DialogService.API.promotionDialog, componentFactory, true, {
      data: {
        promotion: this.promotion,
        callConfirm: (congratsMsg: any) => {
          this.confirm();
          this.dialogService.closeDialog(DialogService.API.promotionDialog);
        }
      }
    });
  }

  /**
   * On Confirm event of Dialog
   */
  private confirm(): void {
    this.validPromotion.htmlMarkup = null;
    this.validPromotion.description = null;
    this.validPromotion.safeCongratsMsg = this.promotionsService.decorateLinkAndTrust(this.promotion.betPack.congratsMsg);
  }

  closeDialogClick(event) {
    this.freeRideFlag = event.value;
  }

    /**
   * On Click of Nav Item
   */
  clickNavItem(item, event): void {
    if ((item && item.navType.includes(LEADERBOARD_CONSTANTS.NAVTYPE_LB) || item.navType.includes(LEADERBOARD_CONSTANTS.NAVTYPE_DESC))) {
      event && event.preventDefault();
      this.isLeaderBoard = true;
      this.leaderBoardConfigId = item.leaderboardId;
      this.descriptionTxt = item.descriptionTxt ? this.promotionsService.decorateLinkAndTrust(item.descriptionTxt) : null;
      this.activeNav = item.name;
      this.filterLeaderBoardById(this.leaderBoardConfigId);
    }
  }

   /**
   * get Leaderboards config
   */
  getLeaderBoards(): void {
    this.promotionsNavigationService.getLeaderBoards().subscribe((ldData: ILeaderBoard[]) => {
      this.leaderBoardList = ldData;
      const [navGroupItem] = this.navGroupItem;
      this.clickNavItem(navGroupItem, '');
    });
  }

  /**
   * filter Leaderboard by Id
   */
  filterLeaderBoardById(id): void {
    this.lbConfigData = this.leaderBoardList.find(leaderBoard => leaderBoard.id == id);
  }

  /**
   * get Class Name for Leaderbaord
   */
  getLbClassName(navGroup) {
    return {
      'nav-link': this.BRAND === LEADERBOARD_CONSTANTS.BRAND_NAME,
      'activeLads': this.activeNav === navGroup.name && this.BRAND === LEADERBOARD_CONSTANTS.BRAND_NAME,
      'activeCoral': this.activeNav === navGroup.name && this.BRAND === LEADERBOARD_CONSTANTS.BRAND_NAME_CORAL
    }
  }
}

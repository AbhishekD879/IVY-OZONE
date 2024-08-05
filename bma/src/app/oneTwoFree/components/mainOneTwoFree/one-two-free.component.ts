import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { forkJoin as observableForkJoin } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { AddToBetslipByOutcomeIdService } from '@betslipModule/services/addToBetslip/add-to-betslip-by-outcome-id.service';
import { AsyncScriptLoaderService } from '@coreModule/services/asyncScriptLoader/async-script-loader.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { WindowRefService } from '@coreModule/services/windowRef/window-ref.service';
import { ONE_TWO_FREE_EVENTS } from '@app/oneTwoFree/components/mainOneTwoFree/one-two-free.constants';
import { UserService } from '@core/services/user/user.service';
import { IOtfIosToggle, IOtfStaticContent } from '@core/services/cms/models';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';
import { rgyellow } from '@bma/constants/rg-yellow.constant';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { StorageService } from '@core/services/storage/storage.service';

@Component({
  selector: 'one-two-free',
  templateUrl: './one-two-free.component.html',
  styleUrls: ['./one-two-free.component.scss']
})
export class OneTwoFreeComponent implements OnInit, OnDestroy {
  isGuest: boolean = this.showSplashLogin();
  isInShopUser: boolean = this.userService.isInShopUser();
  otfLoadingTimeout: number = 20 * 1000; // 20 sec
  showBackButton: boolean = false;
  splashContent: string = this.localeService.getString('bma.otf.noContent');

  hiddenLoginModal: boolean = true;
  showIOSDialog: boolean = false;
  dialogContent: any;

  private tag: string = 'OneTwoFree';
  private BODY_CLASS: string = 'menu-opened';
  private moduleName = rgyellow.ONE_TWO_FREE;
  private readonly OTF_SEGMENT_STORE_KEYTEXT: string = 'OTF_SEGMENT';

  constructor(
    private windowRef: WindowRefService,
    private asyncLoad: AsyncScriptLoaderService,
    private router: Router,
    private pubSubService: PubSubService,
    private cmsService: CmsService,
    private addToBetslipService: AddToBetslipByOutcomeIdService,
    private userService: UserService,
    private deviceService: DeviceService,
    private routingState: RoutingState,
    protected localeService: LocaleService,
    private awsService: AWSFirehoseService,
    private domToolsService: DomToolsService,
    private bonusSuppressionService: BonusSuppressionService,
    protected serviceClosureService: ServiceClosureService,
    protected storageService:StorageService
  ) {
    this.destroyOneTwoFree = this.destroyOneTwoFree.bind(this);
    this.addToBetslip = this.addToBetslip.bind(this);
    this.goToBetting = this.goToBetting.bind(this);
    this.sendAwsRequest = this.sendAwsRequest.bind(this);
    this.updateOtfSegmentStorage = this.updateOtfSegmentStorage.bind(this);
  }

  ngOnInit(): void {
    this.cmsService.getOTFStaticContent()
      .subscribe(
        (data: IOtfStaticContent[]) => {
          if (data && data.length > 0) {
            this.splashContent = data.find((item: IOtfStaticContent) => !!item.pageName.toLowerCase().match('splash')).pageText1;
          }
        },
        (err) => this.awsService.addAction('1-2-free=>Get_OTFLoginStaticContent_Error', { error: err || 'no error data' })
      );

    this.checkIsIOSApp() ? this.getIosRedirectCmsData() : this.handleInit();
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM', true);
  }

  redirectHandler(): void {
    const route = this.routingState && this.routingState.getPreviousUrl();
    this.router
      .navigate([`${(route && route !== this.windowRef.nativeWindow.location.pathname) ? route : '/'}`]);
  }

  ngOnDestroy(): void {
    this.windowRef.document.removeEventListener(ONE_TWO_FREE_EVENTS.DESTROY_ONE_TWO_FREE, this.destroyOneTwoFree);
    this.windowRef.document.removeEventListener(ONE_TWO_FREE_EVENTS.ADD_TO_BETSLIP, this.addToBetslip);
    this.windowRef.document.removeEventListener(ONE_TWO_FREE_EVENTS.GO_TO_BETTING, this.goToBetting);
    this.windowRef.document.removeEventListener(ONE_TWO_FREE_EVENTS.OTF_NEW_RELIC, this.sendAwsRequest);
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM', false);
    this.pubSubService.unsubscribe(this.tag);
  }

  handleInit(): void {
    this.hiddenLoginModal = false;
    this.userService.status ?  this.initIfAllowed() : this.openLoginPopUp();
  }

  handleIOSDialogBtn(): void {
    const previousUrl = this.routingState.getPreviousUrl();
    const route = [`${(previousUrl && previousUrl !== this.windowRef.nativeWindow.location.pathname) ? previousUrl : '/'}`];
    this.domToolsService.removeClass(this.windowRef.document.body, this.BODY_CLASS);
    this.router.navigate(route);
  }

  private showSplashLogin(): boolean {
    return !this.userService.status;
  }

  /*IOS*/
  private checkIsIOSApp(): boolean {
    return this.deviceService.isIos && !this.deviceService.isSafari;
  }

  /**
   *  get CMS data and call for build IOS redirect dialog
   */
  private getIosRedirectCmsData(): void {
    this.cmsService.getOTFIosToggle()
      .subscribe((data: IOtfIosToggle) => {
          if (data.iosAppOff || (data[0] && data[0].iosAppOff)) {
            this.buildIosCmsToggleDialog(data.iosAppOff ? data : data[0]);
          } else {
            this.handleInit();
          }
      },
        (err) => this.awsService.addAction('1-2-free=>Get_IosToggleData_Error', { error: err || 'no error data' })
      );
  }

  /**
   * build IOS redirect dialog
   */
  private buildIosCmsToggleDialog(data): void {
    const { text, url, urlText } = data;
    const urlHtml = `<a href="${url}" rel="noopener" target="_blank" class="iosDialogLink">${urlText}</a>`;
    const textHtml = text.replace('{{URL}}', urlHtml);
    this.showIOSDialog = true;
    this.dialogContent = {
      header: '1-2-Free has moved!',
      body: textHtml,
      btnPrimary: {
        caption: data.proceedCtaText,
        cssClass: (url && data.proceedCtaText) ? 'iosDialogBtn-primary' : 'hidden',
        url
      },
      btnSecondary: {
        caption: data.closeCtaText,
        cssClass: 'iosDialogBtn-secondary',
      },
    };

    this.domToolsService.addClass(this.windowRef.document.body, this.BODY_CLASS);
  }

  public openLoginPopUp(): void {
    this.pubSubService.subscribe(this.tag, [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], (data) => {
      if (!this.bonusSuppressionService.checkIfYellowFlagDisabled(this.moduleName)) {
        this.bonusSuppressionService.navigateAwayForRGYellowCustomer();
      }
      this.initIfAllowed();
    });
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, {moduleName: 'header'});
  }

  private initIfAllowed(): void {
    if (this.userService.isInShopUser()) {
      this.isInShopUser = true;
      return;
    }

    this.initOneTwoFree();
  }

  private initOneTwoFree(): void {
    this.isGuest = false;
    this.windowRef.document.addEventListener(ONE_TWO_FREE_EVENTS.DESTROY_ONE_TWO_FREE, this.destroyOneTwoFree);
    this.windowRef.document.addEventListener(ONE_TWO_FREE_EVENTS.ADD_TO_BETSLIP, this.addToBetslip);
    this.windowRef.document.addEventListener(ONE_TWO_FREE_EVENTS.GO_TO_BETTING, this.goToBetting);
    this.windowRef.document.addEventListener(ONE_TWO_FREE_EVENTS.OTF_NEW_RELIC, this.sendAwsRequest);
    this.windowRef.document.addEventListener('OTF_PREDICTION_DONE', this.updateOtfSegmentStorage);
    if (this.userService.bppToken) {
      this.bootstrapOneTwoFree();
    }
  }

  private F2PSuspension(){
    this.windowRef.document.dispatchEvent(new CustomEvent(ONE_TWO_FREE_EVENTS.F2P_ACTIVATE, {
      detail:{
        F2P : this.serviceClosureService.userServiceClosureOrPlayBreak &&
        this.serviceClosureService.userServiceClosureOrPlayBreakCheck()
      }
    }))
  } 
  private bootstrapOneTwoFree(): void {
    const { bppToken, playerCode, username } = this.userService;

    if ( typeof this.windowRef.nativeWindow.CustomEvent !== 'function' ) {
      this.ie11CustomEventPolyfill();
    }
    const bootstrapEvent = new CustomEvent(ONE_TWO_FREE_EVENTS.BOOTSTRAP_ONE_TWO_FREE, {
      detail: Object.assign({}, {
        token: bppToken,
        customerId: playerCode,
        username,
        isMobile: this.deviceService.isMobile
      })
    });

    // if bundle loading fails - show quit button
    setTimeout(() => this.showBackButton = true, this.otfLoadingTimeout);

    observableForkJoin([
      this.asyncLoad.loadJsFile(`${environment.ONE_TWO_FREE_ENDPOINT}bundle.js`),
      this.asyncLoad.loadCssFile(`${environment.ONE_TWO_FREE_ENDPOINT}style.css`)
    ]).subscribe(
      () => {
        this.windowRef.document.dispatchEvent(bootstrapEvent);      
        this.F2PSuspension();
      },
      (err) => {
        this.awsService.addAction('1-2-free=>Loading_OTF_Resources_Error', { error: err  || 'no error data' });
        this.router.navigate(['/']);
      }
    );
  }

  private ie11CustomEventPolyfill(): void {
    function CustomEvent ( event, params ) {
      params = params || { bubbles: false, cancelable: false, detail: undefined };
      const evt = document.createEvent('CustomEvent');
      evt.initCustomEvent( event, params.bubbles, params.cancelable, params.detail );
      return evt;
    }
    CustomEvent.prototype = this.windowRef.nativeWindow.Event.prototype;
    this.windowRef.nativeWindow.CustomEvent = CustomEvent;
    // solution was taken from MDN website - https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/CustomEvent#Polyfill
  }

  private addToBetslip(event: CustomEvent): void {
    const { predictions, isMobile } = event.detail;

    this.addToBetslipService.addToBetSlip(predictions.join(','), true, true, isMobile).subscribe(
      () => this.windowRef.document.dispatchEvent(new CustomEvent(ONE_TWO_FREE_EVENTS.ADD_TO_BETSLIP_FINISHED)),
      (err) => this.awsService.addAction('1-2-free=>Add_To_BetSlip_Error', { error: err || 'no error data' })
    );
  }

  private goToBetting(): void {
    this.router.navigate(['sport', 'football', 'matches']);
  }

  private sendAwsRequest(data: CustomEvent): void {
    const { detail } = data;
    const errorData = (detail && detail.data) || 'app error';
    const err = (detail && detail.err && detail.err.message) ? detail.err.message : 'no error data';
    this.awsService.addAction(`1-2-free=>${errorData}`, { error: err });
  }

  private destroyOneTwoFree(): void {
    this.redirectHandler();
  }

  /**
   * update OTF segment for SB once predictions are submitted
   */
  private updateOtfSegmentStorage() {
    const expiryHours = 1;
    const currentTime = new Date();
 
    currentTime.setHours(currentTime.getHours() + expiryHours);
    const expiryDateTime = currentTime.toUTCString();
    
    this.storageService.set(this.OTF_SEGMENT_STORE_KEYTEXT, { user: this.userService.username, segment: false, timestamp: expiryDateTime });
  }
}

import { Component, Input, OnInit, Output, EventEmitter, OnDestroy } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { DeviceService } from '@coreModule/services/device/device.service';
import { Router } from '@angular/router';
import environment from '@environment/oxygenEnvConfig';
import { AccountUpgradeLinkService } from '@app/vanillaInit/services/accountUpgradeLink/account-upgrade-link.service';
import { GtmService } from '@core/services/gtm/gtm.service';

@Component({
  selector: 'login-splash-screen',
  templateUrl: './login-splash-screen.component.html',
  styleUrls: ['./login-splash-screen.component.scss']
})
export class LoginSplashScreenComponent implements OnInit, OnDestroy {
  @Input() content: string;
  @Input() hiddenLoginModal: boolean;
  @Input() isInShopUser: boolean;
  @Output() readonly invokeLogin = new EventEmitter();
  processingStatus: boolean;
  splashTitle: string = `${environment.ONE_TWO_FREE_ENDPOINT}assets/1-2-free_logo_mobile.svg`;
  splashBgPattern: string = `${environment.ONE_TWO_FREE_ENDPOINT}assets/background.jpeg`;
  loginBtnClicked: boolean = false;
  private isMobile: boolean = true;

  constructor(
    private pubSubService: PubSubService,
    private router: Router,
    private routingState: RoutingState,
    private windowRef: WindowRefService,
    private deviceService: DeviceService,
    private accountUpgradeLinkService: AccountUpgradeLinkService,
    private windowRefService: WindowRefService,
    private gtmService: GtmService,
  ) {}

  ngOnInit(): void {
    this.gaTaggingPush('1-2 free', 'contentView', 'load');
    this.processingStatus = this.hiddenLoginModal;
    this.isMobile = this.deviceService.isMobile;
    if (!this.isMobile) {
      this.splashTitle = `${environment.ONE_TWO_FREE_ENDPOINT}assets/1-2-free_logo_landscape.svg`;
    }

    this.pubSubService.subscribe('LoginSplashScreen', this.pubSubService.API.LOGIN_BUTTON_CLICKED, () => {
      this.loginBtnClicked = true;
    });
    this.pubSubService.subscribe('LoginSplashScreen', this.pubSubService.API.FAILED_LOGIN, () => {
      this.processingStatus = false;
      this.loginBtnClicked = false;
    });

    this.pubSubService.subscribe('LoginSplashScreen', [
      this.pubSubService.API.LOGIN_DIALOG_CLOSED,
      this.pubSubService.API.CLOSE_LOGIN_DIALOG
    ], () => {
      if (!this.loginBtnClicked) {
        this.processingStatus = false;
      }
    });
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM', true);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('LoginSplashScreen');
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM', false);
  }

  playHandler(): void {
    if (this.isInShopUser) {
      this.gaTaggingPush("Upgrade and Play", 'Event.Tracking', 'click');
      this.navigateToUpgrade();
    } else {
      this.gaTaggingPush("Login to play", 'Event.Tracking', 'click');
      this.invokeLoginHandler();
    }
  }

  cancelLoginHandler(): void {
    this.gaTaggingPush("Cancel", 'Event.Tracking', 'click');
    const route = this.routingState.getPreviousUrl();

    this.router
      .navigate([`${(route && route !== this.windowRef.nativeWindow.location.pathname) ? route : '/'}`]);
    this.pubSubService.publish('NETWORK_INDICATOR_BOTTOM', false);
  }

  private navigateToUpgrade(): void {
    const gtmData = {
      event: 'trackEvent',
      eventCategory: 'cta',
      eventAction: 'upgrade account',
      eventLabel: 'yes - upgrade Account'
    };

    this.gtmService.push(gtmData.event, gtmData);

    this.windowRefService.nativeWindow.location.href =  this.accountUpgradeLinkService.inShopToMultiChannelLink;
  }

  private invokeLoginHandler(): void {
    this.processingStatus = true;
    this.invokeLogin.emit();
  }

  private gaTaggingPush(eventDetails, event, actionEvent){
    const gtmData = {
      'event': event,
      'component.CategoryEvent': 'promotions',
      'component.LabelEvent': '1-2 free',
      'component.ActionEvent': actionEvent,
      'component.PositionEvent': 'not applicable',
      'component.LocationEvent': 'login', 
      'component.EventDetails': eventDetails, 
      'component.URLClicked': 'not applicable', 
      'component.ContentPosition': 'not applicable', 
      'campaignId': '',
      'page.siteSection':'sports promotions',
      'page.siteSubSection':'engagement tool',
      'component.PromotionType':'static promotions',
      'component.Product':'sportsbook',
      'component.PromoOfferName':'1-2 free',
      'component.PromoIntent':''
  };
  this.gtmService.push(gtmData.event, gtmData);
  }
}

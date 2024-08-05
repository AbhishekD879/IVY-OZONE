import { forkJoin as observableForkJoin, Subscription } from 'rxjs';
import { ChangeDetectorRef, Component, Input, OnInit, OnDestroy } from '@angular/core';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
import { UserService } from '@core/services/user/user.service';
import { IBetTrackerParams } from '@core/models/bet-tracker-params.model';
import { UpgradeAccountProviderService } from '@app/retail/services/upgradeAccountProvider/upgrade-account-provider.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BET_TRACKER } from '@app/retail/constants/retail.constant';
import { IGetIdTokenInfoFromUserNameResponseModel } from '@retail/services/upgradeAccountProvider/upgrade-account-provider.model';
import { RecapchaService } from '@app/retail/services/reCapcha/recapcha.service';

@Component({
  selector: 'bet-tracker',
  templateUrl: 'bet-tracker.component.html',
  styleUrls: ['bet-tracker.component.scss']
})

export class BetTrackerComponent implements OnInit, OnDestroy {
  @Input() public mode?: string;
  @Input() public betType?: string;
  @Input() fromDate?: string;
  @Input() toDate?: string;
  isBetTrackerLoaded: boolean = false;
  readonly BET_HISTORY = 'BET_HISTORY';
  private upgradeAccountSubscribe: Subscription;
  private bootstrapBetSubscribe: Subscription;

  constructor(
    private asyncLoad: AsyncScriptLoaderService,
    private windowRef: WindowRefService,
    private upgradeAccountProviderService: UpgradeAccountProviderService,
    private userService: UserService,
    private pubSubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    private recService : RecapchaService
  ) {}

  ngOnInit(): void {
    this.changeDetectorRef.detach();
    this.initBetTracker();
    this.pubSubService.subscribe('betTrackerComponent', this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.initBetTracker();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('betTrackerComponent');
    this.upgradeAccountSubscribe && this.upgradeAccountSubscribe.unsubscribe();
    this.bootstrapBetSubscribe && this.bootstrapBetSubscribe.unsubscribe();
    this.windowRef.document.dispatchEvent(
      new CustomEvent(BET_TRACKER.DESTROY_SUBSCRIPTIONS)
    );
  }

  get userStatus(): boolean {
    return this.userService.status;
  }
  set userStatus(value:boolean){}

  /*
  * Identifing the user type and getting user card number
  * @return {void}
  */
  private initBetTracker(): void {
    if (this.userService.isRetailUser() && !this.userService.cardNumber) {
      this.upgradeAccountSubscribe = this.upgradeAccountProviderService.getCardRequest(
        { 'username': this.userService.username, 'customerSessionId': this.userService.sessionToken }
      ).subscribe(
        (resp: IGetIdTokenInfoFromUserNameResponseModel) => {
          if (resp.body.data.printedTokenCode) {
            this.userService.set({ cardNumber: resp.body.data.printedTokenCode });
          }
          this.bootstrapBetTracker();
        });
    } else {
      this.bootstrapBetTracker();
    }
  }

  /**
   * initialize Bet Tracker with specific params
   */
  private bootstrapBetTracker() {
    const clientConfig = this.windowRef.nativeWindow.clientConfig;
    let RECAPTCHA_SITE_KEY = environment.GOOGLE_RECAPTCHA.ACCESS_TOKEN;
    const vnReCaptcha = clientConfig.vnReCaptcha || {};
    if (vnReCaptcha && vnReCaptcha.instrumentationOnPageLoad) {
      RECAPTCHA_SITE_KEY = vnReCaptcha.enterpriseSiteKey;
    }
    this.recService.addScript();
    this.bootstrapBetSubscribe = observableForkJoin([
      this.asyncLoad.loadJsFile(`${environment.BET_TRACKER_ENDPOINT}main.bundle.js`)
    ]).subscribe(() => {
      this.isBetTrackerLoaded = true;
      this.changeDetectorRef.detectChanges();
      this.windowRef.document.dispatchEvent(
        new CustomEvent(BET_TRACKER.BOOTSTRAP_BET_TRACKER, {
          detail: {
            mode: this.mode,
            username: this.userService.username,
            sessionToken: this.userService.sessionToken,
            accountBusinessPhase: this.userService.accountBusinessPhase,
            cardNumber: this.userService.cardNumber,
            devicePlatform: environment.CURRENT_PLATFORM,
            betType: this.betType,
            fromDate: this.fromDate,
            toDate: this.toDate,
            RECAPTCHA_SITE_KEY
          } as IBetTrackerParams
        })
      );
    });
  }
}

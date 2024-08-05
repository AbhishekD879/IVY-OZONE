import { ChangeDetectorRef, Component, ComponentFactoryResolver, EventEmitter, Input, OnDestroy, Output } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { SplashPopupComponent } from '@lazy-modules/freeRide/components/splash-popup/splash-popup.component';
import { FreeRideService } from '@lazy-modules/freeRide/services/freeRide.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { FreeRideCMSService } from '@lazy-modules/freeRide/services/freeRide-cms.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { IFreeRideCampaign, ISplashPage } from '@lazy-modules/freeRide/models/free-ride';
import { FREE_RIDE_CONSTS, FREE_RIDE_DIALOG_CONSTS } from '@lazy-modules/freeRide/constants/free-ride-constants';
import environment from '@environment/oxygenEnvConfig';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';

@Component({
  selector: 'launch-banner',
  templateUrl: './launch-banner.component.html',
  styleUrls: ['./launch-banner.component.scss'],
})
export class LaunchBannerComponent extends AbstractOutletComponent implements OnDestroy {
  @Input() config?: string;
  @Output() readonly closeFlag: EventEmitter<boolean> = new EventEmitter<boolean>();
  launchImg: string;
  freeBetToken: string;
  isUsed$: boolean;
  closePopFlag:boolean;
  isLoaded: boolean = false;
  splashConfig: boolean = false;
  splashInfo: ISplashPage;
  activeCampaignInfo: IFreeRideCampaign;
  cmsUri: string = environment.CMS_ROOT_URI;
  changeStrategy = STRATEGY_TYPES.ON_PUSH;

  constructor(
    public freeBetsService: FreeBetsService,
    public userService: UserService,
    public componentFactoryResolver: ComponentFactoryResolver,
    public dialogService: DialogService,
    public freeRideService: FreeRideService,
    public freeRideHelperService: FreeRideHelperService,
    public freeRideCMSService: FreeRideCMSService,
    public sessionStorageService: SessionStorageService,
    private pubSubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    super();
    this.loadInitialData();
    this.pubSubService.subscribe(FREE_RIDE_DIALOG_CONSTS.FREERIDE_OVERLAY, this.pubSubService.API.FREE_RIDE_BET,
      (data: boolean) => {
        this.isUsed$ = data;
        this.changeDetectorRef.markForCheck();
      });
  }

  /**
   * get SplashPopupComponent
   * @returns {typeof SplashPopupComponent}
   */
  get dialogComponent(): typeof SplashPopupComponent {
    return SplashPopupComponent;
  }

  /**
   * handle opening splash popup
   * @returns {void}
   */
  public openPopUp(): void {
    this.closeFlag.emit(false);
    this.freeRideService.sendGTM('entry banner', 'click');
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.dialogService.openDialog(DialogService.API.splashPopup, componentFactory, true, {
      dialogClass: FREE_RIDE_DIALOG_CONSTS.SPLASH_POPUP,
      data: {
        campaginDetails: this.activeCampaignInfo,
        splashInfo: this.splashInfo,
        freeBetToken: this.freeBetToken,
        callClose: (flag: boolean) => {
          this.closePopFlag = flag;
        }
      }
    });
  }

  /**
   * loads launch banner
   * @returns {void}
   */
  public loadInitialData(): void {
    this.isLoaded = true;
    this.freeRideCMSService.getFreeRideSplashPage().pipe(
      finalize(() => {
        this.isLoaded = false;
      })
    ).subscribe((freeRideData: ISplashPage) => {
      const freeBetDetails = JSON.parse(this.sessionStorageService.get(FREE_RIDE_CONSTS.FREERIDE_DETAILS));
      const freeRideCampaign = JSON.parse(this.sessionStorageService.get(FREE_RIDE_CONSTS.FR_CAMPAIGN_DATA));
      if (freeRideData) {
        [this.splashInfo, this.activeCampaignInfo, this.freeBetToken] = [freeRideData, freeRideCampaign, freeBetDetails.freeBetTokenId];
        this.launchImg = `${this.cmsUri}${this.splashInfo.bannerImageUrl}`;
        this.freeRideService.sendGTM('entry banner', 'load');
      }
      this.checkHomeBetslipConfig(this.config);
    }, (err) => {
      console.warn(err);
    });
  }

  /**
   * checks from where module has been loaded
   * @param {string} config
   * @returns {void}
   */
  public checkHomeBetslipConfig(config: string): void {
    this.splashConfig = (config == 'BETSLIP')? this.splashInfo.isBetReceipt: (config == 'HOME')? this.splashInfo.isHomePage: true;
  }
}

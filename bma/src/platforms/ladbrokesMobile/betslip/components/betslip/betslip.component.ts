import { Component, ComponentFactoryResolver, OnDestroy, OnInit, Type, ChangeDetectorRef } from '@angular/core';
import { BetslipComponent } from '@app/betslip/components/betslip/betslip.component';
import { TimeService } from '@core/services/time/time.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BetslipLiveUpdateService } from '@betslip/services/betslipLiveUpdate/betslip-live-update.service';
import { BetslipService } from '@betslip/services/betslip/betslip.service';
import { ToteBetslipService } from '@betslip/services/toteBetslip/tote-betslip.service';
import { UserService } from '@core/services/user/user.service';
import { ResolveService } from '@core/services/resolve/resolve.service';
import { BetReceiptService } from '@betslip/services/betReceipt/bet-receipt.service';
import { QuickDepositService } from '@betslipModule/services/quickDeposit/quick-deposit.service';
import { BetInfoDialogService } from '@betslip/services/betInfoDialog/bet-info-dialog.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { StorageService } from '@core/services/storage/storage.service';
import { DigitalSportBetsService } from '@core/services/digitalSportBets/digital-sport-bets.service';
import { DeviceService } from '@core/services/device/device.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { SessionService } from '@authModule/services/session/session.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { ToteBetReceiptService } from '@betslip/services/toteBetReceipt/tote-bet-receipt.service';
import { BetslipFiltersService } from '@betslip/services/betslipFilters/betslip-filters.service';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';
import { BetslipDataService } from '@betslip/services/betslip/betslip-data.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { BetslipStakeService } from '@betslip/services/betslip/betslip-stake.service';
import { DatePipe } from '@angular/common';
import { FiltersService } from '@core/services/filters/filters.service';
import { Router } from '@angular/router';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { BodyScrollLockService } from '@betslip/services/bodyScrollLock/betslip-body-scroll-lock.service';
import { AccountUpgradeLinkService } from '@app/vanillaInit/services/accountUpgradeLink/account-upgrade-link.service';
import { QuickDepositIframeService } from '@app/quick-deposit/services/quick-deposit-iframe.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import {
  LadbrokesSelectionInfoDialogComponent
} from '@ladbrokesMobile/betslip/components/selectionInfoDialog/selection-info-dialog.component';
import { Bet } from '@betslip/services/bet/bet';
import { IConstant } from '@core/services/models/constant.model';
import { IBetsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { SignpostingCmsService } from '@lazy-modules/signposting/services/signposting.service';
import { GetSelectionDataService } from '@betslip/services/getSelectionData/get-selection-data.service';

@Component({
  selector: 'betslip',
  templateUrl: './betslip.component.html',
  styleUrls: ['./betslip.component.scss']
})
export class LadbrokesBetslipComponent extends BetslipComponent implements OnInit, OnDestroy {
  isGermanUser: boolean;
  overlayMsgConfig: IConstant = { message: '', type: '' };
  get infoDialogComponent(): Type<LadbrokesSelectionInfoDialogComponent> {
    return LadbrokesSelectionInfoDialogComponent;
  }
  set infoDialogComponent(value:Type<LadbrokesSelectionInfoDialogComponent>){}

  constructor(overAskService: OverAskService,
              windowRefService: WindowRefService,
              betslipLiveUpdateService: BetslipLiveUpdateService,
              betslipService: BetslipService,
              toteBetslipService: ToteBetslipService,
              userService: UserService,
              resolveService: ResolveService,
              betReceiptService: BetReceiptService,
              localeService: LocaleService,
              quickDepositService: QuickDepositService,
              betInfoDialogService: BetInfoDialogService,
              infoDialogService: InfoDialogService,
              storageService: StorageService,
              digitalSportBetsService: DigitalSportBetsService,
              deviceService: DeviceService,
              freeBetsService: FreeBetsService,
              sessionService: SessionService,
              fracToDecService: FracToDecService,
              gtmService: GtmService,
              pubSubService: PubSubService,
              commandService: CommandService,
              toteBetReceiptService: ToteBetReceiptService,
              bsFiltersService: BetslipFiltersService,
              betslipStorageService: BetslipStorageService,
              betslipDataService: BetslipDataService,
              cmsService: CmsService,
              betslipStakeService: BetslipStakeService,
              datePipe: DatePipe,
              filterService: FiltersService,
              awsService: AWSFirehoseService,
              router: Router,
              routingState: RoutingState,
              timeService: TimeService,
              bodyScrollLockService: BodyScrollLockService,
              dialogService: DialogService,
              componentFactoryResolver: ComponentFactoryResolver,
              accountUpgradeLinkService: AccountUpgradeLinkService,
              quickDepositIframeService: QuickDepositIframeService,
              private germanSupportService: GermanSupportService,
              changeDetectorRef: ChangeDetectorRef,
              serviceClosureService: ServiceClosureService,
              siteServerRequestHelperService:SiteServerRequestHelperService,
              protected sessionStorageService: SessionStorageService,
              protected coreToolsService: CoreToolsService,
              signpostingCmsService: SignpostingCmsService,
              getSelectionDataService: GetSelectionDataService

  ) {
    super(overAskService, windowRefService, betslipLiveUpdateService, betslipService, toteBetslipService, userService, resolveService,
      betReceiptService, localeService, quickDepositService, betInfoDialogService, infoDialogService, storageService,
      digitalSportBetsService, deviceService, freeBetsService, sessionService, fracToDecService, gtmService,
      pubSubService, commandService, toteBetReceiptService, bsFiltersService, betslipStorageService, betslipDataService,
      cmsService, betslipStakeService, datePipe, filterService, awsService, router, routingState, timeService,
      bodyScrollLockService, dialogService, componentFactoryResolver, accountUpgradeLinkService,
      quickDepositIframeService, changeDetectorRef, serviceClosureService, siteServerRequestHelperService, sessionStorageService, coreToolsService, signpostingCmsService,getSelectionDataService
    );
  }

  ngOnInit() {
    super.ngOnInit();

    this.isGermanUser = this.germanSupportService.isGermanUser();

    /* eslint-disable-next-line  */
    this.pubSubService.subscribe(this.tagName,
      [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
        this.isGermanUser = this.germanSupportService.isGermanUser();
        this.serviceClosureService.checkUserServiceClosureStatus();
      }
    );

    this.pubSubService.subscribe(this.tagName,
      [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SUCCESSFUL_LOGIN], (placeBet) => {
        this.betslipService.removeFzSelectionsOnLogout();
        this.betslipSuccessfulLogin(placeBet);
        this.serviceClosureService.checkUserServiceClosureStatus();
      }
    );

    this.betslipService.removeFzSelectionsOnLogout();

    /* eslint-disable-next-line  */
    this.pubSubService.subscribe(this.tagName,
      this.pubSubService.API.BS_SHOW_OVERLAY, (message: string) => {
        this.showOverlayMessage({ message, type: '' });
      });

    /* eslint-disable-next-line */
    this.pubSubService.subscribe(this.tagName,
      this.pubSubService.API.BS_SHOW_SUSP_OVERLAY,
      () => {
        this.showOverlayMessage({ message: this.placeSuspendedErr.msg, type: '' });
      });
  }

  /**
   * Clear overlayMsgConfig after add/remove selection to/from betslip
   */
  clearOverlayMessage(type?: string): void {
    if (!type || this.overlayMsgConfig.type === type) {
      this.overlayMsgConfig = { message: '', type: '' };
    }
  }

  /**
   * Show overlay message(event started/suspension/price change/acca insurance messages) in the top of betslip
   * @param messageConfig {IConstant}
   */
   showOverlayMessage(messageConfig: IConstant): void {
    this.overlayMsgConfig = messageConfig;
  }

  protected handleDefaultError(result: IBetsResponse): boolean {
    const res = super.handleDefaultError(result);

    if (this.placeStakeErr) {
      this.showOverlayMessage({ message: this.placeStakeErr, type: '' });
    }

    return res;
  }

  protected selectionLiveUpdate(bet: Bet): void {
    super.selectionLiveUpdate(bet);
    if (!this.overask.isInProcess) {
      const msg = this.betslipService.getOverlayLiveUpdateMessage(bet, this.isBoostActive);
      if (msg) {
        this.showOverlayMessage({ message: msg, type: '' });
      }
    }
  }
}

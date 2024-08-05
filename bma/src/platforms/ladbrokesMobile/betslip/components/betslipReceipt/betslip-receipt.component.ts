import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

import { UserService } from '@core/services/user/user.service';
import { BetReceiptService } from '@betslip/services/betReceipt/bet-receipt.service';
import { DeviceService } from '@core/services/device/device.service';
import { SessionService } from '@authModule/services/session/session.service';
import { StorageService } from '@core/services/storage/storage.service';
import { BetInfoDialogService } from '@betslip/services/betInfoDialog/bet-info-dialog.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BetslipReceiptComponent } from '@betslip/components/betslipReceipt/betslip-receipt.component';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { BodyScrollLockService } from '@betslip/services/bodyScrollLock/betslip-body-scroll-lock.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BppErrorService } from '@app/bpp/services/bppError/bpp-error.service';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { FirstBetGAService } from '@app/lazy-modules/onBoardingTutorial/firstBetPlacement/services/first-bet-ga.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';
@Component({
  selector: 'betslip-receipt',
  templateUrl: 'betslip-receipt.component.html',
  styleUrls: ['./betslip-receipt.component.scss']
})
export class LadbrokesBetslipReceiptComponent extends BetslipReceiptComponent implements OnInit {
  isGermanUser: boolean;
  constructor(
              public user: UserService,
              public betReceiptService: BetReceiptService,
              sessionService: SessionService,
              storageService: StorageService,
              betInfoDialogService: BetInfoDialogService,
              location: Location,
              gtmService: GtmService,
              router: Router,
              comandService: CommandService,
              device: DeviceService,
              gtmTrackingService: GtmTrackingService,
              bodyScrollLockService: BodyScrollLockService,
              nativeBridge: NativeBridgeService,
              window: WindowRefService,
              overAskService: OverAskService,
              localeService: LocaleService,
              protected pubSubService: PubSubService,
              protected bppErrorService: BppErrorService,
              protected racingPostTipService: RacingPostTipService,
              protected sessionStorageService: SessionStorageService,
              public freeRideHelperService: FreeRideHelperService,
              protected fbService: FreeBetsService,
              private germanSupportService: GermanSupportService,
              protected firstBetGAService:FirstBetGAService,
              changeDetectionRef:ChangeDetectorRef,
              protected bonusSuppressionService: BonusSuppressionService,
              scorecastDataService: ScorecastDataService
              ) {
    super(user, betReceiptService, sessionService, storageService, betInfoDialogService,
      location, gtmService, router, comandService, device, gtmTrackingService, bodyScrollLockService,
      nativeBridge, window, overAskService, localeService, pubSubService, bppErrorService, racingPostTipService, sessionStorageService, fbService, firstBetGAService,changeDetectionRef, scorecastDataService);
  }

  ngOnInit() {
    super.ngOnInit();
    this.isGermanUser = this.germanSupportService.isGermanUser();
  }
  reloadComponent(): void {
    this.ngOnDestroy();
    this.ngOnInit();
  }

}

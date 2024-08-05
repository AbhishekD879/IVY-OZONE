import { Component, OnInit } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { QuickbetReceiptComponent } from '@app/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { StorageService } from '@core/services/storage/storage.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { HttpClient } from '@angular/common/http';
import { RacingPostTipService } from '@app/lazy-modules/racingPostTip/service/racing-post-tip.service';

import { CmsService } from '@app/core/services/cms/cms.service';
import {
  FiveASideEntryConfirmationService
} from '@app/fiveASideShowDown/services/fiveAside-Entry-confirmation.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { MaxPayOutErrorService } from '@app/lazy-modules/maxpayOutErrorContainer/services/maxpayout-error.service';
import { FiveASideContestSelectionService } from '@app/fiveASideShowDown/services/fiveASide-ContestSelection.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { FirstBetGAService } from '@app/lazy-modules/onBoardingTutorial/firstBetPlacement/services/first-bet-ga.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { BetReuseService } from '@app/betslip/services/betReUse/bet-reuse.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'quickbet-receipt',
  templateUrl: 'quickbet-receipt.component.html',
  styleUrls: ['./quickbet-receipt.component.scss']
})

export class LadbrokesQuickbetReceiptComponent extends QuickbetReceiptComponent implements OnInit {
  isGermanUser: boolean;
  constructor(
              public user: UserService,
              filtersService: FiltersService,
              quickbetService: QuickbetService,
              nativeBridge: NativeBridgeService,
              window: WindowRefService,
              protected pubSubService: PubSubService,
              protected http: HttpClient,
              storageService: StorageService,
              racingPostTipService: RacingPostTipService,
              cmsService: CmsService,
              fiveASideEntryConfirmationService: FiveASideEntryConfirmationService,
              fiveASideContestSelectionService: FiveASideContestSelectionService,
              freeBetsService: FreeBetsService,
              private germanSupportService: GermanSupportService,
              gtmService: GtmService,
              maxPayOutErrorService: MaxPayOutErrorService,
              public freeRideHelperService: FreeRideHelperService,
              protected locale: LocaleService,
              firstBetGAService: FirstBetGAService,
              betReuseService: BetReuseService,
              sessionStorage: SessionStorageService,
              bonusSuppressionService: BonusSuppressionService
              ) {
    super(user, filtersService, quickbetService, nativeBridge, window, pubSubService, http, storageService,
      racingPostTipService, cmsService, fiveASideEntryConfirmationService, fiveASideContestSelectionService, freeBetsService,gtmService,maxPayOutErrorService, locale, firstBetGAService, betReuseService, sessionStorage, bonusSuppressionService);
  }

  ngOnInit(): void {
  super.ngOnInit();
    this.isGermanUser = this.germanSupportService.isGermanUser();
  }
}

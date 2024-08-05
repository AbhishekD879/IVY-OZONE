import { Component } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { QuickbetService } from '@app/quickbet/services/quickbetService/quickbet.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';
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

import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { LadbrokesQuickbetReceiptComponent } from '@ladbrokesMobile/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { BetReuseService } from '@app/betslip/services/betReUse/bet-reuse.service';

@Component({
  selector: 'sb-quickbet-receipt',
  templateUrl: '../../../../../app/quickbet-stream-bet/components/quickbetReceipt/sb-quickbet-receipt.component.html',
  styleUrls: ['../../../../../app/quickbet-stream-bet/components/quickbetReceipt/sb-quickbet-receipt.component.scss']
})
export class SbQuickbetReceiptComponent extends LadbrokesQuickbetReceiptComponent {

  receiptId: string;

  constructor(
    user: UserService,
    filtersService: FiltersService,
    quickbetService: QuickbetService,
    nativeBridge: NativeBridgeService,
    window: WindowRefService,
    pubSubService: PubSubService,
    http: HttpClient,
    storageService: StorageService,
    racingPostTipService: RacingPostTipService,
    cmsService: CmsService,
    fiveASideEntryConfirmationService: FiveASideEntryConfirmationService,
    fiveASideContestSelectionService: FiveASideContestSelectionService,
    freeBetsService: FreeBetsService,
    gtmService: GtmService,
    maxPayOutErrorService: MaxPayOutErrorService,
    locale: LocaleService,
    firstBetGAService: FirstBetGAService,
    betReuseService: BetReuseService,
    sessionStorage: SessionStorageService,
    germanSupportService: GermanSupportService,
    public freeRideHelperService: FreeRideHelperService,
    bonusSuppressionService: BonusSuppressionService
  ) {
    super(user, filtersService, quickbetService, nativeBridge, window, pubSubService, http,
       storageService, racingPostTipService, cmsService, fiveASideEntryConfirmationService, 
       fiveASideContestSelectionService, freeBetsService,germanSupportService, gtmService, maxPayOutErrorService,freeRideHelperService,  locale, 
       firstBetGAService, betReuseService, sessionStorage, bonusSuppressionService);
    }
    ngOnInit(): void {
      super.ngOnInit();
      this.receiptId = this.betReceipt && this.betReceipt.receipt && this.betReceipt.receipt.id;
      this.quickbetService.qbReceiptDataSubj.next({
        stake: this.finalStake,
        returns: (this.payout || 'N/A'),
        odds: this.odds,
        freeBetData: {
          hasFreebet: this.hasFreebet,
          selection: this.selection,
          betReceipt: this.betReceipt
        }
      });
      this.quickbetService.quickBetOnOverlayCloseSubj.next('qb receipt');
      this.quickbetService.quickBetOnOverlayCloseSubj.subscribe((qbStatusMsg: string) => {
        if(qbStatusMsg === 'fullscreen exit') {
          this.onQuickbetEvent();
        }
      });
    }
}

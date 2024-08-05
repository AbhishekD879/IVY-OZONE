
import { FormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { BetHistoryRoutingModule } from '@betHistoryModule/bet-history-routing.module';
import { BetHistoryRunService } from '@app/betHistory/services/betHistoryRunService/bet-history-run.service';

import { CancelWithDrawDialogComponent } from '@app/betHistory/components/cancelWithDrawDialog/cancel-withdraw-dialog.component';
import { NoBetsSectionComponent } from '@app/betHistory/components/noBetsSection/no-bets-section.component';
import { BetslipTabsComponent } from '@betHistoryModule/components/betslipTabs/betslip-tabs.component';
import { LiveScoresComponent } from '@app/betHistory/components/liveScores/live-scores.component';
import { RegularBetHeaderComponent } from '@app/betHistory/components/regularBetHeader/regular-bet-header.component';
import { TotePoolBetCardComponent } from '@app/betHistory/components/totePoolBetCard/totePoolBetCard.component';
import { LottoBetsComponent } from '@app/betHistory/components/lottoBets/lotto-bets.component';
import { StakeAndReturnsHeaderComponent } from '@app/betHistory/components/stakeAndReturnsHeader/stake-and-returns-header.component';
import { BetReceiptInfoComponent } from '@app/betHistory/components/betReceiptInfo/bet-receipt-info.component';
import { TotePotPoolBetCardComponent } from '@app/betHistory/components/totePotPoolBetCard/tote-pot-pool-bet-card.component';
import { JackpotPoolLegListComponent } from '@app/betHistory/components/jackpotPoolLegList/jackpot-pool-leg-list.component';
import { CashOutPageComponent } from '@app/betHistory/components/cashOutPage/cash-out-page.component';
import { PoolBetHistoryComponent } from '@app/betHistory/components/poolBetHistory/pool-bet-history.component';
import { BetLegItemComponent } from '@betHistoryModule/components/betLegItem/bet-leg-item.component';
import { BetLegListComponent } from '@app/betHistory/components/betLegList/bet-leg-list.component';
import { MyBetsComponent } from '@betHistoryModule/components/myBets/my-bets.component';
import { RegularBetsComponent } from '@app/betHistory/components/regularBets/regular-bets.component';
import { FiveASideComponent } from '@app/betHistory/components/fiveASideButton/five-a-side-button.component';
import { DigitalSportBetsComponent } from '@app/betHistory/components/digitalSportBets/digital-sport-bets.component';
import { PartialCashoutHistoryComponent } from '@app/betHistory/components/partialCashoutHistory/partial-cashout-history.component';
import { CashoutPanelComponent } from '@app/betHistory/components/cashoutPanel/cashout-panel.component';
import { CashOutPageWrapperComponent } from '@app/betHistory/components/cashoutPageWrapper/cash-out-page-wrapper.component';
import { OpenBetsPageWrapperComponent } from '@app/betHistory/components/openBetsPageWrapper/open-bets-page-wrapper.component';
import { InShopBetsPageWrapperComponent } from '@app/betHistory/components/inShopBetsPageWrapper/in-shop-bets-page-wrapper.component';
import { InShopBetsPageComponent } from '@app/betHistory/components/inShopBetsPage/in-shop-bets-page.component';
import { BetHistoryPageWrapperComponent } from '@app/betHistory/components/betHistoryPageWrapper/bet-history-page-wrapper.component';
import { EditMyAccaButtonComponent } from '@app/betHistory/components/editMyAccaButton/edit-my-acca-button.component';
import { EditMyAccaRemoveIconComponent } from '@app/betHistory/components/editMyAccaRemoveIcon/edit-my-acca-remove-icon.component';
import { EditMyAccaConfirmComponent } from '@app/betHistory/components/editMyAccaConfirm/edit-my-acca-confirm.component';
import { EditMyAccaWarningComponent } from '@app/betHistory/components/editMyAccaWarning/edit-my-acca-warning.component';
import { EditMyAccaHistoryComponent } from '@app/betHistory/components/editMyAccaHistory/edit-my-acca-history.component';
import { EditMyAccaHistoryListComponent } from '@app/betHistory/components/editMyAccaHistoryList/edit-my-acca-history-list.component';
import { EditMyAccaHistoryDialogComponent } from '@app/betHistory/components/editMyAccaHistoryDialog/edit-my-acca-history-dialog.component';
import { BetHistoryPromptComponent } from '@betHistoryModule/components/betHistoryPrompt/bet-history-prompt.component';
import { LadbrokesTermsConditionsComponent } from '@ladbrokesMobile/betHistory/components/terms-conditions/terms-conditions.component';
import { TopSuccessMessageComponent } from '@app/betHistory/components/topSuccessMessage/top-success-message.component';
import { BetPromotionComponent } from '@app/betHistory/components/betPromotions/bet-promotions.component';
import { CashoutErrorMessageComponent } from '@ladbrokesMobile/betHistory/components/cashoutErrorMessage/cashout-error-message.component';
import { OpenBetsComponent } from '@betHistoryModule/components/openBets/open-bets.component';
import { LadbrokesBetHistoryPageComponent as BetHistoryPageComponent } from '@ladbrokesMobile/betHistory/components/betHistoryPage/bet-history-page.component';
import { EventHeaderComponent } from '@betHistoryModule/components/eventHeader/event-header.component';
import { CashOutBetsComponent } from '@betHistoryModule/components/cashOutBets/cash-out-bets.component';
import { WhatIsCashOutDialogComponent } from '@app/betHistory/components/whatIsCashoutPopup/what-is-cashout-dialog.component';
import { WhatIsCashoutComponent } from '@app/betHistory/components/what-is-cashout/what-is-cashout.component';
import { ProfitLossLinkComponent } from '@app/betHistory/components/profitLossLink/profit-loss-link.component';
import { DigitListComponent } from '@app/betHistory/components/digitList/digit-list.component';
import { NgxSliderModule } from 'ngx-slider-v2';
import { RangeSliderComponent } from '@app/betHistory/components/rangeSlider/range-slider.component';
import { OptaInfoPopupComponent } from '@lazy-modules/bybHistory/components/optaInfoPopup/opta-info-popup.component';
import { CashOutPopUpComponent } from '@app/betHistory/components/cashOutMessaging/cashOutPopUp/cash-out-popup.component';
import { CashOutMessageComponent } from '@app/betHistory/components/cashOutMessaging/cash-out-message.component';
import { LiveLabelUpdatedComponent } from '@app/betHistory/components/liveLabelUpdated/live-label-updated.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { ShareToSocialMediaDialogComponent } from '@lazy-modules/bet-share-image-card/shareToSocialMediaDialog/share-to-social-media-dialog.component';
import { LottoResultCardComponent } from '@app/betHistory/components/lotto-result-card/lotto-result-card.component';
import { BlurbMessageComponent } from '@app/betHistory/components/blurb-message/blurb-message.component';

@NgModule({
  declarations: [
    FiveASideComponent,
    DigitListComponent,
    WhatIsCashoutComponent,
    WhatIsCashOutDialogComponent,
    LottoBetsComponent,
    TotePoolBetCardComponent,
    NoBetsSectionComponent,
    RegularBetHeaderComponent,
    CashOutPageComponent,
    BetHistoryPageWrapperComponent,
    CancelWithDrawDialogComponent,
    StakeAndReturnsHeaderComponent,
    BetReceiptInfoComponent,
    LiveScoresComponent,
    TotePotPoolBetCardComponent,
    OpenBetsComponent,
    JackpotPoolLegListComponent,
    EventHeaderComponent,
    PoolBetHistoryComponent,
    BetLegItemComponent,
    BetLegListComponent,
    MyBetsComponent,
    RegularBetsComponent,
    RangeSliderComponent,
    CashOutBetsComponent,
    PartialCashoutHistoryComponent,
    DigitalSportBetsComponent,
    CashOutPageWrapperComponent,
    CashoutPanelComponent,
    BetslipTabsComponent,
    OpenBetsPageWrapperComponent,
    BetHistoryPageComponent,
    InShopBetsPageComponent,
    InShopBetsPageWrapperComponent,
    EditMyAccaButtonComponent,
    EditMyAccaRemoveIconComponent,
    EditMyAccaConfirmComponent,
    EditMyAccaWarningComponent,
    EditMyAccaHistoryComponent,
    EditMyAccaHistoryListComponent,
    EditMyAccaHistoryDialogComponent,
    BetHistoryPromptComponent,
    TopSuccessMessageComponent,
    BetPromotionComponent,
    LadbrokesTermsConditionsComponent,
    ProfitLossLinkComponent,
    CashoutErrorMessageComponent,
    LiveLabelUpdatedComponent,
    OptaInfoPopupComponent,
    CashOutMessageComponent,
    CashOutPopUpComponent,
    ShareToSocialMediaDialogComponent,
    LottoResultCardComponent,
    BlurbMessageComponent,
  ],
  imports: [
    SharedModule,
    FormsModule,
    NgxSliderModule,
    BetHistoryRoutingModule
  ],
  providers: [],
  exports: [
    ShareToSocialMediaDialogComponent,
    FiveASideComponent,
    DigitListComponent,
    WhatIsCashoutComponent,
    WhatIsCashOutDialogComponent,
    LottoBetsComponent,
    TotePoolBetCardComponent,
    NoBetsSectionComponent,
    RegularBetHeaderComponent,
    LiveScoresComponent,
    CancelWithDrawDialogComponent,
    StakeAndReturnsHeaderComponent,
    BetHistoryPageWrapperComponent,
    BetReceiptInfoComponent,
    TotePotPoolBetCardComponent,
    JackpotPoolLegListComponent,
    EventHeaderComponent,
    PoolBetHistoryComponent,
    BetLegItemComponent,
    BetLegListComponent,
    RegularBetsComponent,
    RangeSliderComponent,
    CashOutBetsComponent,
    PartialCashoutHistoryComponent,
    DigitalSportBetsComponent,
    CashOutPageWrapperComponent,
    CashoutPanelComponent,
    BetslipTabsComponent,
    OpenBetsPageWrapperComponent,
    InShopBetsPageWrapperComponent,
    EditMyAccaButtonComponent,
    EditMyAccaRemoveIconComponent,
    EditMyAccaConfirmComponent,
    EditMyAccaWarningComponent,
    EditMyAccaHistoryComponent,
    EditMyAccaHistoryListComponent,
    EditMyAccaHistoryDialogComponent,
    BetHistoryPromptComponent,
    TopSuccessMessageComponent,
    BetPromotionComponent,
    LadbrokesTermsConditionsComponent,
    CashoutErrorMessageComponent,
    CashOutMessageComponent,
    CashOutPopUpComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})

export class BetHistoryModule {
  static entry = {BetHistoryPageComponent, CashOutPageComponent,
        OpenBetsComponent, MyBetsComponent, InShopBetsPageComponent};
  constructor(private betHistoryRunService: BetHistoryRunService,private asls: AsyncScriptLoaderService) {
    this.betHistoryRunService.run();
    this.asls.loadCssFile('assets-bet-history.css',true, true).subscribe();
  }
}
// This module is required only to allow coralDesktop to build with AOT
// Here you should place all components which extented by coral desktop
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { OddsCardResultComponent } from '@shared/components/oddsCardResult/odds-card-result.component';
import { BetslipCounterComponent } from '@shared/components/betslipCounter/betslip-counter.component';
import { AccordionComponent } from '@shared/components/accordion/accordion.component';
import { TabsPanelComponent } from '@shared/components/tabsPanel/tabs-panel.component';
import { FooterSectionComponent } from '@shared/components/footerSection/footer-section.component';
import { SwitchersComponent } from '@shared/components/switchers/switchers.component';
import { PromotionsListComponent } from '@app/promotions/components/promotionsList/promotions-list.component';
import { RacingSpecialsCarouselComponent } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.component';
import { RacingSpecialsTabComponent } from '@racing/components/racingSpecialsTab/racing-specials-tab.component';
import { HistoricPricesComponent } from '@shared/components/historicPrices/historic-prices.component';
import { OffersAndFeaturedRacesComponent } from '@racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';
import { RetailPageComponent } from '@app/retail/components/retailPage/retail-page.component';
import { BetFilterComponent as OxygenBetFilterComponent } from '@app/retail/components/betFilter/bet-filter.component';
import { BetslipHeaderIconComponent } from '@shared/components/betslipHeaderIcon/betslip-header-icon.component';
import { FeaturedQuickLinksComponent } from '@featured/components/featured-quick-links/featured-quick-links.component';
import { FeaturedModuleComponent } from '@featured/components/featured-module/featured-module.component';
import { OddsBoostInfoDialogComponent } from '@shared/components/oddsBoostInfoDialog/odds-boost-info-dialog.component';
import { CouponsDetailsComponent } from '@sb/components/couponsDetails/coupons-details.component';
import { CorrectScoreCouponComponent } from '@sb/components/correctScoreCoupon/correct-score-coupon.component';
import { GoalscorerCouponComponent } from '@sb/components/goalscorerCoupon/goalscorer-coupon.component';
import {
  PrivateMarketsTabComponent as AppPrivateMarketsTabComponent
} from '@sb/components/privateMarketsTab/private-markets-tab.component';
import { BreadcrumbsComponent } from '@app/shared/components/breadcrumbs/breadcrumbs.component';
import { TopBarComponent } from '@shared/components/topBar/top-bar.component';
import { RaceGridComponent } from '@shared/components/raceGrid/race-grid';
import { CashoutLabelComponent } from '@app/shared/components/cashoutLabel/cashout-label.component';
import { PromotionIconComponent } from '@app/promotions/components/promotionIcon/promotion-icon.component';
import { HorseRaceGridComponent } from '@app/lazy-modules/racingFeatured/components/horseRaceGrid/horse-race-grid.component';
import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { RaceCardsControlsComponent } from '@racing/components/raceCardControls/race-cards-controls.component';
import {
  ForecastTricastMarketComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastMarketComponent/forecast-tricast-market.component';
import {
  ForcastTricastRaceCardComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastRaceCard/forecast-tricast-race-card.component';
import {
  EventVideoStreamComponent
} from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream.component';
import {
  VideoStreamErrorDialogComponent
} from '@lazy-modules/eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';
import {
  NextRacesHomeTabComponent
} from '@app/lazy-modules/lazyNextRacesTab/components/nextRacesHomeTab/next-races-home-tab.component';
import { ExtraPlaceHomeComponent } from '@app/lazy-modules/lazyNextRacesTab/components/extraPlaceHome/extra-place-home.component';
import {
  CompetitionsResultsTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-results-tab.component';
// import {
//   OddsCardHighlightCarouselComponent
// } from '@shared/components/oddsCard/oddsCardHightlightCarousel/odds-card-highlight-carousel.component';
import {
  FeaturedHighlightsCarouselComponent
} from '@featured/components/featured-highlights-carousel/featured-highlights-carousel.component';
import {
  OddsCardSurfaceBetComponent
} from '@shared/components/oddsCard/oddsCardSurfaceBet/odds-card-surface-bet.component';
import { InplayAllSportsPageComponent } from '@app/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { InplayPageComponent } from '@app/inPlay/components/inplayPage/inplay-page.component';
import { InplaySingleSportPageComponent } from '@app/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayTabComponent } from '@app/inPlay/components/inplayTab/inplay-tab.component';
import { InplayWatchLivePageComponent } from '@app/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import { LpSpDropdownComponent } from '@freebets/components/lpSpDropdown/lp-sp-dropdown.component';
import { BmaMainComponent } from '@app/bma/components/bmaMain/bma-main.component';
import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';
import { HorseracingTabsComponent } from '@racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';
import { RacingOutcomeCardComponent } from '@racing/components/racingOutcomeCard/racing-outcome-card.component';
import { OxygenDialogComponent } from '@shared/components/oxygenDialogs/oxygen-dialog.component';
import { GreyhoundsTabsComponent } from '@racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { FeaturedInplayComponent } from '@featured/components/featured-inplay/featured-inplay.component';
import { DropDownMenuComponent } from '@shared/components/dropDownMenu/drop-down-menu.component';
import { QuickNavigationComponent } from '@racing/components/quickNavigation/quick-navigation.component';
import { DrawerComponent } from '@shared/components/drawer/drawer.component';
import { ToggleSwitchComponent } from '@shared/components/toggleSwitch/toggle-switch.component';
// eslint-disable-next-line max-len
import { RacingPoolIndicatorComponent } from '@app/lazy-modules/racingFeatured/components/racingPoolIndicator/racing-pool-indicator.component';
import { BetBuilderComponent } from '@uktote/components/betBuilder/bet-builder.component';
import { RacingAntepostTabComponent } from '@racing/components/racingAntepostTab/racing-antepost-tab.component';
import { GreyhoundFutureTabComponent } from '@racing/components/greyhound/greyhoundFutureTab/greyhound-future-tab.component';
import { EventTitleBarComponent } from '@edp/components/eventTitleBar/event-title-bar.component';
import { ScorecastComponent } from '@edp/components/markets/scorecast/scorecast.component';
import { ToteSliderComponent } from '@app/tote/components/toteSlider/tote-slider.component';
import { MultipleSportsSectionsComponent } from '@app/inPlay/components/multipleSportsSections/multiple-sports-sections.component';
import { SingleSportSectionComponent } from '@app/inPlay/components/singleSportSection/single-sport-section.component';
import { RacingEventResultedComponent } from '@racing/components/racingEventResultedComponent/racing-event-resulted.component';
import { RacingOutcomeResultedCardComponent } from '@racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';
import { BetFinderComponent } from '@app/bf/components/betFinder/bet-finder.component';
import { BetFinderResultComponent } from '@app/bf/components/betFinderResult/bet-finder-result.component';
import {
  CompetitionsStandingsTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component';
import { CompetitionsPageComponent } from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import { SportEventMainComponent } from '@edp/components/sportEventMain/sport-event-main.component';
import { RacingMainComponent } from '@racing/components/racingMain/racing-main.component';
import { NextRacesHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.component';
import { BetslipComponent } from '@betslip/components/betslip/betslip.component';
import { BetslipReceiptComponent } from '@app/betslip/components/betslipReceipt/betslip-receipt.component';
import { SlideOutBetslipComponent } from '@app/betslip/components/slideOutBetslip/slide-out-betslip.component';
import { BetSummaryComponent } from '@app/quickbet/components/betSummary/bet-summary.component';
import { QuickbetReceiptComponent } from '@app/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { SportMainComponent } from '@sb/components/sportMain/sport-main.component';
import { RacingPanelComponent } from '@shared/components/racingPanel/racing-panel.component';
import { InformationDialogComponent } from '@shared/components/informationDialog/information-dialog.component';
import { OddsCardSportComponent } from '@shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { OddsCardHeaderComponent } from '@shared/components/oddsCardHeader/odds-card-header.component';
import { BetslipTotalWrapperComponent } from '@app/betslip/components/betslipTotalWrapper/betslip-total-wrapper.component';
import { BetslipSubheaderComponent } from '@app/betslip/components/betslipSubheader/betslip-subheader.component';
import { EmptyBetslipComponent } from '@app/betslip/components/emptyBetslip/empty-betslip.component';
import { WatchLabelComponent } from '@shared/components/watchLabel/watch-label.component';
import { QuickbetSelectionComponent } from '@app/quickbet/components/quickbetSelection/quickbet-selection.component';
import { QuickbetPanelComponent } from '@app/quickbet/components/quickbetPanel/quickbet-panel.component';
import { QuickStakeComponent } from '@app/quickbet/components/quickStake/quick-stake.component';
import { QuickbetInfoPanelComponent } from '@app/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';
import { RaceCardHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/raceCardHome/race-card-home.component';
import { EventMarketsComponent } from '@edp/components/eventMarkets/event-markets.component';
import { ShowAllButtonComponent } from '@shared/components/showAllButton/show-all-button.component';
import { FeaturedEventMarketsComponent } from '@featured/components/featured-outright-market/event-markets.component';
import { FeaturedRaceCardHomeComponent } from '@featured/components/featured-race-card/race-card-home.component';
import { RaceTimerComponent } from '@shared/components/raceTimer/race-timer.component';
import { SurfaceBetsCarouselComponent } from '@shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { FreeBetToggleComponent } from '@freebets/components/freeBetToggle/free-bet-toggle.component';
import { FreeBetSelectDialogComponent } from '@freebets/components/freeBetSelectDialog/free-bet-select-dialog.component';
import { ToteFreeBetSelectDialogComponent } from '@freebets/components/tote-free-bet-select-dialog/tote-free-bet-select-dialog.component';
import { BetslipSinglesReceiptComponent } from '@app/betslip/components/betslipSinglesReceipt/betslip-singles-receipt.component';
import { BetslipMultiplesReceiptComponent } from '@app/betslip/components/betslipMultiplesReceipt/betslip-multiples-receipt.component';
import {
  BetslipReceiptSubheaderComponent
} from '@app/betslip/components/betslipReceiptSubheader/betslip-receipt-subheader.component';
import { OddsBoostBetslipHeaderComponent } from '@app/oddsBoost/components/oddsBoostBetslipHeader/odds-boost-betslip-header.component';
import { OddsBoostButtonComponent } from '@app/oddsBoost/components/oddsBoostButton/odds-boost-button.component';
import { TooltipComponent } from '@app/shared/components/tooltip/tooltip.component';
import { PromoLabelsComponent } from '@promotions/components/promoLabels/promo-labels.component';
import { SelectionInfoDialogComponent } from '@app/betslip/components/selectionInfoDialog/selection-info-dialog.component';
// eslint-disable-next-line max-len
import { OddsBoostPriceComponent } from '@oddsBoost/components/oddsBoostPrice/odds-boost-price.component';
import { ToteBetReceiptItemComponent } from '@app/betslip/components/toteBetReceiptItem/tote-bet-receipt-item.component';
import { RequestErrorComponent } from '@shared/components/requestError/request-error.component';
import { SportMatchesTabComponent } from '@sb/components/sportMatchesTab/sport-matches-tab.component';
import { FootballTutorialOverlayComponent } from '@sb/components/footballTutorialOverlay/football-tutorial-overlay.component';
import { BetslipOfferedDataComponent } from '@app/betslip/components/betslipOfferedData/betslip-offered-data.component';
import { OpenBetsComponent } from '@app/betHistory/components/openBets/open-bets.component';
import { BetHistoryPageComponent } from '@app/betHistory/components/betHistoryPage/bet-history-page.component';
import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';

import { VirtualSportsPageComponent } from '@app/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import { VirtualSportClassesComponent } from '@app/vsbr/components/virtualSportClasses/virtual-sport-classes.component';
import { VirtualCarouselMenuComponent } from '@app/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';
import { VirtualCarouselSubMenuComponent } from '@app/vsbr/components/virtualCarouselSubMenu/virtual-carousel-sub-menu.component';
import { VsOddsCardComponent } from '@app/vsbr/components/vsOddsCard/vs-odds-card.component';
import { BetHistoryPromptComponent } from '@app/betHistory/components/betHistoryPrompt/bet-history-prompt.component';
import { ToteBetReceiptComponent } from '@app/betslip/components/toteBetReceipt/tote-bet-receipt.component';
import { SportEventPageComponent } from '@edp/components/sportEventPage/sport-event-page.component';
import { AggregatedMarketsComponent } from '@edp/components/markets/aggregatedMarkets/aggregated-markets.component';
import { SingleMarketsComponent } from '@edp/components/markets/singleMarkets/single-markets.component';
import { ConnectionLostDialogComponent } from '@app/shared/components/connectionLostDialog/connection-lost-dialog.component';
import { AccaNotificationComponent } from '@app/shared/components/accaNotification/acca-notification.component';
import { MaxStakeDialogComponent } from '@app/betslip/components/maxStakeDialog/max-stake-dialog.component';
import { ExpandPanelComponent } from '@app/shared/components/expandPanel/expand-panel.component';
import {
  EventHeaderComponent as CoralEventHeaderComponent
} from '@app/betHistory/components/eventHeader/event-header.component';
import { FreeBetLabelComponent as AppFreeBetLabelComponent } from '@app/shared/components/freeBetLabel/free-bet-label.component';
import { BetslipTabsComponent } from '@app/betHistory/components/betslipTabs/betslip-tabs.component';
import { LottoNumberSelectorComponent } from '@app/lotto/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { CashOutBetsComponent } from '@app/betHistory/components/cashOutBets/cash-out-bets.component';
import { PromotionsComponent } from '@app/promotions/components/promotion/promotions.component';
import { DatePickerComponent as CoralDatePickerComponent } from '@app/shared/components/datePicker/date-picker.component';
import { DeclinedBetComponent } from '@betslip/components/declinedBet/declined-bet.component';
import { SortByOptionsComponent } from '@lazy-modules/sortByOptions/components/sort-by-options.component';
import { RacingTabsMainComponent } from '@app/racing/components/racingTabsMain/racing-tabs-main.component';
import { MyBetsComponent } from '@app/betHistory/components/myBets/my-bets.component';
import { BetslipLimitationDialogComponent } from '@betslip/components/betslipLimitationDialog/betslip-limitation-dialog.component';
import { PromotionDialogComponent } from '@promotions/components/promotionDialog/promotion-dialog.component';
import { BppErrorDialogComponent } from '@shared/components/bppErrorDialog/bpp-error-dialog.component';
import { YourcallDashboardComponent } from '@yourcall/components/yourcallDashboard/yourcall-dashboard.component';
import { YourCallMarketGroupComponent } from '@yourcall/components/yourCallMarketGroup/your-call-market-group.component';
import { YourCallMarketPlayerBetsComponent } from '@yourcall/components/yourCallMarketPlayerBets/your-call-market-player-bets.component';
import { LoadingScreenComponent } from '@shared/components/loadingScreen/loading-screen.component';
import { BetLegItemComponent as CoralBetLegItemComponent } from '@app/betHistory/components/betLegItem/bet-leg-item.component';
import { BybSelectionsComponent } from '@lazy-modules/bybHistory/components/bybSelections/byb-selections.component';
import { SplashPageComponent } from '@app/questionEngine/components/splashPage/splash-page.component';
import { ResultsPageComponent } from '@app/questionEngine/components/resultsPage/results-page.component';
import { InfoPageComponent } from '@app/questionEngine/components/shared/infoPage/info-page.component';
import { InfoDialogComponent } from '@app/questionEngine/components/shared/infoDialog/info-dialog.component';
import { AnswersSummaryComponent } from '@app/questionEngine/components/shared/answersSummary/answers-summary.component';
import { QuestionsInfoComponent } from '@app/questionEngine/components/questionsPage/questions-info/questions-info.component';
import { QuestionsPageComponent } from '@app/questionEngine/components/questionsPage/questions-page.component';
import { QuestionsCarouselComponent } from '@app/questionEngine/components/questionsPage/questionsCarousel/questions-carousel.component';
import { LatestTabComponent } from '@app/questionEngine/components/resultsPage/tabs/latestTab/latest-tab.component';
import { PreviousTabComponent } from '@app/questionEngine/components/resultsPage/tabs/previousTab/previous-tab.component';
import { UpsellComponent } from '@app/questionEngine/components/resultsPage/upsell/upsell.component';
import { BogLabelComponent } from '@shared/components/bogLabel/bog-label.component';
import { FreebetsComponent } from '@freebets/components/freebets/freebets.component';
import { EnhancedMultiplesTabComponent } from '@app/lazy-modules/enhancedMultiplesTab/components/enhanced-multiples-tab.component';
import { OddsCardScoreComponent as AppOddsCardScoreComponent } from '@shared/components/oddsCard/oddsCardScore/odds-card-score.component';
import { RacingFeaturedComponent } from '@app/lazy-modules/racingFeatured/components/racingFeatured/racing-featured.component';
import { RacingEventsComponent } from '@app/lazy-modules/racingFeatured/components/racingEvents/racing-events.component';
import {
  OddsCardEnhancedMultiplesComponent
} from '@shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
import { StarRatingComponent } from '@shared/components/star-rating/star-rating.component';
import { MarketDescriptionComponent } from '@lazy-modules/market-description/components/market-description/market-description.component';
import { RacingTooltipComponent } from '@lazy-modules/market-description/components/racing-tooltip/racing-tooltip.component';
import { CorrectScoreComponent } from '@app/edp/components/markets/correctScore/correct-score.component';
import { ScorerComponent } from '@app/edp/components/markets/scorer/scorer.component';
import { FreeBetsNotificationComponent } from '@shared/components/freeBetsNotification/free-bets-notification.component';
import { BigCompetitionComponent } from '@app/bigCompetitions/components/bigCompetition/big-competition.component';
import { ToteFreeBetsToggleComponent } from '@freebets/components/tote-free-bets-toggle/tote-free-bets-toggle.component';
import { VirtualHomePageComponent } from '@app/vsbr/components/virtualHomePage/virtual-home-page.component';
import { VirtualOtherSports } from '@app/vsbr/components/virtualOtherSports/virtual-other-sports.component';
import { SbBetSummaryComponent } from '@app/quickbet-stream-bet/components/betSummary/sb-bet-summary.component';
import { SbQuickbetPanelComponent } from '@app/quickbet-stream-bet/components/quickbetPanel/sb-quickbet-panel.component';
import { SbQuickbetSelectionComponent } from '@app/quickbet-stream-bet/components/quickbetSelection/sb-quickbet-selection.component';
import { SbQuickbetReceiptComponent } from '@app/quickbet-stream-bet/components/quickbetReceipt/sb-quickbet-receipt.component';

@NgModule({
  declarations: [
    FreebetsComponent,
    FreeBetsNotificationComponent,
    BetslipTabsComponent,
    CashOutBetsComponent,
    ExpandPanelComponent,
    RaceTimerComponent,
    BmaMainComponent,
    BetslipCounterComponent,
    HistoricPricesComponent,
    AccordionComponent,
    TabsPanelComponent,
    FooterSectionComponent,
    PromotionsListComponent,
    RaceGridComponent,
    SwitchersComponent,
    ToteSliderComponent,
    RacingPoolIndicatorComponent,
    CouponsDetailsComponent,
    BigCompetitionComponent,
    GoalscorerCouponComponent,
    AppPrivateMarketsTabComponent,
    CorrectScoreCouponComponent,
    RacingSpecialsCarouselComponent,
    SwitchersComponent,
    OffersAndFeaturedRacesComponent,
    FeaturedModuleComponent,
    OddsBoostInfoDialogComponent,
    RetailPageComponent,
    OxygenBetFilterComponent,
    FeaturedQuickLinksComponent,
    ForecastTricastMarketComponent,
    ForcastTricastRaceCardComponent,
    EventVideoStreamComponent,
    VideoStreamErrorDialogComponent,
    BreadcrumbsComponent,
    CashoutLabelComponent,
    PromotionIconComponent,
    PromoLabelsComponent,
    RaceCardsControlsComponent,
    HorseRaceGridComponent,
    TopBarComponent,
    RacingEventComponent,
    RacingOutcomeResultedCardComponent,
    RacingEventResultedComponent,
    RacingAntepostTabComponent,
    GreyhoundFutureTabComponent,
    GreyhoundsTabsComponent,
    BetBuilderComponent,
    RacingEventComponent,
    NextRacesHomeTabComponent,
    RaceCardHomeComponent,
    CompetitionsResultsTabComponent,
    CompetitionsStandingsTabComponent,
    CompetitionsPageComponent,
    ExtraPlaceHomeComponent,
    OddsCardSportComponent,
    OddsCardHeaderComponent,
    // OddsCardHighlightCarouselComponent,
    OddsCardResultComponent,
    FeaturedHighlightsCarouselComponent,
    OddsCardSurfaceBetComponent,
    HorseracingTabsComponent,
    InplayAllSportsPageComponent,
    InplayPageComponent,
    InplaySingleSportPageComponent,
    InplayTabComponent,
    InplayWatchLivePageComponent,
    RacingOutcomeCardComponent,
    RacingEventMainComponent,
    SortByOptionsComponent,
    DropDownMenuComponent,
    OxygenDialogComponent,
    GreyhoundsTabsComponent,
    BetBuilderComponent,
    RacingSpecialsTabComponent,
    FeaturedInplayComponent,
    QuickNavigationComponent,
    ToggleSwitchComponent,
    DrawerComponent,
    MultipleSportsSectionsComponent,
    SingleSportSectionComponent,
    HorseracingTabsComponent,
    RacingMainComponent,
    HorseracingTabsComponent,
    SportEventMainComponent,
    BetFinderComponent,
    BetFinderResultComponent,
    EventMarketsComponent,
    EventTitleBarComponent,
    ScorecastComponent,
    BetslipComponent,
    SlideOutBetslipComponent,
    BetSummaryComponent,
    QuickbetReceiptComponent,
    BetslipReceiptComponent,
    SportMainComponent,
    RacingPanelComponent,
    NextRacesHomeComponent,
    InformationDialogComponent,
    BetslipTotalWrapperComponent,
    BetslipSubheaderComponent,
    EmptyBetslipComponent,
    WatchLabelComponent,
    SurfaceBetsCarouselComponent,
    QuickbetSelectionComponent,
    QuickbetPanelComponent,
    QuickStakeComponent,
    QuickbetInfoPanelComponent,
    ShowAllButtonComponent,
    FeaturedEventMarketsComponent,
    FeaturedRaceCardHomeComponent,
    LpSpDropdownComponent,
    FreeBetToggleComponent,
    FreeBetSelectDialogComponent,
    ToteFreeBetSelectDialogComponent,
    ToteFreeBetsToggleComponent,
    BetslipSinglesReceiptComponent,
    BetslipMultiplesReceiptComponent,
    BetslipReceiptSubheaderComponent,
    OddsBoostBetslipHeaderComponent,
    OddsBoostButtonComponent,
    OddsBoostPriceComponent,
    TooltipComponent,
    SelectionInfoDialogComponent,
    ToteBetReceiptItemComponent,
    RequestErrorComponent,
    SportMatchesTabComponent,
    FootballTutorialOverlayComponent, // TODO not in use?
    BetslipOfferedDataComponent,
    OpenBetsComponent,
    BetHistoryPageComponent,
    VirtualSportsPageComponent,
    VirtualSportClassesComponent,
    VirtualCarouselMenuComponent,
    VirtualCarouselSubMenuComponent,
    VsOddsCardComponent,
    BetHistoryPromptComponent,
    AccaNotificationComponent,
    ToteBetReceiptComponent,
    SportEventPageComponent,
    AggregatedMarketsComponent,
    SingleMarketsComponent,
    ConnectionLostDialogComponent,
    MaxStakeDialogComponent,
    LottoNumberSelectorComponent,
    PromotionsComponent,
    CoralEventHeaderComponent,
    AppFreeBetLabelComponent,
    RacingTabsMainComponent,
    CoralDatePickerComponent,
    DeclinedBetComponent,
    CoralDatePickerComponent,
    MyBetsComponent,
    BetslipLimitationDialogComponent,
    PromotionDialogComponent,
    BppErrorDialogComponent,
    LoadingScreenComponent,
    YourcallDashboardComponent,
    BetslipHeaderIconComponent,
    YourCallMarketGroupComponent,
    YourCallMarketPlayerBetsComponent,
    SplashPageComponent,
    ResultsPageComponent,
    InfoDialogComponent,
    QuestionsPageComponent,
    QuestionsCarouselComponent,
    LatestTabComponent,
    PreviousTabComponent,
    UpsellComponent,
    AnswersSummaryComponent,
    QuestionsInfoComponent,
    InfoPageComponent,
    BogLabelComponent,
    CoralBetLegItemComponent,
    EnhancedMultiplesTabComponent,
    BogLabelComponent,
    AppOddsCardScoreComponent,
    RacingFeaturedComponent,
    RacingEventsComponent,
    OddsCardEnhancedMultiplesComponent,
    BybSelectionsComponent,
    StarRatingComponent,
    MarketDescriptionComponent,
    RacingTooltipComponent,
    CorrectScoreComponent,
    ScorerComponent,
    VirtualHomePageComponent,
    VirtualOtherSports,
    SbQuickbetPanelComponent,
    SbQuickbetSelectionComponent,
    SbBetSummaryComponent,
    SbQuickbetReceiptComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    SharedPipesModule
  ],
  exports: [],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FakeModule { }

// This module is required only to allow coralDesktop to build with AOT
// Here you should place all components which extended by coral desktop
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

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

import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';
import { OddsCardHeaderComponent } from '@shared/components/oddsCardHeader/odds-card-header.component';
import { TabsPanelComponent } from '@shared/components/tabsPanel/tabs-panel.component';
import { TopBarComponent } from '@shared/components/topBar/top-bar.component';
import { OddsCardResultComponent } from '@shared/components/oddsCardResult/odds-card-result.component';
import { OddsCardComponent } from '@shared/components/oddsCard/odds-card.component';
import { OffersSectionComponent } from '@bma/components/offerSection/offer-section.component';
import {
  RacingEnhancedMultiplesComponent
} from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.component';
import {
  OddsCardEnhancedMultiplesComponent
} from '@shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
import { HomeComponent } from '@bma/components/home/home.component';
import { BmaMainComponent } from '@app/bma/components/bmaMain/bma-main.component';
import {
  EnhancedMultiplesTabComponent
} from '@ladbrokesMobile/lazy-modules/enhancedMultiplesTab/components/enhanced-multiples-tab.component';
import { LadbrokesBmaMainComponent } from '@ladbrokesMobile/bma/components/bmaMain/bma-main.component';
import { EventTitleBarComponent } from '@edp/components/eventTitleBar/event-title-bar.component';
import { ScorecastComponent } from '@edp/components/markets/scorecast/scorecast.component';
import { SportEventMainComponent } from '@app/edp/components/sportEventMain/sport-event-main.component';
import { MarketsGroupComponent } from '@app/edp/components/marketsGroup/markets-group.component';
import {
  SportEventMainComponent as LMSportEventMainComponent
} from '@ladbrokesMobile/edp/components/sportEventMain/sport-event-main.component';
import { SportEventPageComponent } from '@app/edp/components/sportEventPage/sport-event-page.component';
import { OddsCardSpecialsComponent } from '@shared/components/oddsCard/oddsCardSpecials/odds-card-specials.component';
import { OddsCardSportComponent } from '@shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { BigCompetitionComponent } from '@app/bigCompetitions/components/bigCompetition/big-competition.component';
import { FavouritesMatchesComponent } from '@app/favourites/components/matchList/favourites-matches.component';
import { FeaturedModuleComponent } from '@featured/components/featured-module/featured-module.component';
import { OlympicsPageComponent } from '@app/olympics/components/olympicsPage/olympics-page.component';
import { BybHomeComponent } from '@yourcall/components/bybHome/byb-home.component';
import { YourcallBybLeagueComponent } from '@yourcall/components/bybLeague/yourcall-byb-league.component';
import { YourCallTabContentComponent } from '@yourcall/components/yourCallTabContent/your-call-tab-content.component';
import { VirtualSportsPageComponent } from '@app/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import { TotePageComponent } from '@app/tote/components/totePage/tote-page.component';
import { ToteInfoComponent } from '@app/tote/components/toteInfo/tote-info.component';
import { ToteSliderComponent } from '@app/tote/components/toteSlider/tote-slider.component';
import { LottoMainComponent } from '@app/lotto/components/lottoMain/lotto-main.component';
import { GreyhoundsTabsComponent } from '@racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { HorseracingTabsComponent } from '@racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';
import { HorseRaceGridComponent } from '@app/lazy-modules/racingFeatured/components/horseRaceGrid/horse-race-grid.component';
import { RacingAntepostTabComponent } from '@app/racing/components/racingAntepostTab/racing-antepost-tab.component';
import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { RacingMainComponent } from '@racing/components/racingMain/racing-main.component';
import { RacingSpecialsTabComponent } from '@racing/components/racingSpecialsTab/racing-specials-tab.component';
import { RacingYourcallSpecialsComponent } from '@racing/components/racingYourcallSpecials/racing-yourcall-specials.component';
import { TimeFormSelectionSummaryComponent } from '@racing/components/timeformSummary/time-form-selection-summary.component';
import { RacingOutcomeCardComponent } from '@racing/components/racingOutcomeCard/racing-outcome-card.component';
import { SportMatchesPageComponent } from '@app/sb/components/sportMatchesPage/sport-matches-page.component';
import { SportMainComponent } from '@app/sb/components/sportMain/sport-main.component';
import { RaceCardsControlsComponent } from '@racing/components/raceCardControls/race-cards-controls.component';
import {
  CompetitionsOutrightsTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-outrights-tab.component';
import { CouponsDetailsComponent } from '@sb/components/couponsDetails/coupons-details.component';
import { CompetitionsPageComponent } from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import { OffersAndFeaturedRacesComponent } from '@racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';
import {
  CompetitionsFutureSportTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsFutureSportTab/competitions-future-sport-tab.component';
import {
  CompetitionsSportTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-sport-tab.component';
import { AllPromotionsPageComponent } from '@promotions/components/allPromotionsPage/all-promotions-page.component';
import { SinglePromotionPageComponent } from '@promotions/components/singlePromotionPage/single-promotion-page.component';
import { PromotionsComponent } from '@promotions/components/promotion/promotions.component';
import { PromotionsListComponent } from '@app/promotions/components/promotionsList/promotions-list.component';
import { SportMatchesTabComponent } from '@app/sb/components/sportMatchesTab/sport-matches-tab.component';
import {
  CompetitionsMatchesTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-matches-tab.component';
// eslint-disable-next-line
import {
  CompetitionsStandingsTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component';
import { CorrectScoreCouponComponent } from '@sb/components/correctScoreCoupon/correct-score-coupon.component';
import { RetailPageComponent } from '@app/retail/components/retailPage/retail-page.component';
// import { RetailPageComponent as RetailPageComponentLadbroke } from '@ladbrokesMobile/retail/components/retailPage/retail-page.component';
// import { ShopLocatorComponent } from '@app/retail/components/shopLocator/shop-locator.component';
// import { BetFilterDialogComponent } from '@app/retail/components/betFilterDialog/bet-filter-dialog.component';
import { BetFilterComponent as OxygenBetFilterComponent } from '@app/retail/components/betFilter/bet-filter.component';

import { FeaturedQuickLinksComponent } from '@featured/components/featured-quick-links/featured-quick-links.component';
import { NgCarouselExtendedDirective } from '@shared/directives/ng-carousel-extended/carousel.directive';
import { OddsBoostInfoDialogComponent } from '@shared/components/oddsBoostInfoDialog/odds-boost-info-dialog.component';
import { BreadcrumbsComponent } from '@app/shared/components/breadcrumbs/breadcrumbs.component';
import { PromotionIconComponent } from '@app/promotions/components/promotionIcon/promotion-icon.component';
import { CashoutLabelComponent } from '@app/shared/components/cashoutLabel/cashout-label.component';
import { InplayAllSportsPageComponent } from '@app/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { InplayPageComponent } from '@app/inPlay/components/inplayPage/inplay-page.component';
import { InplaySingleSportPageComponent } from '@app/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayTabComponent } from '@app/inPlay/components/inplayTab/inplay-tab.component';
import { InplayWatchLivePageComponent } from '@app/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import { MultipleSportsSectionsComponent } from '@app/inPlay/components/multipleSportsSections/multiple-sports-sections.component';
import { SingleSportSectionComponent } from '@app/inPlay/components/singleSportSection/single-sport-section.component';
import { FeaturedInplayComponent } from '@featured/components/featured-inplay/featured-inplay.component';
import { LpSpDropdownComponent } from '@freebets/components/lpSpDropdown/lp-sp-dropdown.component';
import { DropDownMenuComponent } from '@shared/components/dropDownMenu/drop-down-menu.component';
// eslint-disable-next-line
import { BetBuilderComponent } from '@uktote/components/betBuilder/bet-builder.component';
import { StickyVirtualScrollerComponent } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.component';
import { BetslipComponent } from '@betslip/components/betslip/betslip.component';
import { BetslipReceiptComponent } from '@app/betslip/components/betslipReceipt/betslip-receipt.component';
// import { NextRacesModuleComponent } from '@app/racing/components/nextRaces/next-races.component';
import { DrawerComponent } from '@shared/components/drawer/drawer.component';
import { SwitchersComponent } from '@shared/components/switchers/switchers.component';
import { RacingEventResultedComponent } from '@racing/components/racingEventResultedComponent/racing-event-resulted.component';
import { RacingOutcomeResultedCardComponent } from '@racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';
import { OddsCardSurfaceBetComponent } from '@shared/components/oddsCard/oddsCardSurfaceBet/odds-card-surface-bet.component';
import { SurfaceBetsCarouselComponent } from '@shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { OutrightsSportTabComponent } from '@sb/components/outrightsSportTab/outrights-sport-tab.component';
import { DatePickerComponent } from '@shared/components/datePicker/date-picker.component';
import {
  PrivateMarketsTabComponent as AppPrivateMarketsTabComponent
} from '@sb/components/privateMarketsTab/private-markets-tab.component';

import {
  NextRacesHomeTabComponent
} from '@app/lazy-modules/lazyNextRacesTab/components/nextRacesHomeTab/next-races-home-tab.component';
import { ExtraPlaceHomeComponent } from '@app/lazy-modules/lazyNextRacesTab/components/extraPlaceHome/extra-place-home.component';
import { RacingPanelComponent } from '@shared/components/racingPanel/racing-panel.component';
import { NextRacesHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.component';
import {
  RightColumnWidgetItemComponent
} from '@app/lazy-modules/rightColumn/components/rightColumnWidgetItem/right-column-widget-item.component';
import { RightColumnWidgetComponent } from '@app/lazy-modules/rightColumn/components/rightColumnWidget/right-column-widget.component';
import { InformationDialogComponent } from '@shared/components/informationDialog/information-dialog.component';
import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';
import { RaceCardHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/raceCardHome/race-card-home.component';
import { FeaturedEventMarketsComponent } from '@featured/components/featured-outright-market/event-markets.component';
import { FeaturedRaceCardHomeComponent } from '@featured/components/featured-race-card/race-card-home.component';
import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';
import { BetslipTotalWrapperComponent } from '@app/betslip/components/betslipTotalWrapper/betslip-total-wrapper.component';
import { BetslipSubheaderComponent } from '@app/betslip/components/betslipSubheader/betslip-subheader.component';
import { EmptyBetslipComponent } from '@app/betslip/components/emptyBetslip/empty-betslip.component';
import { WatchLabelComponent } from '@shared/components/watchLabel/watch-label.component';
import { AccordionComponent } from '@shared/components/accordion/accordion.component';
import { FreeBetToggleComponent } from '@freebets/components/freeBetToggle/free-bet-toggle.component';
import { FreeBetSelectDialogComponent } from '@freebets/components/freeBetSelectDialog/free-bet-select-dialog.component';
import { ToteFreeBetsToggleComponent } from '@freebets/components/tote-free-bets-toggle/tote-free-bets-toggle.component';
import { ToteFreeBetSelectDialogComponent } from '@freebets/components/tote-free-bet-select-dialog/tote-free-bet-select-dialog.component';
import { BetslipSinglesReceiptComponent } from '@app/betslip/components/betslipSinglesReceipt/betslip-singles-receipt.component';
import { BetslipMultiplesReceiptComponent } from '@app/betslip/components/betslipMultiplesReceipt/betslip-multiples-receipt.component';
import {
  BetslipReceiptSubheaderComponent
} from '@app/betslip/components/betslipReceiptSubheader/betslip-receipt-subheader.component';
import { OddsBoostBetslipHeaderComponent } from '@app/oddsBoost/components/oddsBoostBetslipHeader/odds-boost-betslip-header.component';
import { OddsBoostButtonComponent } from '@app/oddsBoost/components/oddsBoostButton/odds-boost-button.component';
import { TooltipComponent } from '@app/shared/components/tooltip/tooltip.component';
import { SelectionInfoDialogComponent } from '@app/betslip/components/selectionInfoDialog/selection-info-dialog.component';
import { OxygenDialogComponent } from '@app/shared/components/oxygenDialogs/oxygen-dialog.component';
import { OddsBoostPriceComponent } from '@oddsBoost/components/oddsBoostPrice/odds-boost-price.component';
import { PromoLabelsComponent } from '@app/promotions/components/promoLabels/promo-labels.component';
import { FootballTutorialOverlayComponent } from '@sb/components/footballTutorialOverlay/football-tutorial-overlay.component';
import { RequestErrorComponent } from '@shared/components/requestError/request-error.component';
import { BetSummaryComponent } from '@app/quickbet/components/betSummary/bet-summary.component';
import { QuickStakeComponent } from '@app/quickbet/components/quickStake/quick-stake.component';
import { QuickbetComponent } from '@app/quickbet/components/quickbet/quickbet.component';
import { QuickbetInfoPanelComponent } from '@app/quickbet/components/quickbetInfoPanel/quickbet-info-panel.component';
import { QuickbetPanelComponent } from '@app/quickbet/components/quickbetPanel/quickbet-panel.component';
import { QuickbetReceiptComponent } from '@app/quickbet/components/quickbetReceipt/quickbet-receipt.component';
import { QuickbetSelectionComponent } from '@app/quickbet/components/quickbetSelection/quickbet-selection.component';
import { BetslipOfferedDataComponent } from '@betslip/components/betslipOfferedData/betslip-offered-data.component';
import { OpenBetsComponent } from '@app/betHistory/components/openBets/open-bets.component';
import { BetHistoryPageComponent } from '@app/betHistory/components/betHistoryPage/bet-history-page.component';
import { ToteBetReceiptItemComponent } from '@app/betslip/components/toteBetReceiptItem/tote-bet-receipt-item.component';
import { VirtualSportClassesComponent } from '@app/vsbr/components/virtualSportClasses/virtual-sport-classes.component';
import { VirtualCarouselMenuComponent } from '@app/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';
import { VirtualCarouselSubMenuComponent } from '@app/vsbr/components/virtualCarouselSubMenu/virtual-carousel-sub-menu.component';
import { VsOddsCardComponent } from '@app/vsbr/components/vsOddsCard/vs-odds-card.component';
import { BetHistoryPromptComponent } from '@app/betHistory/components/betHistoryPrompt/bet-history-prompt.component';
import { ConnectionLostDialogComponent } from '@app/shared/components/connectionLostDialog/connection-lost-dialog.component';
import { MaxStakeDialogComponent } from '@app/betslip/components/maxStakeDialog/max-stake-dialog.component';
import { GoalscorerCouponComponent } from '@app/sb/components/goalscorerCoupon/goalscorer-coupon.component';
import { ExpandPanelComponent } from '@app/shared/components/expandPanel/expand-panel.component';
import { BetslipTabsComponent } from '@app/betHistory/components/betslipTabs/betslip-tabs.component';
import { LottoNumberSelectorComponent } from '@app/lotto/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { CashOutBetsComponent } from '@app/betHistory/components/cashOutBets/cash-out-bets.component';
import {
  EventHeaderComponent as CoralEventHeaderComponent
} from '@app/betHistory/components/eventHeader/event-header.component';
import { FreeBetLabelComponent as AppFreeBetLabelComponent } from '@app/shared/components/freeBetLabel/free-bet-label.component';
import { SortByOptionsComponent } from '@lazy-modules/sortByOptions/components/sort-by-options.component';
import { RacingTabsMainComponent } from '@app/racing/components/racingTabsMain/racing-tabs-main.component';
import { MyBetsComponent } from '@app/betHistory/components/myBets/my-bets.component';
import { DeclinedBetComponent } from '@betslip/components/declinedBet/declined-bet.component';

import { BetslipLimitationDialogComponent } from '@betslip/components/betslipLimitationDialog/betslip-limitation-dialog.component';
import { PromotionDialogComponent } from '@promotions/components/promotionDialog/promotion-dialog.component';
import { BppErrorDialogComponent } from '@shared/components/bppErrorDialog/bpp-error-dialog.component';
import { YourcallDashboardComponent } from '@yourcall/components/yourcallDashboard/yourcall-dashboard.component';
import { YourCallMarketGroupComponent } from '@yourcall/components/yourCallMarketGroup/your-call-market-group.component';
import { YourCallMarketPlayerBetsComponent } from '@yourcall/components/yourCallMarketPlayerBets/your-call-market-player-bets.component';
import { LoadingScreenComponent } from '@shared/components/loadingScreen/loading-screen.component';
import { BetslipHeaderIconComponent } from '@ladbrokesMobile/shared/components/betslipHeaderIcon/betslip-header-icon.component';
import { BetLegItemComponent as CoralBetLegItemComponent } from '@app/betHistory/components/betLegItem/bet-leg-item.component';
import { BogLabelComponent } from '@shared/components/bogLabel/bog-label.component';
import { FreebetsComponent } from '@freebets/components/freebets/freebets.component';
import { OddsCardScoreComponent as AppOddsCardScoreComponent } from '@shared/components/oddsCard/oddsCardScore/odds-card-score.component';

// eslint-disable-next-line max-len
import { RacingFeaturedComponent } from '@app/lazy-modules/racingFeatured/components/racingFeatured/racing-featured.component';
// eslint-disable-next-line max-len
import { RacingEventsComponent } from '@app/lazy-modules/racingFeatured/components/racingEvents/racing-events.component';
import { StarRatingComponent } from '@shared/components/star-rating/star-rating.component';
import { BybSelectionsComponent } from '@lazy-modules/bybHistory/components/bybSelections/byb-selections.component';
import { MarketDescriptionComponent } from '@lazy-modules/market-description/components/market-description/market-description.component';
import { RacingTooltipComponent } from '@lazy-modules/market-description/components/racing-tooltip/racing-tooltip.component';
import { CorrectScoreComponent } from '@app/edp/components/markets/correctScore/correct-score.component';
import { ScorerComponent } from '@app/edp/components/markets/scorer/scorer.component';
import { FreeBetsNotificationComponent } from '@shared/components/freeBetsNotification/free-bets-notification.component';
import { StreamBetTemplatesComponent } from '@eventVideoStream/components/stream-bet/templates-provider/stream-bet-templates.component';
import { StreamBetProviderComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/video-providers/stream-bet-provider.component';
import { StreamBetIOSProviderComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/video-providers-ios/stream-bet-ios-provider.component';
import { StreamBetOverlayProviderComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/overlay-provider/stream-bet-overlay-provider.component'
import { StreamBetOverlayProviderRacingComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/overlay-provider-racing/stream-bet-overlay-provider-racing.component';
import { SbCorrectScoreMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/correct-score-market-item/sb-correct-score-market-item.component';
import { StreamBetTemplateDropDownComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/drop-down/sb-template-drop-down.component';
import { SbSingleDropDownSingleOddComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/single-drop-down-single-odd/sb-single-drop-down-single-odd.component';
import { SbPriceOddsButtonComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/price-odds-button/sb-price-odds-button.component';
import { SbRacingMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/racing-market-item/sb-racing-market-item.component';
import { SBPriceOddsClassDirective } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/price-odds-button/sb-price-odds-class.directive';
import { SBPriceOddsDisabledDirective } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/price-odds-button/sb-price-odds-disabled.directive';
import { SbOverUnderMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/over-under-market-item/sb-over-under-market-item.component';
import { SbSingleDropDoubleOddItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/single-drop-double-odd-item/sb-single-drop-double-odd-item.component';
import { SbGroupedMarketTemplatesComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/grouped-market-templates/sb-grouped-market-templates.component';
import { SbMultipleOddsMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/multiple-odds-market-item/sb-multiple-odds-market-item.component';
import { SbCounterComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/counter/sb-counter.component';

@NgModule({
  declarations: [
    // overridden ladbrokes mobile components
    BetslipTabsComponent,
    BetslipHeaderIconComponent,
    CashOutBetsComponent,
    OffersAndFeaturedRacesComponent,
    FeaturedEventMarketsComponent,
    ExpandPanelComponent,
    FeaturedRaceCardHomeComponent,
    // NextRacesModuleComponent,
    NextRacesHomeTabComponent,
    ExtraPlaceHomeComponent,
    DatePickerComponent,
    RaceCardHomeComponent,
    RightColumnWidgetItemComponent,
    RightColumnWidgetComponent,
    LpSpDropdownComponent,
    SinglePromotionPageComponent,
    AllPromotionsPageComponent,
    CompetitionsSportTabComponent,
    CorrectScoreCouponComponent,
    CompetitionsPageComponent,
    CompetitionsFutureSportTabComponent,
    CouponsDetailsComponent,
    SportMatchesTabComponent,
    CompetitionsOutrightsTabComponent,
    SportMainComponent,
    SportMatchesPageComponent,
    AccordionComponent,
    OddsCardHeaderComponent,
    TabsPanelComponent,
    TopBarComponent,
    OddsCardResultComponent,
    OddsCardComponent,
    OffersSectionComponent,
    OddsCardEnhancedMultiplesComponent,
    OddsCardSurfaceBetComponent,
    SurfaceBetsCarouselComponent,
    HomeComponent,
    BmaMainComponent,
    LadbrokesBmaMainComponent,
    EventTitleBarComponent,
    ScorecastComponent,
    SportEventMainComponent,
    MarketsGroupComponent,
    RaceCardsControlsComponent,
    SportEventPageComponent,
    OddsCardSpecialsComponent,
    OddsCardSportComponent,
    BigCompetitionComponent,
    FavouritesMatchesComponent,
    FeaturedModuleComponent,
    OlympicsPageComponent,
    BybHomeComponent,
    YourcallBybLeagueComponent,
    YourCallTabContentComponent,
    VirtualSportsPageComponent,
    VirtualSportClassesComponent,
    VirtualCarouselMenuComponent,
    VirtualCarouselSubMenuComponent,
    RacingEnhancedMultiplesComponent,
    VsOddsCardComponent,
    TotePageComponent,
    ToteInfoComponent,
    ToteSliderComponent,
    LottoMainComponent,
    GreyhoundsTabsComponent,
    HorseracingTabsComponent,
    // InspiredVirtualComponent,
    HorseRaceGridComponent,
    RacingAntepostTabComponent,
    RacingEventComponent,
    RacingMainComponent,
    RacingSpecialsTabComponent,
    RacingYourcallSpecialsComponent,
    TimeFormSelectionSummaryComponent,
    RacingOutcomeCardComponent,
    CompetitionsMatchesTabComponent,
    CompetitionsStandingsTabComponent,
    PromotionsComponent,
    RetailPageComponent,
    // RetailPageComponentLadbroke,
    // ShopLocatorComponent,
    // BetFilterDialogComponent,
    OxygenBetFilterComponent,
    FeaturedQuickLinksComponent,
    NgCarouselExtendedDirective,
    OddsBoostInfoDialogComponent,
    BreadcrumbsComponent,
    PromotionIconComponent,
    PromotionsListComponent,
    CashoutLabelComponent,
    ForecastTricastMarketComponent,
    ForcastTricastRaceCardComponent,
    EventVideoStreamComponent,
    VideoStreamErrorDialogComponent,
    RacingEventResultedComponent,
    RacingOutcomeResultedCardComponent,
    InplayAllSportsPageComponent,
    InplayPageComponent,
    InplaySingleSportPageComponent,
    InplayTabComponent,
    InplayWatchLivePageComponent,
    MultipleSportsSectionsComponent,
    SingleSportSectionComponent,
    FeaturedInplayComponent,
    DropDownMenuComponent,
    RacingSpecialsTabComponent,
    BetBuilderComponent,
    StickyVirtualScrollerComponent,
    DrawerComponent,
    BetslipComponent,
    BetslipReceiptComponent,
    SwitchersComponent,
    NextRacesHomeComponent,
    InformationDialogComponent,
    RacingAntepostTabComponent,
    RacingEventMainComponent,
    RacingPanelComponent,
    SportTabsPageComponent,
    BetslipTotalWrapperComponent,
    BetslipSubheaderComponent,
    EmptyBetslipComponent,
    WatchLabelComponent,
    LMSportEventMainComponent,
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
    PromoLabelsComponent,
    OxygenDialogComponent,
    OutrightsSportTabComponent,
    AppPrivateMarketsTabComponent,
    EnhancedMultiplesTabComponent,
    FootballTutorialOverlayComponent, // TODO not in use?
    RequestErrorComponent,
    BetSummaryComponent,
    QuickStakeComponent,
    QuickbetComponent,
    QuickbetInfoPanelComponent,
    QuickbetPanelComponent,
    QuickbetReceiptComponent,
    QuickbetSelectionComponent,
    StreamBetProviderComponent,
    StreamBetIOSProviderComponent,
    StreamBetTemplatesComponent,
    StreamBetOverlayProviderComponent,
    StreamBetOverlayProviderRacingComponent,
    SbCorrectScoreMarketItemComponent,
    SbOverUnderMarketItemComponent,
    SbSingleDropDoubleOddItemComponent,
    BetslipOfferedDataComponent,
    OpenBetsComponent,
    BetHistoryPageComponent,
    ToteBetReceiptItemComponent,
    BetHistoryPromptComponent,
    ConnectionLostDialogComponent,
    MaxStakeDialogComponent,
    GoalscorerCouponComponent,
    CoralEventHeaderComponent,
    AppFreeBetLabelComponent,
    LottoNumberSelectorComponent,
    SortByOptionsComponent,
    RacingTabsMainComponent,
    MyBetsComponent,
    DeclinedBetComponent,
    BetslipLimitationDialogComponent,
    PromotionDialogComponent,
    BppErrorDialogComponent,
    LoadingScreenComponent,
    YourcallDashboardComponent,
    YourCallMarketGroupComponent,
    YourCallMarketPlayerBetsComponent,
    CoralBetLegItemComponent,
    BogLabelComponent,
    FreebetsComponent,
    FreeBetsNotificationComponent,
    AppOddsCardScoreComponent,
    RacingFeaturedComponent,
    RacingEventsComponent,
    BybSelectionsComponent,
    StarRatingComponent,
    MarketDescriptionComponent,
    RacingTooltipComponent,
    CorrectScoreComponent,
    ScorerComponent,
    StreamBetTemplateDropDownComponent,
    SbSingleDropDownSingleOddComponent,
    SbPriceOddsButtonComponent,
    SbRacingMarketItemComponent,
    SBPriceOddsClassDirective,
    SBPriceOddsDisabledDirective,
    SbGroupedMarketTemplatesComponent,
    SbMultipleOddsMarketItemComponent,
    SbCounterComponent
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

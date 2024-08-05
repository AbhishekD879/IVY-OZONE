import { CommonModule,NgOptimizedImage  } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { RouterModule } from '@angular/router';
import { TimeFormSelectionSummaryComponent } from '@racing/components/timeformSummary/time-form-selection-summary.component';
import { SeeAllLinkComponent } from '@shared/components/seeAllLink/see-all-link.component';
import { SvgListComponent } from '@shared/components/svgList/svg-list.component';
import { FavouritesAddAllButtonComponent } from '@shared/components/favourites/components/addAllButton/favourites-add-all-button.component';
import { FavouritesAddButtonComponent } from '@shared/components/favourites/components/addButton/favourites-add-button.component';
import { FavouriteIconComponent } from '@shared/components/favourites/components/favourite-icon/favourite-icon.component';
import { FavouritesCounterComponent } from '@shared/components/favourites/components/favouritesCounter/favourites-counter.component';
import { RacingGridComponent } from '@shared/components/racingGrid/racing-grid.component';
import { FreeBetsDialogComponent } from '@shared/components/freeBetsDialog/free-bets-dialog.component';
import { FreeBetsNotificationComponent } from '@ladbrokesMobile/shared/components/freeBetsNotification/free-bets-notification.component';
import { FreeBetLabelComponent } from '@ladbrokesMobile/shared/components/freeBetLabel/free-bet-label.component';
import { AccaNotificationComponent } from '@sharedModule/components/accaNotification/acca-notification.component';
import { AccordionService } from '@shared/components/accordion/accordion.service';
import { ModuleDisabledComponent } from '@shared/components/moduleDisabled/module-disabled.component';
import { CustomSelectComponent } from '@shared/components/customSelect/custom-select.component';
import { LiveClockComponent } from '@shared/components/liveClock/live-clock.component';
import { LiveEventClockProviderService } from '@shared/components/liveClock/live-event-clock-provider.service';
import { PriceOddsButtonAnimationService } from '@shared/components/priceOddsButton/price-odds-button.animation.service';
import { PriceOddsButtonService } from '@shared/components/priceOddsButton/price-odds-button.service';
import { PriceOddsButtonComponent } from '@shared/components/priceOddsButton/price-odds-button.component';
import { PriceOddsButtonOnPushComponent } from '@shared/components/priceOddsButtonOnPush/price-odds-button-onpush.component';
import { PriceOddsValueDirective } from '@shared/components/priceOddsButton/price-odds-value.directive';
import { PriceOddsDisabledDirective } from '@shared/components/priceOddsButton/price-odds-disabled.directive';
import { PriceOddsClassDirective } from '@shared/components/priceOddsButton/price-odds-class.directive';
import { OddsCardHeaderService } from '@shared/components/oddsCardHeader/odds-card-header.service';
import { StaticBlockComponent } from '@sharedModule/components/staticBlock/static-block.component';
import { LocaleDirective } from '@shared/directives/locale.directive';
import { RaceListComponent } from '@shared/components/raceList/race-list.component';
import { ShowMoreComponentComponent } from '@shared/components/showMore/show-more.component';
import { ExpandPanelComponent } from '@ladbrokesMobile/shared/components/expandPanel/expand-panel.component';
import { LoadingOverlayComponent } from '@shared/components/loadingOverlay/loading-overlay.component';
import { NoEventsComponent } from '@shared/components/noEvents/no-events.component';
import { ConnectionLostDialogComponent } from '@sharedModule/components/connectionLostDialog/connection-lost-dialog.component';
import { SessionLogoutDialogComponent } from '@shared/components/sessionLogoutDialog/session-logout-dialog.component';
import { BppErrorDialogComponent } from '@sharedModule/components/bppErrorDialog/bpp-error-dialog.component';
import { InformationDialogComponent } from '@sharedModule/components/informationDialog/information-dialog.component';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { ScoreMarketBaseService } from '@shared/services/scoreMarketBase/score-market-base.service';
import { OddsCardSpecialsComponent } from '@shared/components/oddsCard/oddsCardSpecials/odds-card-specials.component';
import { OddsCardComponent } from '@shared/components/oddsCard/odds-card.component';
import { ListCardComponent } from '@shared/components/listCard/list-card.component';
import { QuickbetPanelWrapperComponent } from '@shared/components/quickbetPanelWrapper/quickbet-panel-wrapper.component';
import { NgCarouselDirective } from '@shared/directives/ng-carousel/carousel.directive';
import { PatternRestrictDirective } from '@shared/directives/pattern-restrict.directive';
import { ScrollableDirective } from '@shared/directives/scrollable.directive';
import { ScrollableRacingDirective } from '@shared/directives/scrollable-racing.directive';
import { BackButtonDirective } from '@shared/directives/back-button.directive';
import { ClickLinkDirective } from '@shared/directives/click-link.directive';
import { TriggerDirective } from '@shared/directives/trigger.directive';
import { DisableDraggingDirective } from '@shared/directives/disable-dragging.directive';
import { LazyRenderDirective } from '@shared/directives/lazy-render.directive';
import { LastMadeBetDirective } from '@shared/directives/last-made-bet.directive';
import { OverscrollFixDirective } from '@shared/directives/overscroll-fix';
import { NgInfoPanelComponent } from '@shared/components/infoPanel/ng-info-panel.component';
import { InputValueDirective } from '@shared/directives/input-value.directive';
import { ScrollFixDirective } from '@shared/directives/scroll-fix.directive';
import { LiveServIframeComponent } from '@shared/components/liveServ/live-serv-iframe.component';
import { EqualColumnDirective } from '@shared/directives/equal-column.directive';
import { MaintenanceComponent } from '@shared/components/maintenance/maintenance.component';
import { VerticalMenuComponent } from '@shared/components/verticalMenu/vertical-menu.component';
import { OxygenDialogContainerDirective } from '@shared/directives/oxygen-dialog-container.directive';
import { MarketSelectorTrackingService } from '@shared/components/marketSelector/market-selector-tracking.service';
import { DigitKeyboardComponent } from '@shared/components/digitKeyboard/digit-keyboard.component';
import { DigitKeyboardInputDirective } from '@shared/components/digitKeyboard/digit-keyboard-input.directive';
import { ScoreDigitComponent } from '@shared/components/scoreDigit/score-digit.component';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { OutletStatusComponent } from '@shared/components/outletStatus/outlet-status.component';
import { LiveLabelComponent } from '@shared/components/liveLabel/live-label.component';
import { NewLabelComponent } from '@shared/components/newLabel/new-label.component';
import { PromotionDialogComponent } from '@promotionsModule/components/promotionDialog/promotion-dialog.component';
import { PromotionOverlayDialogComponent } from '@promotions/components/promotionOverlayDialog/promotion-overlay-dialog.component';
import { OffersSectionComponent } from '@app/bma/components/offerSection/offer-section.component';
import { VisPreMatchWidgetComponent } from '@app/sb/components/visPreMatchWidget/vis-pre-match-widget.component';
import { VisualizationContainerComponent } from '@app/sb/components/visualizationContainer/visualization-container.component';
import { VisIframeDimensionsDirective } from '@app/sb/directives/vis-iframe-dimensions.directive';
import { InplayScoreComponent } from '@shared/components/inplayScore/inplay-score.component';
import { ToggleButtonsComponent } from '@shared/components/toggleButtons/toggle-buttons.component';
import { YourCallLabelComponent } from '@shared/components/yourCallLabel/your-call-label.component';
import { BybLabelComponent } from '@shared/components/bybLabel/byb-label.component';
import { LazyComponent } from '@shared/components/lazy-component/lazy-component.component';
import { LinkHrefDirective } from '@shared/directives/link-href.directive';
import { NgCarouselExtendedDirective } from '@shared/directives/ng-carousel-extended/carousel.directive';
import { SvgTeamKitComponent } from '@shared/components/svgTeamKit/svg-team-kit.component';
import { TooltipComponent } from '@sharedModule/components/tooltip/tooltip.component';
import { SpinnerComponent } from '@sharedModule/components/spinner/spinner.component';
import { TooltipDirective } from '@app/shared/directives/tooltip.directive';
import { OxygenNotificationComponent } from '@shared/components/oxygenNotification/oxygen-notification.component';
// Ladbrokes Components
import { BackButtonComponent } from '@ladbrokesMobile/shared/components/backButton/back-button.component';
import { EventCardComponent } from '@ladbrokesMobile/shared/components/eventCard/event-card.component';
import { RacingPanelComponent } from '@ladbrokesMobile/shared/components/racingPanel/racing-panel.component';
import { SurfaceBetsCarouselComponent } from '@ladbrokesMobile/shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { LadbrokesRaceGridComponent } from '@ladbrokesMobile/shared/components/raceGrid/race-grid';
import { LadbrokesBetslipCounterComponent } from '@ladbrokesMobile/shared/components/betslipCounter/betslip-counter.component';
import { LadbrokesAccordionComponent } from '@ladbrokesMobile/shared/components/accordion/accordion.component';
import { LadbrokesTabsPanelComponent } from '@ladbrokesMobile/shared/components/tabsPanel/tabs-panel.component';
import { FooterSectionComponent } from '@ladbrokesMobile/shared/components/footerSection/footer-section.component';
import { LadbrokesSwitchersComponent } from '@ladbrokesMobile/shared/components/switchers/switchers.component';
import { LadbrokesPromotionsListComponent } from '@ladbrokesMobile/promotions/components/promotionsList/promotions-list.component';
import { LadbrokesHistoricPricesComponent } from '@ladbrokesMobile/shared/components/historicPrices/historic-prices.component';
import {
  LadbrokesOddsBoostInfoDialogComponent
} from '@ladbrokesMobile/shared/components/ladbrokesMobileOddsBoostDialog/odds-boost-info-dialog.component';
// import {
//   LadbrokesMatchesMarketSelectorComponent
// } from '@ladbrokesMobile/shared/components/marketSelector/matchesMarketSelector/matches-market-selector.component';
// import {
//   LadbrokesInplayMarketSelectorComponent
// } from '@ladbrokesMobile/shared/components/marketSelector/inplayMarketSelector/inplay-market-selector.component';
import { LadbrokesBreadcrumbsComponent } from '@ladbrokesMobile/shared/components/breadcrumbs/breadcrumbs.component';
import { LadbrokesCashoutLabelComponent } from '@ladbrokesMobile/shared/components/cashoutLabel/cashout-label.component';
import { TopBarComponent } from '@ladbrokesMobile/shared/components/topBar/top-bar.component';
import { PromotionIconComponent } from '@ladbrokesMobile/promotions/components/promotionIcon/promotion-icon.component';
// import {
//   LadbrokesOddsCardHighlightCarouselComponent
// } from '@ladbrokesMobile/shared/components/oddsCard/oddsCardHightlightCarousel/odds-card-highlight-carousel.component';
import {
  LadbrokesOddsCardSurfaceBetComponent
} from '@ladbrokesMobile/shared/components/oddsCard/oddsCardSurfaceBet/odds-card-surface-bet.component';
import { LadbrokesWatchLabelComponent } from '@ladbrokesMobile/shared/components/watchLabel/watch-label.component';
import { LadbrokesDropDownMenuComponent } from '@ladbrokesMobile/shared/components/dropDownMenu/drop-down-menu.component';
import { LadbrokesOxygenDialogComponent } from '@ladbrokesMobile/shared/components/oxygenDialogs/oxygen-dialog.component';
import { StickyVirtualScrollerComponent } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.component';
import { LadbrokesToggleSwitchComponent } from '@ladbrokesMobile/shared/components/toggleSwitch/toggle-switch.component';
import { LadbrokesDrawerComponent } from '@ladbrokesMobile/shared/components/drawer/drawer.component';
import { LadbrokesOddsCardResultComponent } from '@ladbrokesMobile/shared/components/oddsCardResult/odds-card-result.component';
import { StarRatingComponent } from '@ladbrokesMobile/shared/components/star-rating/star-rating.component';
import { OddsCardSportComponent } from '@ladbrokesMobile/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { OddsCardHeaderComponent } from '@ladbrokesMobile/shared/components/oddsCardHeader/odds-card-header.component';
import { LadbrokesPromoLabelsComponent } from '@ladbrokesMobile/promotions/components/promoLabels/promo-labels.component';
import { ShowAllButtonComponent } from '@ladbrokesMobile/shared/components/showAllButton/show-all-button.component';
import { RaceTimerComponent } from '@ladbrokesMobile/shared/components/raceTimer/race-timer.component';
import { RaceCardHomeComponent } from '@ladbrokesMobile/shared/components/raceCardHome/race-card-home.component';
import { RequestErrorComponent } from '@ladbrokesMobile/shared/components/requestError/request-error.component';
import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';
import { DatePickerComponent } from '@ladbrokesMobile/shared/components/datePicker/date-picker.component';
import { LadbrokesLoadingScreenComponent } from '@ladbrokesMobile/shared/components/loadingScreen/loading-screen.component';
import { MyBetsButtonComponent } from '@shared/components/myBetsButton/my-bets-button.component';
import { BetslipHeaderIconComponent } from '@ladbrokesMobile/shared/components/betslipHeaderIcon/betslip-header-icon.component';
import { LadbrokesBogLabelComponent } from '@ladbrokesMobile/shared/components/bogLabel/bog-label.component';
import { VirtualSilkComponent } from '@shared/components/virtualSilk/virtual-silk.component';
import { OddsCardScoreComponent } from '@sharedModule/components/oddsCard/oddsCardScore/odds-card-score.component';
import { RaceSilkComponent } from '@shared/components/raceSilk/race-silk.component';
import { UkOrIreSilkComponent } from '@shared/components/raceSilk/ukOrIreSilk/uk-or-ire-silk.component';
import { GhSilkComponent } from '@shared/components/ghSilk/gh-silk.component';
import { ShowCurrencyDirective } from '@shared/directives/show-currency/show-currency.directive';
import {
  OddsCardEnhancedMultiplesComponent
} from '@ladbrokesMobile/shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
import { LadbrokesRaceCardsControlsComponent } from '@ladbrokesMobile/racing/components/race-cards-controls/race-cards-controls.component';
import { ScrollOnceDirective } from '@app/core/directives/scroll-once-directive';
import { BonusSuppressionErrorDialogComponent } from '@shared/components/bonusSuppressionErrorDialog/bonus-suppression-error-dialog.component';
import { ConnectionInterruptionDialogComponent } from '@sharedModule/components/connection-interruption-dialog/connection-interruption-dialog.component';
import { DateTimeChangeDirective } from '@app/shared/directives/date-time-change.directive';
import { FreeBetEmptyComponent } from '@sharedModule/components/freeBetEmpty/free-bet-empty.component';
import { LadbrokesRacingOutcomeCardComponent } from '@ladbrokesMobile/racing/components/racingOutcomeCard/racing-outcome-card.component';
import { ModalComponent } from '@shared/components/customModal/custom-modal.component';
import { SymbolBackgroundDirective } from '@shared/directives/symbol-background.directive';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    FormsModule,
    SharedPipesModule,
    NgOptimizedImage 
  ],
  declarations: [
    ModalComponent,
    GhSilkComponent,
    LadbrokesRacingOutcomeCardComponent,
    FreeBetEmptyComponent,
    LadbrokesAccordionComponent,
    LadbrokesTabsPanelComponent,
    LadbrokesSwitchersComponent,
    FooterSectionComponent,
    LadbrokesHistoricPricesComponent,
    LadbrokesDropDownMenuComponent,
    // LadbrokesMatchesMarketSelectorComponent,
    // LadbrokesInplayMarketSelectorComponent,
    LadbrokesBreadcrumbsComponent,
    LadbrokesCashoutLabelComponent,
    // LadbrokesOddsCardHighlightCarouselComponent,
    LadbrokesOddsCardSurfaceBetComponent,
    TopBarComponent,
    LadbrokesOxygenDialogComponent,
    LadbrokesRaceGridComponent,
    LadbrokesToggleSwitchComponent,
    LadbrokesDrawerComponent,
    LadbrokesWatchLabelComponent,
    BackButtonComponent,

    SurfaceBetsCarouselComponent,
    SeeAllLinkComponent,
    SpinnerComponent,
    LiveLabelComponent,
    NewLabelComponent,
    ListCardComponent,
    RacingPanelComponent,
    EventCardComponent,
    AccaNotificationComponent,
    OddsCardHeaderComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    CustomSelectComponent,
    OffersSectionComponent,
    LiveClockComponent,
    VisPreMatchWidgetComponent,
    VisualizationContainerComponent,
    VisIframeDimensionsDirective,
    NgCarouselExtendedDirective,
    DatePickerComponent,
    StaticBlockComponent,
    ShowMoreComponentComponent,
    ShowAllButtonComponent,
    RaceListComponent,
    VerticalMenuComponent,
    ExpandPanelComponent,
    RequestErrorComponent,
    NgInfoPanelComponent,
    LoadingOverlayComponent,
    LiveServIframeComponent,
    FreeBetsDialogComponent,
    FreeBetsNotificationComponent,
    FreeBetLabelComponent,
    SessionLogoutDialogComponent,
    ConnectionLostDialogComponent,
    InformationDialogComponent,
    BppErrorDialogComponent,
    ModuleDisabledComponent,
    QuickbetPanelWrapperComponent,
    OddsCardEnhancedMultiplesComponent,
    OddsCardSpecialsComponent,
    OddsCardSportComponent,
    OddsCardComponent,
    SvgTeamKitComponent,
    RacingGridComponent,
    RaceTimerComponent,
    SvgListComponent,
    FavouritesCounterComponent,
    FavouritesAddAllButtonComponent,
    FavouritesAddButtonComponent,
    TimeFormSelectionSummaryComponent,
    LazyComponent,
    NoEventsComponent,
    LocaleDirective,
    PriceOddsValueDirective,
    PriceOddsClassDirective,
    PriceOddsDisabledDirective,
    ScrollableDirective,
    ScrollOnceDirective,
    ScrollableRacingDirective,
    BackButtonDirective,
    ClickLinkDirective,
    DisableDraggingDirective,
    LazyRenderDirective,
    LastMadeBetDirective,
    PatternRestrictDirective,
    ScrollFixDirective,
    OverscrollFixDirective,
    TriggerDirective,
    SymbolBackgroundDirective,
    InputValueDirective,
    EqualColumnDirective,
    OxygenDialogContainerDirective,
    DigitKeyboardComponent,
    DigitKeyboardInputDirective,
    NgCarouselDirective,
    MaintenanceComponent,
    LadbrokesBetslipCounterComponent,
    ScoreDigitComponent,
    AbstractOutletComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    PromotionIconComponent,
    LadbrokesPromotionsListComponent,
    LadbrokesPromoLabelsComponent,
    LadbrokesOddsCardResultComponent,
    InplayScoreComponent,
    ToggleButtonsComponent,
    YourCallLabelComponent,
    LadbrokesOddsBoostInfoDialogComponent,
    BybLabelComponent,
    LinkHrefDirective,
    TooltipComponent,
    TooltipDirective,
    StickyVirtualScrollerComponent,
    OxygenNotificationComponent,
    StarRatingComponent,
    RaceCardHomeComponent,
    BetslipHeaderIconComponent,
    MyBetsButtonComponent,
    VirtualSilkComponent,
    LadbrokesLoadingScreenComponent,
    LadbrokesBogLabelComponent,
    OddsCardScoreComponent,
    FavouriteIconComponent,
    RaceSilkComponent,
    UkOrIreSilkComponent,
    ShowCurrencyDirective,
    LadbrokesRaceCardsControlsComponent,
    BonusSuppressionErrorDialogComponent,
    ConnectionInterruptionDialogComponent,
    DateTimeChangeDirective
  ],
  providers: [
    AccordionService,
    PriceOddsButtonAnimationService,
    OddsCardHeaderService,
    LiveEventClockProviderService,
    MarketTypeService,
    CarouselService,
    MarketSelectorTrackingService
  ],
  exports: [
    LadbrokesAccordionComponent,
    ModalComponent,
    LadbrokesRacingOutcomeCardComponent,
    LadbrokesTabsPanelComponent,
    FreeBetEmptyComponent,
    FooterSectionComponent,
    LadbrokesSwitchersComponent,
    LadbrokesHistoricPricesComponent,
    LadbrokesOddsBoostInfoDialogComponent,
    LadbrokesDropDownMenuComponent,
    // LadbrokesMatchesMarketSelectorComponent,
    // LadbrokesInplayMarketSelectorComponent,
    LadbrokesBreadcrumbsComponent,
    LadbrokesCashoutLabelComponent,
    TopBarComponent,
    // LadbrokesOddsCardHighlightCarouselComponent,
    LadbrokesOddsCardSurfaceBetComponent,
    LadbrokesOxygenDialogComponent,
    LadbrokesRaceGridComponent,
    LadbrokesDrawerComponent,
    LadbrokesToggleSwitchComponent,
    LadbrokesWatchLabelComponent,
    BackButtonComponent,
    LadbrokesBogLabelComponent,

    GhSilkComponent,
    SurfaceBetsCarouselComponent,
    OddsCardSportComponent,
    RacingPanelComponent,
    SeeAllLinkComponent,
    SpinnerComponent,
    LiveLabelComponent,
    NewLabelComponent,
    ListCardComponent,
    EventCardComponent,
    CommonModule,
    RouterModule,
    SharedPipesModule,
    AccaNotificationComponent,
    CustomSelectComponent,
    OddsCardHeaderComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    NoEventsComponent,
    LiveClockComponent,
    StaticBlockComponent,
    ShowMoreComponentComponent,
    ShowAllButtonComponent,
    RaceListComponent,
    ExpandPanelComponent,
    VerticalMenuComponent,
    RequestErrorComponent,
    ModuleDisabledComponent,
    NgInfoPanelComponent,
    LoadingOverlayComponent,
    LiveServIframeComponent,
    LadbrokesOxygenDialogComponent,
    MaintenanceComponent,
    OffersSectionComponent,
    FreeBetsDialogComponent,
    FreeBetsNotificationComponent,
    FreeBetLabelComponent,
    SessionLogoutDialogComponent,
    ConnectionLostDialogComponent,
    VisPreMatchWidgetComponent,
    VisualizationContainerComponent,
    VisIframeDimensionsDirective,
    InformationDialogComponent,
    BppErrorDialogComponent,
    OddsCardComponent,
    SvgTeamKitComponent,
    RacingGridComponent,
    RaceTimerComponent,
    QuickbetPanelWrapperComponent,
    SvgListComponent,
    FavouritesCounterComponent,
    FavouritesAddAllButtonComponent,
    FavouritesAddButtonComponent,
    DatePickerComponent,
    LocaleDirective,
    NgCarouselExtendedDirective,
    ScrollableDirective,
    ScrollOnceDirective,
    ScrollableRacingDirective,
    LazyRenderDirective,
    BackButtonDirective,
    LastMadeBetDirective,
    PatternRestrictDirective,
    OverscrollFixDirective,
    TriggerDirective,
    SymbolBackgroundDirective,
    ClickLinkDirective,
    DisableDraggingDirective,
    InputValueDirective,
    EqualColumnDirective,
    DigitKeyboardComponent,
    DigitKeyboardInputDirective,
    NgCarouselDirective,
    LadbrokesBetslipCounterComponent,
    AbstractOutletComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    PromotionIconComponent,
    LadbrokesPromotionsListComponent,
    LadbrokesPromoLabelsComponent,
    ScoreDigitComponent,
    LadbrokesOddsCardResultComponent,
    InplayScoreComponent,
    ToggleButtonsComponent,
    TimeFormSelectionSummaryComponent,
    YourCallLabelComponent,
    BybLabelComponent,
    LazyComponent,
    LinkHrefDirective,
    TooltipComponent,
    TooltipDirective,
    StickyVirtualScrollerComponent,
    OxygenNotificationComponent,
    StarRatingComponent,
    RaceCardHomeComponent,
    BetslipHeaderIconComponent,
    MyBetsButtonComponent,
    VirtualSilkComponent,
    LadbrokesLoadingScreenComponent,
    OddsCardScoreComponent,
    FavouriteIconComponent,
    RaceSilkComponent,
    UkOrIreSilkComponent,
    ShowCurrencyDirective,
    LadbrokesRaceCardsControlsComponent,
    BonusSuppressionErrorDialogComponent,
    ConnectionInterruptionDialogComponent,
    PriceOddsValueDirective,
    PriceOddsDisabledDirective,
    DateTimeChangeDirective
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SharedModule {
  static forRoot() {
    return {
      ngModule: SharedModule,
      providers: [
        RoutingState,
        AccordionService,
        PriceOddsButtonAnimationService,
        PriceOddsButtonService,
        OddsCardHeaderService,
        LiveEventClockProviderService,
        MarketTypeService,
        TemplateService,
        CarouselService,
        MarketSelectorTrackingService,
        ScoreMarketBaseService
      ]
    };
  }
}

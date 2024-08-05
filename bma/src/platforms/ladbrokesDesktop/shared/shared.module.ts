import { CommonModule,NgOptimizedImage  } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { RouterModule } from '@angular/router';
import {
  DesktopTimeFormSelectionSummaryComponent
} from '@ladbrokesDesktop/racing/components/timeformSelectionSummary/timeform-selection-summary.component';
import { ShowMoreLinkComponent } from '@desktop/components/showMoreLink/show-more-link.component';
import { ModalComponent } from '@shared/components/customModal/custom-modal.component';
import { ScoreDigitComponent } from '@shared/components/scoreDigit/score-digit.component';
import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';
import { SeeAllLinkComponent } from '@shared/components/seeAllLink/see-all-link.component';
import { SpinnerComponent } from '@sharedModule/components/spinner/spinner.component';
import { ListCardComponent } from '@shared/components/listCard/list-card.component';
import { LiveLabelComponent } from '@shared/components/liveLabel/live-label.component';
import { NewLabelComponent } from '@shared/components/newLabel/new-label.component';
import { SvgListComponent } from '@shared/components/svgList/svg-list.component';
import { FavouritesAddAllButtonComponent } from '@shared/components/favourites/components/addAllButton/favourites-add-all-button.component';
import { FavouritesAddButtonComponent } from '@shared/components/favourites/components/addButton/favourites-add-button.component';
import { FavouritesCounterComponent } from '@shared/components/favourites/components/favouritesCounter/favourites-counter.component';
import { FavouriteIconComponent } from '@shared/components/favourites/components/favourite-icon/favourite-icon.component';
import { RaceTimerComponent } from '@shared/components/raceTimer/race-timer.component';
import { RacingGridComponent } from '@shared/components/racingGrid/racing-grid.component';
import { FreeBetsDialogComponent } from '@shared/components/freeBetsDialog/free-bets-dialog.component';
import { FreeBetsNotificationComponent } from '@ladbrokesMobile/shared/components/freeBetsNotification/free-bets-notification.component';
import { FreeBetLabelComponent } from '@ladbrokesMobile/shared/components/freeBetLabel/free-bet-label.component';
import { ToggleSwitchComponent } from '@shared/components/toggleSwitch/toggle-switch.component';
import { AccaNotificationComponent } from '@shared/components/accaNotification/acca-notification.component';
import { AccordionService } from '@shared/components/accordion/accordion.service';
import { ModuleDisabledComponent } from '@shared/components/moduleDisabled/module-disabled.component';
import { CustomSelectComponent } from '@shared/components/customSelect/custom-select.component';
import { HistoricPricesComponent } from '@shared/components/historicPrices/historic-prices.component';
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
import { StaticBlockComponent } from '@shared/components/staticBlock/static-block.component';
import { LadbrokesSwitchersComponent } from '@ladbrokesMobile/shared/components/switchers/switchers.component';
import { DatePickerComponent } from '@ladbrokesMobile/shared/components/datePicker/date-picker.component';
import { LocaleDirective } from '@shared/directives/locale.directive';
import { ActiveLinkClassDirective } from '@shared/directives/active-link-class/active-link-class.directive';
import { RaceListComponent } from '@shared/components/raceList/race-list.component';
import { RaceGridComponent } from '@shared/components/raceGrid/race-grid';
import { ShowMoreComponentComponent } from '@shared/components/showMore/show-more.component';
import { ExpandPanelComponent } from '@sharedModule/components/expandPanel/expand-panel.component';
import { LoadingOverlayComponent } from '@shared/components/loadingOverlay/loading-overlay.component';
import { OxygenNotificationComponent } from '@shared/components/oxygenNotification/oxygen-notification.component';
import { ConnectionLostDialogComponent } from '@sharedModule/components/connectionLostDialog/connection-lost-dialog.component';
import { SessionLogoutDialogComponent } from '@shared/components/sessionLogoutDialog/session-logout-dialog.component';
import { BppErrorDialogComponent } from '@sharedModule/components/bppErrorDialog/bpp-error-dialog.component';
import { InformationDialogComponent } from '@ladbrokesMobile/shared/components/informationDialog/information-dialog.component';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { QuickbetPanelWrapperComponent } from '@shared/components/quickbetPanelWrapper/quickbet-panel-wrapper.component';
import { LazyComponent } from '@shared/components/lazy-component/lazy-component.component';
import { LadbrokesDrawerComponent } from '@ladbrokesMobile/shared/components/drawer/drawer.component';
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
import { ShowAllButtonComponent } from '@shared/components/showAllButton/show-all-button.component';
import { VerticalMenuComponent } from '@shared/components/verticalMenu/vertical-menu.component';
import { OxygenDialogContainerDirective } from '@shared/directives/oxygen-dialog-container.directive';
// import { InplayMarketSelectorComponent } from '@shared/components/marketSelector/inplayMarketSelector/inplay-market-selector.component';
import { MarketSelectorTrackingService } from '@shared/components/marketSelector/market-selector-tracking.service';
import { MarketSelectorConfigService } from '@shared/components/marketSelector/market-selector-config.service';
import { DigitKeyboardComponent } from '@shared/components/digitKeyboard/digit-keyboard.component';
import { DigitKeyboardInputDirective } from '@shared/components/digitKeyboard/digit-keyboard-input.directive';
import { BetslipCounterComponent } from '@shared/components/betslipCounter/betslip-counter.component';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { OutletStatusComponent } from '@shared/components/outletStatus/outlet-status.component';
import { PromotionDialogComponent } from '@promotionsModule/components/promotionDialog/promotion-dialog.component';
import { PromotionOverlayDialogComponent } from '@promotions/components/promotionOverlayDialog/promotion-overlay-dialog.component';
import { LadbrokesPromoLabelsComponent } from '@ladbrokesMobile/promotions/components/promoLabels/promo-labels.component';
import { LadbrokesPromotionsListComponent } from '@ladbrokesMobile/promotions/components/promotionsList/promotions-list.component';
import { TooltipComponent } from '@sharedModule/components/tooltip/tooltip.component';
import { TooltipDirective } from '@app/shared/directives/tooltip.directive';
import { OffersSectionComponent } from '@ladbrokesDesktop/bma/components/offerSection/offer-section.component';
import { VisPreMatchWidgetComponent } from '@app/sb/components/visPreMatchWidget/vis-pre-match-widget.component';
import { VisualizationContainerComponent } from '@app/sb/components/visualizationContainer/visualization-container.component';
import { VisIframeDimensionsDirective } from '@app/sb/directives/vis-iframe-dimensions.directive';
import { InplayScoreComponent } from '@app/shared/components/inplayScore/inplay-score.component';
import { YourCallLabelComponent } from '@shared/components/yourCallLabel/your-call-label.component';
import { BybLabelComponent } from '@shared/components/bybLabel/byb-label.component';
import { LinkHrefDirective } from '@shared/directives/link-href.directive';
import { ScoreMarketBaseService } from '@shared/services/scoreMarketBase/score-market-base.service';
import { StarRatingComponent } from '@ladbrokesMobile/shared/components/star-rating/star-rating.component';
import { DesktopOddsCardHeaderComponent } from '@ladbrokesDesktop/shared/components/oddsCardHeader/odds-card-header.component';
import {
  DesktopOddsCardEnhancedMultiplesComponent
} from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
import {
  DesktopOddsCardOutrightsComponent
} from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardOutrights/odds-card-outrights.component';
import {
  OddsCardSportComponent
} from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import {
  DesktopOddsCardSpecialsComponent
} from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardSpecials/odds-card-specials.component';
import { DesktopOddsCardComponent } from '@ladbrokesDesktop/shared/components/oddsCard/odds-card.component';
import { DesktopTabsPanelComponent } from '@ladbrokesDesktop/shared/components/tabsPanel/tabs-panel.component';
import { TopBarComponent } from '@ladbrokesDesktop/shared/components/topBar/top-bar.component';
import { DesktopOddsCardResultComponent } from '@ladbrokesDesktop/shared/components/oddsCardResult/odds-card-result.component';
import { GridHelperService } from '@ladbrokesDesktop/shared/services/gridHelperService/grid-helper.service';
import {
  OddsCardFeaturedOfferComponent
} from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardFeaturedOffer/odds-card-featured-offer.component';
import {
  OddsCardFavouriteComponent
} from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardSport/oddsCardFavourite/odds-card-favourite.component';
import { DropDownMenuComponent } from '@ladbrokesDesktop/shared/components/dropDownMenu/drop-down-menu.component';
import { BreadcrumbsComponent } from '@ladbrokesDesktop/shared/components/breadcrumbs/breadcrumbs.component';
import { ToggleButtonsComponent } from '@shared/components/toggleButtons/toggle-buttons.component';
import {
  DesktopOddsBoostInfoDialogComponent
} from '@ladbrokesDesktop/shared/components/ladbrokesDesktopOddsBoostDialog/odds-boost-info-dialog.component';
import { PromotionIconComponent } from '@ladbrokesMobile/promotions/components/promotionIcon/promotion-icon.component';
import { LadbrokesCashoutLabelComponent } from '@ladbrokesMobile/shared/components/cashoutLabel/cashout-label.component';
// import {
//   OddsCardHighlightCarouselComponent
// } from '@shared/components/oddsCard/oddsCardHightlightCarousel/odds-card-highlight-carousel.component';
import { SvgTeamKitComponent } from '@shared/components/svgTeamKit/svg-team-kit.component';
import {
  DesktopSurfaceBetsCarouselComponent
} from '@ladbrokesDesktop/shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import {
  DesktopOddsCardSurfaceBetComponent
} from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardSurfaceBet/odds-card-surface-bet.component';
// import {
//   InplayMarketSelectorDesktopComponent
// } from '@ladbrokesDesktop/shared/components/marketSelector/inplayMarketSelectorDesktop/inplay-market-selector.component';
import { LadbrokesWatchLabelComponent } from '@ladbrokesMobile/shared/components/watchLabel/watch-label.component';
import { AccordionComponent } from '@ladbrokesDesktop/shared/components/accordion/accordion.component';
import { LadbrokesOxygenDialogComponent } from '@ladbrokesMobile/shared/components/oxygenDialogs/oxygen-dialog.component';
import { RequestErrorComponent } from '@ladbrokesMobile/shared/components/requestError/request-error.component';
import { RaceCardHomeComponent } from '@ladbrokesDesktop/shared/components/raceCardHome/race-card-home.component';
import { RacingPanelComponent } from '@ladbrokesDesktop/shared/components/racingPanel/racing-panel.component';
import { LadbrokesDesktopLoadingScreenComponent } from '@ladbrokesDesktop/shared/components/loadingScreen/loading-screen.component';
import { BetslipHeaderIconComponent } from '@shared/components/betslipHeaderIcon/betslip-header-icon.component';
import { MyBetsButtonComponent } from '@shared/components/myBetsButton/my-bets-button.component';
import { NoEventsComponent } from '@shared/components/noEvents/no-events.component';
import { LadbrokesBogLabelComponent } from '@ladbrokesMobile/shared/components/bogLabel/bog-label.component';
import { VirtualSilkComponent } from '@shared/components/virtualSilk/virtual-silk.component';
import { OddsCardScoreComponent } from '@sharedModule/components/oddsCard/oddsCardScore/odds-card-score.component';
import { RaceSilkComponent } from '@shared/components/raceSilk/race-silk.component';
import { UkOrIreSilkComponent } from '@shared/components/raceSilk/ukOrIreSilk/uk-or-ire-silk.component';
import { GhSilkComponent } from '@shared/components/ghSilk/gh-silk.component';
import { ShowCurrencyDirective } from '@shared/directives/show-currency/show-currency.directive';
import { LadbrokesRaceCardsControlsComponent } from '@ladbrokesDesktop/racing/components/race-cards-controls/race-cards-controls.component';
import { BonusSuppressionErrorDialogComponent } from '@shared/components/bonusSuppressionErrorDialog/bonus-suppression-error-dialog.component';
import { FreeBetEmptyComponent } from '@sharedModule/components/freeBetEmpty/free-bet-empty.component';
import { ConnectionInterruptionDialogComponent } from '@sharedModule/components/connection-interruption-dialog/connection-interruption-dialog.component';
import { DateTimeChangeDirective } from '@app/shared/directives/date-time-change.directive';
import {
    LadbrokesDesktopRacingOutcomeCardComponent
  } from '@ladbrokesDesktop/racing/components/racingOutcomeCard/racing-outcome-card.component';
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
    // Overridden app components
    AccordionComponent,
    LadbrokesDesktopRacingOutcomeCardComponent,
    ScoreDigitComponent,
    FreeBetEmptyComponent,
    DesktopOddsCardHeaderComponent,
    DesktopOddsCardEnhancedMultiplesComponent,
    DesktopOddsCardOutrightsComponent,
    DesktopOddsCardSpecialsComponent,
    DesktopOddsCardComponent,
    OddsCardSportComponent,
    DesktopTabsPanelComponent,
    DesktopOddsCardResultComponent,
    TopBarComponent,
    DesktopTimeFormSelectionSummaryComponent,
    PromotionIconComponent,
    DesktopSurfaceBetsCarouselComponent,
    ModalComponent,
    // Platform app components
    LadbrokesWatchLabelComponent,
    LadbrokesBogLabelComponent,
    OddsCardFeaturedOfferComponent,
    OddsCardFavouriteComponent,
    DropDownMenuComponent,
    BreadcrumbsComponent,

    // Main app components
    AccaNotificationComponent,
    HistoricPricesComponent,
    SeeAllLinkComponent,
    SpinnerComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    ListCardComponent,
    LiveLabelComponent,
    NewLabelComponent,
    CustomSelectComponent,
    LadbrokesSwitchersComponent,
    LadbrokesSwitchersComponent,
    OffersSectionComponent,
    LiveClockComponent,
    VisPreMatchWidgetComponent,
    VisualizationContainerComponent,
    VisIframeDimensionsDirective,
    DatePickerComponent,
    StaticBlockComponent,
    ShowMoreComponentComponent,
    ShowAllButtonComponent,
    RaceListComponent,
    RaceGridComponent,
    VerticalMenuComponent,
    ExpandPanelComponent,
    RequestErrorComponent,
    ToggleSwitchComponent,
    NgInfoPanelComponent,
    LoadingOverlayComponent,
    LiveServIframeComponent,
    LadbrokesOxygenDialogComponent,
    OxygenNotificationComponent,
    FreeBetsDialogComponent,
    FreeBetsNotificationComponent,
    FreeBetLabelComponent,
    SessionLogoutDialogComponent,
    ConnectionLostDialogComponent,
    InformationDialogComponent,
    BppErrorDialogComponent,
    ModuleDisabledComponent,
    RacingGridComponent,
    RaceTimerComponent,
    // InplayMarketSelectorComponent,
    SvgListComponent,
    FavouritesCounterComponent,
    FavouritesAddAllButtonComponent,
    FavouritesAddButtonComponent,
    // OddsCardHighlightCarouselComponent,
    SvgTeamKitComponent,
    LazyComponent,
    LadbrokesDrawerComponent,
    RacingPanelComponent,
    NoEventsComponent,
    FavouriteIconComponent,

    DesktopOddsCardSurfaceBetComponent,
    LocaleDirective,
    PriceOddsValueDirective,
    PriceOddsClassDirective,
    PriceOddsDisabledDirective,
    ScrollableDirective,
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
    ActiveLinkClassDirective,

    NgCarouselDirective,
    MaintenanceComponent,
    BetslipCounterComponent,
    AbstractOutletComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    LadbrokesPromoLabelsComponent,
    LadbrokesPromotionsListComponent,
    InplayScoreComponent,
    // MatchesMarketSelectorComponent,
    QuickbetPanelWrapperComponent,
    LadbrokesCashoutLabelComponent,
    YourCallLabelComponent,
    DesktopOddsBoostInfoDialogComponent,
    BybLabelComponent,
    LinkHrefDirective,
    VirtualSilkComponent,
    TooltipComponent,
    TooltipDirective,
    StarRatingComponent,
    // desktop individual
    ShowMoreLinkComponent,
    ToggleButtonsComponent,
    RaceCardHomeComponent,
    RacingPanelComponent,
    LadbrokesDesktopLoadingScreenComponent,
    BetslipHeaderIconComponent,
    MyBetsButtonComponent,
    OddsCardScoreComponent,
    RaceSilkComponent,
    UkOrIreSilkComponent,
    GhSilkComponent,
    LadbrokesRaceCardsControlsComponent,
    ShowCurrencyDirective,
    BonusSuppressionErrorDialogComponent,
    ConnectionInterruptionDialogComponent,
    DateTimeChangeDirective
  ],
  exports: [
    // Overridden app components
    ModalComponent,
    AccordionComponent,
    ScoreDigitComponent,
    LadbrokesDesktopRacingOutcomeCardComponent, 
    FreeBetEmptyComponent,
    DesktopOddsCardHeaderComponent,
    DesktopTabsPanelComponent,
    TopBarComponent,
    DesktopOddsCardHeaderComponent,
    DesktopOddsCardResultComponent,
    DesktopOddsCardComponent,
    DesktopTimeFormSelectionSummaryComponent,
    DesktopOddsBoostInfoDialogComponent,
    PromotionIconComponent,
    DesktopSurfaceBetsCarouselComponent,
    // Platform app components
    DropDownMenuComponent,
    BreadcrumbsComponent,
    LadbrokesWatchLabelComponent,
    // Main app components
    CommonModule,
    RouterModule,
    SharedPipesModule,
    AccaNotificationComponent,
    HistoricPricesComponent,
    SeeAllLinkComponent,
    SpinnerComponent,
    ListCardComponent,
    LiveLabelComponent,
    NewLabelComponent,
    CustomSelectComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    LadbrokesSwitchersComponent,
    LiveClockComponent,
    StaticBlockComponent,
    ShowMoreComponentComponent,
    ShowAllButtonComponent,
    RaceListComponent,
    RaceGridComponent,
    ExpandPanelComponent,
    VerticalMenuComponent,
    RequestErrorComponent,
    ToggleSwitchComponent,
    ModuleDisabledComponent,
    NgInfoPanelComponent,
    LoadingOverlayComponent,
    LiveServIframeComponent,
    LadbrokesOxygenDialogComponent,
    OxygenNotificationComponent,
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
    RacingGridComponent,
    RaceTimerComponent,
    // InplayMarketSelectorComponent,
    SvgListComponent,
    FavouritesCounterComponent,
    FavouritesAddAllButtonComponent,
    FavouritesAddButtonComponent,
    DatePickerComponent,
    LocaleDirective,
    ScrollableDirective,
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
    ActiveLinkClassDirective,
    DigitKeyboardComponent,
    DigitKeyboardInputDirective,
    NgCarouselDirective,
    BetslipCounterComponent,
    AbstractOutletComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    LadbrokesPromoLabelsComponent,
    LadbrokesPromotionsListComponent,
    InplayScoreComponent,
    // MatchesMarketSelectorComponent,
    ToggleButtonsComponent,
    ShowMoreLinkComponent,
    ShowMoreLinkComponent,
    LadbrokesCashoutLabelComponent,
    YourCallLabelComponent,
    BybLabelComponent,
    LazyComponent,
    LinkHrefDirective,
    NoEventsComponent,
    // OddsCardHighlightCarouselComponent,
    SvgTeamKitComponent,
    TooltipComponent,
    TooltipDirective,
    LadbrokesDrawerComponent,
    StarRatingComponent,
    RaceCardHomeComponent,
    RacingPanelComponent,
    RacingPanelComponent,
    BetslipHeaderIconComponent,
    MyBetsButtonComponent,
    LadbrokesDesktopLoadingScreenComponent,
    VirtualSilkComponent,
    RacingPanelComponent,
    LadbrokesBogLabelComponent,
    OddsCardScoreComponent,
    FavouriteIconComponent,
    RaceSilkComponent,
    UkOrIreSilkComponent,
    FavouriteIconComponent,
    GhSilkComponent,
    LadbrokesRaceCardsControlsComponent,
    ShowCurrencyDirective,
    BonusSuppressionErrorDialogComponent,
    ConnectionInterruptionDialogComponent,
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
        MarketSelectorConfigService,
        GridHelperService,
        ScoreMarketBaseService
      ]
    };
  }
}

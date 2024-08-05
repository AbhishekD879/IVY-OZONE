import { CommonModule,NgOptimizedImage  } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA,NO_ERRORS_SCHEMA } from '@angular/core';
import { RouterModule } from '@angular/router';


// TODO move these components to @shared dir
import { ListCardComponent } from '@sharedModule/components/listCard/list-card.component';
import { WatchLabelComponent } from '@sharedModule/components/watchLabel/watch-label.component';
import { LiveLabelComponent } from '@sharedModule/components/liveLabel/live-label.component';
import { NewLabelComponent } from '@sharedModule/components/newLabel/new-label.component';
import { TimeFormSelectionSummaryComponent } from '@racing/components/timeformSummary/time-form-selection-summary.component';
import { SeeAllLinkComponent } from '@sharedModule/components/seeAllLink/see-all-link.component';
import { RacingGridComponent } from '@sharedModule/components/racingGrid/racing-grid.component';
import { QuickbetPanelWrapperComponent } from '@sharedModule/components/quickbetPanelWrapper/quickbet-panel-wrapper.component';
import { SvgListComponent } from '@sharedModule/components/svgList/svg-list.component';
import {
  FavouritesAddAllButtonComponent
} from '@sharedModule/components/favourites/components/addAllButton/favourites-add-all-button.component';
import { FavouritesAddButtonComponent } from '@sharedModule/components/favourites/components/addButton/favourites-add-button.component';
import { FavouriteIconComponent } from '@shared/components/favourites/components/favourite-icon/favourite-icon.component';
import { FavouritesCounterComponent } from '@sharedModule/components/favourites/components/favouritesCounter/favourites-counter.component';
import { RaceTimerComponent } from '@sharedModule/components/raceTimer/race-timer.component';
import { FreeBetsDialogComponent } from '@sharedModule/components/freeBetsDialog/free-bets-dialog.component';
import { FreeBetsNotificationComponent } from '@sharedModule/components/freeBetsNotification/free-bets-notification.component';
import { FreeBetLabelComponent } from '@sharedModule/components/freeBetLabel/free-bet-label.component';
import { ToggleSwitchComponent } from '@sharedModule/components/toggleSwitch/toggle-switch.component';
import { AccaNotificationComponent } from '@sharedModule/components/accaNotification/acca-notification.component';
import { AccordionComponent } from '@sharedModule/components/accordion/accordion.component';
import { AccordionService } from '@sharedModule/components/accordion/accordion.service';
import { ModuleDisabledComponent } from '@sharedModule/components/moduleDisabled/module-disabled.component';
import { CustomSelectComponent } from '@sharedModule/components/customSelect/custom-select.component';
import { HistoricPricesComponent } from '@sharedModule/components/historicPrices/historic-prices.component';
import { LiveClockComponent } from '@sharedModule/components/liveClock/live-clock.component';
import { LiveEventClockProviderService } from '@sharedModule/components/liveClock/live-event-clock-provider.service';
import { PriceOddsButtonAnimationService } from '@sharedModule/components/priceOddsButton/price-odds-button.animation.service';
import { PriceOddsButtonService } from '@sharedModule/components/priceOddsButton/price-odds-button.service';
import { PriceOddsButtonComponent } from '@sharedModule/components/priceOddsButton/price-odds-button.component';
import { PriceOddsButtonOnPushComponent } from '@shared/components/priceOddsButtonOnPush/price-odds-button-onpush.component';
import { PriceOddsValueDirective } from '@sharedModule/components/priceOddsButton/price-odds-value.directive';
import { PriceOddsDisabledDirective } from '@sharedModule/components/priceOddsButton/price-odds-disabled.directive';
import { PriceOddsClassDirective } from '@sharedModule/components/priceOddsButton/price-odds-class.directive';
import { OddsCardHeaderComponent } from '@sharedModule/components/oddsCardHeader/odds-card-header.component';
import { OddsCardHeaderService } from '@sharedModule/components/oddsCardHeader/odds-card-header.service';
import { StaticBlockComponent } from '@sharedModule/components/staticBlock/static-block.component';
import { SwitchersComponent } from '@sharedModule/components/switchers/switchers.component';
import { DatePickerComponent } from '@sharedModule/components/datePicker/date-picker.component';
import { LocaleDirective } from '@sharedModule/directives/locale.directive';
import { RaceListComponent } from '@sharedModule/components/raceList/race-list.component';
import { RaceGridComponent } from '@sharedModule/components/raceGrid/race-grid';
import { RequestErrorComponent } from '@sharedModule/components/requestError/request-error.component';
import { ShowMoreComponentComponent } from '@sharedModule/components/showMore/show-more.component';
import { ExpandPanelComponent } from '@sharedModule/components/expandPanel/expand-panel.component';
import { LoadingOverlayComponent } from '@sharedModule/components/loadingOverlay/loading-overlay.component';
import { OxygenDialogComponent } from '@sharedModule/components/oxygenDialogs/oxygen-dialog.component';
import { ConnectionLostDialogComponent } from '@sharedModule/components/connectionLostDialog/connection-lost-dialog.component';
import { SessionLogoutDialogComponent } from '@sharedModule/components/sessionLogoutDialog/session-logout-dialog.component';
import { BppErrorDialogComponent } from '@sharedModule/components/bppErrorDialog/bpp-error-dialog.component';
import { InformationDialogComponent } from '@sharedModule/components/informationDialog/information-dialog.component';
import { MarketTypeService } from '@sharedModule/services/marketType/market-type.service';
import { TemplateService } from '@sharedModule/services/template/template.service';
import { CarouselService } from '@sharedModule/directives/ng-carousel/carousel.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { ScoreDigitComponent } from '@sharedModule/components/scoreDigit/score-digit.component';
import {
  OddsCardEnhancedMultiplesComponent
} from '@sharedModule/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
// import {
//   OddsCardHighlightCarouselComponent
// } from '@sharedModule/components/oddsCard/oddsCardHightlightCarousel/odds-card-highlight-carousel.component';
import { OddsCardSurfaceBetComponent } from '@sharedModule/components/oddsCard/oddsCardSurfaceBet/odds-card-surface-bet.component';
import { OddsCardSpecialsComponent } from '@sharedModule/components/oddsCard/oddsCardSpecials/odds-card-specials.component';
import { OddsCardSportComponent } from '@sharedModule/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { OddsCardComponent } from '@sharedModule/components/oddsCard/odds-card.component';
import { NgCarouselDirective } from '@sharedModule/directives/ng-carousel/carousel.directive';
import { PatternRestrictDirective } from '@sharedModule/directives/pattern-restrict.directive';
import { ScrollableDirective } from '@sharedModule/directives/scrollable.directive';
import { ScrollableRacingDirective } from '@sharedModule/directives/scrollable-racing.directive';
import { BackButtonDirective } from '@sharedModule/directives/back-button.directive';
import { ClickLinkDirective } from '@sharedModule/directives/click-link.directive';
import { TriggerDirective } from '@sharedModule/directives/trigger.directive';
import { DisableDraggingDirective } from '@sharedModule/directives/disable-dragging.directive';
import { LazyRenderDirective } from '@sharedModule/directives/lazy-render.directive';
import { LastMadeBetDirective } from '@sharedModule/directives/last-made-bet.directive';
import { HomeScreenComponent } from '@sharedModule/components/homeScreen/home-screen.component';
import { OverscrollFixDirective } from '@sharedModule/directives/overscroll-fix';
import { NgInfoPanelComponent } from '@sharedModule/components/infoPanel/ng-info-panel.component';
import { InputValueDirective } from '@sharedModule/directives/input-value.directive';
import { ScrollFixDirective } from '@sharedModule/directives/scroll-fix.directive';
import { LiveServIframeComponent } from '@sharedModule/components/liveServ/live-serv-iframe.component';
import { EqualColumnDirective } from '@sharedModule/directives/equal-column.directive';
import { MaintenanceComponent } from '@sharedModule/components/maintenance/maintenance.component';
import { ShowAllButtonComponent } from '@sharedModule/components/showAllButton/show-all-button.component';
import { TopBarComponent } from '@sharedModule/components/topBar/top-bar.component';
import { VerticalMenuComponent } from '@sharedModule/components/verticalMenu/vertical-menu.component';
import {
  TabsPanelComponent
} from '@sharedModule/components/tabsPanel/tabs-panel.component';
import {
  OxygenDialogContainerDirective
} from '@sharedModule/directives/oxygen-dialog-container.directive';
import { MarketSelectorTrackingService } from '@sharedModule/components/marketSelector/market-selector-tracking.service';
import { DigitKeyboardComponent } from '@sharedModule/components/digitKeyboard/digit-keyboard.component';
import { DigitKeyboardInputDirective } from '@sharedModule/components/digitKeyboard/digit-keyboard-input.directive';
import { RacingPanelComponent } from '@sharedModule/components/racingPanel/racing-panel.component';

import { BetslipCounterComponent } from '@sharedModule/components/betslipCounter/betslip-counter.component';
import { AbstractOutletComponent } from '@sharedModule/components/abstractOutlet/abstract-outlet.component';
import { OutletStatusComponent } from '@sharedModule/components/outletStatus/outlet-status.component';
import { OddsCardResultComponent } from '@sharedModule/components/oddsCardResult/odds-card-result.component';

import { PromotionsComponent } from '@app/promotions/components/promotion/promotions.component';
import { PromotionDialogComponent } from '@app/promotions/components/promotionDialog/promotion-dialog.component';
import { PromotionOverlayDialogComponent } from '@promotions/components/promotionOverlayDialog/promotion-overlay-dialog.component';
import { PromotionIconComponent } from '@app/promotions/components/promotionIcon/promotion-icon.component';
import { PromoLabelsComponent } from '@app/promotions/components/promoLabels/promo-labels.component';
import { PromotionsListComponent } from '@app/promotions/components/promotionsList/promotions-list.component';

import { OffersSectionComponent } from '@bmaModule/components/offerSection/offer-section.component';
import { VisPreMatchWidgetComponent } from '@sbModule/components/visPreMatchWidget/vis-pre-match-widget.component';
import { VisualizationContainerComponent } from '@sbModule/components/visualizationContainer/visualization-container.component';
import { VisIframeDimensionsDirective } from '@sbModule/directives/vis-iframe-dimensions.directive';
import { InplayScoreComponent } from '@sharedModule/components/inplayScore/inplay-score.component';
import { ToggleButtonsComponent } from '@sharedModule/components/toggleButtons/toggle-buttons.component';
import { LinkHrefDirective } from '@sharedModule/directives/link-href.directive';
import { CashoutLabelComponent } from '@sharedModule/components/cashoutLabel/cashout-label.component';
import { YourCallLabelComponent } from '@sharedModule/components/yourCallLabel/your-call-label.component';
import { StarRatingComponent } from '@shared/components/star-rating/star-rating.component';
import { NgCarouselExtendedDirective } from '@sharedModule/directives/ng-carousel-extended/carousel.directive';
import { OddsBoostInfoDialogComponent } from '@sharedModule/components/oddsBoostInfoDialog/odds-boost-info-dialog.component';
import { BybLabelComponent } from '@sharedModule/components/bybLabel/byb-label.component';
import { LazyComponent } from '@sharedModule/components/lazy-component/lazy-component.component';
import { BreadcrumbsComponent } from '@sharedModule/components/breadcrumbs/breadcrumbs.component';

import { TooltipComponent } from '@sharedModule/components/tooltip/tooltip.component';
import { TooltipDirective } from '@sharedModule/directives/tooltip.directive';

import { SvgTeamKitComponent } from '@sharedModule/components/svgTeamKit/svg-team-kit.component';
import { ScoreMarketBaseService } from '@sharedModule/services/scoreMarketBase/score-market-base.service';
import { DropDownMenuComponent } from '@sharedModule/components/dropDownMenu/drop-down-menu.component';
import { NoEventsComponent } from '@shared/components/noEvents/no-events.component';
import { SurfaceBetsCarouselComponent } from '@sharedModule/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { DrawerComponent } from '@sharedModule/components/drawer/drawer.component';
import { OxygenNotificationComponent } from '@sharedModule/components/oxygenNotification/oxygen-notification.component';
import { StickyVirtualScrollerComponent } from '@sharedModule/components/stickyVirtualScroller/sticky-virtual-scroller.component';
import { BonusSuppressionErrorDialogComponent } from '@sharedModule/components/bonusSuppressionErrorDialog/bonus-suppression-error-dialog.component';
import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';
import { SpinnerComponent } from '@sharedModule/components/spinner/spinner.component';
import { FooterSectionComponent } from '@sharedModule/components/footerSection/footer-section.component';
import { BetslipHeaderIconComponent } from '@sharedModule/components/betslipHeaderIcon/betslip-header-icon.component';
import { MyBetsButtonComponent } from '@shared/components/myBetsButton/my-bets-button.component';
import { LoadingScreenComponent } from '@shared/components/loadingScreen/loading-screen.component';
import { BogLabelComponent } from '@shared/components/bogLabel/bog-label.component';
import { VirtualSilkComponent } from '@shared/components/virtualSilk/virtual-silk.component';
import { OddsCardScoreComponent } from '@shared/components/oddsCard/oddsCardScore/odds-card-score.component';
import { RaceSilkComponent } from '@shared/components/raceSilk/race-silk.component';
import { UkOrIreSilkComponent } from '@shared/components/raceSilk/ukOrIreSilk/uk-or-ire-silk.component';
import { GhSilkComponent } from '@shared/components/ghSilk/gh-silk.component';
import { ShowCurrencyDirective } from '@shared/directives/show-currency/show-currency.directive';
import { ScrollOnceDirective } from '@core/directives/scroll-once-directive';
import { RaceCardsControlsComponent } from '@racing/components/raceCardControls/race-cards-controls.component';
import { ConnectionInterruptionDialogComponent } from '@sharedModule/components/connection-interruption-dialog/connection-interruption-dialog.component';
import { DateTimeChangeDirective } from '@sharedModule/directives/date-time-change.directive';
import { FreeBetEmptyComponent } from '@sharedModule/components/freeBetEmpty/free-bet-empty.component';
import { RacingOutcomeCardComponent } from '@racing/components/racingOutcomeCard/racing-outcome-card.component';
import { SymbolBackgroundDirective } from './directives/symbol-background.directive';
import { ModalComponent } from '@sharedModule/components/customModal/custom-modal.component';

@NgModule({
  imports: [
    SharedPipesModule,
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    FormsModule,
    NgOptimizedImage 
  ],
  declarations: [
    GhSilkComponent,
    RacingOutcomeCardComponent,
    FreeBetEmptyComponent,
    SeeAllLinkComponent,
    SpinnerComponent,
    AccaNotificationComponent,
    AccordionComponent,
    HistoricPricesComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    OddsCardHeaderComponent,
    CustomSelectComponent,
    SwitchersComponent,
    WatchLabelComponent,
    OffersSectionComponent,
    LiveClockComponent,
    VisPreMatchWidgetComponent,
    VisualizationContainerComponent,
    VisIframeDimensionsDirective,
    DatePickerComponent,
    StaticBlockComponent,
    ShowMoreComponentComponent,
    ShowAllButtonComponent,
    TopBarComponent,
    RaceListComponent,
    RaceGridComponent,
    VerticalMenuComponent,
    ExpandPanelComponent,
    RequestErrorComponent,
    ModalComponent,
    TabsPanelComponent,
    ToggleSwitchComponent,
    NgInfoPanelComponent,
    LoadingOverlayComponent,
    LiveServIframeComponent,
    OxygenDialogComponent,
    OxygenNotificationComponent,
    FreeBetsDialogComponent,
    FreeBetsNotificationComponent,
    FreeBetLabelComponent,
    SessionLogoutDialogComponent,
    ConnectionLostDialogComponent,
    InformationDialogComponent,
    BppErrorDialogComponent,
    ModuleDisabledComponent,
    OddsCardEnhancedMultiplesComponent,
    // OddsCardHighlightCarouselComponent,
    SurfaceBetsCarouselComponent,
    OddsCardSurfaceBetComponent,
    OddsCardSpecialsComponent,
    OddsCardSportComponent,
    OddsCardComponent,
    RacingGridComponent,
    RaceTimerComponent,
    DropDownMenuComponent,
    SvgListComponent,
    SvgTeamKitComponent,
    FavouritesCounterComponent,
    FavouritesAddAllButtonComponent,
    FavouritesAddButtonComponent,
    QuickbetPanelWrapperComponent,
    TimeFormSelectionSummaryComponent,
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
    HomeScreenComponent,
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
    NgCarouselExtendedDirective,
    MaintenanceComponent,
    BetslipCounterComponent,
    AbstractOutletComponent,
    ScoreDigitComponent,
    OddsBoostInfoDialogComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    PromotionIconComponent,
    PromoLabelsComponent,
    PromotionsListComponent,
    PromotionsComponent,
    OddsCardResultComponent,
    InplayScoreComponent,
    OddsCardResultComponent,
    ToggleButtonsComponent,
    CashoutLabelComponent,
    YourCallLabelComponent,
    BybLabelComponent,
    ToggleButtonsComponent,
    LinkHrefDirective,
    LazyComponent,
    BreadcrumbsComponent,
    TooltipComponent,
    TooltipDirective,
    StickyVirtualScrollerComponent,
    DrawerComponent,
    RacingPanelComponent,
    ListCardComponent,
    LiveLabelComponent,
    WatchLabelComponent,
    BogLabelComponent,
    NewLabelComponent,
    FooterSectionComponent,
    BetslipHeaderIconComponent,
    VirtualSilkComponent,
    MyBetsButtonComponent,
    LoadingScreenComponent,
    OddsCardScoreComponent,
    FavouriteIconComponent,
    StarRatingComponent,
    RaceSilkComponent,
    UkOrIreSilkComponent,
    ShowCurrencyDirective,
    BonusSuppressionErrorDialogComponent,
    RaceCardsControlsComponent,
    ConnectionInterruptionDialogComponent,
    DateTimeChangeDirective
  ],
  exports: [
    ScrollFixDirective,
    RacingOutcomeCardComponent,
    ModalComponent,
    GhSilkComponent,
    FreeBetEmptyComponent,
    SharedPipesModule,
    CommonModule,
    RouterModule,
    SeeAllLinkComponent,
    SpinnerComponent,
    AccaNotificationComponent,
    HistoricPricesComponent,
    CustomSelectComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    OddsCardHeaderComponent,
    AccordionComponent,
    SwitchersComponent,
    WatchLabelComponent,
    LiveClockComponent,
    StaticBlockComponent,
    TabsPanelComponent,
    TopBarComponent,
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
    OxygenDialogComponent,
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
    OddsCardComponent,
    // OddsCardHighlightCarouselComponent,
    SurfaceBetsCarouselComponent,
    OddsCardSurfaceBetComponent,
    RacingGridComponent,
    NoEventsComponent,
    RaceTimerComponent,
    DropDownMenuComponent,
    SvgListComponent,
    FavouritesCounterComponent,
    FavouritesAddAllButtonComponent,
    FavouritesAddButtonComponent,
    DatePickerComponent,
    QuickbetPanelWrapperComponent,
    OddsBoostInfoDialogComponent,

    LocaleDirective,
    ScrollableDirective,
    ScrollOnceDirective,
    ScrollableRacingDirective,
    LazyRenderDirective,
    BackButtonDirective,
    HomeScreenComponent,
    LastMadeBetDirective,
    PatternRestrictDirective,
    OverscrollFixDirective,
    TriggerDirective,
    SymbolBackgroundDirective,
    ClickLinkDirective,
    DisableDraggingDirective,
    LinkHrefDirective,
    InputValueDirective,
    EqualColumnDirective,
    DigitKeyboardComponent,
    DigitKeyboardInputDirective,
    NgCarouselDirective,
    NgCarouselExtendedDirective,
    BetslipCounterComponent,
    AbstractOutletComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    PromotionIconComponent,
    PromoLabelsComponent,
    PromotionsListComponent,
    PromotionsComponent,
    OddsCardResultComponent,
    ScoreDigitComponent,
    InplayScoreComponent,
    OddsCardResultComponent,
    TimeFormSelectionSummaryComponent,
    ToggleButtonsComponent,
    SvgTeamKitComponent,
    ToggleButtonsComponent,
    CashoutLabelComponent,
    YourCallLabelComponent,
    BybLabelComponent,
    LazyComponent,
    BreadcrumbsComponent,
    TooltipComponent,
    TooltipDirective,
    StickyVirtualScrollerComponent,
    DrawerComponent,
    RacingPanelComponent,
    ListCardComponent,
    LiveLabelComponent,
    WatchLabelComponent,
    BogLabelComponent,
    NewLabelComponent,
    FooterSectionComponent,
    BetslipHeaderIconComponent,
    VirtualSilkComponent,
    MyBetsButtonComponent,
    LoadingScreenComponent,
    MyBetsButtonComponent,
    OddsCardScoreComponent,
    FavouriteIconComponent,
    StarRatingComponent,
    RaceSilkComponent,
    UkOrIreSilkComponent,
    ShowCurrencyDirective,
    BonusSuppressionErrorDialogComponent,
    RaceCardsControlsComponent,
    ConnectionInterruptionDialogComponent,
    PriceOddsValueDirective,
    PriceOddsDisabledDirective,
    DateTimeChangeDirective
  ],
  schemas: [NO_ERRORS_SCHEMA ,CUSTOM_ELEMENTS_SCHEMA]
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

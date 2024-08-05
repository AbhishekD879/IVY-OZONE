import { CommonModule,NgOptimizedImage  } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RouterModule } from '@angular/router';

import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';
import {
  DesktopTimeFormSelectionSummaryComponent
} from '@coralDesktop/racing/components/timeformSelectionSummary/timeform-selection-summary.component';
import { ShowMoreLinkComponent } from '@desktop/components/showMoreLink/show-more-link.component';

import { SeeAllLinkComponent } from '@shared/components/seeAllLink/see-all-link.component';
import { WatchLabelComponent } from '@shared/components/watchLabel/watch-label.component';
import { SvgListComponent } from '@shared/components/svgList/svg-list.component';
import { ListCardComponent } from '@shared/components/listCard/list-card.component';
import { LiveLabelComponent } from '@shared/components/liveLabel/live-label.component';
import { NewLabelComponent } from '@shared/components/newLabel/new-label.component';
import { FavouritesAddAllButtonComponent } from '@shared/components/favourites/components/addAllButton/favourites-add-all-button.component';
import { FavouritesAddButtonComponent } from '@shared/components/favourites/components/addButton/favourites-add-button.component';
import { FavouritesCounterComponent } from '@shared/components/favourites/components/favouritesCounter/favourites-counter.component';
import { FavouriteIconComponent } from '@shared/components/favourites/components/favourite-icon/favourite-icon.component';
import { RaceTimerComponent } from '@shared/components/raceTimer/race-timer.component';
import { RacingGridComponent } from '@shared/components/racingGrid/racing-grid.component';
import { FreeBetsDialogComponent } from '@shared/components/freeBetsDialog/free-bets-dialog.component';
import { FreeBetsNotificationComponent } from '@shared/components/freeBetsNotification/free-bets-notification.component';
import { FreeBetLabelComponent } from '@sharedModule/components/freeBetLabel/free-bet-label.component';
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
import { SwitchersComponent } from '@shared/components/switchers/switchers.component';
import { DatePickerComponent } from '@shared/components/datePicker/date-picker.component';
import { LocaleDirective } from '@shared/directives/locale.directive';
import { RaceListComponent } from '@shared/components/raceList/race-list.component';
import { RaceGridComponent } from '@shared/components/raceGrid/race-grid';
import { RequestErrorComponent } from '@shared/components/requestError/request-error.component';
import { ShowMoreComponentComponent } from '@shared/components/showMore/show-more.component';
import { ExpandPanelComponent } from '@shared/components/expandPanel/expand-panel.component';
import { LoadingOverlayComponent } from '@shared/components/loadingOverlay/loading-overlay.component';
import { OxygenDialogComponent } from '@shared/components/oxygenDialogs/oxygen-dialog.component';
import { OxygenNotificationComponent } from '@shared/components/oxygenNotification/oxygen-notification.component';
import { ConnectionLostDialogComponent } from '@shared/components/connectionLostDialog/connection-lost-dialog.component';
import { SessionLogoutDialogComponent } from '@shared/components/sessionLogoutDialog/session-logout-dialog.component';
import { BppErrorDialogComponent } from '@shared/components/bppErrorDialog/bpp-error-dialog.component';
import { InformationDialogComponent } from '@shared/components/informationDialog/information-dialog.component';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { QuickbetPanelWrapperComponent } from '@shared/components/quickbetPanelWrapper/quickbet-panel-wrapper.component';
import { LazyComponent } from '@shared/components/lazy-component/lazy-component.component';
import { DrawerComponent } from '@shared/components/drawer/drawer.component';

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
import { MarketSelectorTrackingService } from '@shared/components/marketSelector/market-selector-tracking.service';
import { MarketSelectorConfigService } from '@shared/components/marketSelector/market-selector-config.service';
import { DigitKeyboardComponent } from '@shared/components/digitKeyboard/digit-keyboard.component';
import { DigitKeyboardInputDirective } from '@shared/components/digitKeyboard/digit-keyboard-input.directive';
import { BetslipCounterComponent } from '@shared/components/betslipCounter/betslip-counter.component';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { OutletStatusComponent } from '@shared/components/outletStatus/outlet-status.component';
import { PromotionDialogComponent } from '@app/promotions/components/promotionDialog/promotion-dialog.component';
import { PromotionOverlayDialogComponent } from '@promotions/components/promotionOverlayDialog/promotion-overlay-dialog.component';
import { PromotionIconComponent } from '@app/promotions/components/promotionIcon/promotion-icon.component';
import { PromoLabelsComponent } from '@app/promotions/components/promoLabels/promo-labels.component';
import { PromotionsListComponent } from '@app/promotions/components/promotionsList/promotions-list.component';
import { TooltipComponent } from '@shared/components/tooltip/tooltip.component';
import { TooltipDirective } from '@app/shared/directives/tooltip.directive';
import { ActiveLinkClassDirective } from '@shared/directives/active-link-class/active-link-class.directive';

import { OffersSectionComponent } from '@coralDesktop/bma/components/offerSection/offer-section.component';
import { VisPreMatchWidgetComponent } from '@app/sb/components/visPreMatchWidget/vis-pre-match-widget.component';
import { VisualizationContainerComponent } from '@app/sb/components/visualizationContainer/visualization-container.component';
import { VisIframeDimensionsDirective } from '@app/sb/directives/vis-iframe-dimensions.directive';
import { InplayScoreComponent } from '@app/shared/components/inplayScore/inplay-score.component';
import { CashoutLabelComponent } from '@shared/components/cashoutLabel/cashout-label.component';
import { YourCallLabelComponent } from '@shared/components/yourCallLabel/your-call-label.component';
import { SpinnerComponent } from '@sharedModule/components/spinner/spinner.component';
import { BybLabelComponent } from '@shared/components/bybLabel/byb-label.component';
import { ScoreMarketBaseService } from '@shared/services/scoreMarketBase/score-market-base.service';
import { NoEventsComponent } from '@shared/components/noEvents/no-events.component';
import { VirtualSilkComponent } from '@shared/components/virtualSilk/virtual-silk.component';
import { ScoreDigitComponent } from '@shared/components/scoreDigit/score-digit.component';
// Overridden components
import { DesktopPromotionsComponent } from '@coralDesktop/shared/components/promotion/promotions.component';
import { AccordionComponent } from '@coralDesktop/shared/components/accordion/accordion.component';
import { OddsCardHeaderComponent } from '@coralDesktop/shared/components/oddsCardHeader/odds-card-header.component';
import {
  OddsCardEnhancedMultiplesComponent
} from '@coralDesktop/shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
import {
  DesktopOddsCardOutrightsComponent
} from '@coralDesktop/shared/components/oddsCard/oddsCardOutrights/odds-card-outrights.component';
import { OddsCardSportComponent } from '@coralDesktop/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { OddsCardSpecialsComponent } from '@coralDesktop/shared/components/oddsCard/oddsCardSpecials/odds-card-specials.component';
import { OddsCardComponent } from '@coralDesktop/shared/components/oddsCard/odds-card.component';
import { TabsPanelComponent } from '@coralDesktop/shared/components/tabsPanel/tabs-panel.component';
import { TopBarComponent } from '@coralDesktop/shared/components/topBar/top-bar.component';
import { OddsCardResultComponent } from '@coralDesktop/shared/components/oddsCardResult/odds-card-result.component';
import { DesktopLoadingScreenComponent } from '@coralDesktop/shared/components/loadingScreen/loading-screen.component';

// Platform app services
import { GridHelperService } from '@coralDesktop/shared/services/gridHelperService/grid-helper.service';

// Platform app components
import {
  OddsCardFeaturedOfferComponent
} from '@coralDesktop/shared/components/oddsCard/oddsCardFeaturedOffer/odds-card-featured-offer.component';
import {
  OddsCardPreMatchComponent
} from '@coralDesktop/shared/components/oddsCard/oddsCardSport/oddsCardPreMatch/odds-card-pre-match.component';
import {
  OddsCardInplayComponent
} from '@coralDesktop/shared/components/oddsCard/oddsCardSport/oddsCardInplay/odds-card-inplay.component';
import {
  OddsCardFavouriteComponent
} from '@coralDesktop/shared/components/oddsCard/oddsCardSport/oddsCardFavourite/odds-card-favourite.component';
import { DropDownMenuComponent } from '@coralDesktop/shared/components/dropDownMenu/drop-down-menu.component';
import { BreadcrumbsComponent } from '@coralDesktop/shared/components/breadcrumbs/breadcrumbs.component';
import { ToggleButtonsComponent } from '@shared/components/toggleButtons/toggle-buttons.component';
import { LinkHrefDirective } from '@shared/directives/link-href.directive';
import { OddsBoostInfoDialogComponent } from '@shared/components/oddsBoostInfoDialog/odds-boost-info-dialog.component';
// import {
//   OddsCardHighlightCarouselComponent
// } from '@shared/components/oddsCard/oddsCardHightlightCarousel/odds-card-highlight-carousel.component';
import { SvgTeamKitComponent } from '@shared/components/svgTeamKit/svg-team-kit.component';
import { OddsCardSurfaceBetComponent } from '@shared/components/oddsCard/oddsCardSurfaceBet/odds-card-surface-bet.component';
import { SurfaceBetsCarouselComponent } from '@coralDesktop/shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { RacingPanelComponent } from '@shared/components/racingPanel/racing-panel.component';

// Vanilla overrides
import { BetslipHeaderIconComponent } from '@shared/components/betslipHeaderIcon/betslip-header-icon.component';
import { MyBetsButtonComponent } from '@shared/components/myBetsButton/my-bets-button.component';
import { BogLabelComponent } from '@shared/components/bogLabel/bog-label.component';
import { OddsCardScoreComponent } from '@shared/components/oddsCard/oddsCardScore/odds-card-score.component';
import { RaceSilkComponent } from '@shared/components/raceSilk/race-silk.component';
import { UkOrIreSilkComponent } from '@shared/components/raceSilk/ukOrIreSilk/uk-or-ire-silk.component';
import { GhSilkComponent } from '@shared/components/ghSilk/gh-silk.component';
import { StarRatingComponent } from '@shared/components/star-rating/star-rating.component';
import { ShowCurrencyDirective } from '@shared/directives/show-currency/show-currency.directive';
import { BonusSuppressionErrorDialogComponent } from '@shared/components/bonusSuppressionErrorDialog/bonus-suppression-error-dialog.component';
import { RaceCardsControlsComponent } from '@coralDesktop/racing/components/race-cards-controls/race-cards-controls.component';
import { ConnectionInterruptionDialogComponent } from '@sharedModule/components/connection-interruption-dialog/connection-interruption-dialog.component';
import { DateTimeChangeDirective } from '@app/shared/directives/date-time-change.directive';
import { FreeBetEmptyComponent } from '@sharedModule/components/freeBetEmpty/free-bet-empty.component';
import { DesktopRacingOutcomeCardComponent } from '@coralDesktop/racing/components/racingOutcomeCard/racing-outcome-card.component';
import { MatDialogModule } from '@angular/material/dialog';
import { ModalComponent } from '@shared/components/customModal/custom-modal.component';
import { SymbolBackgroundDirective } from '@shared/directives/symbol-background.directive';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatDialogModule,
    FormsModule,
    SharedPipesModule,
    NgOptimizedImage 
  ],
  declarations: [
    // Overridden app components
    RacingPanelComponent,
    ModalComponent,
    DesktopRacingOutcomeCardComponent,
    FreeBetEmptyComponent,
    ScoreDigitComponent,
    AccordionComponent,
    OddsCardHeaderComponent,
    OddsCardEnhancedMultiplesComponent,
    DesktopOddsCardOutrightsComponent,
    OddsCardSpecialsComponent,
    OddsCardComponent,
    OddsCardSportComponent,
    TabsPanelComponent,
    OddsCardResultComponent,
    TopBarComponent,
    DesktopPromotionsComponent,
    DesktopTimeFormSelectionSummaryComponent,

    // Platform app components
    OddsCardFeaturedOfferComponent,
    OddsCardPreMatchComponent,
    OddsCardFavouriteComponent,
    OddsCardInplayComponent,
    DropDownMenuComponent,
    BreadcrumbsComponent,

    // Main app components
    AccaNotificationComponent,
    HistoricPricesComponent,
    SeeAllLinkComponent,
    SpinnerComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    CustomSelectComponent,
    SwitchersComponent,
    OffersSectionComponent,
    LiveClockComponent,
    ListCardComponent,
    LiveLabelComponent,
    WatchLabelComponent,
    NewLabelComponent,
    VisPreMatchWidgetComponent,
    VisualizationContainerComponent,
    VisIframeDimensionsDirective,
    ActiveLinkClassDirective,
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
    RacingGridComponent,
    RaceTimerComponent,
    SvgListComponent,
    FavouritesCounterComponent,
    FavouritesAddAllButtonComponent,
    FavouritesAddButtonComponent,
    // OddsCardHighlightCarouselComponent,
    SvgTeamKitComponent,
    LazyComponent,
    DrawerComponent,
    OddsCardSurfaceBetComponent,
    SurfaceBetsCarouselComponent,
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
    OddsBoostInfoDialogComponent,
    ScrollFixDirective,
    OverscrollFixDirective,
    TriggerDirective,
    SymbolBackgroundDirective,
    InputValueDirective,
    EqualColumnDirective,
    OxygenDialogContainerDirective,
    DigitKeyboardComponent,
    DigitKeyboardInputDirective,
    LinkHrefDirective,
    NgCarouselDirective,
    MaintenanceComponent,
    BetslipCounterComponent,
    AbstractOutletComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    PromotionIconComponent,
    PromoLabelsComponent,
    PromotionsListComponent,
    InplayScoreComponent,
    QuickbetPanelWrapperComponent,
    CashoutLabelComponent,
    YourCallLabelComponent,
    BybLabelComponent,
    TooltipComponent,
    TooltipDirective,
    NoEventsComponent,
    VirtualSilkComponent,
    BogLabelComponent,
    // desktop individual
    ShowMoreLinkComponent,
    ToggleButtonsComponent,
    DesktopLoadingScreenComponent,
    BetslipHeaderIconComponent,
    MyBetsButtonComponent,
    GhSilkComponent,
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
    // Overridden app components
    AccordionComponent,
     ModalComponent,
    DesktopRacingOutcomeCardComponent,
    ScoreDigitComponent,
    FreeBetEmptyComponent,
    OddsCardHeaderComponent,
    TabsPanelComponent,
    TopBarComponent,
    OddsCardResultComponent,
    OddsCardComponent,
    DesktopPromotionsComponent,
    DesktopTimeFormSelectionSummaryComponent,

    // Platform app components
    DropDownMenuComponent,
    SeeAllLinkComponent,
    SpinnerComponent,
    // InplayMarketSelectorDesktopComponent,
    BreadcrumbsComponent,

    // Main app components
    OddsCardSurfaceBetComponent,
    RacingPanelComponent,
    SurfaceBetsCarouselComponent,
    CommonModule,
    RouterModule,
    SharedPipesModule,
    AccaNotificationComponent,
    HistoricPricesComponent,
    CustomSelectComponent,
    WatchLabelComponent,
    PriceOddsButtonComponent,
    PriceOddsButtonOnPushComponent,
    SwitchersComponent,
    LiveClockComponent,
    ListCardComponent,
    LiveLabelComponent,
    NewLabelComponent,
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
    RacingGridComponent,
    RaceTimerComponent,
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
    LinkHrefDirective,
    TriggerDirective,
    SymbolBackgroundDirective,
    ClickLinkDirective,
    DisableDraggingDirective,
    InputValueDirective,
    EqualColumnDirective,
    DigitKeyboardComponent,
    DigitKeyboardInputDirective,
    NgCarouselDirective,
    ActiveLinkClassDirective,
    BetslipCounterComponent,
    AbstractOutletComponent,
    OutletStatusComponent,
    PromotionDialogComponent,
    PromotionOverlayDialogComponent,
    PromotionIconComponent,
    PromoLabelsComponent,
    PromotionsListComponent,
    InplayScoreComponent,
    ToggleButtonsComponent,
    ShowMoreLinkComponent,
    ShowMoreLinkComponent,
    CashoutLabelComponent,
    YourCallLabelComponent,
    NoEventsComponent,
    VirtualSilkComponent,
    BybLabelComponent,
    // OddsCardHighlightCarouselComponent,
    SvgTeamKitComponent,
    LazyComponent,
    DrawerComponent,
    TooltipComponent,
    TooltipDirective,
    BetslipHeaderIconComponent,
    MyBetsButtonComponent,
    DesktopLoadingScreenComponent,
    BogLabelComponent,
    GhSilkComponent,
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

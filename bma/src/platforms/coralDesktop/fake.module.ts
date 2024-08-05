import { BrowserModule } from '@angular/platform-browser';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';

import { OddsCardHeaderComponent } from '@shared/components/oddsCardHeader/odds-card-header.component';
import { AccordionComponent } from '@shared/components/accordion/accordion.component';
import { TabsPanelComponent } from '@shared/components/tabsPanel/tabs-panel.component';
import { OddsCardComponent } from '@shared/components/oddsCard/odds-card.component';
import { OddsCardResultComponent } from '@shared/components/oddsCardResult/odds-card-result.component';
import {
  OddsCardEnhancedMultiplesComponent
} from '@shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
import { OddsCardSpecialsComponent } from '@shared/components/oddsCard/oddsCardSpecials/odds-card-specials.component';
import { SurfaceBetsCarouselComponent } from '@shared/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { TopBarComponent } from '@shared/components/topBar/top-bar.component';
import { PromotionsComponent } from '@promotions/components/promotion/promotions.component';
import { OffersSectionComponent } from '@bma/components/offerSection/offer-section.component';
import { OddsCardSportComponent } from '@shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { BigCompetitionComponent } from '@app/bigCompetitions/components/bigCompetition/big-competition.component';
import { BmaMainComponent } from '@bma/components/bmaMain/bma-main.component';
import { HomeComponent } from '@bma/components/home/home.component';
import { EventMarketsComponent } from '@edp/components/eventMarkets/event-markets.component';
import { EventTitleBarComponent } from '@edp/components/eventTitleBar/event-title-bar.component';
import { SportEventMainComponent } from '@edp/components/sportEventMain/sport-event-main.component';
import { SportEventPageComponent } from '@edp/components/sportEventPage/sport-event-page.component';
import { FavouritesMatchesComponent } from '@app/favourites/components/matchList/favourites-matches.component';
import { FeaturedInplayComponent } from '@featured/components/featured-inplay/featured-inplay.component';
import { FeaturedModuleComponent } from '@featured/components/featured-module/featured-module.component';
import { FeaturedEventMarketsComponent } from '@featured/components/featured-outright-market/event-markets.component';
import { OlympicsPageComponent } from '@app/olympics/components/olympicsPage/olympics-page.component';
import { BybHomeComponent } from '@yourcall/components/bybHome/byb-home.component';
import { YourcallBybLeagueComponent } from '@yourcall/components/bybLeague/yourcall-byb-league.component';
import { YourCallTabContentComponent } from '@yourcall/components/yourCallTabContent/your-call-tab-content.component';
import { VirtualSportsPageComponent } from '@app/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import { VirtualCarouselMenuComponent } from '@app/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';
import { VirtualCarouselSubMenuComponent } from '@app/vsbr/components/virtualCarouselSubMenu/virtual-carousel-sub-menu.component';
import { TotePageComponent } from '@app/tote/components/totePage/tote-page.component';
import { ToteInfoComponent } from '@app/tote/components/toteInfo/tote-info.component';
import { LottoMainComponent } from '@app/lotto/components/lottoMain/lotto-main.component';
import { GreyhoundsTabsComponent } from '@racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { HorseracingTabsComponent } from '@racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';
import { RacingAntepostTabComponent } from '@app/racing/components/racingAntepostTab/racing-antepost-tab.component';
import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { RacingMainComponent } from '@racing/components/racingMain/racing-main.component';
import { RacingSpecialsTabComponent } from '@racing/components/racingSpecialsTab/racing-specials-tab.component';
import { RacingYourcallSpecialsComponent } from '@racing/components/racingYourcallSpecials/racing-yourcall-specials.component';
import { TimeFormSelectionSummaryComponent } from '@racing/components/timeformSummary/time-form-selection-summary.component';
import { SportMatchesPageComponent } from '@app/sb/components/sportMatchesPage/sport-matches-page.component';
import { SportMainComponent } from '@app/sb/components/sportMain/sport-main.component';
import {
  CompetitionsOutrightsTabComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-outrights-tab.component';
import { AllPromotionsPageComponent } from '@promotions/components/allPromotionsPage/all-promotions-page.component';
import { SinglePromotionPageComponent } from '@promotions/components/singlePromotionPage/single-promotion-page.component';
import { CorrectScoreCouponComponent } from '@sb/components/correctScoreCoupon/correct-score-coupon.component';
import { FeaturedQuickLinksComponent } from '@featured/components/featured-quick-links/featured-quick-links.component';
import { FeaturedRaceCardHomeComponent } from '@featured/components/featured-race-card/race-card-home.component';
import { InplayAllSportsPageComponent } from '@app/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { InplayPageComponent } from '@app/inPlay/components/inplayPage/inplay-page.component';
import { InplaySingleSportPageComponent } from '@app/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayTabComponent } from '@app/inPlay/components/inplayTab/inplay-tab.component';
import { InplayWatchLivePageComponent } from '@app/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import { MultipleSportsSectionsComponent } from '@app/inPlay/components/multipleSportsSections/multiple-sports-sections.component';
import { SingleSportSectionComponent } from '@app/inPlay/components/singleSportSection/single-sport-section.component';
import { CompetitionsPageComponent } from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import { RaceCardsControlsComponent } from '@racing/components/raceCardControls/race-cards-controls.component';
import {
  CompetitionsFutureSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsFutureSportTab/competitions-future-sport-tab.component';
import {
  CompetitionsMatchesTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-matches-tab.component';
import {
  CompetitionsStandingsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component';
import {
  CompetitionsSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-sport-tab.component';
import {
  RacingEnhancedMultiplesComponent
} from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.component';
import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';
import { HorseRaceGridComponent } from '@app/lazy-modules/racingFeatured/components/horseRaceGrid/horse-race-grid.component';
import { RacingEventResultedComponent } from '@racing/components/racingEventResultedComponent/racing-event-resulted.component';
import { CouponsDetailsComponent } from '@sb/components/couponsDetails/coupons-details.component';
import { CouponsListComponent } from '@sb/components/couponsList/coupons-list.component';
import { FootballTutorialOverlayComponent } from '@sb/components/footballTutorialOverlay/football-tutorial-overlay.component';
import { SportMatchesTabComponent } from '@sb/components/sportMatchesTab/sport-matches-tab.component';
import { BreadcrumbsComponent } from '@shared/components/breadcrumbs/breadcrumbs.component';
import { DropDownMenuComponent } from '@shared/components/dropDownMenu/drop-down-menu.component';
import { StickyVirtualScrollerComponent } from '@shared/components/stickyVirtualScroller/sticky-virtual-scroller.component';
import { NgCarouselExtendedDirective } from '@shared/directives/ng-carousel-extended/carousel.directive';
import { ToteSliderComponent } from '@app/tote/components/toteSlider/tote-slider.component';
import { LoadingScreenComponent } from '@shared/components/loadingScreen/loading-screen.component';
import { RacingFeaturedComponent } from '@app/lazy-modules/racingFeatured/components/racingFeatured/racing-featured.component';
import { RacingEventsComponent } from '@app/lazy-modules/racingFeatured/components/racingEvents/racing-events.component';
import { OffersAndFeaturedRacesComponent } from '@racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';
import { HomeScreenComponent } from '@shared/components/homeScreen/home-screen.component';
import { RacingOutcomeCardComponent } from '@racing/components/racingOutcomeCard/racing-outcome-card.component';
import { RightColumnWidgetComponent } from '@app/lazy-modules/rightColumn/components/rightColumnWidget/right-column-widget.component';
import {
  RightColumnWidgetItemComponent
} from '@app/lazy-modules/rightColumn/components/rightColumnWidgetItem/right-column-widget-item.component';
import { VirtualHomePageComponent } from '@app/vsbr/components/virtualHomePage/virtual-home-page.component';
import { VirtualOtherSports } from '@app/vsbr/components/virtualOtherSports/virtual-other-sports.component';

@NgModule({
  declarations: [
    RacingOutcomeCardComponent,
    OddsCardHeaderComponent,
    AccordionComponent,
    OffersAndFeaturedRacesComponent,
    TabsPanelComponent,
    OddsCardComponent,
    OddsCardResultComponent,
    OddsCardEnhancedMultiplesComponent,
    OddsCardSpecialsComponent,
    SurfaceBetsCarouselComponent,
    RacingMainComponent,
    TopBarComponent,
    PromotionsComponent,
    TimeFormSelectionSummaryComponent,
    OffersSectionComponent,
    OddsCardSportComponent,
    BigCompetitionComponent,
    RacingEnhancedMultiplesComponent,
    BmaMainComponent,
    RightColumnWidgetComponent,
    RightColumnWidgetItemComponent,
    HomeComponent,
    EventMarketsComponent,
    EventTitleBarComponent,
    SportEventMainComponent,
    SportEventPageComponent,
    FavouritesMatchesComponent,
    FeaturedInplayComponent,
    FeaturedModuleComponent,
    FeaturedEventMarketsComponent,
    FeaturedQuickLinksComponent,
    FeaturedRaceCardHomeComponent,
    InplayAllSportsPageComponent,
    InplayPageComponent,
    InplaySingleSportPageComponent,
    InplayTabComponent,
    InplayWatchLivePageComponent,
    MultipleSportsSectionsComponent,
    SingleSportSectionComponent,
    CompetitionsPageComponent,
    CompetitionsFutureSportTabComponent,
    CompetitionsMatchesTabComponent,
    CompetitionsOutrightsTabComponent,
    CompetitionsStandingsTabComponent,
    CompetitionsSportTabComponent,
    LottoMainComponent,
    OlympicsPageComponent,
    SportMatchesPageComponent,
    SportTabsPageComponent,
    AllPromotionsPageComponent,
    SinglePromotionPageComponent,
    HorseRaceGridComponent,
    RacingAntepostTabComponent,
    RacingEventComponent,
    RacingEventResultedComponent,
    RacingSpecialsTabComponent,
    GreyhoundsTabsComponent,
    HorseracingTabsComponent,
    RacingYourcallSpecialsComponent,
    CorrectScoreCouponComponent,
    CouponsDetailsComponent,
    CouponsListComponent,
    FootballTutorialOverlayComponent,
    SportMatchesTabComponent,
    BreadcrumbsComponent,
    DropDownMenuComponent,
    StickyVirtualScrollerComponent,
    NgCarouselExtendedDirective,
    ToteInfoComponent,
    TotePageComponent,
    ToteSliderComponent,
    VirtualSportsPageComponent,
    VirtualCarouselMenuComponent,
    VirtualCarouselSubMenuComponent,
    BybHomeComponent,
    YourcallBybLeagueComponent,
    YourCallTabContentComponent,
    SportMainComponent,
    LoadingScreenComponent,
    RacingEventsComponent,
    RacingFeaturedComponent,
    HomeScreenComponent,
    RaceCardsControlsComponent,
    RacingOutcomeCardComponent,
    RaceCardsControlsComponent,
    VirtualHomePageComponent,
    VirtualOtherSports
  ],
  imports: [
    BrowserModule,
    SharedPipesModule
  ],
  exports: [],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FakeModule { }

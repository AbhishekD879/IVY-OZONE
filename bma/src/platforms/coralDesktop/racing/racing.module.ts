import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingRoutingModule } from './racing-routing.module';
import { QuantumLeapComponent } from '@racing/components/quantumLeap/quantum-leap.component';
import { RacingTabYourcallComponent } from '@racing/components/racingTabYourcall/racing-tab-yourcall.component';
import { TimeFormSummaryComponent } from '@racing/components/timeformSummary/time-form-summary.component';
import { SharedModule } from '@sharedModule/shared.module';
import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';
import { DesktopRacingMainComponent } from './components/racingMain/racing-main.component';
import { RacingTabsMainComponent } from '@racing/components/racingTabsMain/racing-tabs-main.component';
import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';
import { DailyRacingModuleComponent } from '@racing/components/dailyRacing/daily-racing.component';
import { RacingEnhancedMultiplesService } from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.service';
import {
  RacingEnhancedMultiplesComponent
} from '@coralDesktop/racing/components/racingEnhancedMultiples/racing-enhanced-multiples.component';
import { SbModule } from '@sbModule/sb.module';
import { RacingRunService } from '@racing/services/racingRunService/racing-run.service';
import { RacingSpecialsCarouselComponent } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.component';
import { DesktopRacingPostWidgetComponent } from '@coralDesktop/racing/components/racingPostWidget/racing-post-widget.component';
import { DesktopHorseracingTabsComponent } from '@coralDesktop/racing/components/horseracingTabs/horseracing-tabs.component';
import { DesktopGreyhoundsTabsComponent } from '@coralDesktop/racing/components/greyhoundsTabs/greyhounds-tabs.component';
import { DesktopModule } from '@desktopModule/desktop.module';
import { BuildRaceCardComponent } from '@coralDesktop/racing/components/buildRaceCard/build-race-card.component';
import { DesktopRacingAntepostTabComponent } from '@coralDesktop/racing/components/racingAntepostTab/racing-antepost-tab.component';
import { DesktopRacingEventComponent } from '@coralDesktop/racing/components/racingEventComponent/racing-event.component';
import { QuickNavigationComponent } from '@racing/components/quickNavigation/quick-navigation.component';
import { RacingResultsService } from '@core/services/sport/racing-results.service';
import { RacingPostPickComponent } from '@racing/components/racingPostPick/racing-post-pick.component';

// Platform app components / services
import { BuildYourRaceCardPageComponent } from '@coralDesktop/racing/components/buildYourRaceCardPage/build-your-race-card-page.component';
import { BuildYourRaceCardPageService } from '@coralDesktop/racing/components/buildYourRaceCardPage/build-your-race-card-page.service';
import { StickyBuildCardDirective } from '@coralDesktop/racing/directives/sticky-build-card.directive';
import {
  DesktopRacingYourcallSpecialsComponent
} from '@coralDesktop/racing/components/racingYourcallSpecials/racing-yourcall-specials.component';
import {
  DesktopRacingSpecialsTabComponent
} from '@coralDesktop/racing/components/racingSpecialsTab/racing-specials-tab.component';
import {
  OffersAndFeaturedRacesComponent
} from '@coralDesktop/racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';
import { GreyhoundFutureTabComponent } from '@racing/components/greyhound/greyhoundFutureTab/greyhound-future-tab.component';
import { RacingOutcomeResultedCardComponent } from '@racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';
import {
  DesktopRacingEventResultedComponent
} from '@coralDesktop/racing/components/racingEventResultedComponent/racing-event-resulted.component';
import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service'; 
import { GreyhoundService } from '@core/services/racing/greyhound/greyhound.service'; 
@NgModule({
  declarations: [
    // Overridden app components
    DesktopHorseracingTabsComponent,
    DesktopGreyhoundsTabsComponent,
    DesktopRacingMainComponent,
    DesktopRacingAntepostTabComponent,
    DesktopRacingEventComponent,
    // Platform app components
    BuildYourRaceCardPageComponent,
    DesktopRacingYourcallSpecialsComponent,
    DesktopRacingSpecialsTabComponent,
    // Main app components
    TimeFormSummaryComponent,
    RacingSpecialsCarouselComponent,
    DailyRacingModuleComponent,
    RacingEnhancedMultiplesComponent,
    DesktopHorseracingTabsComponent,
    DesktopGreyhoundsTabsComponent,
    QuantumLeapComponent,
    RacingTabYourcallComponent,
    RacingTabsMainComponent,
    RacingEventMainComponent,
    RacingOutcomeResultedCardComponent,
    DesktopRacingEventResultedComponent,
    DesktopRacingPostWidgetComponent,
    QuickNavigationComponent,
    BuildRaceCardComponent,
    StickyBuildCardDirective,
    OffersAndFeaturedRacesComponent,
    GreyhoundFutureTabComponent,
    RacingPostPickComponent
  ],
  imports: [
    HttpClientModule,
    SharedModule,
    SbModule,
    RacingRoutingModule,
    DesktopModule
  ],
  exports: [
    // Overridden app components
    DesktopHorseracingTabsComponent,
    DesktopGreyhoundsTabsComponent,
    DesktopRacingMainComponent,
    DesktopRacingAntepostTabComponent,
    DesktopRacingEventComponent,
    // Platform app components
    BuildYourRaceCardPageComponent,
    DesktopRacingYourcallSpecialsComponent,
    DesktopRacingSpecialsTabComponent,
    // Main app components
    TimeFormSummaryComponent,
    RacingSpecialsCarouselComponent,
    DailyRacingModuleComponent,
    RacingEnhancedMultiplesComponent,
    DesktopHorseracingTabsComponent,
    QuantumLeapComponent,
    RacingTabYourcallComponent,
    RacingTabsMainComponent,
    RacingEventMainComponent,
    RacingOutcomeResultedCardComponent,
    DesktopRacingEventResultedComponent,
    DesktopRacingPostWidgetComponent,
    QuickNavigationComponent,
    StickyBuildCardDirective,
    OffersAndFeaturedRacesComponent,
    RacingPostPickComponent
  ],
  providers: [
    RoutesDataSharingService,
    RacingEnhancedMultiplesService,
    RacingRunService,
    // Platform app services
    BuildYourRaceCardPageService,
    HorseracingService,
    GreyhoundService,
    RacingResultsService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingModule {
  constructor(racingRunService: RacingRunService) {
    racingRunService.run();
  }
}

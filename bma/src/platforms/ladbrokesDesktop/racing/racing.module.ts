import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { QuantumLeapComponent } from '@racing/components/quantumLeap/quantum-leap.component';
import { RacingTabYourcallComponent } from '@racing/components/racingTabYourcall/racing-tab-yourcall.component';
import { TimeFormSummaryComponent } from '@racing/components/timeformSummary/time-form-summary.component';
import { SharedModule } from '@sharedModule/shared.module';
import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';
import { DesktopRacingMainComponent } from './components/racingMain/racing-main.component';
import { RacingTabsMainComponent } from '@ladbrokesMobile/racing/components/racingTabsMain/racing-tabs-main.component';
import { RacingEnhancedMultiplesService } from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.service';
import {
  RacingEnhancedMultiplesComponent
} from '@ladbrokesDesktop/racing/components/racingEnhancedMultiples/racing-enhanced-multiples.component';
import { SbModule } from '@sbModule/sb.module';
import { RacingRunService } from '@racing/services/racingRunService/racing-run.service';
import { RacingSpecialsCarouselComponent } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.component';
import { DesktopHorseracingTabsComponent } from '@ladbrokesDesktop/racing/components/horseracingTabs/horseracing-tabs.component';
import { DesktopGreyhoundsTabsComponent } from '@ladbrokesDesktop/racing/components/greyhoundsTabs/greyhounds-tabs.component';
import { DesktopModule } from '@desktop/desktop.module';
import { BuildRaceCardComponent } from '@ladbrokesDesktop/racing/components/buildRaceCard/build-race-card.component';
import { DesktopRacingAntepostTabComponent } from '@ladbrokesDesktop/racing/components/racingAntepostTab/racing-antepost-tab.component';
import { DesktopRacingEventComponent } from '@ladbrokesDesktop/racing/components/racingEventComponent/racing-event.component';
import { GreyhoundFutureTabComponent } from '@racing/components/greyhound/greyhoundFutureTab/greyhound-future-tab.component';
import { QuickNavigationComponent } from '@racing/components/quickNavigation/quick-navigation.component';
import { LadbrokesRacingPostWidgetComponent } from '@ladbrokesDesktop/racing/components/racingPostWidget/racing-post-widget.component';
import { RacingResultsService } from '@core/services/sport/racing-results.service';
import { LadbrokesRacingEventMainComponent } from '@ladbrokesMobile/racing/components/racingEventMain/racing-event-main.component';
import { RacingPostPickComponent } from '@racing/components/racingPostPick/racing-post-pick.component';
// Platform app components / services
/* eslint-disable max-len */
import {
  BuildYourRaceCardPageComponent
} from '@ladbrokesDesktop/racing/components/buildYourRaceCardPage/build-your-race-card-page.component';
import { BuildYourRaceCardPageService } from '@ladbrokesDesktop/racing/components/buildYourRaceCardPage/build-your-race-card-page.service';
import { StickyBuildCardDirective } from '@ladbrokesDesktop/racing/directives/sticky-build-card.directive';
import {
  DesktopRacingYourcallSpecialsComponent
} from '@ladbrokesDesktop/racing/components/racingYourcallSpecials/racing-yourcall-specials.component';
import {
  DesktopRacingSpecialsTabComponent
} from '@ladbrokesDesktop/racing/components/racingSpecialsTab/racing-specials-tab.component';
import { OffersAndFeaturedRacesComponent } from '@ladbrokesDesktop/racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';
import {
  DesktopRacingEventResultedComponent
} from '@ladbrokesDesktop/racing/components/racingEventResultedComponent/racing-event-resulted.component';
import {
  DesktopRacingOutcomeResultedCardComponent
} from '@ladbrokesDesktop/racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';
import { GreyhoundSpecialsTabComponent } from '@ladbrokesDesktop/racing/components/greyhoundSpecialsTab/greyhound-specials-tab.component';
import { LadbrokesDesktopQuickNavigationComponent } from '@ladbrokesDesktop/lazy-modules/quickNavigation/quick-navigation.component';
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
    GreyhoundSpecialsTabComponent,
    TimeFormSummaryComponent,
    RacingSpecialsCarouselComponent,
    QuickNavigationComponent,
    RacingEnhancedMultiplesComponent,
    DesktopHorseracingTabsComponent,
    DesktopGreyhoundsTabsComponent,
    QuantumLeapComponent,
    RacingTabYourcallComponent,
    RacingTabsMainComponent,
    LadbrokesRacingEventMainComponent,
    DesktopRacingOutcomeResultedCardComponent,
    DesktopRacingEventResultedComponent,
    LadbrokesRacingPostWidgetComponent,
    BuildRaceCardComponent,
    StickyBuildCardDirective,
    OffersAndFeaturedRacesComponent,
    GreyhoundFutureTabComponent,
    RacingPostPickComponent,
    LadbrokesDesktopQuickNavigationComponent
  ],
  imports: [
    HttpClientModule,
    SharedModule,
    SbModule,
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
    GreyhoundSpecialsTabComponent,
    TimeFormSummaryComponent,
    RacingSpecialsCarouselComponent,
    QuickNavigationComponent,
    RacingEnhancedMultiplesComponent,
    DesktopHorseracingTabsComponent,
    QuantumLeapComponent,
    RacingTabYourcallComponent,
    RacingTabsMainComponent,
    LadbrokesRacingEventMainComponent,
    DesktopRacingOutcomeResultedCardComponent,
    DesktopRacingEventResultedComponent,
    LadbrokesRacingPostWidgetComponent,
    StickyBuildCardDirective,
    OffersAndFeaturedRacesComponent,
    RacingPostPickComponent,
    LadbrokesDesktopQuickNavigationComponent
  ],
  providers: [
    RoutesDataSharingService,
    RacingEnhancedMultiplesService,
    RacingRunService,
    // Platform app services
    BuildYourRaceCardPageService,
    RacingResultsService,
    HorseracingService,
    GreyhoundService,
  
   
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingModule {
  constructor(racingRunService: RacingRunService) {
    racingRunService.run();
  }
}

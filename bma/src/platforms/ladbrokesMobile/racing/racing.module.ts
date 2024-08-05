import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingTabYourcallComponent } from '@racing/components/racingTabYourcall/racing-tab-yourcall.component';
import { TimeFormSummaryComponent } from '@racing/components/timeformSummary/time-form-summary.component';
import { SharedModule } from '@sharedModule/shared.module';
import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';
import { RacingTabsMainComponent } from '@racingModule/components/racingTabsMain/racing-tabs-main.component';
import { QuantumLeapComponent } from '@racing/components/quantumLeap/quantum-leap.component';

import { RacingYourcallSpecialsComponent } from '@racing/components/racingYourcallSpecials/racing-yourcall-specials.component';

import { RacingSpecialsCarouselService } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.service';
import { RacingEnhancedMultiplesService } from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.service';
import { RacingEnhancedMultiplesComponent } from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.component';

import { SbModule } from '@sbModule/sb.module';

import { RacingRunService } from '@racing/services/racingRunService/racing-run.service';
import { RacingResultsService } from '@core/services/sport/racing-results.service';

import {
  LadbrokesRacingSpecialsCarouselComponent
} from '@ladbrokesMobile/racing/components/racingSpecialsCarousel/racing-specials-carousel.component';
import {
  HorseracingTabsComponent
} from '@ladbrokesMobile/racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';
/* eslint-disable max-len */
import { LadbrokesRacingEventComponent } from '@ladbrokesMobile/racing/components/racingEventComponent/racing-event.component';
import { LadbrokesRacingAntepostTabComponent } from '@ladbrokesMobile/racing/components/racingAntepostTab/racing-antepost-tab.component';
import { LadbrokesGreyhoundFutureTabComponent } from '@ladbrokesMobile/racing/components/greyhound/greyhoundFutureTab/greyhound-future-tab.component';
import { LadbrokesGreyhoundsTabsComponent } from '@ladbrokesMobile/racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { EventTimeService } from '@ladbrokesMobile/racing/services/event-time.service';
import { LadbrokesRacingEventResultedComponent } from '@ladbrokesMobile/racing/components/racingEventResultedComponent/racing-event-resulted.component';
import { LadbrokesRacingEventMainComponent } from '@ladbrokesMobile/racing/components/racingEventMain/racing-event-main.component';
import { LadbrokesMobileRacingSpecialsTabComponent } from '@ladbrokesMobile/racing/components/racingSpecialsTab/racing-specials-tab.component';
import { LadbrokesRacingOutcomeResultedCardComponent } from '@ladbrokesMobile/racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';
import { LadbrokesMobileQuickNavigationComponent } from '@ladbrokesMobile/racing/components/quickNavigation/quick-navigation.component';
import { RacingMainComponent } from '@ladbrokesMobile/racing/components/racingMain/racing-main.component';
import { RacingPostPickComponent } from '@racing/components/racingPostPick/racing-post-pick.component';
import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service'; 
import { GreyhoundService } from '@core/services/racing/greyhound/greyhound.service'; 

@NgModule({
  declarations: [
    // Overridden Component
    LadbrokesRacingSpecialsCarouselComponent,
    LadbrokesMobileRacingSpecialsTabComponent,
    LadbrokesGreyhoundsTabsComponent,
    LadbrokesMobileQuickNavigationComponent,

    TimeFormSummaryComponent,
    RacingYourcallSpecialsComponent,
    RacingEnhancedMultiplesComponent,
    LadbrokesRacingAntepostTabComponent,
    LadbrokesRacingEventComponent,
    LadbrokesRacingOutcomeResultedCardComponent,
    LadbrokesRacingEventResultedComponent,
    QuantumLeapComponent,
    RacingTabYourcallComponent,
    RacingMainComponent,
    RacingTabsMainComponent,
    LadbrokesGreyhoundFutureTabComponent,
    HorseracingTabsComponent,
    LadbrokesRacingEventMainComponent,
    RacingPostPickComponent
  ],
  imports: [
    HttpClientModule,
    SharedModule,
    SbModule
  ],
  exports: [
    // Overridden Component
    LadbrokesRacingSpecialsCarouselComponent,
    TimeFormSummaryComponent,
    RacingYourcallSpecialsComponent,
    RacingEnhancedMultiplesComponent,
    LadbrokesRacingAntepostTabComponent,
    QuantumLeapComponent,
    LadbrokesGreyhoundsTabsComponent,
    RacingTabYourcallComponent,
    RacingMainComponent,
    RacingTabsMainComponent,
    HorseracingTabsComponent,
    LadbrokesRacingEventMainComponent,
    LadbrokesMobileRacingSpecialsTabComponent,
    RacingPostPickComponent,
    LadbrokesMobileQuickNavigationComponent,
    LadbrokesRacingOutcomeResultedCardComponent
  ],
  providers: [
    RoutesDataSharingService,
    RacingSpecialsCarouselService,
    RacingEnhancedMultiplesService,
    RacingRunService,
    EventTimeService,
    RacingResultsService,
    HorseracingService,
    GreyhoundService
    
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingModule {
  constructor(racingRunService: RacingRunService) {
    racingRunService.run();
  }
}

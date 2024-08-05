import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { QuantumLeapComponent } from '@racing/components/quantumLeap/quantum-leap.component';
import { RacingTabYourcallComponent } from '@racing/components/racingTabYourcall/racing-tab-yourcall.component';
import { TimeFormSummaryComponent } from '@racing/components/timeformSummary/time-form-summary.component';
import { SharedModule } from '@sharedModule/shared.module';
import { RoutesDataSharingService } from './services/routesDataSharing/routes-data-sharing.service';
import { RacingMainComponent } from '@racing/components/racingMain/racing-main.component';
import { RacingTabsMainComponent } from './components/racingTabsMain/racing-tabs-main.component';
import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';

import { RacingYourcallSpecialsComponent } from './components/racingYourcallSpecials/racing-yourcall-specials.component';

import { RacingSpecialsCarouselService } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.service';
import { RacingEnhancedMultiplesService } from './components/racingEnhancedMultiples/racing-enhanced-multiples.service';
import { RacingEnhancedMultiplesComponent } from './components/racingEnhancedMultiples/racing-enhanced-multiples.component';
import { RacingAntepostTabComponent } from '@racing/components/racingAntepostTab/racing-antepost-tab.component';
import { RacingSpecialsTabComponent } from '@racing/components/racingSpecialsTab/racing-specials-tab.component';

import { HorseracingTabsComponent } from '@racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';
import { GreyhoundsTabsComponent } from '@racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { SbModule } from '@sbModule/sb.module';
import { RacingRunService } from '@racing/services/racingRunService/racing-run.service';
import { RacingSpecialsCarouselComponent } from '@racing/components/racingSpecialsCarousel/racing-specials-carousel.component';
import { GreyhoundFutureTabComponent } from '@racing/components/greyhound/greyhoundFutureTab/greyhound-future-tab.component';
import { RacingOutcomeResultedCardComponent } from '@racing/components/racingOutcomeResultedCard/racing-outcome-resulted-card.component';
import { RacingEventResultedComponent } from '@racing/components/racingEventResultedComponent/racing-event-resulted.component';
import { QuickNavigationComponent } from '@racing/components/quickNavigation/quick-navigation.component';
import { RacingResultsService } from '@core/services/sport/racing-results.service';
import { RacingPostPickComponent } from '@racing/components/racingPostPick/racing-post-pick.component';
@NgModule({
  declarations: [
    TimeFormSummaryComponent,
    RacingYourcallSpecialsComponent,
    RacingSpecialsCarouselComponent,
    RacingSpecialsTabComponent,
    RacingEnhancedMultiplesComponent,
    RacingAntepostTabComponent,
    HorseracingTabsComponent,
    GreyhoundsTabsComponent,
    RacingEventComponent,
    QuickNavigationComponent,
    QuantumLeapComponent,
    RacingTabYourcallComponent,
    RacingMainComponent,
    RacingTabsMainComponent,
    RacingEventMainComponent,
    RacingEventResultedComponent,
    RacingOutcomeResultedCardComponent,
    GreyhoundFutureTabComponent,
    RacingPostPickComponent,
    ],
  imports: [
    HttpClientModule,
    SharedModule,
    SbModule
  ],
  exports: [
    TimeFormSummaryComponent,
    RacingYourcallSpecialsComponent,
    RacingSpecialsCarouselComponent,
    RacingSpecialsTabComponent,
    RacingEnhancedMultiplesComponent,
    HorseracingTabsComponent,
    RacingAntepostTabComponent,
    QuantumLeapComponent,
    GreyhoundsTabsComponent,
    RacingTabYourcallComponent,
    RacingMainComponent,
    RacingTabsMainComponent,
    RacingEventMainComponent,
    RacingPostPickComponent,
    RacingOutcomeResultedCardComponent
    ],
  providers: [
    RoutesDataSharingService,
    RacingSpecialsCarouselService,
    RacingEnhancedMultiplesService,
    RacingRunService,
    RacingResultsService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingModule {
  constructor(racingRunService: RacingRunService) {
    racingRunService.run();
  }
}

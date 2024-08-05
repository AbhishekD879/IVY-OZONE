/**
 * Inplay Module documentation
 * https://confluence.egalacoral.com/display/SPI/Inplay
 */
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { MultipleSportsSectionsComponent } from '@inplayModule/components/multipleSportsSections/multiple-sports-sections.component';
import { InplayTabComponent } from '@inplayModule/components/inplayTab/inplay-tab.component';
import { InplayAllSportsPageComponent } from '@inplayModule/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { InplayRunService } from '@app/inPlay/services/inplayRunService/inplay-run.service';
import { InplaySingleSportPageComponent } from '@inplayModule/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayWatchLivePageComponent } from '@inplayModule/components/inplayWatchLivePage/inplay-watch-live-page.component';

import { InPlayRoutingModule } from '@inplayModule/inplay-routing.module';
import { SingleSportSectionComponent } from '@inplayModule/components/singleSportSection/single-sport-section.component';
import { InplayPageComponent } from '@inplayModule/components/inplayPage/inplay-page.component';
import { RaceCardInplayComponent } from '@inplayModule/components/raceCardInplay/race-card-inplay.component';

@NgModule({
  imports: [
    SharedModule,
    InPlayRoutingModule
  ],
  exports: [],
  declarations: [
    InplayTabComponent,
    MultipleSportsSectionsComponent,

    InplaySingleSportPageComponent,
    InplayAllSportsPageComponent,
    InplayWatchLivePageComponent,

    InplayPageComponent,
    SingleSportSectionComponent,
    RaceCardInplayComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class InplayModule {
  static entry = { InplayTabComponent, InplayWatchLivePageComponent };

  constructor(inplayRunService: InplayRunService) {
    inplayRunService.run();
  }
}

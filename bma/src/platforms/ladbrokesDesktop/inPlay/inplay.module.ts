/**
 * Inplay Module documentation
 * https://confluence.egalacoral.com/display/SPI/Inplay
 */
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { MultipleSportsSectionsComponent } from '@inplayModule/components/multipleSportsSections/multiple-sports-sections.component';
import { InplayTabComponent } from '@inplayModule/components/inplayTab/inplay-tab.component';
import { InplayAllSportsPageComponent } from '@inplayModule/components//inplayAllSportsPage/inplay-all-sports-page.component';
import { InplayRunService } from '@app/inPlay/services/inplayRunService/inplay-run.service';
import { InplaySingleSportPageComponent
} from '@ladbrokesDesktop/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayWatchLivePageComponent } from '@ladbrokesDesktop/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';

import { InPlayRoutingModule } from '@inplayModule/inplay-routing.module';
import { SingleSportSectionComponent
} from '@ladbrokesDesktop/inPlay/components/singleSportSection/single-sport-section.component';
import { InplayPageComponent } from '@ladbrokesDesktop/inPlay/components/inplayPage/inplay-page.component';

@NgModule({
  imports: [
    SharedModule,
    InPlayRoutingModule
  ],
  exports: [
    InplayTabComponent
  ],
  declarations: [
    InplayTabComponent,
    MultipleSportsSectionsComponent,

    InplaySingleSportPageComponent,
    InplayAllSportsPageComponent,
    InplayWatchLivePageComponent,

    InplayPageComponent,
    SingleSportSectionComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class InplayModule {
  static entry = { InplayTabComponent, InplayWatchLivePageComponent };

  constructor(inplayRunService: InplayRunService) {
    inplayRunService.run();
  }
}

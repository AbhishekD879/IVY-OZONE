/**
 * Inplay Module documentation
 * https://confluence.egalacoral.com/display/SPI/Inplay
 */
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { InplayTabComponent } from '@ladbrokesMobile/inPlay/components/inplayTab/inplay-tab.component';
import { InplayPageComponent } from '@ladbrokesMobile/inPlay/components/inplayPage/inplay-page.component';
import { InplayAllSportsPageComponent } from '@ladbrokesMobile/inPlay/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { InplayWatchLivePageComponent } from '@ladbrokesMobile/inPlay/components/inplayWatchLivePage/inplay-watch-live-page.component';
import {
  InplaySingleSportPageComponent } from '@ladbrokesMobile/inPlay/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayRunService } from '@app/inPlay/services/inplayRunService/inplay-run.service';
import {
  LadbrokesSingleSportSectionComponent
} from '@ladbrokesMobile/inPlay/components/single-sport-section/single-sport-section.component';
import { InPlayRoutingModule } from '@app/inPlay/inplay-routing.module';
import {
  LadbrokesMultipleSportsSectionsComponent
} from '@ladbrokesMobile/inPlay/components/multiple-sports-sections/multiple-sports-sections.component';

@NgModule({
  imports: [
    SharedModule,
    InPlayRoutingModule
  ],
  exports: [InplayTabComponent],
  declarations: [
    InplayTabComponent,

    InplayPageComponent,
    InplayAllSportsPageComponent,
    InplayWatchLivePageComponent,
    InplaySingleSportPageComponent,

    // Overridden Component
    LadbrokesSingleSportSectionComponent,
    LadbrokesMultipleSportsSectionsComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class InplayModule {
  static entry = { InplayTabComponent, InplayWatchLivePageComponent };

  constructor(inplayRunService: InplayRunService) {
    inplayRunService.run();
  }
}

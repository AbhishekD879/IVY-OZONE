import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import {
  CompetitionsMatchesTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-matches-tab.component';
import {
  CompetitionsSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-sport-tab.component';
import {
  LadbrokesCompetitionsPageComponent
} from '@ladbrokesMobile/lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import {
  CompetitionsOutrightsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-outrights-tab.component';
// eslint-disable-next-line max-len
import { LadbrokesCompetitionsResultsTabComponent } from '@ladbrokesMobile/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-results-tab.component';
import {
  CompetitionsCategoryComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-categories.component';
import {
  LadbrokesCompetitionsTabRoutingModule
} from '@ladbrokesMobile/lazy-modules/competitionsSportTab/competitionsSportTab-routing.module';
// eslint-disable-next-line max-len
import { LadbrokesCompetitionsStandingsTabComponent } from '@ladbrokesMobile/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component';
import {
  CompetitionsFutureSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsFutureSportTab/competitions-future-sport-tab.component';

@NgModule({
  imports: [
    SharedModule,
    LadbrokesCompetitionsTabRoutingModule
  ],
  declarations: [
    CompetitionsSportTabComponent,
    CompetitionsMatchesTabComponent,
    LadbrokesCompetitionsPageComponent,
    LadbrokesCompetitionsStandingsTabComponent,
    LadbrokesCompetitionsResultsTabComponent,
    CompetitionsOutrightsTabComponent,
    CompetitionsCategoryComponent,
    CompetitionsFutureSportTabComponent
  ],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CompetitionsTabModule {
  static entry = {CompetitionsSportTabComponent, CompetitionsMatchesTabComponent};
}

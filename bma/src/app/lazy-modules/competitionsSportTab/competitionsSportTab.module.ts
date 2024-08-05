import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import {
  CompetitionsMatchesTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-matches-tab.component';
import {
  CompetitionsSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-sport-tab.component';
import { CompetitionsPageComponent } from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import {
  CompetitionsResultsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-results-tab.component';
import {
  CompetitionsOutrightsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-outrights-tab.component';
import {
  CompetitionsCategoryComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-categories.component';
import { CompetitionsTabRoutingModule } from '@lazy-modules/competitionsSportTab/competitionsSportTab-routing.module';
import {
  CompetitionsStandingsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component';
import {
  CompetitionsFutureSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsFutureSportTab/competitions-future-sport-tab.component';

@NgModule({
  imports: [
    SharedModule,
    CompetitionsTabRoutingModule
  ],
  declarations: [
    CompetitionsSportTabComponent,
    CompetitionsPageComponent,
    CompetitionsMatchesTabComponent,
    CompetitionsResultsTabComponent,
    CompetitionsOutrightsTabComponent,
    CompetitionsCategoryComponent,
    CompetitionsStandingsTabComponent,
    CompetitionsFutureSportTabComponent
  ],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CompetitionsTabModule {
  static entry = {CompetitionsSportTabComponent, CompetitionsMatchesTabComponent};
}

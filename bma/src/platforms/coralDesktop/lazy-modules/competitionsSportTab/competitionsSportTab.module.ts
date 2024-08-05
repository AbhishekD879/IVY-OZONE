import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import {
  CompetitionsResultsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-results-tab.component';
import {
  CompetitionsCategoryComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-categories.component';

import {
  CompetitionsCategoryListComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsCategoryList/competitions-category-list.component';
import {
  CompetitionSelectorComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionSelector/competition-selector.component';
import {
  DesktopCompetitionsMatchesTabComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsMatchesTab/competitions-matches-tab.component';
import {
  DesktopCompetitionsOutrightsTabComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsOutrightsTab/competitions-outrights-tab.component';
import {
  CompetitionsOutrightsTabMultipleEventsComponent
// eslint-disable-next-line max-len
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsOutrightsTabMultipleEvents/competitions-outrights-tab-multiple-events.component';
import {
  CompetitionsOutrightsTabOneEventComponent
// eslint-disable-next-line max-len
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsOutrightsTabOneEvent/competitions-outrights-tab-one-event.component';
import {
  DesktopCompetitionsPageComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import {
  DesktopCompetitionsSportTabComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-sport-tab.component';
import {
  QuickLinksHeaderComponent
} from '@coralDesktop/lazy-modules/competitionsSportTab/components/quickLinksHeader/quick-links-header.component';
import {
  CompetitionsFutureSportTabComponent
} from '@lazy-modules-module/competitionsSportTab/components/competitionsFutureSportTab/competitions-future-sport-tab.component';

import { CompetitionsTabRoutingModule } from '@coralDesktop/lazy-modules/competitionsSportTab/competitionsSportTab-routing.module';
import { CompetitionsService } from '@coralDesktop/lazy-modules/competitionsSportTab/services/competitons/competitons.service';

import { DesktopModule } from '@desktopModule/desktop.module';

@NgModule({
  imports: [
    SharedModule,
    DesktopModule,
    CompetitionsTabRoutingModule
  ],
  declarations: [
    CompetitionsCategoryListComponent,
    CompetitionSelectorComponent,
    DesktopCompetitionsOutrightsTabComponent,
    DesktopCompetitionsMatchesTabComponent,
    CompetitionsOutrightsTabMultipleEventsComponent,
    CompetitionsOutrightsTabOneEventComponent,
    DesktopCompetitionsPageComponent,
    DesktopCompetitionsSportTabComponent,
    QuickLinksHeaderComponent,
    CompetitionsResultsTabComponent,
    CompetitionsCategoryComponent,
    CompetitionsFutureSportTabComponent
  ],
  providers: [
    CompetitionsService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CompetitionsTabModule {
  static entry = {DesktopCompetitionsSportTabComponent, DesktopCompetitionsMatchesTabComponent};
}

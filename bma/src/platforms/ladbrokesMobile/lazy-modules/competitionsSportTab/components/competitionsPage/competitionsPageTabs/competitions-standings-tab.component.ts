import { Component } from '@angular/core';
import {
  CompetitionsStandingsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component';

@Component({
  selector: 'competitions-standings-tab',
  // eslint-disable-next-line
  templateUrl: '../../../../../../../app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component.html',
  styleUrls: [
    // eslint-disable-next-line
    '../../../../../../../app/lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-standings-tab.component.scss',
    './competitions-standings-tab.component.scss']
})
export class LadbrokesCompetitionsStandingsTabComponent extends CompetitionsStandingsTabComponent {}

import { Component, OnInit } from '@angular/core';

import {
  CompetitionsOutrightsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-outrights-tab.component';

@Component({
  selector: 'competitions-outrights-tab',
  templateUrl: './competitions-outrights-tab.component.html'
})
export class DesktopCompetitionsOutrightsTabComponent extends CompetitionsOutrightsTabComponent implements OnInit {
  openedItems: boolean[];
  isSingleEvent: boolean;

  ngOnInit(): void {
    // First item (accordion) should be opened.
    this.openedItems = [true];

    this.isSingleEvent = this.outrights.length === 1;
  }

}

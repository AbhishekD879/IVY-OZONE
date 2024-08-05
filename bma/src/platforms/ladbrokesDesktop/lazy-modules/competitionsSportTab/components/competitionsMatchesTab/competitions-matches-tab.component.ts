import { Component } from '@angular/core';
import {
  CompetitionsMatchesTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-matches-tab.component';

@Component({
  selector: 'competitions-matches-tab',
  templateUrl: 'competitions-matches-tab.component.html' // TODO reuse core? (diff only at matches-market-selector-desktop)
})
export class DesktopCompetitionsMatchesTabComponent extends CompetitionsMatchesTabComponent {
  public isMarketSelectorSticky: boolean = false;
}

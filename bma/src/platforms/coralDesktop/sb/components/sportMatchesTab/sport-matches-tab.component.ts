import { Component } from '@angular/core';

import { SportMatchesTabComponent } from '@app/sb/components/sportMatchesTab/sport-matches-tab.component';

@Component({
  selector: 'sport-matches-tab',
  templateUrl: 'sport-matches-tab.component.html'
})
export class DesktopSportMatchesTabComponent extends SportMatchesTabComponent {

  filterEvents(marketFilter: string): void {
    this.selectedMarketSwitcher = this.twoUpMarkets[marketFilter];
    if (!this.activeMarketFilter || this.activeMarketFilter !== marketFilter) {
      this.initMarketSelector(marketFilter);
    }
  }
}

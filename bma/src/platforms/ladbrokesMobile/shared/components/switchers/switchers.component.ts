import { Component } from '@angular/core';
import { SwitchersComponent } from '@shared/components/switchers/switchers.component';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';

@Component({
  selector: 'switchers',
  styleUrls: ['switchers.component.scss', 'custom-switchers.component.scss'],
  templateUrl: 'switchers.component.html'
})
export class LadbrokesSwitchersComponent extends SwitchersComponent {
  trackByFilter(index: number, item: ISwitcherConfig | ITab | any): string {
    return item.viewByFilters;
  }

  /**
   * Check for 5ASide Tab
   * @param tab
   * @returns {boolean}
   */
  is5ASideTab(marketName: string): boolean {
    return marketName === '5-a-side';
  }
}

import { Component } from '@angular/core';
import {
  MatchesMarketSelectorComponent as AppMatchesMarketSelectorComponent
} from '@shared/components/marketSelector/matchesMarketSelector/matches-market-selector.component';

@Component({
  selector: 'matches-market-selector',
  styleUrls: ['./matches-market-selector.component.scss'],
  templateUrl: './matches-market-selector.component.html'
})
export class MatchesMarketSelectorComponent extends  AppMatchesMarketSelectorComponent {
  setTitle(marketFilter: string): string {
    const activeOption = this.selectOptions.find((option) => option.templateMarketName === marketFilter);
    const title = activeOption ? activeOption.title : marketFilter;
    return title;
  }
}

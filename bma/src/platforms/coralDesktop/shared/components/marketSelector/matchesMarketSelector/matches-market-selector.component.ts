import { Component } from '@angular/core';

import {
  MatchesMarketSelectorComponent as AppMatchesMarketSelectorComponent
} from '@shared/components/marketSelector/matchesMarketSelector/matches-market-selector.component';

@Component({
  selector: 'matches-market-selector-desktop',
  templateUrl: 'matches-market-selector.component.html',
  styleUrls: ['matches-market-selector.component.scss']
})

export class MatchesMarketSelectorComponent extends AppMatchesMarketSelectorComponent {}

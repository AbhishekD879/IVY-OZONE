import { Component } from '@angular/core';

import { MatchesMarketSelectorComponent } from '@shared/components/marketSelector/matchesMarketSelector/matches-market-selector.component';

@Component({
  selector: 'wrapped-market-selector',
  styleUrls: ['./wrapped-market-selector.component.scss'],
  templateUrl: './wrapped-market-selector.component.html'
})

export class WrappedMarketSelectorComponent extends MatchesMarketSelectorComponent {}

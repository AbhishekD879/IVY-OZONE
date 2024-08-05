import { Component } from '@angular/core';

import { MatchesMarketSelectorComponent } from '@shared/components/marketSelector/matchesMarketSelector/matches-market-selector.component';

@Component({
  selector: 'matches-market-custom-selector-desktop',
  templateUrl: 'matches-market-custom-selector.component.html'
})

export class DesktopMatchesMarketCustomSelectorComponent extends MatchesMarketSelectorComponent {}

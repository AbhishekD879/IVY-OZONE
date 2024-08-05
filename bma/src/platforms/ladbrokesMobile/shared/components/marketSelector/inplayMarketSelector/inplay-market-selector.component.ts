import { Component } from '@angular/core';
import { InplayMarketSelectorComponent } from '@shared/components/marketSelector/inplayMarketSelector/inplay-market-selector.component';

@Component({
  selector: 'inplay-market-selector',
  styleUrls: ['../matchesMarketSelector/matches-market-selector.component.scss'],
  templateUrl: './inplay-market-selector.component.html'
})
export class LadbrokesInplayMarketSelectorComponent extends  InplayMarketSelectorComponent {}

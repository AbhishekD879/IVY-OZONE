import { Component } from '@angular/core';

import { InplayMarketSelectorComponent } from '@shared/components/marketSelector/inplayMarketSelector/inplay-market-selector.component';

@Component({
  selector: 'inplay-market-selector-desktop',
  styleUrls: ['../wrappedMarketSelector/wrapped-market-selector.component.scss'],
  templateUrl: '../wrappedMarketSelector/wrapped-market-selector.component.html'
})
export class InplayMarketSelectorDesktopComponent extends InplayMarketSelectorComponent {}


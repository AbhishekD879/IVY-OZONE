import { Component } from '@angular/core';
import { LadbrokesRaceMarketComponent } from '@ladbrokesMobile/lazy-modules/raceMarket/race-market.component';

@Component({
  selector: 'race-market-component',
  templateUrl: './race-market.component.html',
  styleUrls: ['race-market.scss']
})
export class RaceMarketComponent extends LadbrokesRaceMarketComponent { }

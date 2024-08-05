import { Component, ViewEncapsulation } from '@angular/core';
import {
  RaceMarketComponent as MobileRaceMarketComponent
} from '@lazy-modules/raceMarket/race-market.component';

@Component({
  selector: 'race-market-component',
  templateUrl: '../../../../app/lazy-modules/raceMarket/race-market.component.html',
  styleUrls: ['race-market.scss'],
  encapsulation: ViewEncapsulation.None
})
export class RaceMarketComponent extends MobileRaceMarketComponent {
  isCoralDesktop: boolean = true;
}

import { Component } from '@angular/core';
import {
  ForecastTricastMarketComponent as CoralForecastTricastMarketComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastMarketComponent/forecast-tricast-market.component';

@Component({
  selector: 'forecast-tricast-market',
  templateUrl: './forecast-tricast-market.component.html',
  styleUrls: ['forecast-tricast-market.component.scss']
})
export class ForecastTricastMarketComponent extends CoralForecastTricastMarketComponent { }

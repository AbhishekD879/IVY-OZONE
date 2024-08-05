import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { ForcastTricastRaceCardComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastRaceCard/forecast-tricast-race-card.component';
import { ForecastTricastCheckboxMatrixComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastCheckboxMatrix/forecast-tricast-checkbox-matrix.component';
import { ForecastTricastMarketComponent
} from '@lazy-modules/forecastTricast/components/forecastTricastMarketComponent/forecast-tricast-market.component';

@NgModule({
  imports: [
    SharedModule
  ],
  providers: [],
  exports: [],
  declarations: [
    ForecastTricastCheckboxMatrixComponent,
    ForcastTricastRaceCardComponent,
    ForecastTricastMarketComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class ForecastTricastModule {
  static entry = ForecastTricastMarketComponent;
}

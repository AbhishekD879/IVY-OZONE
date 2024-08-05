import { Component } from '@angular/core';

import {
  RacingPoolIndicatorComponent
} from '@app/lazy-modules/racingFeatured/components/racingPoolIndicator/racing-pool-indicator.component';

@Component({
  selector: 'racing-pool-indicator',
  styleUrls: ['./racing-pool-indicator.component.scss'],
  templateUrl: './../../../../../../app/lazy-modules/racingFeatured/components/racingPoolIndicator/racing-pool-indicator.component.html'
})
export class LadbrokesRacingPoolIndicatorComponent extends RacingPoolIndicatorComponent {}

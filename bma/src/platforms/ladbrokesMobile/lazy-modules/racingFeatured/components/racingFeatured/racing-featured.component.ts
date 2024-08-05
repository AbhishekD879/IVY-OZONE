import { Component } from '@angular/core';

import {
  RacingFeaturedComponent as CoralRacingFeaturedComponent
} from '@app/lazy-modules/racingFeatured/components/racingFeatured/racing-featured.component';

@Component({
  selector: 'racing-featured',
  templateUrl: './racing-featured.component.html',
  styleUrls: ['./racing-featured.component.scss']
})
export class RacingFeaturedComponent extends CoralRacingFeaturedComponent {}

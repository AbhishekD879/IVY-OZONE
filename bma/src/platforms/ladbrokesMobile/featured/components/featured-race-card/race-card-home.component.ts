import { Component, ViewEncapsulation } from '@angular/core';
import { RaceCardHomeComponent } from '@ladbrokesMobile/shared/components/raceCardHome/race-card-home.component';

@Component({
  selector: 'featured-race-card-home',
  templateUrl: '../../../shared/components/raceCardHome/race-card-home.component.html',
  styleUrls: [
    '../../../../../app/lazy-modules/lazyNextRacesTab/components/raceCardHome/race-card-home.component.scss',
    '../../../shared/components/raceCardHome/race-card-home.component.scss',
  ],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class FeaturedRaceCardHomeComponent extends RaceCardHomeComponent {}

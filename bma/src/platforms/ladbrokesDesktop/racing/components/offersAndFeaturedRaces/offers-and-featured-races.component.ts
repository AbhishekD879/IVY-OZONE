import { Component, ChangeDetectionStrategy } from '@angular/core';
import { OffersAndFeaturedRacesComponent as AppOffersAndFeaturedRacesComponent
} from '@racing/components/offersAndFeaturedRaces/offers-and-featured-races.component';

@Component({
  selector: 'offers-and-featured-races',
  templateUrl: 'offers-and-featured-races.component.html',
  styleUrls: ['offers-and-featured-races.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OffersAndFeaturedRacesComponent extends AppOffersAndFeaturedRacesComponent {}


import { Component, Input } from '@angular/core';
import { OddsCardSportComponent } from '@ladbrokesDesktop/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';

@Component({
  selector: 'odds-card-favourite',
  templateUrl: 'odds-card-favourite.component.html',
  styleUrls: ['./odds-card-favourite.component.scss']
})

export class OddsCardFavouriteComponent {
  @Input() gtmModuleTitle?: string;
  @Input() oddsCard: OddsCardSportComponent;
}


import { Component, Input } from '@angular/core';
import { OddsCardSportComponent } from '@coralDesktop/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';

@Component({
  selector: 'odds-card-pre-match',
  templateUrl: 'odds-card-pre-match.component.html'
})

export class OddsCardPreMatchComponent {
  @Input() gtmModuleTitle?: string;
  @Input() oddsCard: OddsCardSportComponent;
  @Input() isFootballCoupon?: boolean;
}

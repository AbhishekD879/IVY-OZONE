import { Component, ViewEncapsulation } from '@angular/core';
import { OddsCardHeaderComponent } from '@shared/components/oddsCardHeader/odds-card-header.component';

@Component({
  selector: 'odds-card-header',
  templateUrl: 'odds-card-header.component.html',
  styleUrls: ['odds-card-header.component.scss'],
  encapsulation:ViewEncapsulation.None
  
})

export class DesktopOddsCardHeaderComponent extends OddsCardHeaderComponent {
  /**
   * Disable logic to show/hide score headers (S/G/P) (not used in Ladbrokes)
   */
  showScoreHeaders(sportId: string): void { }
}

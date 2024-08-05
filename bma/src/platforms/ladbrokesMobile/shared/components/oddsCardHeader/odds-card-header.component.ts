import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OddsCardHeaderComponent as AppOddsCardHeaderComponent } from '@shared/components/oddsCardHeader/odds-card-header.component';

@Component({
  selector: 'odds-card-header',
  templateUrl: 'odds-card-header.component.html',
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None,
})
export class OddsCardHeaderComponent extends AppOddsCardHeaderComponent implements OnInit {
  ngOnInit(): void {
    super.ngOnInit();
  }

  /**
   * Disable logic to show/hide score headers (S/G/P) (not used in Ladbrokes)
   */
  showScoreHeaders(sportId: string): void { }
}

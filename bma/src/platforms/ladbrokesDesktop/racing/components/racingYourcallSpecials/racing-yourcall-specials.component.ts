import { Component } from '@angular/core';
import { RacingYourcallSpecialsComponent } from '@racing/components/racingYourcallSpecials/racing-yourcall-specials.component';
import { IRacingYourCallMarket } from '@core/models/racing-your-call-market.model';

@Component({
  selector: 'racing-yourcall-specials',
  templateUrl: 'racing-yourcall-specials.component.html'
})
export class DesktopRacingYourcallSpecialsComponent extends RacingYourcallSpecialsComponent {
  /**
   * @param {IRacingYourCallMarket | IOutcome} items
   * @returns {IRacingYourCallMarket | IOutcome}
   */
  orderByDisplayOrder(items: IRacingYourCallMarket[]): IRacingYourCallMarket[] {
    return this.filtersService.orderBy(items, ['displayOrder']);
  }
}


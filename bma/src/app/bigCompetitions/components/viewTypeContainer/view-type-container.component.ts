import { Component, Input, OnInit } from '@angular/core';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { ICompetitionMarket } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';

@Component({
  selector: 'view-type-container',
  templateUrl: './view-type-container.html'
})
export class ViewTypeContainerComponent implements OnInit {

  _market: ICompetitionMarket;
  @Input() market;
  @Input() gtmModuleTitle?: string;

  constructor(
    private sbFiltersService: SbFiltersService
  ) { }

  ngOnInit(): void {
    if (this.market.data) {
      this._market = {...this.market};
      const market = this._market.data.markets[0];
      market.outcomes = this.sbFiltersService.orderOutcomeEntities(market.outcomes, market.isLpAvailable);
    }
  }
}

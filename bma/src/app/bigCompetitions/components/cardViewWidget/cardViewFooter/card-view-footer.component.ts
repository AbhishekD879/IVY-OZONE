import { Component, Input, OnChanges, OnInit, OnDestroy } from '@angular/core';
import * as _ from 'underscore';

import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { ISportInstance, ISportConfig } from '@app/core/services/cms/models';
import { SportsConfigService } from '@app/sb/services/sportsConfig/sports-config.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'card-view-footer',
  templateUrl: './card-view-footer.component.html',
  styleUrls: ['./card-view-footer.component.scss']
})
export class CardViewFooterComponent implements OnInit, OnChanges, OnDestroy {
  @Input() event: IBigCompetitionSportEvent;
  @Input() outcomesLength: number;
  @Input() gtmModuleTitle?: string;

  sportName: string;
  isFootball: boolean;
  marketsCount: string;
  EDPpath: string;
  market: IMarket;
  groupedOutcomes: IOutcome[];
  private sportConfig: ISportConfig;
  private headerHas2Columns: boolean;
  private headerHas3Columns: boolean;
  private sportsConfigSubscription: Subscription;

  constructor(private marketTypeService: MarketTypeService,
              private sportEventHelperService: SportEventHelperService,
              private filtersService: FiltersService,
              private sportsConfigService: SportsConfigService) {
  }

  ngOnInit(): void {
    this.headerHas2Columns = this.market && !this.marketTypeService.isMatchResultType(this.market) &&
      !this.marketTypeService.isHomeDrawAwayType(this.market);
    const categoryName = this.event.categoryName && this.event.categoryName.toLowerCase();
    this.sportsConfigSubscription = this.sportsConfigService.getSport(categoryName).subscribe((sportInstance: ISportInstance) => {
      this.sportConfig = sportInstance.sportConfig;
    });

    this.market = this.event.markets[0];
    this.groupedOutcomes = this.market ? this.getGroupedOutcomes() : [];
  }

  ngOnDestroy(): void {
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  ngOnChanges(changes): void {
    if (changes.outcomesLength) {
      this.market = this.event.markets[0];
      this.groupedOutcomes = this.market ? this.getGroupedOutcomes() : [];
    }
  }

  /**
   * Returns grouped outcomes based on correctedOutcomeMeaningMinorCode
   * @returns {IBigCompetitionSportEvent[]}
   */
  getGroupedOutcomes(): IOutcome[] {
    return _.map(this.filtersService.groupBy(this.market.outcomes, 'correctedOutcomeMeaningMinorCode'),
      value => value[0]);
  }

  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Checks if odds button wrapper should be shown
   * @param index
   * @returns {boolean}
   */
  shouldShowOddButton(index: number): boolean {
    this.headerHas3Columns = this.sportEventHelperService.isHomeDrawAwayType(this.event, this.sportConfig);
    return (((!this.headerHas2Columns || (this.headerHas2Columns && index !== 1)) &&
      this.headerHas3Columns) || (!this.headerHas3Columns && index !== 1));
  }
}



import { Component, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { RacingSpecialsTabComponent } from '@racing/components/racingSpecialsTab/racing-specials-tab.component';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { GridHelperService } from '@coralDesktop/shared/services/gridHelperService/grid-helper.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IEmptySpecialHorseOutcome } from '@coralDesktop/racing/components/racingSpecialsTab/racing-specials-tab.model';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';

@Component({
  selector: 'racing-specials-tab',
  templateUrl: 'racing-specials-tab.component.html',
  styleUrls: ['racing-specials-tab.component.scss']
})
export class DesktopRacingSpecialsTabComponent extends RacingSpecialsTabComponent implements OnInit {
  outcomeLimitNum: number;

  constructor(filterService: FiltersService,
              sbFilters: SbFiltersService,
              smartBoostsService: SmartBoostsService,
              private gridHelperService: GridHelperService,
              private window: WindowRefService) {
    super(filterService, sbFilters, smartBoostsService);
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.outcomeLimitNum = this.window.nativeWindow.innerWidth <= 1025 ? 8 : 9;
    _.each(this.eventsByType, (typeData: { typeName: string, events: ISportEvent[] }) => {
      _.each(typeData.events, (eventEntity: ISportEvent) => {
        if (eventEntity.markets[0].outcomes.length > 2) {
          this.applyGrid(eventEntity.markets[0].outcomes);
        }
      });
    });
  }

  /**
   * @param {(IOutcome | IEmptySpecialHorseOutcome)[]} outcomes
   */
  private applyGrid(outcomes: (IOutcome | IEmptySpecialHorseOutcome)[]): void {
    let rowCount: number;
    if (this.outcomeLimitNum === 9) {
      rowCount = this.gridHelperService.addCells(3, outcomes.length);
    } else {
      rowCount = this.gridHelperService.addCells(2, outcomes.length);
    }
    for (let i = 0; rowCount > i; i++) {
      outcomes.push({
        name: ' ',
        prices: [],
        runnerNumber: '99999',
        displayOrder: '9999999',
        outcomeMeaningMinorCode: '2',
        type: {
          grid: this.outcomeLimitNum === 9 ? '3' : '2'
        }
      });

    }
  }
}

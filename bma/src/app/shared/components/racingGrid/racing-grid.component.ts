import { Component, OnInit, Input} from '@angular/core';

import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { greyhoundConfig } from '@core/services/racing/config/greyhound.config';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';

@Component({
  selector: 'racing-grid',
  templateUrl: 'racing-grid.component.html',
})
export class RacingGridComponent implements OnInit {
  // ToDo: @Sanzharevskiy ToDo type when raceService is migrated

  @Input() raceGridRaces: { data: any; };
  @Input() sportId: string;

  sportName: string;
  racing: any;
  eventsOrder: any;

  constructor(
    private horseracing: HorseracingService,
    private greyhound: GreyhoundService
  ) { }

  ngOnInit(): void {
    let sportConfig;
    let racing;
    const isHorseRacing = this.sportId === horseracingConfig.config.request.categoryId;
    const isGrayHound = !isHorseRacing && this.sportId === greyhoundConfig.config.request.categoryId;
    const sportDefined = isHorseRacing || isGrayHound;

    if (isHorseRacing) {
      sportConfig = horseracingConfig;
      racing = this.horseracing;
    } else if (isGrayHound) {
      sportConfig = greyhoundConfig;
      racing = this.greyhound;
    }


    if (sportConfig) {
      this.sportName = sportConfig.config.name;

      // Events ordering
      this.eventsOrder = sportConfig.order.EVENTS_ORDER;
    }

    if (sportDefined && (!this.raceGridRaces || !this.raceGridRaces.data)) {
      racing.getByTab('today', true).then(result => {
        this.racing = result;
        racing.addFirstActiveEventProp(this.racing);
        this.raceGridRaces.data = result;
      });
    } else if (sportDefined) {
      this.racing = this.raceGridRaces.data;
    }
  }

  /***
   * Group Races
   * @param group
   * @returns {boolean}
   */
  isRaceGridGroup(group): boolean {
    return this.raceGridRaces.data.classesTypeNames[group.flag].length > 0 &&
      (group.flag !== 'VR' && group.flag !== 'ALL');
  }

  trackByGroupedRacing(i: number, racingGrid) {
    return `${i}_${racingGrid.data.map(r => r.id).join('|')}`;
  }
}

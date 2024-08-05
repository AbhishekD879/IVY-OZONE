import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { RacingSpecialsTabComponent } from '@racing/components/racingSpecialsTab/racing-specials-tab.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';

interface IGroupEvent extends ISportEvent {
  isExpandedEvent?: boolean;
  link: string;
}

@Component({
  selector: 'racing-specials-tab',
  templateUrl: 'racing-specials-tab.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class LadbrokesMobileRacingSpecialsTabComponent extends RacingSpecialsTabComponent implements OnInit {
  eventsByType: Array<{typeName: string; events: IGroupEvent[]}> = [];

  constructor(filterService: FiltersService,
              sbFilters: SbFiltersService,
              smartBoostsService: SmartBoostsService,
              private routingHelperService: RoutingHelperService) {
    super(filterService, sbFilters, smartBoostsService);
  }

  ngOnInit(): void {
    super.ngOnInit();
    if (this.eventsByType.length) {
      this.eventsByType.forEach((eventsGroup) => {
        eventsGroup['isExpandedGroup'] = false;
      });
      this.eventsByType[0]['isExpandedGroup'] = true;
      this.racing.events.forEach((eventEntity: IGroupEvent) => {
        eventEntity.link = this.formEdpUrl(eventEntity);
      });
    }
  }

  /**
   * Forms event details page or sport results page based on event's "isResulted" property.
   * @param {Object} eventEntity
   * @return {string}
   */
  formEdpUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(eventEntity);
  }
}

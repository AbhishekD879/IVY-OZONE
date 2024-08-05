import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';

@Component({
  selector: 'daily-racing-module',
  templateUrl: 'daily-racing.component.html'
})
export class DailyRacingModuleComponent implements OnInit {
  @Input() eventsBySections: {[key: string]: ISportEvent[]};
  @Input() collapsedSections?: {[key: string]: ISportEvent[]};
  @Input() sportName: string;
  @Input() isRacingFeatured? :boolean;

  filteredEventsBySection: {sectionName: string; events: ISportEvent[]}[];
  bannerBeforeAccorditionHeader: string= '';
  targetTab: ISportConfigTab | null = null;

  constructor(
    private routingHelperService: RoutingHelperService,
    private filterService: FiltersService,
    private vEPService : VirtualEntryPointsService) {}

  ngOnInit(): void {
    this.filteredEventsBySection = _.map(this.eventsBySections, (val: ISportEvent[], key: string) => {
      return { sectionName: key, events: this.filterService.orderBy(val, ['startTime', 'name'])};
    });

    this.vEPService.bannerBeforeAccorditionHeader.subscribe((header: string) => {
      this.bannerBeforeAccorditionHeader = header;
    });
  
    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });
  }

  formEdpUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(eventEntity);
  }

  trackByIndex(index: number): number {
    return index;
  }

  isDisplayBanner(name) {
    return this.bannerBeforeAccorditionHeader?.toLowerCase() === name?.toLowerCase();
  }

}

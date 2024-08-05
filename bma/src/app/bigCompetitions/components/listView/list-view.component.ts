import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { ISportEvent } from '@core/models/sport-event.model';
import { ISportConfig } from '@core/services/cms/models';

@Component({
  selector: 'list-view',
  templateUrl: 'list-view.component.html'
})
export class ListViewComponent implements OnInit {

  @Input() events: ISportEvent[];
  @Input() maxDisplay: number;
  @Input() gtmModuleTitle?: string;
  @Input() sportConfig?: ISportConfig;
  @Input() deviceType?:string;

  selectedMarket: string;
  limit: number;

  ngOnInit(): void {
    this.limit = this.maxDisplay;
  }

  /**
   * Load next events(regarding to maxDisplay configuration)
   */
  loadChunk(): void {
    this.limit = this.limit + this.maxDisplay;
  }

  /**
   * Track by id
   * @param index
   * @param event
   */
  trackById(index: number, event: ISportEvent): string {
    return `${index}${event.id}`;
  }

  /**
   * Hide/show "Show next" button
   */
  hideShowNext(): boolean {
    return this.limit >= this.events.length;
  }

  /**
   * Get primary template market name
   * @param events
   * @returns {string}
   * @private
   */
  private getPrimaryMarketName(events: ISportEvent[]): string {
    return _.chain(events)
      .map(e => e.markets && e.markets[0])
      .pluck('templateMarketName')
      .first()
      .value();
  }
}

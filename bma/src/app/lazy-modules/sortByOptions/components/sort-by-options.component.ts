import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SortByOptionsService } from '@racing/services/sortByOptions/sort-by-options.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'sort-by-options',
  templateUrl: './sort-by-options.component.html',
  styleUrls: ['./sort-by-options.component.scss']
})
export class SortByOptionsComponent implements OnInit, OnDestroy {
  @Input() sortBy: string;
  @Input() eventEntityId: string;

  showSortBy: boolean = false;
  sortByOptions: string[] = ['Price', 'Racecard'];
  private name: string = _.uniqueId('SortByOptionsComponent');

  constructor(
    private pubSubService: PubSubService,
    private sortByOptionsService: SortByOptionsService,
    private gtmService: GtmService
  ) {
  }

  ngOnInit(): void {
    this.pubSubService.subscribe(this.name, this.pubSubService.API.CLOSE_SORT_BY, () => this.showDropdown(false));
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.name);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  indexNumber(index: number): number {
    return index;
  }

  /**
   * Apply sorting by pubsub
   * @param {string} option
   */
  selectSortByOption(option: string): void {
    if (this.sortBy !== option) {
      this.sortBy = option;
      this.sortByOptionsService.set(option);
      this.pubSubService.publish(`${this.pubSubService.API.SORT_BY_OPTION}${this.eventEntityId || ''}`, option);
    }
  }

  /**
   * Open/Close dropdown.
   * @param {boolean} show
   */
  showDropdown(show: boolean): void {
    this.showSortBy = show;
  }
}

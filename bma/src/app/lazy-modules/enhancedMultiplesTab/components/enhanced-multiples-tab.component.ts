import { Component, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { FiltersService } from '@core/services/filters/filters.service';
import { EnhancedMultiplesService } from '@sb/services/enhancedMultiples/enhanced-multiples.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { ICategory } from '@core/models/category.model';

@Component({
  selector: 'enhanced-multiples-tab',
  templateUrl: 'enhanced-multiples-tab.component.html'
})
export class EnhancedMultiplesTabComponent implements OnInit {
  eventsSortOrder: string[] = ['startTime', 'markets[0].outcomes[0].name'];
  showLoader: boolean = true;
  ssDown: boolean;
  eventsCategories: ICategory[];

  constructor(
    private enhancedMultiplesService: EnhancedMultiplesService,
    private filterSerice: FiltersService
  ) {}

  ngOnInit(): void {
    this.getAllEnhancedMultiplesEvents();
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * check for event presence
   * @return {boolean}
   */
  isNoEvents(): boolean {
    return (!this.eventsCategories || !this.eventsCategories.length) && !this.showLoader && !this.ssDown;
  }

  /**
   * Chec for request error to show error message
   * @return {boolean}
   */
  isRequestError(): boolean {
    return this.ssDown && !this.showLoader;
  }

  /**
   * Reload current directive data
   */
  reloadComponent(): void {
    this.showLoader = true;
    this.ssDown = false;
    this.getAllEnhancedMultiplesEvents();
  }

  /**
   * Load new or cached enhansed events categories
   */
  getAllEnhancedMultiplesEvents(): void {
    this.enhancedMultiplesService.getAllEnhancedMultiplesEvents()
      .subscribe(eventsCategories => {
        this.eventsLoaded(eventsCategories);
      },
      () => {
        this.showLoader = false;
        this.ssDown = true;
      });
  }

  protected eventsLoaded(eventsCategories: ICategory[]): void {
    this.showLoader = false;
    this.eventsCategories = this.sortCategoriesAndEvents(eventsCategories);
  }

  /**
   * Reorder categories and thier events.
   * @param {ICategory[]} categories
   * @return {ICategory[]}
   */
  private sortCategoriesAndEvents(categories: ICategory[]): ICategory[] {
    const reOrderedCategories = _.sortBy(categories, 'displayOrder');

    _.each(reOrderedCategories, category => {
      category.events = this.reOrderEvents(category.events);
    });

    return reOrderedCategories;
  }

  /**
   * reorder events list
   * @param {ISportEvent[]} events
   * @return {ISportEvent[]}
   */
  private reOrderEvents(events: ISportEvent[]): ISportEvent[] {
    return this.filterSerice.orderBy(events, this.eventsSortOrder).filter(event => {
      return event.markets[0].outcomes.length > 0;
    });
  }
}

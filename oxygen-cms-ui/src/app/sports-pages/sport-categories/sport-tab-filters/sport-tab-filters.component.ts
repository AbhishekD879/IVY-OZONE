import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import {
  SPORT_TAB_FILTERS_CONFIG,
  SPORT_TAB_LEAGUE_FILTER,
  SPORT_TAB_TIME_FILTER
} from '@app/sports-pages/sport-categories/sport-tab-filters/sport-tab-filters.config';
import {
  SportTabFilterInstance, SportTabFilters,
  SportTabLeagueFilterValue
} from '@app/client/private/models/sporttabFilters.model';
import { LeagueFilterCreateComponent } from "@app/sports-pages/sport-categories/league-filter-create/league-filter-create.component";
import { AppConstants } from "@app/app.constants";
import { DialogService } from "@app/shared/dialog/dialog.service";
import * as _ from "lodash";
import { LeagueFilterEditComponent } from "@app/sports-pages/sport-categories/league-filter-edit/league-filter-edit.component";

@Component({
  selector: 'sport-tab-filters',
  templateUrl: './sport-tab-filters.component.html',
  styleUrls: ['./sport-tab-filters.component.scss']
})
export class SportTabFiltersComponent implements OnChanges {
  @Input() sportTabFilters: SportTabFilters = {};

  filtersList: SportTabFilterInstance<any>[] = [];
  searchField: string = '';

  readonly timeFilterName = SPORT_TAB_TIME_FILTER;
  readonly leagueFilterName = SPORT_TAB_LEAGUE_FILTER;
  private readonly filtersConfig = SPORT_TAB_FILTERS_CONFIG;

  constructor(
    private dialogService: DialogService,
  ) { }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.sportTabFilters && changes.sportTabFilters.currentValue) { this.createFiltersList(); }
  }

  trackByName<T>(index: number, filter: SportTabFilterInstance<T>): string {
    return filter.name;
  }

  toggleFilter<T>(checked: boolean, filter: SportTabFilterInstance<T>): void {
    filter.data.enabled = checked;
  }

  updateFilter<T>(values: T[], filter: SportTabFilterInstance<T>): void {
    filter.data.values = values;
  }
  editFilter(filterItem: SportTabLeagueFilterValue): void {
    this.dialogService.showCustomDialog(LeagueFilterEditComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New League Filter',
      data: _.cloneDeep(filterItem),
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (updatedItem: SportTabLeagueFilterValue): void => {
        filterItem.leagueName = updatedItem.leagueName;
        filterItem.leagueIds = updatedItem.leagueIds;
      }
    });
  }

  public removeLeagueHandler(filterItem: SportTabLeagueFilterValue, leagueFilter: SportTabFilterInstance<SportTabLeagueFilterValue>): void {
    const notificationMessage = 'Are You Sure You Want to Remove Filter ?';
    this.dialogService.showConfirmDialog({
      title: 'Remove',
      message: notificationMessage,
      yesCallback: (): void => {
        const index = leagueFilter.data.values.indexOf(filterItem);
        leagueFilter.data.values.splice(index, 1);
      }
    });
  }

  public createLeagueFilter(leagueFilter: SportTabFilterInstance<SportTabLeagueFilterValue>): void {
    this.dialogService.showCustomDialog(LeagueFilterCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New League Filter',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (filterItem: SportTabLeagueFilterValue): void => {
        leagueFilter.data.values.push(filterItem);
      }
    });
  }

  private createFiltersList(): void {
    this.filtersList = [];
    Object.keys(this.sportTabFilters).forEach((filterName: string) => {
      this.filtersList.push({
        name: filterName,
        data: this.sportTabFilters[filterName],
        params: this.filtersConfig[filterName].params || {}
      });
    });
  }
}

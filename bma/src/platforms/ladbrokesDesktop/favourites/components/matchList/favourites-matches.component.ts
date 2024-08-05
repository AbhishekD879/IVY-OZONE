import { Component } from '@angular/core';
import * as _ from 'underscore';

import { FavouritesMatchesComponent } from '@app/favourites/components/matchList/favourites-matches.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'favourites-matches',
  templateUrl: './favourites-matches.component.html'
})
export class DesktopFavouritesMatchesComponent extends FavouritesMatchesComponent {
  FAVOURITES_LIMIT = 3;
  isShowAll = false;
  filteredMatches: ISportEvent[] = [];

  init(): Observable<void> {
    return super.init()
      .pipe(map(() => {
        this.filteredMatches = this.getFavourites();
      }));
  }

  orderMatches(): void {
    super.orderMatches();
    this.filteredMatches = this.getFavourites();
  }

  /**
   * Returns sorted favourites
   */
  getFavourites(): ISportEvent[] {
    const sortedMatches = _.sortBy(this.matches, (match: ISportEvent) => match.startTime);
    return this.isShowAll ? sortedMatches : _.first(sortedMatches, this.FAVOURITES_LIMIT);
  }
  /**
   * Toggle show all button
   */
  toggleShowAllButton(): void {
    this.isShowAll = !this.isShowAll;
    this.filteredMatches = this.getFavourites();
  }

  /**
   * Check if show more button should be shown
   * @returns {boolean}
   */
  get isShowAllButtonShown(): boolean {
    return this.showHeader && this.isUserLoggedIn && this.matches && this.matches.length > this.FAVOURITES_LIMIT;
  }
  set isShowAllButtonShown(value:boolean){}
  /**
   * Check if text when no mathes were selected should be shown.
   * @returns {boolean}
   */
  get isNoMatchesTextShown(): boolean {
    return !this.showHeader && this.isUserLoggedIn && !this.state.loading;
  }
  set isNoMatchesTextShown(value:boolean){}
}

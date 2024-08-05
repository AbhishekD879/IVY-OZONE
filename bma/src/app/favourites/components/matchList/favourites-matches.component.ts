import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { from, Subscription, Observable, throwError } from 'rxjs';
import { switchMap, catchError, map } from 'rxjs/operators';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';

import { IFavouritesText } from '@app/favourites/models/favourites-config.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { FavouritesMatchesService } from '@app/favourites/services/favourites-matches.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMatch } from '@sb/components/matchResultsSportTab/match.model';

@Component({
  selector: 'favourites-matches',
  templateUrl: './favourites-matches.component.html'
})
export class FavouritesMatchesComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() bsTab?: boolean;
  @Input() widget: string;
  @Input() isWidgetColumn: string;

  isUserLoggedIn: boolean;
  matches = [];
  introductoryText: string = '';
  loginButtonText: string = '';

  isBsTab: string;
  title: string;
  applyingParams: boolean = true;
  displayPageHeader: boolean;
  timeOutListener: number;

  private getFavouritesSubscription: Subscription;

  constructor(
    private favouritesService: FavouritesService,
    private userService: UserService,
    private pubSubService: PubSubService,
    private favouritesMatchesService: FavouritesMatchesService,
    private filtersService: FiltersService
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit () {
    this.isUserLoggedIn = !!this.userService.username;
    this.isBsTab = this.bsTab ? 'bs' : '';
    this.title = `favouritesMatches${this.isBsTab}${this.isWidgetColumn || ''}`;
    this.displayPageHeader = !this.bsTab && !this.widget;

    this.addEventListeners();
    this.getFavouritesSubscription = this.init().subscribe();
  }

  ngOnDestroy(): void {
    this.getFavouritesSubscription && this.getFavouritesSubscription.unsubscribe();
    this.pubSubService.unsubscribe(this.title);
    this.favouritesMatchesService.unSubscribeForUpdates(this.widget, this.bsTab);
  }

  trackById(index: number, event: ISportEvent): number {
    return event.id;
  }

  /**
   * addEventListeners()
   */
  addEventListeners(): void {
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SET_ODDS_FORMAT, () => {
      this.getFavouritesSubscription = this.init().subscribe();
    });
    this.pubSubService.subscribe(this.title, this.pubSubService.API.EVENT_ADDED, () => {
      this.applyingParams = true;
      this.getFavouritesSubscription = this.init().subscribe();
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.EVENT_REMOVED, (matchId: number) => {
      this.removeEvent(matchId);
    });

    this.pubSubService.subscribe(this.title, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, (matchId: number) => {
      if (this.matches && this.matches.length) {
        const match: ISportEvent = this.matches.find((el: ISportEvent) => el.id === matchId);
        if (match) {
          const sportName: string = match.categoryName.toLowerCase();
          this.favouritesService.add(match, sportName, {}); // remove match from Local Storage
        }
      }
    });

    this.pubSubService.subscribe(
        this.title,
        [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGOUT, this.pubSubService.API.SESSION_LOGIN],
        () => {
          this.isUserLoggedIn = this.favouritesService.isUserLoggedIn();
          this.getFavouritesSubscription = this.init().subscribe();
        }
    );
  }

  /**
   * showHeader()
   * @returns {boolean}
   */
  get showHeader(): boolean {
    return this.isFavourite(this.matches);
  }
  set showHeader(value:boolean){}
  /**
   * removeMatch()
   * @param {number} eventId
   */
  removeEvent(eventId: number) {
    this.applyingParams = true;
    this.matches = this.favouritesMatchesService.removeMatch(this.matches, eventId);
    this.orderMatches();
    this.applyingParams = false;
    this.updateData();
  }

  /**
   * updateData()
   */
  updateData(): void {
    this.matches = this.favouritesMatchesService.trimFinishedEvents(this.matches);
  }

  /**
   * logIn()
   */
  logIn(): void {
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, {
      moduleName: `favourites${this.widget ? 'widget' : ''}`
    });
  }

  /**
   * Remove all favourites events
   */
  removeAllFavourites(): void {
    _.forEach(this.matches, event => {
      // @ts-ignore
      this.favouritesService.add(event, event.categoryCode.toLowerCase());
    });
  }

  /**
   * init()
   * @returns {Observable<void>}
   */
  init(): Observable<void> {
    if (this.isUserLoggedIn) {
      return this.favouritesService.getFavourites('football').pipe(
        switchMap((data: IMatch[]) => from(this.favouritesMatchesService.getFavouritesMatches(this.title, data))),
        map((data: ISportEvent[]) => {
          this.matches = data;
          if (data.length) {
            this.favouritesMatchesService.subscribeForUpdates(this.matches, this.widget, this.bsTab);
            this.orderMatches();
          }
          this.applyingParams = false;
          this.hideSpinner();
          this.hideError();
        }),
        catchError(err => {
          this.showError();
          this.applyingParams = false;
          this.hideSpinner();
          return throwError(err);
        })
      );
    } else {
      return this.favouritesService.getFavoritesText().pipe(
        map((cmsData: IFavouritesText) => {
          this.introductoryText = cmsData.introductoryText;
          this.loginButtonText = cmsData.loginButtonText;
          this.applyingParams = false;
        }),
        catchError(err => {
          this.applyingParams = false;
          return throwError(err);
        })
      );
    }
  }

  /**
   * orderMatches()
   */
  orderMatches(): void {
    this.matches = this.filtersService.orderBy(this.matches, ['startTime']);
  }

  isFavourite(events: ISportEvent[]): boolean {
    const ids = this.favouritesService.getFavouritesEventsIds('football');
    return events.filter((event: ISportEvent) => {
      return ids.includes(event.id) && !event.isFinished && event.isDisplayed;
    }).length > 0;
  }
}

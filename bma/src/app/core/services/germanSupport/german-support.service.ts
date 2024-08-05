import { Injectable } from '@angular/core';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { Router, NavigationEnd, Event } from '@angular/router';
import { LocaleService } from '../locale/locale.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { ISportCategory } from '../cms/models';
import { ICategory } from '@core/models/category.model';
import { Subscription } from 'rxjs';
import { ISportEvent } from '../../models/sport-event.model';

@Injectable()
export class GermanSupportService {

  public restrictedSportsCategoriesIds = ['19', '21', '161']; // 19 - GH, 21 - HR, 161 - INT TOTE
  private restrictedSportNames: Array<string> = ['racing', 'lotto', 'tote', 'jackpot'];
  private routeListener: Subscription;

  constructor(
    private userService: UserService,
    private storageService: StorageService,
    private router: Router,
    private localeService: LocaleService,
    private infoDialogService: InfoDialogService
  ) {}

  isGermanUser(): boolean {
    return this.userService.countryCode === 'DE' || this.storageService.get('countryCode') === 'DE';
  }

  /**
   * Check if sport is restricted for german user
   * @param {ISportCategory} item
   * @returns {boolean}
   */
  isRestrictedSport(item: ISportCategory ): boolean {
    if (item.sportName  && this.isGermanUser()) {
      const result = this.restrictedSportNames.filter(name => item.sportName.includes(name));
      return result.length > 0;
    }
    return false;
  }

  filterNextRaces(menuItems) {
    return menuItems.filter((item) => !item.directiveName.includes('NextRaces'));
  }

  filterRestrictedSports(menuItems) {
    return menuItems.filter((item) => {
      if (item.sportName) {
        return !(item.sportName.includes('racing') ||
                  item.sportName.includes('lotto')  ||
                  item.sportName.includes('tote')  ||
                  item.sportName.includes('jackpot'));
      }
    });
  }

  filterEnhancedCategories(categories: ICategory[]): ICategory[] {
    return categories.filter((category: ICategory) => !this.restrictedSportsCategoriesIds.includes(`${category.id}`));
  }

  filterEnhancedOutcomes(events: ISportEvent[]): ISportEvent[] {
    return events.filter((event: ISportEvent) => !this.restrictedSportsCategoriesIds.includes(event.categoryId));
  }

  toggleItemsList(menuItems, action) {
    const items = menuItems;
    if (this.isGermanUser()) {
      switch (action) {
        case 'filterNextRaces':
          return this.filterNextRaces(items);
        case 'filterRestrictedSports':
          return this.filterRestrictedSports(items);
      }
    } else {
      return menuItems;
    }
  }

  redirectToMainPage(): void {
    if (this.userService.countryCode === 'DE') {
      this.router.navigate(['/']);
    }
  }

  /**
   * Workaround to fix - https://jira.egalacoral.com/browse/BMA-51919
   * After Login - the vanilla forcibly change the route to the one (same!) that was used when
   * user started to login. This couse redirect back to initial page after login. This code
   * is here: coralsports/node_modules/@frontend/vanilla/fesm5/vanilla-core-core.js:3596
   * This workaround will wait when this redirect back is done and start his own navigation to the Home page.
   */
  redirectToMainPageOnLogin(): void {
    const currentUrl = this.router.url;
    let navigationEndEventsCount = 0;
    this.routeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        navigationEndEventsCount++;
        if (navigationEndEventsCount === 1 && (event.url === currentUrl && event.urlAfterRedirects === currentUrl)) {
          this.routeListener.unsubscribe();
          this.redirectToMainPage();
        }
      }
    });
  }

  showDialog(message: string): void {
    this.infoDialogService.openInfoDialog(
      this.localeService.getString('bma.countryRestriction.header'),
      message,
      undefined,
      undefined,
      undefined,
      [{
        caption: 'OK',
        cssClass: 'btn-style2 okButton'
      }]
    );
  }
}

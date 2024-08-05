import { Injectable } from '@angular/core';
import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { StorageService } from '@app/core/services/storage/storage.service';

@Injectable({providedIn: 'root'})
export class MarketSelectorStorageService {
  marketSelectorSport: string = 'football';
  selectorStoredData: { [key: string]: { selectedOption: string } } = {};
  removeRouteChangeListener: Subscription;
  sportNameByParam: string;
  sportNameFlag: boolean = false;
  private isListenForClean: boolean = false;
  sportsList: ISystemConfig;
  sportName: string;
  allSportsList: string[];
  constructor(
    private storage: StorageService,
    private router: Router,
    private route: ActivatedRoute,
    private routingState: RoutingState,
    private cmsService: CmsService
  ) {
    this.cmsService.getSystemConfig()
    .subscribe((config: ISystemConfig) => {
      this.sportName = this.getSportsName();
      this.sportNameFlag = config['MarketSwitcher'][this.sportName];
      this.sportsList = Object.keys(config['MarketSwitcher']);
      this.allSportsList = config['MarketSwitcher'];
      for(const sportNameIndex in this.allSportsList) {
        if (this.allSportsList.hasOwnProperty(sportNameIndex)) {
          if(this.allSportsList[sportNameIndex]) {
            this.sportsList.push(sportNameIndex);
          }
        }
      }
    });
    this.checkRouteForCleanUpData();
  }
  getSportsName() {
    return (this.routingState.getRouteParam('sport', this.route.snapshot)?.replace(/-/g, ""));
  }
  /**
   * Save selected option
   * @param sportName
   * @param optionValue
   */
  storeSelectedOption(sportName: string, optionValue: string): void {
    this.selectorStoredData[sportName] = {
      selectedOption: optionValue
    };
    this.storage.set('storeSelectedOption', this.selectorStoredData);
    this.addCleanUpListener();
  }

  /**
   * restore data to set active option
   * @param sportName
   * @returns {String}
   */
   restoreSelectedOption(sportName: string): string {
    let option = this.storage.get('storeSelectedOption');
    if(option){
    option =  option[sportName] ? option[sportName].selectedOption : '';
    }
    return option || '';
  }

  /**
   * URL validation for cleaning data.
   */
  private isValidFootballLocation(): boolean {
   if(this.sportNameFlag) {
    let previousUrl: string;
     if(this.routingState.getPreviousUrl()) {
     previousUrl = (this.routingState.getPreviousUrl().replace(/-/g, ""));
     }
      const selectedTab = this.routingState.getPathName();
      const selectedTabOptionsArr = ['today', 'live', 'competitions', 'coupons', 'matches'];
      const tabRouteparam = this.routingState.getRouteParam('tab', this.route.snapshot);
      const tabRouteparamOptionsArr = ['today', 'tomorrow', 'future'];
      this.sportNameByParam = this.getSportsName();
      if(previousUrl.includes('/event/'+ this.sportNameByParam)) {
        return true;
      }

      if(this.sportsList.includes(this.sportNameByParam) &&
      previousUrl.includes('/sport/'+ this.sportNameByParam) && selectedTabOptionsArr.includes(selectedTab)) {
        return false;
      }

      if(this.sportsList.includes(this.getSportsName())) {
        return true;
      } else {
        return tabRouteparamOptionsArr.includes(tabRouteparam);
      }
   }
  }

  /**
   * Clean up stored data if user navigates to different page
   */
  private cleanUpStoredData(): void {
    this.storage.remove('storeSelectedOption');
  }

  /**
   * Check page for cleaning up stored data
   */
  private checkRouteForCleanUpData(): void {
    if (!this.isValidFootballLocation()) {
      this.cleanUpStoredData();
      this.removeCleanUpListener();
    }
  }

  /**
   * Start listen user navigation
   */
  private addCleanUpListener(): void {
    if (!this.isListenForClean) {
      this.isListenForClean = true;
      this.removeRouteChangeListener = this.router.events.subscribe((event: Event) => {
        if (event instanceof NavigationEnd) {
          this.checkRouteForCleanUpData();
        }
      });
    }
  }

  /**
   * remove navigation listener after deleting stored data
   */
  private removeCleanUpListener(): void {
    if (this.isListenForClean) {
      this.isListenForClean = false;
      this.removeRouteChangeListener.unsubscribe();
    }
  }
}

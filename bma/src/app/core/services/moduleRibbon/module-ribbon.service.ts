import { Injectable } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { PrivateMarketsService } from '@core/services/privateMarkets/private-markets.service';
import { DeviceService } from '@core/services/device/device.service';
import { LocaleService } from '@core/services/locale/locale.service';

import { IModuleRibbonTab } from '@core/services/cms/models';
import { ISportEvent } from '@core/models/sport-event.model';
import { Observable, of } from 'rxjs';
import { catchError, mergeMap } from 'rxjs/operators';

@Injectable()
export class ModuleRibbonService {

  moduleList: Partial<IModuleRibbonTab>[] = [];

  private readonly privateMarketNamespace: string = 'ModuleRibbonService';
  private readonly pmURL: string = '/home/private-markets'; // Private Markets URL;
  private readonly privateMarketsName: string = 'PrivateMarkets';
  private readonly privateMarket: Partial<IModuleRibbonTab>;

  constructor(
    private location: Location,
    private device: DeviceService,
    private pubSubService: PubSubService,
    private locale: LocaleService,
    private privateMarketsService: PrivateMarketsService,
    private router: Router
  ) {
    this.privateMarket = {
      directiveName: this.privateMarketsName,
      title: this.locale.getString('sb.yourEnhanceMarkets'),
      visible: true,
      modules: [],
      showTabOn: 'both',
      url: this.pmURL,
      id: 'tab-private-markets'
    };
  }

  get privateMarketsUrl(): string {
    return this.pmURL;
  }
  set privateMarketsUrl(value:string){}

  /**
   * Remove Private Market Tab
   */
  removeTab(): void {
    if (this.isPrivateMarketsTab()) {
      this.moduleList.shift();
      this.pubSubService.unsubscribe(this.privateMarketNamespace);
    }

    if (this.location.isCurrentPathEqualTo(this.pmURL)) {
      this.router.navigate(['/']);
    }
  }

  /**
   * Get Private Market Tab
   */
  getPrivateMarketTab(modules: IModuleRibbonTab[]): Observable<Partial<IModuleRibbonTab>[]> {
    this.moduleList = this.filterTabs(modules);
    return this.privateMarketsService.markets().pipe(
      mergeMap((events: ISportEvent[]) => {
        if (this.isPrivateMarketsAvailable(events)) {
          this.addTab(events);
        } else if (this.location.isCurrentPathEqualTo(this.pmURL)) {
          this.router.navigate(['/']);
        }
        return of(this.moduleList);
      }),
      catchError(() => of(this.moduleList))
    );
  }

  /**
   * Filter Module List
   */
  filterTabs(modules: IModuleRibbonTab[]): Partial<IModuleRibbonTab>[] {
    const moduleList = modules.slice(0, -1); // remove object of event/EM/outcome/type ids
    _.each(moduleList, module => {
      if (module.url && _.isString(module.url)) {
        module.url = module.url.replace('#/', '/');
      }
    });
    this.moduleList = _.filter(moduleList, item => {
      return (this.device.isDesktop && item.showTabOn === 'desktop') ||
        (!this.device.isDesktop && item.showTabOn === 'mobtablet') ||
        (item.showTabOn === 'both');
    });
    return this.moduleList;
  }

  isPrivateMarketsTab(): boolean {
    return this.moduleList && this.moduleList[0] && this.moduleList[0].directiveName === this.privateMarketsName;
  }

  /**
   * Add Private Market Tab
   */
  private addTab(events: ISportEvent[]): void {
    if (this.moduleList && this.moduleList.length) {
      this.moduleList.unshift(this.privateMarket);

      this.pubSubService.subscribe(this.privateMarketNamespace,
        [this.pubSubService.API.SESSION_LOGOUT, this.pubSubService.API.HIDE_PRIVATE_MARKETS_TAB], () => {
          this.removeTab();
        });
    }
  }

  /**
   * Check if PrivateMarkets is not already in moduleList and
   * at least one event with one market outcome is present
   * @returns {boolean}
   */
  private isPrivateMarketsAvailable(events: ISportEvent[]): boolean {
    return !this.isPrivateMarketsTab() &&
      events && events.length && events.some(e => e.markets.some(m => m.outcomes.length > 0));
  }
}

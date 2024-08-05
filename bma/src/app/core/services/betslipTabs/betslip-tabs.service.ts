import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { DeviceService } from '../device/device.service';
import { IBetslipTab } from './betslip-tab.model';
import { tabsLinks } from './tabs-links.constant';
import { LocaleService } from '@core/services/locale/locale.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Observable } from 'rxjs';
import * as _ from 'underscore';

@Injectable()
export class BetslipTabsService {

  constructor(private locale: LocaleService,
              private pubsub: PubSubService,
              private device: DeviceService,
              private cmsService: CmsService) {
  }

  /**
   * @param {string} tabName
   * @param {string} id
   * @param {string} url
   * @return {IBetslipTab}
   */
  createTab(tabName: string, id: number, url: string = ''): IBetslipTab {
    const tabTranslation: string = this.locale.getString(`app.betslipTabs.${tabName}`);

    return {
      title: tabTranslation,
      name: tabTranslation,
      id: id,
      url: url
    };
  }

  /**
   * Gets number or nothing and return layout data for betslip tabs
   * Return tabs layout model
   * @return {Observable<IBetslipTab[]>}
   */
  getTabsList(): Observable<IBetslipTab[]> {
    let defaultTabs = [
      this.createTab('betslip', 0, '/betslip'),
      this.createTab('cashout', 1, '/cashout'),
      this.createTab('openbets', 2, '/open-bets'),
      this.createTab('betHistory', 3, '/bet-history'),
    ];

    return this.cmsService.getSystemConfig().pipe(map((data) => {
      if (data.CashOut && !data.CashOut.isCashOutTabEnabled) {
        defaultTabs = _.without(defaultTabs, _.findWhere(defaultTabs, { url: '/cashout' }));
      }
      /*
      inshop tab has been moved from mybets tab to open and settled tabs in ladbrokes.
      shopBetHistory field is always false for ladbrokes.
      configured inShopBets field to display in open and settled bets.
      */
      if (data.Connect && data.Connect.shopBetHistory) { // TODO: rename to retail after changes in cms.
        return [...defaultTabs, this.createTab('inShopBets', 4, '/in-shop-bets')];
      } else {
        return defaultTabs;
      }
    }));
  }

  /**
   * Triggers pubsub publish event when conditions are met and returns name of the link
   * @param {string} link
   * @param {boolean} shouldPublishEvent
   * @return {string | null}
   */
  redirectToBetSlipTab(link: string, shouldPublishEvent?: boolean): string | null {
    const tabLink = tabsLinks[link.toUpperCase()];
    if (shouldPublishEvent && tabLink && !this.device.isMobile) {
      this.pubsub.publish(tabLink);
    }

    return tabLink ? link : null;
  }
}

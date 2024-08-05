import { Component } from '@angular/core';
import { BetHistoryPageComponent } from '@app/betHistory/components/betHistoryPage/bet-history-page.component';
import { IBetHistorySwitcherConfig } from '@app/betHistory/models/bet-history-switcher-config.model';
import { BET_HISTORY_CONFIG } from '@betHistoryModule/constants/bet-promotions.constant';
import { ISystemConfig } from '@core/services/cms/models';

@Component({
  selector: 'bet-history-page',
  templateUrl: 'bet-history-page.component.html',
  styleUrls: ['./bet-history-page.scss', '../../../../../app/betHistory/components/betHistoryPage/bet-history-error-template.scss']
})
export class LadbrokesBetHistoryPageComponent extends BetHistoryPageComponent {
  readonly BETHISTORYCONFIG = BET_HISTORY_CONFIG;
  shopType: IBetHistorySwitcherConfig;

  /**
   * set shop bet tab
   * Remove player bets on ladbrokes
   * @return {void}
   */
  createFilters(): void {
    super.createFilters();
    this.cmsSubscription = this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config.Connect && config.Connect.inShopBets) {
        this.shopType = {
          viewByFilters: this.BETHISTORYCONFIG.shopBet,
          name: this.localeService.getString('bethistory.shop'),
          onClick: filter => this.changeFilter(filter)
        };
        this.betTypes = [...this.betTypes, this.shopType];
      }
    // remove Player bets on ladbrokes
    this.betTypes = this.betTypes.filter((type) => type.viewByFilters !== this.BETHISTORYCONFIG.digitalSportBet);
    });
  }
}

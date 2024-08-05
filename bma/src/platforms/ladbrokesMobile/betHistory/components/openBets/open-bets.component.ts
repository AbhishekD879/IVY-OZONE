import { Component, OnInit } from '@angular/core';
import { OpenBetsComponent as BaseOpenBetsComponent } from '@app/betHistory/components/openBets/open-bets.component';
import { IBetHistorySwitcherConfig } from '@app/betHistory/models/bet-history-switcher-config.model';
import { BET_HISTORY_CONFIG } from '@betHistoryModule/constants/bet-promotions.constant';
import { ISystemConfig } from '@core/services/cms/models';
import { MYBETS_AREAS } from '@app/betHistory/constants/bet-leg-item.constant';

@Component({
  selector: 'open-bets',
  templateUrl: 'open-bets.component.html'
})
export class OpenBetsComponent extends BaseOpenBetsComponent implements OnInit {
  readonly BETHISTORYCONFIG = BET_HISTORY_CONFIG;
  readonly MYBETS_WIDGET = MYBETS_AREAS.WIDGET;
  shopType: IBetHistorySwitcherConfig;
  // remove Player bets on ladbrokes
  protected readonly TYPES: string[] = ['regularType', 'lottoType', 'poolType'];

  ngOnInit(): void {
    super.ngOnInit();
    this.updateBetTypes();
  }

  /*
  * Add shop bet type to Bet types
  * Remove Player bets on ladbrokes
  * @return {void}
  */
  private updateBetTypes(): void {
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

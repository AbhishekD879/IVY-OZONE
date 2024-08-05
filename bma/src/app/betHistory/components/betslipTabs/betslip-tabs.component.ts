import { Component, OnInit, OnDestroy } from '@angular/core';
import { Location } from '@angular/common';
import * as _ from 'underscore';

import { BetslipTabsService } from '@core/services/betslipTabs/betslip-tabs.service';
import { UserService } from '@core/services/user/user.service';

import { IBetslipTab } from '@core/services/betslipTabs/betslip-tab.model';
import { Subscription } from 'rxjs';
import { BetHistoryMainService } from '../../services/betHistoryMain/bet-history-main.service';

@Component({
  selector: 'betslip-tabs',
  templateUrl: './betslip-tabs.component.html'
})
export class BetslipTabsComponent implements OnInit, OnDestroy {
  public betslipTabs: IBetslipTab[];
  public activeTab: IBetslipTab;
  public isLoggedIn: boolean;
  public initialised: boolean;
  private getTabsSubscription: Subscription;

  constructor(
    private betslipTabsService: BetslipTabsService,
    private location: Location,
    private userService: UserService,
    private betHistoryMainService: BetHistoryMainService
  ) {}

  ngOnInit(): void {
    this.getTabsSubscription = this.betslipTabsService.getTabsList().subscribe(tabs => {
      this.betslipTabs = tabs.filter(item => {
        return item.name !== 'Bet Slip';
      });
      const location: string = `/${this.location.path().split('/')[1]}`;
      this.activeTab = _.findWhere(this.betslipTabs, { url: `${location}` });
    });
    this.isLoggedIn = this.userService.status;
    this.initialised = true;
  }

  ngOnDestroy() {
    this.initialised = false;
    this.getTabsSubscription && this.getTabsSubscription.unsubscribe();
    this.betHistoryMainService.showFirstBet('bet');
  }
}

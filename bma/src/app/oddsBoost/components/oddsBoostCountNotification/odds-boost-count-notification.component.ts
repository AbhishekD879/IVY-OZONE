import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { OddsBoostService } from '@oddsBoostModule/services/odds-boost.service';
import { Location } from '@angular/common';

@Component({
  selector: 'odds-boost-count-notification',
  templateUrl: './odds-boost-count-notification.component.html',
  styleUrls: ['./odds-boost-count-notification.component.scss']
})
export class OddsBoostCountNotificationComponent implements OnInit, OnDestroy {
  oddsBoostCount: number = 0;
  private countListener: Subscription;

  constructor(private oddsBoostService: OddsBoostService,
              public location: Location) {}

  ngOnInit(): void {
    this.countListener = this.oddsBoostService.oddsBoostsCountListener.subscribe((n: number) => this.setOddsBoostCount(n));
    if (this.location.path() === '/my-account') {
      this.oddsBoostService.getOddsBoostTokensCount().subscribe((n: number) => this.setOddsBoostCount(n));
    }
  }

  ngOnDestroy(): void {
    this.countListener.unsubscribe();
  }

  private setOddsBoostCount(oddsBoostsCount: number): void {
    this.oddsBoostCount = oddsBoostsCount;
  }
}

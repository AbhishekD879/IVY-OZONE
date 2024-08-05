import { Component, Input, OnInit } from '@angular/core';

import { LocaleService } from '@core/services/locale/locale.service';
import { TimeService } from '@core/services/time/time.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { ILeg } from '@betslip/services/models/bet.model';
import FootballJackpotBet from '../../betModels/footballJackpotBet/football-jackpot-bet.class';

@Component({
  selector: 'jackpot-pool-leg-list',
  templateUrl: './jackpot-pool-leg-list.component.html'
})
export class JackpotPoolLegListComponent implements OnInit {
  @Input() pool: FootballJackpotBet;
  @Input() isSportIconEnabled: boolean;

  startTime: Date;
  otherDay: Date | string;
  todayText: string;
  readonly filtersOrder: string[] = ['startTime', 'classDisplayOrder', 'typeDisplayOrder', 'displayOrder', 'name'];

  constructor(
    private localeService: LocaleService,
    private timeService: TimeService,
    private filtersService: FiltersService
  ) {}

  ngOnInit(): void {
    this.pool.legs = this.filtersService.orderBy(this.pool.legs, this.filtersOrder);
    this.todayText = this.localeService.getString('bethistory.today');
  }

  /**
   * Get start time for current leg
   * @param leg {object} jackpot leg
   */
  getEventStartTime(leg: ILeg): string {
    this.setStartTime(leg);
    return this.otherDay
      ? this.filtersService.date(this.otherDay, 'dd MMM, h:mm a')
      : `${this.todayText}, ${this.filtersService.date(this.startTime, 'h:mm a')}`;
  }

  trackById(index: number, leg: ILeg): string {
    return leg.id;
  }

  /**
   * Set start time for current leg and handle date time if it's today event
   * @param leg {object} jackpot leg
   */
  private setStartTime(leg: ILeg): void {
    this.otherDay = '';
    this.startTime = this.timeService.getLocalDateFromString(leg.startTime.replace(/T/gi, ' '));
    const currentDate: Date = new Date(),
      isSameDate: boolean = this.startTime.getDate() === currentDate.getDate(),
      isSameMonth: boolean = this.startTime.getMonth() === currentDate.getMonth(),
      isSameYear: boolean = this.startTime.getFullYear() === currentDate.getFullYear();

    if (!(isSameMonth && isSameDate && isSameYear)) {
      this.otherDay = this.startTime;
    }
  }
}

import { Component, Input, OnChanges, ChangeDetectionStrategy } from '@angular/core';

import { OFFSIDES, MARKETS } from '../../constants/five-a-side.constant';
import { IConstant } from '@app/core/services/models/constant.model';

@Component({
  selector: 'five-a-side-player-stat',
  templateUrl: './five-a-side-player-stat.component.html',
  styleUrls: ['./five-a-side-player-stat.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveASidePlayerStatComponent implements OnChanges {
  @Input() statLabel: string;
  @Input() mainStat: string;
  @Input() statValue: number | string;
  @Input() cards?: { cardsYellow: string|number, cardsRed: string|number};

  isAvailable: boolean;
  isMainStat: boolean;
  isToBeCarded: boolean;
  label: string;
  mainLabel: string;
  statIcon: string;
  readonly marketsMap: IConstant = MARKETS;
  readonly offsides: string = OFFSIDES;

  ngOnChanges(): void {
    this.setData();
  }

  private setData(): void {
    this.statValue = (this.statValue === undefined || this.statValue === null) ? 0 : this.statValue;
    this.isMainStat = this.statLabel === 'main-stat';
    this.mainLabel = `yourCall.playerStats.${this.marketsMap[this.mainStat]}`;
    this.statIcon = this.isMainStat ? this.marketsMap[this.mainStat] : this.statLabel;
    this.label = this.isMainStat ? this.mainLabel : `yourCall.playerStats.${this.statLabel}`;
    this.isAvailable = this.statIcon !== this.offsides && (this.marketsMap[this.mainStat] !== this.statLabel);
    this.isToBeCarded = this.marketsMap[this.mainStat] === 'cards' && this.isMainStat;
  }
}

import { Component, Input, OnInit, AfterViewInit } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';

import { IFiveASidePlayer } from '@yourcall/services/fiveASide/five-a-side.model';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { IMatrixFormation } from '@yourcall/models/five-a-side.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { GOALKEEPER_MARKETS } from '@yourcall/constants/five-a-side.constant';
import { IYourcallStatisticItem } from '@yourcall/models/yourcall-api-response.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Component({
  selector: 'five-a-side-player-list',
  templateUrl: './five-a-side-player-list.component.html',
  styleUrls: ['./five-a-side-player-list.component.scss']
})
export class FiveASidePlayerListComponent implements OnInit, AfterViewInit {
  @Input() eventEntity: ISportEvent;

  switchers: ISwitcherConfig[];
  playerFormation: IMatrixFormation;
  filter = 'allPlayers';
  playersList: IFiveASidePlayer[];
  isGKmarket: boolean;
  optaStatisticsAvailable: boolean;
  player: IFiveASidePlayer;

  constructor(private fiveASideService: FiveASideService,
    private gtmService: GtmService,
    private windowRefService: WindowRefService) {}

  ngOnInit(): void {
    this.optaStatisticsAvailable = this.fiveASideService.optaStatisticsAvailable;
    this.playerFormation = this.fiveASideService.activeItem;
    this.isGKmarket = GOALKEEPER_MARKETS.includes(this.playerFormation.stat);
    this.playersList = this.fiveASideService.sortPlayers(this.playerFormation);
    if (this.isGKmarket) {
      this.playersList = this.playersList.filter((player: IFiveASidePlayer) => player.isGK);
    } else {
      this.formSwitchers();
    }
    this.setPlayer();
  }

  ngAfterViewInit() {
    this.getScrollPosition();
  }

  trackById(index: number, player: IFiveASidePlayer): string {
    return `${index}_${player.id}`;
  }

  hide(): void {
    this.fiveASideService.hideView();
  }

  handleTabClick(filterBy: string): void {
    this.filter = filterBy;
    this.playersList = this.fiveASideService.sortPlayers(this.playerFormation, filterBy);
  }

  /**
   * Triggered whenever therese is change in stat value
   * @param {IYourcallStatisticItem} newStat
   */
  changeStat(newStat: IYourcallStatisticItem): void {
    this.fiveASideService.saveDefaultStat();
    this.playerFormation = {
      ...this.playerFormation, stat: newStat.title, statId: newStat.id
    };
    this.playersList = this.fiveASideService.sortPlayers(this.playerFormation, this.filter);
    this.gtmService.push('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: 'Edit Market',
      eventLabel: this.playerFormation.stat
    });
  }

  /**
   * To get scroll position and move to that position
   */
  private getScrollPosition(): void {
    const scrollPosition: number = this.fiveASideService.playerListScrollPosition;
    if (scrollPosition) {
      const drawerBody: HTMLElement = this.windowRefService.document.querySelector('five-a-side-player-list .drawer-body');
      drawerBody.scroll(0, scrollPosition);
    }
  }

  /**
   * To set player data based on response
   */
  private setPlayer(): void {
    if (this.playersList && this.playersList.length) {
      this.player = this.playersList[0];
    }
  }

  private formSwitchers(): void {
    this.switchers = [{
      name: 'All Players',
      viewByFilters: 'allPlayers',
      onClick: (filterBy: string) => this.handleTabClick(filterBy)
    }, {
      name: 'Home',
      viewByFilters: 'home',
      onClick: (filterBy: string) => this.handleTabClick(filterBy)
    }, {
      name: 'Away',
      viewByFilters: 'away',
      onClick: (filterBy: string) => this.handleTabClick(filterBy)
    }];
  }
}

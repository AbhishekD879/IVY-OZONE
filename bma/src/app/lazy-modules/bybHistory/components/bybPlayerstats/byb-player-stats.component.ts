import { Component, Inject, ViewChild } from '@angular/core';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA } from '@angular/material/legacy-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { IConstant } from '@app/core/services/models/constant.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { IFiveASidePlayer } from '@app/yourCall/services/fiveASide/five-a-side.model';
import { BYB_MARKETS, MARKET_ORDER } from './byb-player-stats-constant';

@Component({
  selector: 'byb-player-stats-component',
  templateUrl: 'byb-player-stats.component.html',
  styleUrls: ['./byb-player-stats.component.scss'],
})

export class BybPlayerstatsComponent extends AbstractDialogComponent {
  @ViewChild('bybStatsDialog', { static: true }) dialog: any;
  @Inject(MAT_DIALOG_DATA) public data: any;
  player: IFiveASidePlayer;
  market: string;
  readonly marketsMap: IConstant = BYB_MARKETS;
  readonly marketsOrder: IConstant = MARKET_ORDER;
  close: boolean = true;
  playerStatMap = [];
  constructor(device: DeviceService, windowRef: WindowRefService) {
    super(device, windowRef);
  }

  /**
   * to open dialog box of congrats message
   * @returns {void}
   */
  public open(): void {
    super.open();
    if (this.params && this.params.data && this.params.data.player && this.params.data.market) {
      this.player = this.params.data.player;
      this.market = this.params.data.market;
      this.createPlayerStatMap(this.marketsOrder[this.market.toLowerCase()]);
    }
  }

  private createPlayerStatMap(order: Array<string>): void {
    this.playerStatMap = [];
    order.forEach(market => {
      this.playerStatMap.push({ statLabel: market, statValue: this.player[this.marketsMap[market.toString()]] ? this.player[this.marketsMap[market.toString()]] : '0' });
    });
  }
}

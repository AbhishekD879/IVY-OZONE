import { Component, ViewChild, ChangeDetectionStrategy } from '@angular/core';

import { AbstractDialogComponent } from '../oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';

@Component({
  selector: 'free-bet-dialog',
  templateUrl: 'free-bets-dialog.component.html',
  styleUrls: ['./free-bets-dialog.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FreeBetsDialogComponent extends AbstractDialogComponent {

  @ViewChild('freeBetDialog', {static: true}) dialog;

  isMyBetsInCasino: boolean = false;

  constructor(
    device: DeviceService, windowRef: WindowRefService, 
    private ezNavVanillaService: EzNavVanillaService
  ) {
    super(device, windowRef);
    
    this.isMyBetsInCasino = this.ezNavVanillaService.isMyBetsInCasino;
  }

  open(): void {
    !this.isMyBetsInCasino && super.open();
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }
}

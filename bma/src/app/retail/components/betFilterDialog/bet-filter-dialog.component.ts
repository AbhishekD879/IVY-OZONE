import { Component, ViewChild } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { ITrackEvent } from '@core/services/gtm/models';
import { BET_FILTER_DIALOG } from '@app/retail/constants/retail.constant';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Component({
  selector: 'bet-filter-dialog',
  templateUrl: './bet-filter-dialog.component.html'
})
export class BetFilterDialogComponent extends AbstractDialogComponent {
  @ViewChild('betFilterDialog', { static: true }) dialog;

  readonly CONST = BET_FILTER_DIALOG;

  constructor(device: DeviceService, private gtmService: GtmService, windowRef: WindowRefService) {
    super(device, windowRef);
  }

  selectMode(mode: string): void {
    this.closeDialog();
    this.params.selectMode(mode);
    this.gtmService.push('trackEvent', {
      eventCategory: 'bet filter',
      eventAction: 'you\'re betting',
      eventLabel: mode === 'online' ? 'online' : 'in-shop'
    } as ITrackEvent);
  }

  cancel(): void {
    this.closeDialog();
    this.params.cancel(true);
  }
}

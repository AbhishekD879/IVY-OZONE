import { AfterViewInit, Component, OnDestroy, ViewChild, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FOOTBALL_FILTER_CONFIRM } from '@app/retail/constants/retail.constant';

@Component({
  selector: 'football-filter-confirm-dialog',
  templateUrl: './football-filter-confirm-dialog.component.html',
  styleUrls: ['./football-filter-confirm-dialog.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FootballFilterConfirmDialogComponent extends AbstractDialogComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('footballFilterConfirmDialog',{static: true}) dialog;
  radioInshop: string = FOOTBALL_FILTER_CONFIRM.INSHOP_RADIO;
  radioOnline: string = FOOTBALL_FILTER_CONFIRM.ONLINE_RADIO;

  constructor(deviceService: DeviceService,
    protected windowRef: WindowRefService,
    private pubSubService: PubSubService) {
    super(deviceService, windowRef);
  }

  ngAfterViewInit(): void {
    this.pubSubService.subscribe('FootballFilterConfirmDialogComponent', this.pubSubService.API.NEW_DIALOG_OPENED, () => {
      this.dialog.changeDetectorRef.detectChanges();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('FootballFilterConfirmDialogComponent');
  }

  /*
  * Handling button click events
  * @return {void}
  */
  handleBtnClick(button: any, footBallBetFilterType: string): void {
    button.handler(footBallBetFilterType);
  }
}

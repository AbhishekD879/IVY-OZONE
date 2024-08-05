import { Component, OnInit, OnDestroy } from '@angular/core';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { VisDataHandlerService } from '@core/services/visDataHandler/vis-data-handler.service';

import { IStreamDetails } from '@rightColumnModule/components/wMatchCentre/w-match-centre.model';

@Component({
  selector: 'w-match-centre',
  templateUrl: 'w-match-centre.component.html'
})
export class WMatchCentreComponent implements OnInit, OnDestroy {
  streamShown: string;
  visData: any;
  document: any;

  constructor(
    private windowRefService: WindowRefService,
    private deviceService: DeviceService,
    private visDataHandlerService: VisDataHandlerService
  ) {
    this.document = this.windowRefService.document;
  }

  ngOnInit(): void {
    this.visDataHandlerService
      .init()
      .subscribe((visData: any) => {
        this.visData = visData;
      });

    // add listener for native player only on wrapper
    if (this.deviceService.isWrapper) {
      this.document.addEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', (data: IStreamDetails) => this.setStreamShowFlag(data));
    }
  }

  ngOnDestroy(): void {
    this.document.removeEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', (data: IStreamDetails) => this.setStreamShowFlag(data));
  }

  private setStreamShowFlag(data: IStreamDetails): void {
    this.streamShown = data.detail.settingValue;
  }
}

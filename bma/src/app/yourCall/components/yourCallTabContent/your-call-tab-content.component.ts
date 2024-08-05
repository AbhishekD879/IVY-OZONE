import { Component, Input, ViewChild } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { YourcallDashboardComponent } from '@app/yourCall/components/yourcallDashboard/yourcall-dashboard.component';

@Component({
  selector: 'yourcall-tab-content',
  templateUrl: './your-call-tab-content.component.html'
})
export class YourCallTabContentComponent{

  @Input() eventEntity: ISportEvent;
  timeStamp = new Date().getSeconds();
  staticType: string;
  showIcon: boolean;
  isLoaded: boolean;
  isMarkets: boolean;
  @ViewChild('dashBoardBox',{static: false}) dashBoardBox: YourcallDashboardComponent;
  constructor() { }

  get reLocate(): boolean {
    if(this.dashBoardBox) {
      this.dashBoardBox.relocate();
    }
    return true;
  }
}

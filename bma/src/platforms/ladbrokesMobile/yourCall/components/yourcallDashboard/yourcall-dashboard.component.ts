import { Component, ViewEncapsulation } from '@angular/core';

import { YourcallDashboardComponent } from '@yourcall/components/yourcallDashboard/yourcall-dashboard.component';

@Component({
  selector: 'yourcall-dashboard',
  templateUrl: './yourcall-dashboard.component.html',
  styleUrls: ['../../../../../app/yourCall/components/yourcallDashboard/yourcall-dashboard.component.scss',
    './yourcall-dashboard.component.scss'],
    // eslint-disable-next-line
    encapsulation: ViewEncapsulation.None
})
export class LadbrokesYourcallDashboardComponent extends YourcallDashboardComponent {}

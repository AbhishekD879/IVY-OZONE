import { Component, Input } from '@angular/core';
import { LaunchBannerComponent } from '@lazy-modules/freeRide/components/launch-banner/launch-banner.component';

@Component({
  selector: 'launch-banner',
  templateUrl: '../../../../../../app/lazy-modules/freeRide/components/launch-banner/launch-banner.component.html',
  styleUrls: ['../../../../../../app/lazy-modules/freeRide/components/launch-banner/launch-banner.component.scss']
})
export class LadsDeskLaunchBannerComponent extends LaunchBannerComponent {
  @Input() config?: string;
}
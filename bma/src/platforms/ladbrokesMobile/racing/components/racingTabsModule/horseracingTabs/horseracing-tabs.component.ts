import { Component, ViewEncapsulation } from '@angular/core';
import {
  HorseracingTabsComponent as CoralHorseracingTabsComponent
} from '@racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';

@Component({
  selector: 'horseracing-tabs',
  templateUrl: 'horseracing-tabs.component.html',
  styleUrls: ['horseracing-tabs.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class HorseracingTabsComponent extends CoralHorseracingTabsComponent {}

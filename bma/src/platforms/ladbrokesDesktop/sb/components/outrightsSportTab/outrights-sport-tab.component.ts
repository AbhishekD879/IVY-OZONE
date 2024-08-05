import { Component, ViewEncapsulation } from '@angular/core';
import {
  OutrightsSportTabComponent as CoralOutrightsSportTabComponent
} from '@sb/components/outrightsSportTab/outrights-sport-tab.component';

@Component({
  selector: 'outrights-sport-tab',
  templateUrl: 'outrights-sport-tab.component.html',
  styleUrls: ['outrights-sport-tab.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class OutrightsSportTabComponent extends CoralOutrightsSportTabComponent {
}

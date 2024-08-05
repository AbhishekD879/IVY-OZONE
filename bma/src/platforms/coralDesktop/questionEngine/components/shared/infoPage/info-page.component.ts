import { Component, ViewEncapsulation } from '@angular/core';

import { InfoPageComponent } from '@app/questionEngine/components/shared/infoPage/info-page.component';

@Component({
  selector: 'info-page',
  templateUrl: './info-page.component.html',
  styleUrls: ['./info-page.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class DesktopInfoPageComponent extends InfoPageComponent {
}

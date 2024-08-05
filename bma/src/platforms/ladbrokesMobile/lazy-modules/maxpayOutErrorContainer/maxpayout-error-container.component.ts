import { Component, ViewEncapsulation } from '@angular/core';
import { MaxpayoutErrorContainerComponent } from '@app/lazy-modules/maxpayOutErrorContainer/maxpayout-error-container.component';


@Component({
  selector: 'ladbrokes-maxpayout-error-container',
  templateUrl: './maxpayout-error-container.component.html',
  styleUrls: ['./maxpayout-error-container.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class LadbrokesMaxpayoutErrorContainerComponent extends MaxpayoutErrorContainerComponent {
}

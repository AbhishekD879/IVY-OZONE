import { Component, ViewEncapsulation } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';

import { CouponsDetailsComponent as CoralCouponsDetailsComponent } from '@sb/components/couponsDetails/coupons-details.component';

@Component({
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None,
  selector: 'coupons-details',
  styleUrls: ['coupons-details.component.scss',  '../../../../../app/sb/components/couponsDetails/coupons-details.component.scss'],
  templateUrl: './coupons-details.component.html'
})
export class CouponsDetailsComponent extends CoralCouponsDetailsComponent {
  trackById(index: number, event: ISportEvent): string {
    return event && event.id ? `${event.id} ${index}` : index.toString();
  }

  protected getStickyElementsHeight(): number {
    const headerElement = this.windowRefService.document.querySelector('header');
    return !headerElement ? 0 : this.domToolsService.getHeight(headerElement);
  }
}

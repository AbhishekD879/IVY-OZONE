import { Component, ViewEncapsulation, HostBinding, Input } from '@angular/core';

import { AccordionComponent } from '@shared/components/accordion/accordion.component';
import { ISportEvent } from '@core/models/sport-event.model';

@Component({
  selector: 'accordion',
  templateUrl: 'accordion.component.html',
  styleUrls: ['accordion.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class LadbrokesAccordionComponent extends AccordionComponent {

  @HostBinding('class.is-expanded') isExpanded: boolean;
  @Input() isVirtual?: boolean = true;
  @Input() isCustomElement?: boolean = false;
  @Input() eventEntity?: ISportEvent;
  @Input() showRaceDetails?: boolean = false;
  @Input() isLuckyDipMarketAvailable?: boolean;

  toggled(event: MouseEvent) {
    super.toggled(event);
    this.headerClasses = this.setHeaderClass();
  }

  /**
   * Set Header CSS Class
   * @returns { [key: string]: boolean }
   */
  setHeaderClass(): { [key: string]: boolean } {
    const classes = {
      'inner-header': this.isChevronToLeft || this.inner,
      'byb-header': this.isBybState && !this.isChevronToLeft,
      'hr-header-section': this.showRaceDetails
    };
    if (this.headerClass) {
      classes[this.headerClass] = this.headerClass;
    }
    return classes;
  }
}


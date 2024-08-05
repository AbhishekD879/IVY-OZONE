import { Component, ViewEncapsulation } from '@angular/core';
import { LadbrokesAccordionComponent } from '@ladbrokesMobile/shared/components/accordion/accordion.component';

@Component({
  selector: 'accordion',
  templateUrl: 'accordion.component.html',
  styleUrls: ['accordion.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class AccordionComponent extends LadbrokesAccordionComponent {
}


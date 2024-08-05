import { Component, ViewEncapsulation } from '@angular/core';
import { AccordionComponent as AppAccordionComponent } from '@shared/components/accordion/accordion.component';

@Component({
  selector: 'accordion',
  templateUrl: 'accordion.component.html',
  styleUrls: ['./accordion.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class AccordionComponent extends AppAccordionComponent {
}


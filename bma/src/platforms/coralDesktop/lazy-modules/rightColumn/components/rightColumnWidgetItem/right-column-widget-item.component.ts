import { Component } from '@angular/core';
import {
  RightColumnWidgetItemComponent as CoralRightColumnWidgetItemComponent
} from '@app/lazy-modules/rightColumn/components/rightColumnWidgetItem/right-column-widget-item.component';

@Component({
  selector: 'right-column-widget-item',
  templateUrl: 'right-column-widget-item.component.html'
})
export class RightColumnWidgetItemComponent extends CoralRightColumnWidgetItemComponent {}

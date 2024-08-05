import { Component, Input } from '@angular/core';

@Component({
  selector: 'right-column-widget-item',
  templateUrl: 'right-column-widget-item.component.html'
})
export class RightColumnWidgetItemComponent {
  @Input() componentName: string;
  @Input() widgetColumn: string;
  @Input() isHidden: boolean;
  @Input() isExpanded: boolean;
}

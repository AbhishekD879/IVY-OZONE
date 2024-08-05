import { Component, Input } from '@angular/core';


/**
 * The property should be set if the component is used from betslip widget on main page
 * Use it if you need to show/hide some content on the widget
 */

@Component({
  selector: 'used-from-widget',
  template: '',
})
export class UsedFromWidgetAbstractComponent {
  @Input() isUsedFromWidget = false;
}

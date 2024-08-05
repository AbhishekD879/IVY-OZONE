import { Component } from '@angular/core';
import {
  RightColumnWidgetComponent
} from '@app/lazy-modules/rightColumn/components/rightColumnWidget/right-column-widget.component';

@Component({
  selector: 'right-column-widget',
  styleUrls: ['right-column-widget.scss'],
  templateUrl: '../../../../../../app/lazy-modules/rightColumn/components/rightColumnWidget/right-column-widget.component.html'
})
export class DesktopRightColumnWidgetComponent extends RightColumnWidgetComponent {}

import { Component } from '@angular/core';

import { EventTitleBarComponent } from '@edp/components/eventTitleBar/event-title-bar.component';

@Component({
  selector: 'event-title-bar',
  templateUrl: './event-title-bar.component.html',
  styleUrls: ['./event-title-bar.component.scss']
})
export class DesktopEventTitleBarComponent extends EventTitleBarComponent {}

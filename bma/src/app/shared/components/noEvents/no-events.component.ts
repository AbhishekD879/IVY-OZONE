import { Component, Input } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'no-events',
  templateUrl: './no-events.component.html',
  styleUrls: ['./no-events.component.scss']
})
export class NoEventsComponent {
  @Input() message: string = 'app.noEventsFound';
  @Input() eventQuickSwitch: boolean = false;
  isCoral: boolean = environment.brand === 'bma';
}

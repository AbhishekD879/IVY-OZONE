import { Component } from '@angular/core';
import { SportEventPageComponent as AppSportEventPageComponent } from '@edp/components/sportEventPage/sport-event-page.component';

@Component({
  selector: 'sport-event-page',
  styleUrls: [
    './sport-event-page.component.scss',
  ],
  templateUrl: './sport-event-page.component.html'
})
export class SportEventPageComponent extends AppSportEventPageComponent {
}

import { Component } from '@angular/core';
import {
  EventHeaderComponent as CoralEventHeaderComponent
} from '@app/betHistory/components/eventHeader/event-header.component';

@Component({
  selector: 'event-header',
  templateUrl: '../../../../../app/betHistory/components/eventHeader/event-header.component.html',
  styleUrls: ['./event-header.component.scss']
})
export class EventHeaderComponent extends CoralEventHeaderComponent {}

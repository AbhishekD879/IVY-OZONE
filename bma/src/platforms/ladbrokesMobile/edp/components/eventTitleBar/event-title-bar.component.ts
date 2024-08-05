import { Component, OnInit } from '@angular/core';
import { EventTitleBarComponent as EdpEventTitleBarComponent } from '@edp/components/eventTitleBar/event-title-bar.component';

@Component({
  selector: 'event-title-bar',
  templateUrl: 'event-title-bar.component.html',
  styleUrls: ['./event-title-bar.component.scss'],
})
export class EventTitleBarComponent extends EdpEventTitleBarComponent implements OnInit {
  ngOnInit() {
    this.eventStartDate = this.event.startTime;
    this.freeBetVisible = this.freeBetsService.isFreeBetVisible(this.event);
  }
}

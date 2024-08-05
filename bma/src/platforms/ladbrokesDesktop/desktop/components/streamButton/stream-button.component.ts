
import { Component, Input, Output, EventEmitter } from '@angular/core';

import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportEvent } from '@core/models/sport-event.model';

@Component({
  selector: 'stream-button',
  templateUrl: './stream-button.component.html',
  styleUrls: ['./stream-button.component.scss']
})
export class StreamButtonComponent {
  @Input() event: ISportEvent;
  @Input() activeEvent: ISportEvent;
  @Output() readonly update: EventEmitter<ISportEvent> = new EventEmitter();

  constructor(
    private userService: UserService,
    private pubsubService: PubSubService
  ) {

  }

  setActiveEvent(event: ISportEvent): void {
    this.activeEvent = event;
    this.update.emit(event);
    if (this.userService.status) {
      this.pubsubService.publish(this.pubsubService.API.PUSH_TO_GTM, ['trackEvent', {
        eventCategory: 'home',
        eventAction: 'live stream',
        eventLabel: 'watch stream'
      }]);
    }
  }

  isLoggedIn(): boolean {
    return this.userService.status;
  }
}

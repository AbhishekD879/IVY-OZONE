import { Component } from '@angular/core';

import { EventVideoStreamComponent } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream.component';

@Component({
  selector: 'event-video-stream',
  templateUrl: './event-video-stream.component.html'
})
export class LadbrokesEventVideoStreamComponent extends EventVideoStreamComponent  {
}

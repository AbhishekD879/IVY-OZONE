import { Component, Input } from '@angular/core';
import { IRacingPostVerdict } from '@app/racing/models/racing-post-verdict.model';
import { ISportEvent } from '@app/core/models/sport-event.model';

@Component({
  selector: 'racing-post-widget',
  templateUrl: 'racing-post-widget.component.html',
})
export class LadbrokesRacingPostWidgetComponent {
  @Input() data: IRacingPostVerdict;
  @Input() eventEntity: ISportEvent;
}

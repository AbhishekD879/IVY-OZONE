import { Component, Input } from '@angular/core';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
@Component({
  selector: 'racing-post-widget',
  templateUrl: 'racing-post-widget.component.html',
})
export class DesktopRacingPostWidgetComponent {
  @Input() racingPostSummary: string;
  @Input() data: IRacingPostVerdict;
  @Input() eventEntity: ISportEvent;
  @Input() showMap: boolean;
}

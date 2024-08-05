import { Component, Input, ViewEncapsulation } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'event-card',
  templateUrl: 'event-card.component.html',
  styleUrls: ['./event-card.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class EventCardComponent {
  @Input() event: ISportEvent;
  @Input() market: IMarket;
  @Input() outcome: IOutcome;
  @Input() gtmModuleTitle?: boolean;
}


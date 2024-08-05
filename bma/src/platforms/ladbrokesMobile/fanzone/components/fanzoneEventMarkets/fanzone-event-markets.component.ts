import { Component } from '@angular/core';
import { EventMarketsComponent } from '@app/edp/components/eventMarkets/event-markets.component';

@Component({
    selector: 'fanzone-event-markets',
    templateUrl: 'fanzone-event-markets.component.html',
    styleUrls: ['fanzone-event-markets.component.scss']
  })
export class FanzoneEventMarketsComponent extends EventMarketsComponent {
}

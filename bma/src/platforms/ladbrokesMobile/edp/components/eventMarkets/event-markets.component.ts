import { Component } from '@angular/core';
import { EventMarketsComponent as AppEventMarketsComponent } from '@edp/components/eventMarkets/event-markets.component';

@Component({
  selector: 'event-markets',
  templateUrl: 'event-markets.component.html',
  styleUrls: ['event-markets.component.scss']
})
export class EventMarketsComponent extends AppEventMarketsComponent {}

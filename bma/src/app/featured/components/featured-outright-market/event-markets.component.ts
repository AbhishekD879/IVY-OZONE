import { Component, ChangeDetectionStrategy } from '@angular/core';
import { EventMarketsComponent } from '@edp/components/eventMarkets/event-markets.component';

@Component({
  selector: 'featured-event-markets',
  templateUrl: '../../../edp/components/eventMarkets/event-markets.html',
  styleUrls: [
    '../../../edp/components/eventMarkets/event-markets.scss',
    'event-markets.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedEventMarketsComponent extends EventMarketsComponent {}

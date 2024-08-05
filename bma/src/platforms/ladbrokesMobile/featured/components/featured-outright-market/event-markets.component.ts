import { Component, ChangeDetectionStrategy } from '@angular/core';
import { EventMarketsComponent } from '@ladbrokesMobile/edp/components/eventMarkets/event-markets.component';

@Component({
  selector: 'featured-event-markets',
  templateUrl: '../../../edp/components/eventMarkets/event-markets.component.html',
  styleUrls: ['../../../edp/components/eventMarkets/event-markets.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedEventMarketsComponent extends EventMarketsComponent {}

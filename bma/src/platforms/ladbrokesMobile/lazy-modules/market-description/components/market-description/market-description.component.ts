import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
  MarketDescriptionComponent as CoralMarketDescriptionComponent
} from '@lazy-modules/market-description/components/market-description/market-description.component';

@Component({
  selector: 'market-description',
  templateUrl: './market-description.component.html',
  styleUrls: ['./market-description.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MarketDescriptionComponent extends CoralMarketDescriptionComponent {
}

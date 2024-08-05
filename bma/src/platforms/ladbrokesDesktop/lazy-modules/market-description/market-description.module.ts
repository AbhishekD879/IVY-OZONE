import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import {
  MarketDescriptionComponent
} from '@ladbrokesMobile/lazy-modules/market-description/components/market-description/market-description.component';
import { MarketTooltipComponent } from '@app/lazy-modules/market-description/components/market-tooltip/market-tooltip.component';
import { RacingTooltipDirective } from '@app/lazy-modules/market-description/directives/racing-tooltip/racing-tooltip.directive';
import { RacingTooltipComponent
} from '@ladbrokesMobile/lazy-modules/market-description/components/racing-tooltip/racing-tooltip.component';

@NgModule({
  declarations: [MarketDescriptionComponent,
    MarketTooltipComponent,
    RacingTooltipDirective,
    RacingTooltipComponent],
  imports: [
    SharedModule
  ],
  exports: [
    MarketDescriptionComponent,
    MarketTooltipComponent,
    RacingTooltipDirective,
    RacingTooltipComponent
  ]
})
export class MarketDescriptionModule {
  static entry = { MarketDescriptionComponent, MarketTooltipComponent };
}

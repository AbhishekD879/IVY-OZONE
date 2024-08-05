import { SharedModule } from '@sharedModule/shared.module';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { FeaturedTabComponent } from '@featured/components/featured-tab/featured-tab.component';
import { LadbrokesFeaturedModuleComponent } from '@ladbrokesMobile/featured/components/featured-module/featured-module.component';
import { FeaturedModuleService } from '@featured/services/featuredModule/featured-module.service';
import {
  LadbrokesFeaturedQuickLinksComponent
} from '@ladbrokesMobile/featured/components/featured-quick-links/featured-quick-links.component';
import { FeaturedRoutingModule } from '@featured/featured-routing.module';
import {
  LadbrokesFeaturedHighlightsCarouselComponent
} from '@ladbrokesMobile/featured/components/featured-highlights-carousel/featured-highlights-carousel.component';
import {
  LadbrokesFeaturedInplayComponent
} from '@ladbrokesMobile/featured/components/featured-inplay/featured-inplay.component';
import { FeaturedRaceCardHomeComponent } from '@ladbrokesMobile/featured/components/featured-race-card/race-card-home.component';
import { FeaturedEventMarketsComponent } from '@ladbrokesMobile/featured/components/featured-outright-market/event-markets.component';
import { FeaturedAemComponent } from '@featured/components/featured-aem/featured-aem.component';

@NgModule({
  declarations: [
    LadbrokesFeaturedModuleComponent,
    FeaturedTabComponent,
    LadbrokesFeaturedQuickLinksComponent,
    LadbrokesFeaturedHighlightsCarouselComponent,
    FeaturedAemComponent,
    LadbrokesFeaturedInplayComponent,
    FeaturedRaceCardHomeComponent,
    FeaturedEventMarketsComponent
  ],
  imports: [
    SharedModule,
    FeaturedRoutingModule
  ],
  exports: [
    LadbrokesFeaturedModuleComponent,
    FeaturedTabComponent,
    LadbrokesFeaturedQuickLinksComponent,
    LadbrokesFeaturedHighlightsCarouselComponent,
    FeaturedAemComponent
  ],
  providers: [
    FeaturedModuleService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class FeaturedModule {
  static entry = LadbrokesFeaturedModuleComponent;
}

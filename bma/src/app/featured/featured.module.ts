import { FeaturedRoutingModule } from '@featured/featured-routing.module';
import { SharedModule } from '@sharedModule/shared.module';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { FeaturedTabComponent } from '@featured/components/featured-tab/featured-tab.component';
import { FeaturedModuleComponent } from '@featured/components/featured-module/featured-module.component';
import { FeaturedModuleService } from '@featured/services/featuredModule/featured-module.service';
import { FeaturedQuickLinksComponent } from '@featured/components/featured-quick-links/featured-quick-links.component';
import {
  FeaturedHighlightsCarouselComponent
} from '@featured/components/featured-highlights-carousel/featured-highlights-carousel.component';
import { FeaturedInplayComponent } from '@featured/components/featured-inplay/featured-inplay.component';
import { FeaturedEventMarketsComponent } from '@featured/components/featured-outright-market/event-markets.component';
import { FeaturedRaceCardHomeComponent } from '@featured/components/featured-race-card/race-card-home.component';
import { FeaturedAemComponent } from '@featured/components/featured-aem/featured-aem.component';
import { NgOptimizedImage } from '@angular/common';
@NgModule({
  declarations: [
    FeaturedModuleComponent,
    FeaturedTabComponent,
    FeaturedQuickLinksComponent,
    FeaturedHighlightsCarouselComponent,
    FeaturedAemComponent,
    FeaturedInplayComponent,
    FeaturedEventMarketsComponent,
    FeaturedRaceCardHomeComponent
  ],
  imports: [
    SharedModule,
    FeaturedRoutingModule,
    NgOptimizedImage
  ],
  exports: [
  ],
  providers: [
    FeaturedModuleService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class FeaturedModule {
  static entry = FeaturedModuleComponent;
}

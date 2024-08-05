import { DesktopFeaturedRoutingModule } from '@ladbrokesDesktop/featured/featured-routing.module';
import { SharedModule } from '@sharedModule/shared.module';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { FeaturedTabComponent } from '@featured/components/featured-tab/featured-tab.component';
import { FeaturedModuleService } from '@featured/services/featuredModule/featured-module.service';

// Overridden app components
import {
  DesktopFeaturedModuleComponent
} from '@ladbrokesDesktop/featured/components/featured-module/featured-module.component';
import {
  LadbrokesFeaturedHighlightsCarouselComponent as FeaturedHighlightsCarouselComponent
} from '@ladbrokesMobile/featured/components/featured-highlights-carousel/featured-highlights-carousel.component';
import { FeaturedAemComponent } from '@featured/components/featured-aem/featured-aem.component';

@NgModule({
  declarations: [
    // Overridden app components
    DesktopFeaturedModuleComponent,
    FeaturedAemComponent,
    FeaturedTabComponent,
    FeaturedHighlightsCarouselComponent
  ],
  imports: [
    SharedModule,
    DesktopFeaturedRoutingModule
  ],
  exports: [
    // Overridden app components
    DesktopFeaturedModuleComponent,
    FeaturedAemComponent,
    FeaturedHighlightsCarouselComponent
  ],
  providers: [
    FeaturedModuleService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class FeaturedModule {
  static entry = DesktopFeaturedModuleComponent;
}

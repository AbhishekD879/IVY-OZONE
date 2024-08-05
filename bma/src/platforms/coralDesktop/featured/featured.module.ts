import { DesktopFeaturedRoutingModule } from '@coralDesktop/featured/featured-routing.module';
import { SharedModule } from '@sharedModule/shared.module';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { FeaturedTabComponent } from '@featured/components/featured-tab/featured-tab.component';
import { FeaturedModuleService } from '@featured/services/featuredModule/featured-module.service';

// Overridden app components
import {
  DesktopFeaturedModuleComponent
} from '@coralDesktop/featured/components/featured-module/featured-module.component';
import {
  FeaturedHighlightsCarouselComponent
} from '@featured/components/featured-highlights-carousel/featured-highlights-carousel.component';
import { FeaturedAemComponent } from '@featured/components/featured-aem/featured-aem.component';

@NgModule({
  declarations: [
    // Overridden app components
    DesktopFeaturedModuleComponent,
    FeaturedTabComponent,
    FeaturedAemComponent,
    FeaturedHighlightsCarouselComponent
  ],
  imports: [
    SharedModule,
    DesktopFeaturedRoutingModule
  ],
  exports: [
  ],
  providers: [
    FeaturedModuleService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class FeaturedModule {
  static entry = DesktopFeaturedModuleComponent;
}

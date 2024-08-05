import { NgModule } from '@angular/core';
import {
  FeaturedEventsModuleComponent
} from '@app/sports-modules/featured-events-module/featured-events-module/featured-events-module.component';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@app/shared/shared.module';
import { FeaturedEventsModuleRoutingModule } from '@app/sports-modules/featured-events-module/featured-events-module-routing.module';
import { FeaturedTabModule } from '@app/featured-tab/featured-tab.module';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FeaturedTabModule,
    FeaturedEventsModuleRoutingModule
  ],
  exports: [],
  declarations: [
    FeaturedEventsModuleComponent
  ],
  providers: [],
})
export class FeaturedEventsModuleModule {
}

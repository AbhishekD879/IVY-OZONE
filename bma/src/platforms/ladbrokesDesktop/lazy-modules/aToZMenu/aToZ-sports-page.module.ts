import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { LazyAToZSportPageRoutingModule } from '@ladbrokesDesktop/lazy-modules/aToZMenu/aToZ-sports-page-routing.module';
import { LadbrokesAzSportsPageComponent } from '@ladbrokesDesktop/lazy-modules/aToZMenu/components/az-sports-page.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    LazyAToZSportPageRoutingModule
  ],
  declarations: [ LadbrokesAzSportsPageComponent ],
  providers: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyAToZSportPageModule {
  static entry = LadbrokesAzSportsPageComponent;
}

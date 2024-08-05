import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { LazyAToZSportPageRoutingModule } from '@lazy-modules/aToZMenu/aToZ-sports-page-routing.module';
import { AzSportsPageComponent } from '@lazy-modules-module/aToZMenu/components/AzSportsPageComponent/az-sports-page.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    LazyAToZSportPageRoutingModule
  ],
  declarations: [ AzSportsPageComponent ],
  providers: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyAToZSportPageModule {
  static entry = AzSportsPageComponent;
}

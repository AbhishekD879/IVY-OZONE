import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { AzSportsPageLadbrokesMobileComponent } from '@ladbrokesMobile/lazy-modules/aToZMenu/az-sports-page.component';
import { LazyAToZSportPageRoutingModule } from '@ladbrokesMobile/lazy-modules/aToZMenu/aToZ-sports-page-routing.module';

@NgModule({
  imports: [CommonModule, SharedModule, LazyAToZSportPageRoutingModule],
  declarations:
    [AzSportsPageLadbrokesMobileComponent],
  exports: [AzSportsPageLadbrokesMobileComponent],
  providers: []
})
export class LazyAToZSportPageModule {
  static entry = {AzSportsPageLadbrokesMobileComponent};
}

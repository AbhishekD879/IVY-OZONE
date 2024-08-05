import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LazyPromotionIconsComponent } from './components/lazy-promotion-icons.component';

@NgModule({
  imports: [ CommonModule, SharedModule],
  declarations: [LazyPromotionIconsComponent],
  exports: [LazyPromotionIconsComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyPromotionIconsModule {
  static entry = { LazyPromotionIconsComponent }
}

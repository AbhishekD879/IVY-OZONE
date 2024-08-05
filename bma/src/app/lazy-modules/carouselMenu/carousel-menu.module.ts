import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CarouselMenuComponent } from '@app/lazy-modules/carouselMenu/components/carousel-menu.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [CarouselMenuComponent],
  exports: [CarouselMenuComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CarouselMenuModule {
  static entry = CarouselMenuComponent;
}
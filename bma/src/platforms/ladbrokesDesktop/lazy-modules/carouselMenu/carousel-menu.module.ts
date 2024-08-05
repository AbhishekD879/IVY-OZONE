import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DesktopCarouselMenuComponent } from './components/carousel-menu.component'
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [DesktopCarouselMenuComponent],
  exports: [DesktopCarouselMenuComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CarouselMenuModule {
  static entry = DesktopCarouselMenuComponent;
}
import { Component, ChangeDetectionStrategy } from '@angular/core';

import { CarouselMenuComponent as AppCarouselMenuComponent } from '@app/lazy-modules/carouselMenu/components/carousel-menu.component';
@Component({
  selector: 'carousel-menu',
  styleUrls: ['./carousel-menu.component.scss'],
  templateUrl: 'carousel-menu.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CarouselMenuComponent extends AppCarouselMenuComponent {}

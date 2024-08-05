import { Component } from '@angular/core';
import {
  SurfaceBetsCarouselComponent as AppSurfaceBetsCarouselComponent
} from '@shared/components/surfaceBetsCarousel/surface-bets-carousel.component';

@Component({
  selector: 'surface-bets-carousel',
  templateUrl: '../../../../../app/shared/components/surfaceBetsCarousel/surface-bets-carousel.component.html',
  styleUrls: [
    '../../../../../app/shared/components/surfaceBetsCarousel/surface-bets-carousel.component.scss',
    './surface-bets-carousel.component.scss'
  ]
})
export class SurfaceBetsCarouselComponent extends AppSurfaceBetsCarouselComponent {
}

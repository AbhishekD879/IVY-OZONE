import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
  FeaturedHighlightsCarouselComponent
} from '@featured/components/featured-highlights-carousel/featured-highlights-carousel.component';

@Component({
  selector: 'featured-highlight-carousel',
  templateUrl: 'featured-highlights-carousel.component.html',
  styleUrls: ['featured-highlights-carousel.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesFeaturedHighlightsCarouselComponent extends FeaturedHighlightsCarouselComponent { }

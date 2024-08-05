import { Component } from '@angular/core';
import {
  StarRatingComponent as AppStarRatingComponent
} from '@shared/components/star-rating/star-rating.component';

@Component({
  selector: 'star-rating',
  templateUrl: 'star-rating.component.html',
  styleUrls: ['star-rating.component.scss']
})

export class StarRatingComponent extends AppStarRatingComponent {

}

import { Component, Input, OnInit, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'star-rating',
  templateUrl: 'star-rating.component.html',
  styleUrls: ['star-rating.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class StarRatingComponent implements OnInit {
  @Input() rating: number;
  startRating: boolean[];

  ngOnInit(): void {
    this.startRating = new Array(5).fill(false).map((item, index) => index < +this.rating);
  }

  trackByIndex(index: number): number {
    return index;
  }

}

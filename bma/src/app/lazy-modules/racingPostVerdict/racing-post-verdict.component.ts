import { Component, Input, OnInit } from '@angular/core';
import { IRacingPostVerdict, IStarRating } from '@racing/models/racing-post-verdict.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@app/core/models/market.model';
import { IOutcome } from '@app/core/models/outcome.model';


@Component({
  selector: 'racing-post-verdict',
  templateUrl: 'racing-post-verdict.component.html',
  styleUrls: ['racing-post-verdict.component.scss'],
})

export class RacingPostVerdictComponent implements OnInit {
  @Input() data: IRacingPostVerdict;
  @Input() showMap: boolean;
  @Input() eventEntity: ISportEvent;
  @Input() expandedSummary: boolean[][];
  @Input() isRacingSpecialsCondition: boolean;
  @Input() isNotAntepostOrSpecials: boolean;
  resultLimit: number = 3;
  isValidImage: boolean = true;
  @Input() spotlightedOutcome: IOutcome;
  @Input() eachWayMarket: IMarket;

  ngOnInit(): void {
    this.data.starRatings.sort(this.compareByStarsAndName);
    if (this.data.starRatings.length > this.resultLimit) {
      this.data.starRatings.splice(this.resultLimit, this.data.starRatings.length);
    }
  }

  trackByIndex(index: number): number {
    return index;
  }

  private compareByStarsAndName(a: IStarRating, b: IStarRating): number {
    if (Number(a.rating) === Number(b.rating)) {
      return a.name > b.name ? 1 : -1;
    } else if (Number(a.rating) > Number(b.rating)) {
      return -1;
    } else {
      return 1;
    }
  }
}

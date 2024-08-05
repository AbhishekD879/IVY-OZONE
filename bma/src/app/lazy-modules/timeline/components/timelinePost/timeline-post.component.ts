import { Component, Input, ChangeDetectionStrategy, OnInit, Output, EventEmitter, OnChanges } from '@angular/core';
import { IPost } from '@lazy-modules/timeline/models/timeline-post.model';
import environment from '@environment/oxygenEnvConfig';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { TimelineService } from '@lazy-modules/timeline/services/timeline.service';

@Component({
  selector: 'timeline-post',
  templateUrl: './timeline-post.component.html',
  styleUrls: ['./timeline-post.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TimelinePostComponent implements OnInit, OnChanges {
  @Input() post: IPost;
  @Input() first: string | boolean;
  @Input() priceButtonClass: string;
  @Input() isBrandLadbrokes: boolean;
  @Input() gtmModuleBrandName: string;
  @Output() readonly stateChange: EventEmitter<boolean> = new EventEmitter();
  cmsUri: string = environment.CMS_ROOT_URI;
  promoImageUrl: string;

  constructor(
    protected navigationService: NavigationService,
    protected timelineService: TimelineService
  ) {}

  ngOnInit(): void {
    if (this.post.template && this.post.template.topRightCornerImagePath) {
      this.promoImageUrl = this.getPromoImgUrl();
    }
  }

  ngOnChanges(): void {
    if (this.post.selectionEvent) {
      this.checkIfSelnAvailable();
    }
  }

  openUrl(url: string): void {
    if (url) {
      this.timelineService.gtm('navigation', {
        eventLabel: url,
        dimension114: this.post.template.name,
        dimension115: this.post.template.id
      }, this.gtmModuleBrandName);

      this.navigationService.openUrl(url, true);
      this.stateChange.emit(false);
    }
  }

  private getPromoImgUrl(): string {
    return `${this.cmsUri}${this.post.template.topRightCornerImagePath}`;
  }

  private checkIfSelnAvailable(): void {
    const event = this.post.selectionEvent.obEvent;
    const market = event.markets[0];
    const outcome = market.outcomes[0];

    this.post.selectionEvent.isNA =
      outcome.isDisplayed === false || outcome.isResulted ||
      market.isDisplayed === false || market.isResulted ||
      (market.isMarketBetInRun === false && event.rawIsOffCode === 'Y') ||
      event.isDisplayed === false || event.isResulted;
  }
}

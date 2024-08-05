import { ChangeDetectorRef, Component, Input, OnInit, OnChanges, OnDestroy, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';
import { ISurfaceBetModule } from '@shared/models/surface-bet-module.model';
import { ISurfaceBetEvent } from '@shared/models/surface-bet-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IOutputModule } from '@featured/models/output-module.model';
import { GA_TRACKING } from '../../constants/channel.constant';
@Component({
  selector: 'surface-bets-carousel',
  templateUrl: './surface-bets-carousel.component.html',
  styleUrls: ['./surface-bets-carousel.component.scss']
})
export class SurfaceBetsCarouselComponent implements OnInit, OnChanges, OnDestroy {
  @Input() module: ISurfaceBetModule | IOutputModule;

  public slides: number = 0;

  public carouselName: string = _.uniqueId('surface_bet_carousel');

  GATrackingObj = {
    event: GA_TRACKING.event,
    GATracking: {
    eventAction: GA_TRACKING.eventAction,
    eventCategory:GA_TRACKING.surfaceBet.eventCategory,
    eventLabel: ""
    }
  };

  constructor(
    protected changeDetRef: ChangeDetectorRef,
    protected pubsub: PubSubService,
  ) {}

  public trackByCard(index: number, item: ISurfaceBetEvent): string {
    return `${index}_${item.id}`;
  }

  public get isOneCard(): boolean {
    return this.module && this.module.data && this.module.data.length === 1;
  }
  public set isOneCard(value:boolean){}
  ngOnInit(): void {
    this.pubsub.subscribe(this.carouselName, this.pubsub.API.OUTCOME_UPDATED, () => {
        this.changeDetRef.detectChanges();
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.slides = this.module.data.filter(slide => slide.markets && slide.markets.length).length;
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.carouselName);
  }
}

import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'race-cards-controls',
  templateUrl: './race-cards-controls.component.html',
  styleUrls: [ './race-cards-controls.component.scss' ]
})
export class LadbrokesRaceCardsControlsComponent implements OnInit, OnChanges, OnDestroy {
  @Input() sortBy: string;
  @Input() market: IMarket;
  @Input() sortOptionsEnabled: boolean;
  @Input() isGreyhoundEdp: boolean;
  @Input() eventEntityId: string;
  @Input() isInfoHidden: {'info':boolean};

  @Output() readonly toggleShowOptions = new EventEmitter();
  @Output() readonly toggleShowOptionsGATracking = new EventEmitter();

  showMore: boolean = false;
  toggleInfoText: string = 'Show Info';
  showControl: boolean = false;

  constructor(private pubSubService: PubSubService) {}

  ngOnInit(): void {
    this.toggleShowOptions.emit(this.showMore);
    this.showControl = _.some(this.market.outcomes, (outcome: IOutcome) => !!outcome.racingFormOutcome || !!outcome.timeformData);
    this.pubSubService.subscribe('LadbrokesRaceCardsControlsComponent',
      `${this.pubSubService.API.SORT_BY_OPTION}${this.eventEntityId || ''}`, () => {
      });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.isInfoHidden && changes.isInfoHidden.currentValue) {
      if (changes.isInfoHidden.currentValue.info) {
        this.toggleInfoText = 'Hide Info';
        this.showMore = true;
      } else {
        this.toggleInfoText = 'Show Info';
        this.showMore = false;
      }
    }else{
      this.toggleInfoText = 'Show Info';
      this.showMore = false;
    }
    if (changes.market) {
      this.toggleShowOption(false);
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('LadbrokesRaceCardsControlsComponent');
  }

  toggleShowOption(value?: boolean, isGARequired?: boolean): void {
    this.showMore = value !== undefined ? value : !this.showMore;
    this.toggleInfoText = this.showMore ? 'Hide Info' : 'Show Info';
    this.toggleShowOptions.emit(this.showMore);

    if(isGARequired){
      this.toggleShowOptionsGATracking.emit(this.showMore); 
      }
  }

  toggleShowOptionChange(value?: boolean): void {
    this.toggleShowOption(value, true);
  }
}

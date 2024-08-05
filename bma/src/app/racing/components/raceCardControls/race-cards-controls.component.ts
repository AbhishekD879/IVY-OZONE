import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
@Component({
  selector: 'race-cards-controls',
  templateUrl: './race-cards-controls.component.html',
  styleUrls: [ './race-cards-controls.component.scss' ]
})
export class RaceCardsControlsComponent implements OnInit, OnChanges, OnDestroy {
  @Input() sortBy: string;
  @Input() market: IMarket;
  @Input() sortOptionsEnabled: boolean;
  @Input() isGreyhoundEdp: boolean;
  @Input() eventEntityId: string;
  @Input() isInfoHidden: {'info':boolean};

  @Output() readonly toggleShowOptions = new EventEmitter();
  @Output() readonly toggleShowOptionsGATracking = new EventEmitter();

  showMore: boolean = false;
  toggleInfoText: string = this.locale.getString('racing.showInfo');
  showControl: boolean = false;
  private cmpName = 'RaceCardsControlsComponent';

  constructor(private pubSubService: PubSubService, protected gtmService: GtmService, private locale: LocaleService) {}

  ngOnInit(): void {
    this.toggleShowOptions.emit(this.showMore);
    this.showControl = this.market.outcomes.some((outcome:IOutcome) => {
     return !!outcome.racingFormOutcome || !!outcome.timeformData;});
    this.pubSubService.subscribe(this.cmpName,
      `${this.pubSubService.API.SORT_BY_OPTION}${this.eventEntityId || ''}`, () => {
      });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.isInfoHidden && changes.isInfoHidden.currentValue) {
      if (changes.isInfoHidden.currentValue.info) {
        this.toggleInfoText =  this.locale.getString('racing.hideInfo');
        this.showMore = true;
      } else {
        this.toggleInfoText = this.locale.getString('racing.showInfo');
        this.showMore = false;
      }
    }else{
      this.toggleInfoText =  this.locale.getString('racing.showInfo');
      this.showMore = false;
    }
    if (changes.market) {
      this.toggleShowOption(false);
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.cmpName);
  }

  toggleShowOption(value?: boolean, isGARequired?: boolean): void {
    this.showMore = value !== undefined ? value : !this.showMore;
    this.toggleInfoText = this.showMore ? this.locale.getString('racing.hideInfo') : this.locale.getString('racing.showInfo');
    this.toggleShowOptions.emit(this.showMore); 

    if(isGARequired){
    this.toggleShowOptionsGATracking.emit(this.showMore); 
    }
  }

  toggleShowOptionChange(value?: boolean): void {
    this.toggleShowOption(value, true);
  }
}

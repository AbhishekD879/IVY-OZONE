import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { TemplateService } from "@app/shared/services/template/template.service";
import { StreamBetService } from '@lazy-modules/eventVideoStream/services/streamBet/stream-bet.service';
@Component({
  selector: 'sb-multiple-odds-market-item',
  templateUrl: './sb-multiple-odds-market-item.component.html',
  styleUrls: ['./sb-multiple-odds-market-item.component.scss']
})
export class SbMultipleOddsMarketItemComponent implements OnInit {
  @Input() market: IMarket;
  @Input() event: ISportEvent;
  @Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();
  newOutcomes;

  currTemplateNumber = 0;
  constructor(private templateService: TemplateService, private streamBetService: StreamBetService) {
  }

  ngOnInit(): void {
    let outcomes = [...this.market.outcomes];
    outcomes = this.templateService.sortOutcomesByPriceAndDisplayOrder(outcomes);    
    if(this.sortOutcomesDisplayOrder(outcomes) === 0) {
      outcomes = this.templateService.sortOutcomesByPrice(outcomes);      
    }
    this.newOutcomes = outcomes.slice(0,3);
    this.streamBetService.multiOddMarketCounter += 1;
    this.currTemplateNumber = this.streamBetService.multiOddMarketCounter;
  }

  sortOutcomesDisplayOrder(outcomes): number {
    let compareItemValue = 0;
    outcomes.sort((a, b) => {
      if (a.displayOrder > b.displayOrder) {
        compareItemValue = 1;
      }
      if (a.displayOrder < b.displayOrder) {
        compareItemValue =  -1;
      }      
    });
    return compareItemValue;
  }

  handleSelectionClick(market: IMarket) {
    this.selectionClickEmit.emit(market); 
  }

  ngAfterViewInit(): void {
    if(this.streamBetService.totalMultiOddMarketElemsCount && 
      this.currTemplateNumber === this.streamBetService.totalMultiOddMarketElemsCount){
      this.streamBetService.lastTemplateLoadedSubj.next();
    }
  }
}

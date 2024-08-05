import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'sb-grouped-market-templates',
  templateUrl: './sb-grouped-market-templates.component.html',
  styleUrls: ['./sb-grouped-market-templates.component.scss']
})

export class SbGroupedMarketTemplatesComponent implements OnInit {
  @Input() markets: IMarket[];
  @Input() eventEntity: ISportEvent;
  @Output() selectionClickEmit?: EventEmitter<IMarket> = new EventEmitter();
  marketOutcomePair: {outcome: IOutcome, market: IMarket};
  marketOutcomePairs = [];
  @Input() templateType: string;
  @Input() allMarkets: IMarket[];
  initialMarket;

  ngOnInit(): void {
    if(this.templateType === 'special-market') {
      // Handled Special market type grouping
      this.markets.forEach((market: IMarket)=> {
        market.outcomes.forEach((outcome: IOutcome)=> {
          this.marketOutcomePairs.push({outcome, market});
        });
      });
      this.marketOutcomePair = this.marketOutcomePairs.length && this.marketOutcomePairs[0];
      this.initialMarket = [this.markets[0]];
      // END - Handled Special market type grouping
    } else {
      this.initialMarket = [this.markets[0]];
    }    
  }

  handleSelectionClick(market: IMarket) {    
    this.selectionClickEmit.emit(market);    
  }

  getTrackById(index: number, entity: any) {
    return `${entity.id}_${index}`;
  }

  /**
   * Looping outcomes on market(s) - applicable for special market type
   * Looping markets - applicable for non-special market type
   * Displaying outcome (Outcome to be displayed is currently displaying outcome index+1)
   */
  getNextOutcome(): void {
    if(this.templateType === 'special-market') {
      const currentOutcomeIndex = this.marketOutcomePairs.indexOf(this.marketOutcomePair);
      if(currentOutcomeIndex < (this.marketOutcomePairs.length-1)) {
        this.marketOutcomePair = this.marketOutcomePairs[currentOutcomeIndex+1];
      } else {
        this.marketOutcomePair = this.marketOutcomePairs[0]; 
      }
    } else {
      const currentMarketIndex = this.markets.findIndex(market=>market.id===this.initialMarket[0].id);
      if(currentMarketIndex < (this.markets.length-1)) {
        this.initialMarket = [this.markets[currentMarketIndex+1]];
      } else {
        this.initialMarket = [this.markets[0]]; 
      }      
    }
  }

  /**
   * Looping outcomes on market(s) - applicable for special market type
   * Looping markets - applicable for non-special market type
   * Displaying outcome (Outcome to be displayed is currently displaying outcome index-1)
   */
  getPreviousOutcome(): void {
    if(this.templateType === 'special-market') {      
      const currentOutcomeIndex = this.marketOutcomePairs.indexOf(this.marketOutcomePair);
      const outcomesLength = this.marketOutcomePairs.length;
      if(currentOutcomeIndex  !== 0) {
        this.marketOutcomePair = this.marketOutcomePairs[currentOutcomeIndex-1];
      } else {
        this.marketOutcomePair = this.marketOutcomePairs[outcomesLength-1];
      }
    } else {
      const currentMarketIndex = this.markets.findIndex(market=>market.id===this.initialMarket[0].id);
      const marketsLength = this.markets.length;
      if(currentMarketIndex  !== 0) {
        this.initialMarket = [this.markets[currentMarketIndex-1]];
      } else {
        this.initialMarket = [this.markets[marketsLength-1]];
      }
    }
  }
}

import { Component, Input, OnInit } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import environment from '@environment/oxygenEnvConfig';
import * as _ from 'underscore';

@Component({
  selector: 'scorer',
  templateUrl: 'scorer.component.html',
  styleUrls: ['scorer.component.scss']
})

export class ScorerComponent implements OnInit {
  env:string = environment.brand;
  @Input() marketsGroup;
  @Input() markets: IMarket[];
  @Input() isExpanded: boolean;
  @Input() memoryId: string;
  @Input() memoryLocation: string;
  @Input() eventEntity: ISportEvent;

  isAllShow: boolean = false;
  allPlayers: IOutcome[] | IMarket[];
  groupPlayers: IMarket[] = [];
  limitCount: number = 0;
  teamName: string[];
  teamH: string;
  teamA: string;
  marketCount: number;

  constructor() {
  }

  ngOnInit(): void {
    if (this.marketsGroup.header) {
      this.allPlayers = this.groupPlayers;
    }else {
     this.teamName= this.eventEntity.name.split(' v ');
      this.teamH = this.teamName[0];
      this.teamA = this.teamName[1];
      this.marketsGroup.outcomes=_.sortBy(this.marketsGroup.outcomes, 'prices[0].priceDec');
      this.allPlayers = this.marketsGroup.outcomes;
      this.allPlayers.forEach(element => {
        if(element.originalOutcomeMeaningMinorCode === 'H'){
          element.teamName=this.teamH;
        } else if(element.originalOutcomeMeaningMinorCode === 'A'){
          element.teamName=this.teamA;
        }
        if(element.name === 'No Goalscorer'){
          this.marketsGroup.noGoalscorer=element;
        }
      });
      }
      this.marketCount=5;
  
  }

  /***
   * Get Selected Outcomes
   *
   * @param {IOutcome[]} outcomes
   * @returns {IOutcome[]}
   */
  selectedOutcomes(outcomes: IOutcome[] | IMarket[]): IOutcome[] | IMarket[] {
    return outcomes.slice(0, this.limitCount || this.marketCount);
  }

  selectedNoGoalOutcomes(outcomes: IOutcome[] | IMarket[]): IOutcome[] | IMarket[] {
    return outcomes;
  }

  /**
   * Toggle Button for Show All
   */
  toggleShow(): void {
    this.isAllShow = !this.isAllShow;
    this.limitCount = this.isAllShow ? this.allPlayers.length : this.marketCount;
  }
}
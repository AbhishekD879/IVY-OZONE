import { Component, Input, OnInit } from '@angular/core';
import { every } from 'underscore';

import { FiltersService } from '@core/services/filters/filters.service';
import { IOutcome } from '@core/models/outcome.model';


@Component({
  selector: 'post-spotlight',
  templateUrl: './post-spotlight.component.html'
})
export class PostSpotlightComponent implements OnInit {
  @Input() outcome: IOutcome;

  noDetails: boolean;
  sView: boolean;
  filter: string = 'summary';
  viewByFilters: string[] = [
    'summary',
    'details'
  ];
  /**
   * Initiate tabs title according to viewByFilters
   * Use in stripeTab directive
   */
  tabsTitle: object = {
    summary: 'sb.summary',
    details: 'sb.details'
  };

  private readonly details: string[] = ['age', 'draw', 'jockey', 'trainer', 'weight', 'formProviderRating', 'formGuide'];

  constructor(private filterService: FiltersService) {
  }

  ngOnInit() {
    this.noDetails = every(this.details, detail => this.outcome.racingFormOutcome && !this.outcome.racingFormOutcome[detail]);
    this.filterService.removeLineSymbol(this.outcome.name);
    this.sView = !this.outcome.racingFormOutcome.overview;
  }

  /**
   * Horse Weight conversion (lb -> st)
   * @params {string}
   * @returns {string}
   */
  correctingWeight(weight: string): string {
    // receive string like: "Pounds,weight,";
    const clearWeigth: number = Number(weight.replace(/\D+/g, ''));

    // Weight in stones = weight / 14;
    const weightInStones: number = parseInt(`${ clearWeigth / 14 }`, 10);

    // Total weight = weight in stones * 14;
    const totalWeight: number = weightInStones * 14;

    // Lb part = weight - total weigth;
    const secondPart: number = clearWeigth - totalWeight;

    let tempStr: string;
    if (secondPart > 0) {
      tempStr = `-${secondPart}lb`;
    } else {
      tempStr = '';
    }

    return `${weightInStones}st${tempStr}`;
  }
}

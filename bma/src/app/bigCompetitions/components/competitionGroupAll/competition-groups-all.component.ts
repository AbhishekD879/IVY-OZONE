import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { BigCompetitionsLiveUpdatesService } from '../../services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IGroupModule, IGroupModuleData, IGroupTeam } from '@app/bigCompetitions/models/big-competitions.model';
import { IMarket } from '@core/models/market.model';


@Component({
  selector: 'competition-groups-all',
  templateUrl: './competition-groups-all.component.html'
})
export class CompetitionGroupAllComponent implements OnInit {
  @Input() moduleConfig: IGroupModule;

  events: ISportEvent[];
  id: string;
  group: IGroupModuleData;
  markets: IMarket[];
  numberQualifiers: number;

  constructor(
    private bigCompetitionLiveUpdatesService: BigCompetitionsLiveUpdatesService,
  ) {
    this.id = _.uniqueId('GroupAllComponent-');
  }

  ngOnInit(): void {
    this.moduleConfig.isExpanded = true;
    this.numberQualifiers = this.moduleConfig.groupModuleData.numberQualifiers;
    this.group = (this.moduleConfig.groupModuleData.data && this.moduleConfig.groupModuleData.data[0]);
    if (this.group.ssEvents) {
      this.events = this.group.ssEvents;
    }
    this.markets = _.flatten(_.pluck(this.events, 'markets')) || [];
  }


  /**
   * Get qualified class if needed for single team
   * @param {number} index
   * @returns {string}
   */
  getQualifiedClass(index: number): string {
    return index + 1 <= this.numberQualifiers ? 'team-qualified' : '';
  }

  trackByMarket(i: number, element: IMarket): string {
    return `${i}_${element.id}`;
  }

  trackByTeam(i: number, element: IGroupTeam): string {
    return `${i}_${element.name}`;
  }

  /**
   * Check if selection is undisplayed on EVT/MKT/SELN level
   * @param {Object} event
   * @param {Object} market
   * @param {number} index
   * @returns {Boolean}
   */
  isSelnDisplayed(event: ISportEvent, market: IMarket, index: number): boolean {
    if (event.isDisplayed && market.isDisplayed && market.outcomes) {
      const selection = this.getSeln(market, index);
      return selection && selection.isDisplayed;
    }
    return false;
  }

  /**
   * Get Selection if exist
   * @param {Object} market
   * @param {number} indext
   * @returns {Object} selection obj
   */
  getSeln(market: IMarket, index: number): IOutcome {
    return _.find(market.outcomes, (outcome: IOutcome) => outcome.name === this.group.teams[index].name);
  }

  /**
   * Subscribe/unsubscribe live updates for competition events(Live Serve MS) when accordion is expanded/collapsed
   */
  accordionHandler(): void {
    this.moduleConfig.isExpanded = !this.moduleConfig.isExpanded;

    if (this.moduleConfig.isExpanded) {
      this.bigCompetitionLiveUpdatesService.subscribe(this.events);
    } else {
      this.bigCompetitionLiveUpdatesService.unsubscribe(this.events);
    }
  }

}

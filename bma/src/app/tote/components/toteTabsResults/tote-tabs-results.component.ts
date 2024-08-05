import { of as observableOf } from 'rxjs';

import { concatMap } from 'rxjs/operators';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Router, ActivatedRoute } from '@angular/router';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { TOTE_CONFIG } from '../../tote.constant';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IToteEvent } from './../../models/tote-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { ToteService } from '@app/tote/services/mainTote/main-tote.service';
import { UserService } from '@core/services/user/user.service';
import { IToteTabsTitle } from '@app/tote/models/tote-event-tab.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ITab, ITabActive } from '@core/models/tab.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { NavigationService } from '@coreModule/services/navigation/navigation.service';

@Component({
  selector: 'tote-tabs-results',
  templateUrl: './tote-tabs-results.component.html'
})
export class ToteTabsResultsComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  // TODO: add model when racing routing will be migrated
  responseError: Error;
  racing: any;
  filter: string;
  oddsFormat: string;
  switchers: ISwitcherConfig[];

  isImgNotLoad: boolean[] = [];
  activeTab: ITabActive = { id: TOTE_CONFIG.resultFilters[0] };
  viewByFilters: string[] = TOTE_CONFIG.resultFilters;
  images: string = environment.INT_TOTE_IMAGES_ENDPOINT;
  svgId: string = '#icon-horse-racing';
  // Initiate tabs title according to viewByFilters
  // Use in stripeTab directive
  tabsTitle: IToteTabsTitle = {
    'by-latest-results': 'sb.byLatestResults',
    'by-meetings': 'sb.byMeetings'
  };


  constructor(
    private raceOutcomeDetails: RaceOutcomeDetailsService,
    private toteService: ToteService,
    private location: Location,
    private filterService: FiltersService,
    private router: Router,
    private route: ActivatedRoute,
    private user: UserService,
    private pubSubService: PubSubService,
    private navigationService: NavigationService
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    this.oddsFormat = this.user.oddsFormat;
    // Switchers config for results tab
    this.switchers = [{
      onClick: () => this.goToFilter(TOTE_CONFIG.resultFilters[0]),
      viewByFilters: TOTE_CONFIG.resultFilters[0],
      name: `tt.${TOTE_CONFIG.resultFiltersName[0]}`
    }, {
      onClick: () => this.goToFilter(TOTE_CONFIG.resultFilters[1]),
      viewByFilters: TOTE_CONFIG.resultFilters[1],
      name: `tt.${TOTE_CONFIG.resultFiltersName[1]}`
    }];
    this.pubSubService.subscribe('toteResults', this.pubSubService.API.RELOAD_COMPONENTS, this.reloadResults.bind(this));
    this.init();
  }

  init() {
    this.route
      .params.pipe(
      concatMap((params) => {
        this.filter = params.filter;
        // redirect to filer from resultFilters list
        if (!_.contains(TOTE_CONFIG.resultFilters, this.filter)) {
          this.router.navigateByUrl(TOTE_CONFIG.tabs.find((tab: ITab) => tab.title === 'results').url);
          this.filter = TOTE_CONFIG.resultFilters[0];
          return observableOf(null);
        }
        return this.toteService.getToteResults();
      }))
      .subscribe(resultsData => {
        if (resultsData === null) { return; }
        // TODO: add model when racing routing will be migrated
        const timeDescendingComparator = (firstEvent, secondEvent) => secondEvent.startTime - firstEvent.startTime;

        this.racing = resultsData;
        this.racing.events = this.racing.events.sort(timeDescendingComparator);
        this.racing.typeNamesArray = this.racing.typeNamesArray.sort();

        this.hideSpinner();
      }, err => {
        this.showError();
      });
  }

  reloadResults(): void {
    this.showSpinner();
    this.init();
  }

  sortEventsByTimeAscending(eventsArray) {
    const timeAscendingComparator = (firstEvent, secondEvent) => firstEvent.startTime - secondEvent.startTime;
    return eventsArray.sort(timeAscendingComparator);
  }

  getSortedPrizePlaces(outcomes) {
    const checkIfPlaceExist = outcome => outcome.results.outcomePosition;
    return outcomes.filter(checkIfPlaceExist)
      .sort(this.placeAscedingComparator)
      .slice(0, 4);
  }

  // Action on filter change (By time, By meeting)
  goToFilter(filterName: string): void {
    this.filter = filterName;
    const path = `/tote/results/${filterName}`;

    if (path !== this.location.path()) {
      this.navigationService.openUrl(path, true, true);
    }
  }

  /**
   * Returns string in format 'time event name country' to display on collapsible containers
   * @param {Object} eventEntity
   * @returns {String}
   */
  byTimeContainerHeader(eventEntity: IToteEvent): string {
    return `${eventEntity.localTime} ${eventEntity.typeName} ${eventEntity.country}`;
  }

  /**
   * Returns delimited string with Jockey and trainer names
   * @param {Object} outcomeEntity
   * @returns {String}
   */
  getJockeyAndTrainer(outcomeEntity: IOutcome): string {
    return `${outcomeEntity.racingFormOutcome.jockey} / ${outcomeEntity.racingFormOutcome.trainer}`;
  }

  areEventsAvailable(): boolean {
    return this.racing && this.racing.events && this.racing.events.length;
  }

  /**
   * Image Source for Silks
   * @param {string} silkName
   * @returns {string}
   */
  imgSrc(silkName: string): string {
    return `${this.images}/${silkName}`;
  }

  removeLineSymbol(name: string): string {
    return this.filterService.removeLineSymbol(name);
  }

  isLatestResults(filter: string): boolean {
    return filter === 'by-latest-results';
  }

  isByMeetings(filter: string): boolean {
    return filter === 'by-meetings';
  }

  trackByIndex(index: number): number {
    return index;
  }

  isGenericSilk(eventEntity: IToteEvent, outcomeEntity: IOutcome): boolean {
    return this.raceOutcomeDetails.isGenericSilk(eventEntity, outcomeEntity);
  }

  isNumberNeeded(eventEntity: IToteEvent, outcomeEntity: IOutcome): boolean {
    return this.raceOutcomeDetails.isNumberNeeded(eventEntity, outcomeEntity);
  }

  isValidSilkName(outcome: { silkName: string }): boolean {
    return this.raceOutcomeDetails.isValidSilkName(outcome);
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('toteResults');
  }

  private placeAscedingComparator(firstOutcome, secondOutcome) {
    return Number(firstOutcome.results.outcomePosition) - Number(secondOutcome.results.outcomePosition);
  }
}

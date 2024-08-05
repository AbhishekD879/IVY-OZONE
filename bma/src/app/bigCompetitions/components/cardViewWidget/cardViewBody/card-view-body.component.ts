import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'card-view-body',
  templateUrl: './card-view-body.component.html',
  styleUrls: ['./card-view-body.component.scss']
})
export class CardViewBodyComponent implements OnInit {
  @Input() event: IBigCompetitionSportEvent;
  @Input() viewType: string;

  sportName: string;
  isFootball: boolean;
  marketsCount: string;
  EDPpath: string;

  constructor(private sportEventHelperService: SportEventHelperService,
              private router: Router,
              private routingHelperService: RoutingHelperService,
              private routingState: RoutingState,
              private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.sportName = this.event.categoryName && this.event.categoryName.toLowerCase();
    this.isFootball = this.sportEventHelperService.isFootball(this.event);
    this.marketsCount = `+${this.sportEventHelperService.getMarketsCount(this.event)}`;
    this.EDPpath = `/${this.routingHelperService.formEdpUrl(this.event)}`;
  }

  /**
   * Check if live stream is available for event
   * @returns {boolean}
   */
  isStreamAvailable(): boolean {
    return this.sportEventHelperService.isStreamAvailable(this.event);
  }

  /**
   * Check if market counter should be shown
   * @returns {boolean}
   */
  showMarketsCount(): boolean {
    return this.sportEventHelperService.showMarketsCount(this.event);
  }

  /**
   * Returns current location
   */
  getLocation(): string {
    return this.routingState.getRouteParam('name', this.route.snapshot);
  }

  /**
   * Check if live card should be shown
   * @returns {boolean}
   */
  get isInPlay(): boolean {
    return this.viewType === 'inplay';
  }
  set isInPlay(value:boolean){}
  goToEvent($event: MouseEvent): void {
    $event.preventDefault();
    this.router.navigate([this.EDPpath]);
  }
}

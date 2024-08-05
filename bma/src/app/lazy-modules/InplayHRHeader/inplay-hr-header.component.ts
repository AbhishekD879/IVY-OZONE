import { Component, OnInit, Input, ViewEncapsulation } from '@angular/core';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { Router } from '@angular/router';
import { EventService } from '@sb/services/event/event.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'inplay-hr-header',
  templateUrl: './inplay-hr-header.component.html',
  styleUrls: ['./inplay-hr-header.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})

export class InplayHRHeaderComponent implements OnInit{
  @Input() eventEntity: ISportEvent;
  @Input() showRaceDetails: boolean = false;  
  seeAllText = '';
  watchText = '';
  hrHeaderClasses: { [key: string]: boolean };

  constructor(
    private routingHelperService: RoutingHelperService,
    private router: Router,
    private eventService: EventService,
    public locale: LocaleService
  ) { }

  ngOnInit(): void {
    this.hrHeaderClasses = this.setHeaderClass();
    this.seeAllText = this.locale.getString('sb.seeAll');
    this.watchText = this.locale.getString('sb.watch');
  }  

  /**
     * Set Header CSS Class
     * @returns {{toggle-header: boolean, inner-header: (string|boolean)}}
     */
  setHeaderClass(): { [key: string]: any } {
    const classes = {
        'header-details': !this.showRaceDetails,
        'header-race-details': this.showRaceDetails
    };
    return classes;
  }

  /**
   * return whether live streaming available or not
   * @param {ISportEvent} eventEntity
   * @returns {boolean}
   */
  isStreamLabelShown(event: ISportEvent): boolean {
    return this.eventService.isLiveStreamAvailable(event).liveStreamAvailable;
  }

  /**
   * return the EDP URL of the selected event
   * @param {ISportEvent} eventEntity
   * @returns {string}
   */
  formEdpUrl(eventEntity: ISportEvent): string {
    return this.routingHelperService.formEdpUrl(eventEntity);
  }

  /**
   * navigate to EDP URL
   * @param {ISportEvent} eventEntity
   */
  trackEvent(entity: ISportEvent): void {        
    const link = this.formEdpUrl(entity);
    this.router.navigateByUrl(link);
  }

  /**
   * Stopping propagation
   * @param {MouseEvent} event
   */
  handleEvent(event: MouseEvent) {
    event.stopPropagation();
  }
  
}

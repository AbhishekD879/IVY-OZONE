import { Component, Input, Output, OnInit, EventEmitter } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { ActivatedRoute, Router } from '@angular/router';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LpAvailabilityService } from '@app/core/services/lpAvailability/lp-availability.service';

@Component({
  selector: 'racing-panel',
  templateUrl: 'racing-panel.component.html',
  styleUrls: ['./racing-panel.component.scss']
})
export class RacingPanelComponent implements OnInit {
  @Input() events: ISportEvent[];
  @Input() eventId?: string | number;
  @Input() title?: string;
  @Input() isShowName?: boolean = true;
  @Input() origin: string = '';
  @Input() isTote: boolean = false;
  @Input() isHrEdp?: boolean;
  @Input() showSwitcher?: boolean = true;
  @Input() groupFlagText?: string;
  @Input() showSignPost: boolean = false;
  @Input() ladsTabNav: boolean = false;
  @Input() raceType: string;
  @Output() readonly clickFunction?: EventEmitter<ISportEvent> = new EventEmitter();
  eventStatusData: any = {};
  filter: string;
  titleText: string;
  removeEventnameId: string = '';
  routeparams: string = '';
  constructor(
    private localeService: LocaleService,
    private router: Router,
    private routingHelperService: RoutingHelperService,
    private seoDataService: SeoDataService, 
    protected pubsub: PubSubService,
    protected gtmService: GtmService,
    private lpAvailabilityService: LpAvailabilityService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.events = this.events && this.events.filter(event => event.categoryId !== '39')
    this.titleText = this.title ? this.getTitle(this.title) : '';
    this.route.params.subscribe((params)=>{
    this.routeparams = params['display'];
    })
  }

  trackById(index: number, event: ISportEvent): string {
    return event.id ? `${index}${event.id}` : index.toString();
  }

  goToEvent(event: ISportEvent, $event: Event): void {

    if (this.clickFunction.observers.length) {
      this.clickFunction.emit(event);
    } else {
      const link = this.formEdpUrl(event);
      this.router.navigateByUrl(link);
    }
    if(!this.showSwitcher){
      this.eventRacesGATracker(event);
      this.pubsub.publish('MEETING_OVERLAY_FLAG',{id:event.id,flag: false});
    }
    $event.preventDefault();
  }

  eventRacesGATracker(event: ISportEvent) {
    this.gtmService.push('trackEvent', {    
        eventAction: 'meetings',
        eventCategory: event.categoryId == '21' ? 'horse racing' : 'greyhounds',
        eventLabel: `navigation – ${this.groupFlagText.toLowerCase()}`,
        categoryID: event.categoryId,
        typeID: event.typeId,
        eventID: event.id
      });
  }

  goToSeo(eventEntity: ISportEvent): void {
    const edpUrl: string = this.routingHelperService.formEdpUrl(eventEntity);
    this.seoDataService.eventPageSeo(eventEntity, edpUrl);
  }

  formEdpUrl(event: ISportEvent): string {
    let eventUrl = '';
    if (this.isTote) {
      eventUrl += `/tote/event/${event.id}`;
    } else {
      eventUrl += this.routingHelperService.formResultedEdpUrl(event, this.origin ? `?origin=${this.origin}` : '');
    }
    return eventUrl;
  }

  /**
   * handles the child's ouput event emitter
   * @param - output event data
   * @return - void
   */
  handleOutput(event: ILazyComponentOutput): void {
    if(event.output === 'removeEventNameEmitter') {
      this.removeEventnameId = event.value;
    } else if(event.output === 'eventStatusUpdate') {
      this.eventStatusData[event.value.id] = event.value.data
    }
  }

  private getTitle(title: string): string {
    const regex = /(\(.*\))/g;
    const match = title.match(regex);
    if (title.match(/\./)) {
      return this.localeService.getString(title);
    } else if (match) {
      return `${title.replace(regex, '')}<b>${match[0]}</b>`;
    }
    return title;
  }

  isLpAvailable(event: ISportEvent): boolean {
     return this.lpAvailabilityService.check(event);
  }

  /**
   * #OZONE-8265 Story
   * displays the early price sign post
  * Horse racing - Only tommorow && not resulted && not race off && lpAvailable
  * GreyHound - only today and tommorow and not resulted && not race off && lpAvailable
   * @param - events
   * @return - boolean
   */
  isEarlyPricesAvailable(eventsData: ISportEvent[]): boolean {
    const checkIsDayValue = eventsData.every((event) => this.raceType === 'horseracing' ? (event.correctedDayValue !== 'racing.today') : true);
    const isLp = eventsData.filter((event) => {
      let raceOver = false;
      if (this.eventStatusData[event.id]) {
        raceOver = [this.localeService.getString('racing.raceOff'),
        this.localeService.getString('racing.liveNow'),
        this.localeService.getString('racing.inPlay'),
        this.localeService.getString('racing.result')].indexOf(this.eventStatusData[event.id].title) !== -1;
      }
      if (event.isStarted || event.isLiveNowEvent || event.isResulted || event.rawIsOffCode === 'Y' || raceOver) {
        return false;
      }
      return event.markets.some(market => market.isLpAvailable);
    });
    return (checkIsDayValue && isLp.length > 0);
  }

  /**
   * #OZONE-8265 Story
   * align early price sign post when first event is resulted      
   * @param - events
   * @return - boolean
   */
  hasResult(eventsData: ISportEvent[]): boolean {
    return eventsData[0].isResulted ||  eventsData[0].rawIsOffCode === 'Y' ? true : false;
  }

  /**
   * #OZONE-8265 Story
   * get early price sign post title from locale    
   * @param - none
   * @return - string
   */
  earlySignPostTitle(): string {
    return this.localeService.getString(`sb.earlyPricesAvailable`);
  }
}
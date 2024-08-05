import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { IOutputModule } from '@featured/models/output-module.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { TimeService } from '@core/services/time/time.service';

@Component({
  selector: 'odds-card-featured-offer',
  templateUrl: 'odds-card-featured-offer.component.html',
  styleUrls: ['./odds-card-featured-offer.component.scss']
})

export class OddsCardFeaturedOfferComponent implements OnInit {
  @Input() featuredModule: IOutputModule;
  @Input() event: ISportEvent;
  @Input() isOutright: boolean;
  @Input() isStream: boolean;
  @Input() gtmModuleTitle?: string;

  isFavoriteShown: boolean;
  multipleClassName: string;
  typeTitle: string;
  className: string;
  eventTime: string;
  outcome: IOutcome;
  isSmartBoosts: boolean;
  eventName: string;
  wasPrice: string;

  private isMultipleEvent: boolean;

  constructor(private sportEventHelperService: SportEventHelperService,
              private routingHelperService: RoutingHelperService,
              private router: Router,
              private templateService: TemplateService,
              private smartBoostsService: SmartBoostsService,
              private timeService: TimeService) {}

  ngOnInit(): void {
    const isEnhanced = this.featuredModule.isEnhanced;
    const isFootball = this.sportEventHelperService.isFootball(this.event);
    const isSpecialEvent = this.sportEventHelperService.isSpecialEvent(this.event, true);

    this.outcome = this.event.markets[0].outcomes[0];
    this.isMultipleEvent = this.templateService.isMultiplesEvent(this.event);
    this.isFavoriteShown = isFootball && !this.isOutright && !this.isMultipleEvent && !isSpecialEvent;
    this.className = isEnhanced ? 'enhanced-offer' : 'special-offer';
    this.typeTitle = isEnhanced ? 'enhanced' : 'special';
    this.eventTime = this.timeService.getEventTime(this.event.startTime);
    this.isSmartBoosts = this.smartBoostsService.isSmartBoosts(this.event.markets[0]);

    if (this.isSmartBoosts) {
      const parsedName = this.smartBoostsService.parseName(this.event.name);
      this.eventName = parsedName.name;
      this.wasPrice = parsedName.wasPrice;
      this.className = `${this.className} smart-boosts`;
    } else {
      this.eventName = this.event.name;
    }

    // Should not redirect if it is enhanced multiples event
    if (this.isMultipleEvent) {
      this.multipleClassName = 'featured-no-pointer';
    }
  }

  /**
   * Redirects to event details page
   * @param justReturn
   * @param event
   * @returns {*}
   */
  goToEvent(): void {
    const edpUrl: string = this.routingHelperService.formEdpUrl(this.event);

    if (!this.isMultipleEvent && !this.event.isFinished) {
      this.router.navigateByUrl(edpUrl);
    }
  }
}

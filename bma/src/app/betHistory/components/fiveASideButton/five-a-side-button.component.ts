import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IBetHistoryLeg } from '@betHistoryModule/models/bet-history.model';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
@Component({
  selector: 'five-a-side-button',
  templateUrl: './five-a-side-button.component.html',
  styleUrls: ['./five-a-side-button.component.scss'],
})
export class FiveASideComponent {
  @Input() event: ISportEvent;
  @Input() leg: IBetHistoryLeg;

  catergoryName: string;
  className: string;
  typeName: string;

  constructor(
    protected router: Router,
    protected routingHelperService: RoutingHelperService,
    protected gtmService: GtmService,
    protected pubsub: PubSubService
  ) { }

/**
 * to navigate to five a side pitch
 * @return {void}
 */
  navigateToFiveASide(): void {
    const categoryName: string = this.leg && this.leg.part[0] && this.leg.part[0].outcome[0] &&
    this.leg.part[0].outcome[0].eventCategory.name;
    const className: string = this.leg && this.leg.part[0] && this.leg.part[0].outcome[0] &&
    this.leg.part[0].outcome[0].eventClass.name;
    const typeName: string = this.leg && this.leg.part[0] && this.leg.part[0].outcome[0] &&
    this.leg.part[0].outcome[0].eventType.name;
    const name: string = this.leg && this.leg.part[0] && this.leg.part[0].outcome[0] &&
    this.leg.part[0].outcome[0].event.name;
    const id = this.leg && this.leg.part[0] && this.leg.part[0].outcome[0] &&
    this.leg.part[0].outcome[0].event.id;
    const url: string = this.routingHelperService.formFiveASideUrl(categoryName, className, typeName, name, id);
    this.router.navigateByUrl(`/event${url}/5-a-side/pitch`);
    this.pubsub.publish('SHOW_FIVE_A_SIDE', true);
    const gtmData = {
      eventCategory: '5-A-Side',
      eventAction: 'click',
      eventLabel: 'Go to 5-a-side'
    };
    this.gtmService.push('trackEvent', gtmData);
  }

}

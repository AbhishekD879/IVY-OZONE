import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IBetHistoryLeg } from '@betHistoryModule/models/bet-history.model';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { FiveASideComponent } from '@app/betHistory/components/fiveASideButton/five-a-side-button.component';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';
@Component({
  selector: 'casino-mybets-five-a-side-button',
  templateUrl: './casino-mybets-five-a-side-button.component.html',
  styleUrls: ['../../../../betHistory/components/fiveASideButton/five-a-side-button.component.scss'],
})
export class CasinoMyBetsFiveASideComponent extends FiveASideComponent {
  @Input() event: ISportEvent;
  @Input() leg: IBetHistoryLeg;
  @Input() isMyBetsInCasino: boolean = false;

  catergoryName: string;
  className: string;
  typeName: string;
  showLeavingCasinoDialog: boolean = false;
  readonly homePageUrl: string = environment.HOME_PAGE;

  constructor(
    router: Router,
    routingHelperService: RoutingHelperService,
    gtmService: GtmService,
    pubsub: PubSubService,
    private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService
  ) {
    super(router, routingHelperService, gtmService, pubsub);
  }

/**
 * to navigate to five a side pitch
 * @return {void}
 */
  navigateToFiveASide(): void {
    if (!!this.isMyBetsInCasino && !this.showLeavingCasinoDialog) {
      const url: string = this.generateUrl();
      this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.goToSportsCTABtnClick(eznavconfbox.goTofiveAsideCta, this.homePageUrl + `/event${url}/5-a-side/pitch`);
    } else {
      const url: string = this.generateUrl();
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

  /**
   * generate the redirect URL
   * @returns url as string
   */
  generateUrl(): string {
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
    return this.routingHelperService.formFiveASideUrl(categoryName, className, typeName, name, id);
  }

  /**
   * triggers on click of confirmation dialog popup
   * @param event component Event
   */
  confirmationDialogClick(event: ILazyComponentOutput): void {
    const url: string = this.generateUrl();
    
    this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.confirmationPopUpClick(
      event, this.homePageUrl + `/event${url}/5-a-side/pitch`);
  }
}

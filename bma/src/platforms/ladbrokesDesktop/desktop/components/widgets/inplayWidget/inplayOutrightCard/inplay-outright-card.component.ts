import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';

@Component({
  selector: 'inplay-outright-card',
  templateUrl: './inplay-outright-card.component.html',
  styleUrls: ['./inplay-outright-card.component.scss']
})
export class InplayOutrightCardComponent implements OnInit {
  @Input() event: any;

  market: IMarket;
  outcomes: IOutcome[];

  isMarketExists: boolean = true;

  constructor(
    private routingHelperService: RoutingHelperService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.market = this.event.markets[0];
    this.outcomes = this.market && this.market.outcomes;
    if (!this.market) {
      this.isMarketExists = false;
    }
  }

  trackById(index: number, outcome: IOutcome): string {
    return outcome.id;
  }

  goToEDP(event: ISportEvent): void {
    const edpUrl: string = this.routingHelperService.formEdpUrl(event);

    this.router.navigateByUrl(edpUrl);
  }
}

import { Component, Input, OnInit } from '@angular/core';

import { IMarket } from '@core/models/market.model';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { RacingYourCallService } from '@core/services/racing/racingYourCall/racing-your-call.service';

@Component({
  selector: 'racing-tab-yourcall',
  templateUrl: './racing-tab-yourcall.html'
})
export class RacingTabYourcallComponent implements OnInit {
  @Input() racing;

  staticBlockType: string;
  accumulatedMarkets: IMarket[];

  constructor(
    private racingYourCallService: RacingYourCallService,
    private racingGAService: RacingGaService
  ) { }

  ngOnInit() {
    this.staticBlockType = 'yourcall-racing';
    this.accumulatedMarkets = [];
    this.racingYourCallService.prepareData(this.accumulatedMarkets, this.racing);
  }

  trackGa(event): void {
    const eventElement = event.target;

    if (eventElement.tagName === 'A' && /twitter.com/.test(eventElement.href)) {
      this.racingGAService.trackYourcallTwitter();
    }
  }
}

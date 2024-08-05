import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';

@Component({
  selector: 'yourcall-market',
  templateUrl: './your-call-market.component.html'
})
export class YourCallMarketComponent implements OnInit, OnDestroy {
  @Input() type;
  @Input() game;
  @Input() market;
  @Input() limit;

  loading: boolean;

  constructor(
    private yourCallMarketsService: YourcallMarketsService
  ) { }

  ngOnInit(): void {
    this.loading = ['switcher', 'group'].includes(this.market.type);

    this.yourCallMarketsService.onMarketToggled();
  }

  ngOnDestroy(): void {
    this.yourCallMarketsService.onMarketToggled();
  }

  marketLoaded(): void {
    this.loading = false;
  }
}

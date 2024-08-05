import { Component, ChangeDetectionStrategy } from '@angular/core';
import { YourCallMarketPlayerBetsComponent } from '@yourcall/components/yourCallMarketPlayerBets/your-call-market-player-bets.component';

@Component({
  selector: 'yourcall-market-player-bets',
  templateUrl: '../../../../../app/yourCall/components/yourCallMarketPlayerBets/your-call-market-player-bets.component.html',
  styleUrls: ['./your-call-market-player-bets.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesYourCallMarketPlayerBetsComponent extends YourCallMarketPlayerBetsComponent {}

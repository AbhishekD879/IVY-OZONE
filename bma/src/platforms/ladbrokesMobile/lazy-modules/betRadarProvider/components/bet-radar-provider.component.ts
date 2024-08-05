import {
    Component,
    ChangeDetectionStrategy,
  } from '@angular/core';
  import { BetRadarProviderComponent } from '@lazy-modules/betRadarProvider/components/bet-radar-provider.component';
  @Component({
    selector: 'bet-radar-provider',
    templateUrl: './bet-radar-provider.html',
    styleUrls: ['./bet-radar-provider.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
  })
  export class LadbrokesBetRadarProviderComponent extends BetRadarProviderComponent {}

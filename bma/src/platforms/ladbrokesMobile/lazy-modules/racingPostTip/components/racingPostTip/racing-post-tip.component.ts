import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
  RacingPostTipComponent as CoralRacingPostTipComponent
} from '@app/lazy-modules/racingPostTip/components/racingpostTip/racing-post-tip.component';
@Component({
  selector: 'racing-post-tip',
  templateUrl: './../../../../../../app/lazy-modules/racingPostTip/components/racingpostTip/racing-post-tip.component.html',
  styleUrls: ['./racing-post-tip.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LadbrokesRacingPostTipComponent extends CoralRacingPostTipComponent {

}

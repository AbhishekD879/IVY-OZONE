import { Component, ChangeDetectionStrategy } from '@angular/core';
import { RacingPostVerdictComponent } from '@app/lazy-modules/racingPostVerdict/racing-post-verdict.component';


@Component({
  selector: 'racing-post-verdict',
  templateUrl: 'racing-post-verdict.component.html',
  styleUrls: ['racing-post-verdict.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class DesktopRacingPostVerdictComponent extends RacingPostVerdictComponent {

}


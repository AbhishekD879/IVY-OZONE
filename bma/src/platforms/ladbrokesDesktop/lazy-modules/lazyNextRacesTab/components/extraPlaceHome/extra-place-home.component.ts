import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ExtraPlaceHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/extraPlaceHome/extra-place-home.component';

@Component({
  selector: 'extra-place-home-module',
  templateUrl: 'extra-place-home.component.html',
  styleUrls: [
    '../../../../../../app/lazy-modules/lazyNextRacesTab/components/extraPlaceHome/extra-place-home.component.scss',
    './extra-place-home.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesExtraPlaceHomeComponent extends ExtraPlaceHomeComponent {}

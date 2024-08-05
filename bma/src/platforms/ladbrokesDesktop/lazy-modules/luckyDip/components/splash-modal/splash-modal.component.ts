import { Component } from '@angular/core';
import { SplashModalComponent } from '@app/lazy-modules/luckyDip/components/splash-modal/splash-modal.component';

@Component({
  selector: 'splash-modal',
  templateUrl: '../../../../../../app/lazy-modules/luckyDip/components/splash-modal/splash-modal.component.html',
  styleUrls: ['../../../../../../app/lazy-modules/luckyDip/components/splash-modal/splash-modal.component.scss','splash-modal.component.scss']
})

export class LadsDeskSplashModalComponent extends SplashModalComponent {}
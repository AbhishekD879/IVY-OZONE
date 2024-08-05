import { Directive, HostListener } from '@angular/core';
import { StorageService } from '@core/services/storage/storage.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BackButtonService } from '@coreModule/services/backButton/back-button.service';

// eslint-disable-next-line
@Directive({ selector: '[last-made-bet]' })
export class LastMadeBetDirective {
  locationPath: string;

  constructor(
    private backButtonService: BackButtonService,
    private storage: StorageService,
    private windowRef: WindowRefService
  ) {
   // TODO: Route rewrite to use
   this.locationPath = this.windowRef.nativeWindow.location.hash;
  }

  @HostListener('click', [])
  onClick() {
    this.storage.set('lastMadeBet', this.locationPath);

    // Need for done button
    if (this.locationPath.indexOf('event') > 1) {
        const segmentsArray = this.backButtonService.getSegmentsArray();
        this.storage.set('lastMadeBetSport', segmentsArray[segmentsArray.length - 1]);
    }
  }

}

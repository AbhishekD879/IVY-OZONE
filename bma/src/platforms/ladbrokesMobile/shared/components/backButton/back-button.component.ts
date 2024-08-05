import { Component, HostListener } from '@angular/core';
import { BackButtonService } from '@core/services/backButton/back-button.service';

@Component({
    selector: 'back-button',
    template: `<a [i18n]="'bma.back'" class="lads-back-btn" data-crlat="btnBack" ></a>`,
})

export class BackButtonComponent {
  constructor(
    private backButtonService: BackButtonService
  ) {}

  @HostListener('click') redirect() {
    this.backButtonService.redirectToPreviousPage();
  }
}

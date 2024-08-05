import { Directive, HostListener } from '@angular/core';
import { BackButtonService } from '@coreModule/services/backButton/back-button.service';

@Directive({
  // eslint-disable-next-line
  selector: '[back-button]'
})
export class BackButtonDirective {

  constructor(
    private backButtonService: BackButtonService
  ) {}

  @HostListener('click') redirect() {
    this.backButtonService.redirectToPreviousPage();
  }
}

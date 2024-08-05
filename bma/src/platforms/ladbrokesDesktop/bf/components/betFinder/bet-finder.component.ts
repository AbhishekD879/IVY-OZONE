import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';

import { LadbrokesMobileBetFinderComponent } from '@ladbrokesMobile/bf/components/betFinder/bet-finder.component';

@Component({
  selector: 'bet-finder',
  templateUrl: 'bet-finder.component.html'
})

export class DesktopBetFinderComponent extends LadbrokesMobileBetFinderComponent implements OnInit, OnDestroy {
  selectRadioButtonBind: Function;
  outsideDropdownClickListener: () => void;

  ngOnInit(): void {
    super.ngOnInit();

    this.outsideDropdownClickListener = this.rendererService.renderer.listen(this.window, 'click',
      event => this.hideDropdown(event));

    this.selectRadioButtonBind = this.selectRadioButton.bind(this);
  }

  ngOnDestroy(): void {
    super.ngOnDestroy();

    this.outsideDropdownClickListener && this.outsideDropdownClickListener();
  }

  @HostListener('window:resize', [])
  onWindowResize(): void {}

  @HostListener('window:scroll', [])
  onWindowScroll(): void {}
}


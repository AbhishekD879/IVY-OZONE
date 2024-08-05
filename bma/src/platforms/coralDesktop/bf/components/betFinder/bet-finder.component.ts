import { Component, HostListener, OnInit } from '@angular/core';

import { BetFinderComponent } from '@app/bf/components/betFinder/bet-finder.component';

@Component({
  selector: 'bet-finder',
  templateUrl: 'bet-finder.component.html'
})

export class DesktopBetFinderComponent extends BetFinderComponent implements OnInit {
  selectRadioButtonBind: Function;

  ngOnInit(): void {
    super.ngOnInit();
    this.selectRadioButtonBind = this.selectRadioButton.bind(this);
  }

  @HostListener('window:resize', [])
  onWindowResize(): void {}

  @HostListener('window:scroll', [])
  onWindowScroll(): void {}
}


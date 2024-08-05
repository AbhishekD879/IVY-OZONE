import { Component } from '@angular/core';

@Component({
  selector: 'build-your-bet-home',
  templateUrl: './build-your-bet-home.component.html'
})
export class BuildYourBetHomeComponent {
  initialized: boolean = false;

  constructor() {
  }

  childComponentLoaded(): void {
    this.initialized = true;
  }
}

import { Component } from '@angular/core';

@Component({
  selector: 'inplay-home-tab',
  templateUrl: 'inplay-home-tab.component.html'
})
export class InplayHomeTabComponent {
  initialized: boolean = false;

  constructor() {
  }

  childComponentLoaded(): void {
    this.initialized = true;
  }
}

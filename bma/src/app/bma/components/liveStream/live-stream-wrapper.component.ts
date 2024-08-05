import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'live-stream-wrapper',
  templateUrl: 'live-stream-wrapper.component.html'
})
export class LiveStreamWrapperComponent implements OnInit {

  isTopBarShown: boolean = false;
  initialized: boolean = false;

  constructor(
    private location: Location
  ) {}

  ngOnInit(): void {
    this.isTopBarShown = this.location.path().indexOf('home') === -1;
  }

  childComponentLoaded(): void {
    this.initialized = true;
  }
}

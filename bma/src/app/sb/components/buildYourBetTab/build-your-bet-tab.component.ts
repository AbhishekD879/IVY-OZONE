import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'build-your-bet-tab',
  templateUrl: './build-your-bet-tab.html'
})
export class BuildYourBetTabComponent implements OnInit {

  isBuildYourBetTabShown: boolean;

  constructor(
  ) { }

  ngOnInit() {
    // todo: isModuleExist('yourcall');
    this.isBuildYourBetTabShown = true;
  }
}

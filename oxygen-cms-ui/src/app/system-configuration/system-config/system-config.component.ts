import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-system-config',
  templateUrl: './system-config.component.html',
  styleUrls: ['./system-config.component.scss']
})
export class SystemConfigComponent implements OnInit {

  public links: any;

  constructor() {
    this.links = [{
      label: 'Config',
      path: './config'
    }, {
      label: 'Structure',
      path: './structure'
    }];
  }

  ngOnInit() {
  }

}

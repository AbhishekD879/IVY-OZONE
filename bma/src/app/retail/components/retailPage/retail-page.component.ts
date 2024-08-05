import { Component, OnInit } from '@angular/core';

import { RETAIL_PAGE } from '@app/retail/constants/retail.constant';
import { RETAIL_MENU_CONFIG } from '@platform/retail/constants/retail.config';

@Component({
  selector: 'retail-page',
  templateUrl: 'retail-page.component.html'
})

export class RetailPageComponent implements OnInit {
  readonly CONST = RETAIL_PAGE;
  showRetailMenu: boolean = false;

  constructor() { }

  ngOnInit(): void {
    this.showRetailMenu = RETAIL_MENU_CONFIG.includes('HUB');
  }
}

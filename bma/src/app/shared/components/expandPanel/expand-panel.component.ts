import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';

import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'expand-panel',
  templateUrl: 'expand-panel.component.html',
  styleUrls: ['expand-panel.component.scss'],
  encapsulation: ViewEncapsulation.None
})

export class ExpandPanelComponent implements OnInit {
  @Input() heading: string;
  @Input() isOpen: boolean;

  openPanel: boolean;
  showCashoutHistory: string;
  hideCashoutHistory: string;

  constructor(protected locale: LocaleService) {
  }

  ngOnInit() {
    this.openPanel = this.isOpen;
    this.hideCashoutHistory = this.locale.getString('bs.hideCashHistory');
    this.showCashoutHistory = this.locale.getString('bs.showCashHistory');
  }
}

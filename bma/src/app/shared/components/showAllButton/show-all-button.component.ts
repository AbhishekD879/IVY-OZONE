import { Component, Input } from '@angular/core';

import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'show-all-button',
  styleUrls: ['show-all-button.component.scss'],
  templateUrl: 'show-all-button.component.html'
})

export class ShowAllButtonComponent {
  @Input() allShown: boolean;
  @Input() showMoreMode: boolean;
  @Input() seeMoreMode: boolean;
  @Input() customStylesClass: string[];
  @Input() spinnerVisible: boolean;
  @Input() showMoreLocaleStr: string;

  constructor(private localeService: LocaleService) {}

  get cssClass(): string | string[] {
    return this.customStylesClass && this.customStylesClass.length ? this.customStylesClass : 'show-all-button';
  }
  set cssClass(value: string | string[]){}

  getText(): string {
    let textString;

    switch (true) {
      case (this.seeMoreMode && this.allShown):
        textString = this.localeService.getString('sb.seeLess');
        break;
      case (this.seeMoreMode && !this.allShown):
        textString = this.localeService.getString(
          'sb.seeMore');
        break;
      case (this.allShown):
        textString = this.localeService.getString('sb.showLess');
        break;
      case (this.showMoreMode && !this.allShown):
        textString = this.localeService.getString(this.showMoreLocaleStr || 'sb.showMore');
        break;
      case (!this.showMoreMode && !this.allShown):
        textString = this.localeService.getString('sb.showAll');
        break;
    }

    return textString;
  }
}

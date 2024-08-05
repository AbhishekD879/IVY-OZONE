import { Component, Input } from '@angular/core';
import * as _ from 'underscore';

import { ILottoNumber } from '../../models/lotto-numbers.model';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'number-selector',
  templateUrl: './number-selector.component.html'
})
export class NumberSelectorComponent {

  @Input() numbersData: ILottoNumber[];

  isBrandLadbrokes: boolean;
  constructor(
    private locale: LocaleService
  ) {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
  }

  numbersTrackBy(index: number, item): string {
    return `${index}${item.value}`;
  }

  get numbers(): ILottoNumber[] {
    return _.toArray(this.numbersData);
  }
set numbers(value:ILottoNumber[]){}
}
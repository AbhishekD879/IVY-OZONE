import { Component } from '@angular/core';

import {
  LottoNumberSelectorComponent as AppLottoNumberSelectorComponent
} from '@app/lotto/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';

@Component({
  selector: 'lotto-number-selector-dialog',
  templateUrl: './lotto-number-selector-dialog.component.html',
  styleUrls: [
    '../../../../../app/lotto/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component.scss',
    './lotto-number-selector-dialog.component.scss'
  ]
})
export class LottoNumberSelectorComponent extends AppLottoNumberSelectorComponent {
}

import { Component, OnInit, ViewChild } from '@angular/core';

import { ILottoChangeEvent } from '@app/lotto/models/lotteries-config.model';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { SegmentDataUpdateService } from '@app/lotto/services/segmentDataUpdate/segment-data-update.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StorageService } from '@core/services/storage/storage.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@app/core/services/locale/locale.service';
import * as _ from 'underscore';
@Component({
  selector: 'lotto-number-selector-dialog',
  templateUrl: './lotto-number-selector-dialog.component.html',
  styleUrls: ['lotto-number-selector-dialog.component.scss']
})
export class LottoNumberSelectorComponent extends AbstractDialogComponent implements OnInit {

  @ViewChild('lottoNumberSelector', {static: true}) dialog;
  chooseNumber:string;
  isBrandLadbrokes: boolean;
  selectedNumbersExists: boolean = false;
  constructor(
    device: DeviceService,
    private segmentDataUpdateService: SegmentDataUpdateService,
    private filterService: FiltersService,
    windowRef: WindowRefService,
    private storage: StorageService,
    private locale: LocaleService,
  ) {
    super(device, windowRef);
    this.chooseNumber = this.storage.get('IsChooseNumber');
  }

  ngOnInit(): void {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    super.ngOnInit();
    this.segmentDataUpdateService.changes.subscribe((data: ILottoChangeEvent) => {
      if (data && this.params) {
        this.params.numbersSelected = data.numbersSelected;
        this.params.numbersData = data.numbersData;
        this.dialog.changeDetectorRef.detectChanges();
      }
    });
  }

  getDipTranlations(num: string): string {
    this.selectedNumbersExists = false;
    return this.filterService.getComplexTranslation('lotto.lucky', '%num', num);
  }

  get isSelected(): boolean {
      return this.params && this.params.numbersData && this.params.numbersData.filter(num => num.selected).length > 0;
  }
  set isSelected(value:boolean){}

  checkSelectedNumbersExists() {
    if (this.params) {
      const existingLines = this.params.lineSummary ? this.formatNumberListToString(this.params.lineSummary.map(res => res.numbersData)) : '';
      const selectedNumbers = _.pluck(this.params.numbersData.filter(line => line.selected), 'value').join('|');
      if (existingLines.includes(selectedNumbers)) {
        this.selectedNumbersExists = true;
        return false;
      }
      this.params.doneSelected();
    }
    this.closeDialog();
  }

  formatNumberListToString(data) {
    return data.map(line => _.pluck(line, 'value').join('|'));
  }
}

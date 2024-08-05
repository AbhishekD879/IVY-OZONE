import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'digit-list',
  templateUrl: 'digit-list.component.html',
  styleUrls: ['./digit-list.component.scss']
})
export class DigitListComponent implements OnInit, OnChanges {
  @Input() number: string;
  @Input() isDecimalPart: boolean;

  isAndroidWrapper: boolean;
  digits: Array<string>;
  offset: number;

  constructor(private device: DeviceService) {}

  ngOnInit() {
    this.isAndroidWrapper = this.device.isAndroid && this.device.isWrapper;
  }

  changePosition(value: number): void {
    this.offset = -value * 13;
  }

  ngOnChanges(changes: SimpleChanges) {
    if (!this.isAndroidWrapper) {
      if (changes.number) {
        this.generateOptions(+changes.number.currentValue);
        this.changePosition(+changes.number.currentValue);
      }
    }
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  private generateOptions(value: number): void {
    const length = this.isDecimalPart ? 100 : value + 1;

    if (value > 0 || this.isDecimalPart) {
      this.digits = Array.from({ length }).map((v, i) => (i >= 0 && i < 10 && this.isDecimalPart) ? `0${i}` : `${i}`);
    } else {
      this.digits = ['0'];
    }
  }
}

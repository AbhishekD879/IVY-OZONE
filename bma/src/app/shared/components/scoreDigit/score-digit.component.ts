import { Component, Input, OnInit, OnChanges, SimpleChanges, ElementRef } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'score-digit',
  templateUrl: 'score-digit.component.html'
})
export class ScoreDigitComponent implements OnInit, OnChanges {
  @Input() number: number | string;
  @Input() animationDelay?: number;

  showAnimatedDigit: boolean = false;
  isAndroidWrapper: boolean;
  digits: Array<string>;

  private scoreDigitEl: HTMLElement;

  constructor(
    private device: DeviceService,
    private elementRef: ElementRef
  ) {
    this.scoreDigitEl = this.elementRef.nativeElement;
  }

  ngOnInit() {
    this.isAndroidWrapper = this.device.isAndroid && this.device.isWrapper;
    this.digits = `${this.number}`.split('');
  }

  ngOnChanges(changes: SimpleChanges) {
    const numberValue = changes.number;

    if (!this.isAndroidWrapper && numberValue && !numberValue.firstChange && numberValue.currentValue !== numberValue.previousValue) {
      this.showAnimatedDigit = true;

      setTimeout(() => {
        this.digits = `${changes.number.currentValue}`.split('');
      }, this.animationDelay);

      this.scoreDigitEl.addEventListener('transitionend', () => {
        this.showAnimatedDigit = false;
      }, {once: true});
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
}

import { AfterViewInit, Component, ElementRef, Input, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
@Component({
  selector: 'fiveaside-animated-score',
  template: ``
})

export class FiveASideAnimatedScoreComponent implements AfterViewInit, OnChanges {
  @Input() timeDuration: number;
  @Input() digit: number;
  @Input() steps: number;
  @ViewChild('animatedDigit') animatedDigit: ElementRef;

  constructor() {
  }

  /**
   * Triggers specified method after view is initialized
   * @returns void
   */
  ngAfterViewInit(): void {
    if (this.digit) {
      this.animateDigitCount();
    }
  }

  /**
   * Triggers method when change is detected
   * @param  {SimpleChanges} changes
   * @returns void
   */
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['digit']) {
      this.animateDigitCount();
    }
  }

  /**
   * Method which triggers anmation after checking pre conditions
   * @returns void
   */
  private animateDigitCount(): void {
    if (!this.timeDuration) {
      this.timeDuration = 1000;
    }

    if (!isNaN(this.digit)) {
      this.digit = Number(this.digit);
    }

    if (typeof this.digit === 'number') {
      this.numberCounterHandler(this.digit, this.timeDuration, this.animatedDigit);
    }
  }

  /**
   * Triggers animation method with the given parameters
   * @param  {number} endValue
   * @param  {number} durationTime
   * @param  {ElementRef} element
   * @returns void
   */
  private numberCounterHandler(endValue: number, durationTime: number, element: ElementRef): void {
    if (!element) {
      return;
    }
    if (!this.steps) {
      this.steps = 12;
    }

    const stepCount = Math.abs(durationTime / this.steps);
    const valueIncrement = (endValue - 0) / stepCount;
    const sinValueIncrement = Math.PI / stepCount;

    let currentValue = 0;
    let currentSinValue = 0;

    const stepDigit = () => {
      currentSinValue += sinValueIncrement;
      currentValue += valueIncrement * Math.sin(currentSinValue) ** 2 * 2;

      element.nativeElement.textContent = Math.abs(Math.floor(currentValue));

      if (currentSinValue < Math.PI) {
        requestAnimationFrame(stepDigit);
      }
    };
    stepDigit();
  }
}

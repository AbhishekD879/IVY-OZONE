import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Options, ChangeContext } from 'ngx-slider-v2';

@Component({
  selector: 'range-slider',
  templateUrl: 'range-slider.component.html',
  styleUrls: ['range-slider.component.scss']
})
export class RangeSliderComponent implements OnInit {
  @Input() options: Options;
  @Input() model: number;
  @Input() id: string;
  @Input() disableSlider: boolean;
  @Output() readonly modelChangeHandler: EventEmitter<number | any> = new EventEmitter();

  ngOnInit(): void {
    /**
     * Init slider options
     */
    this.options = {
      floor: 10,
      ceil: 100,
      showSelectionBar: true,
      hideLimitLabels: true,
      disabled: this.disableSlider,
      customValueToPosition: (val: number, minVal: number, maxVal: number): number => {
        const range: number = maxVal - minVal;
        return val === (this.options.ceil / 2) ? val / this.options.ceil : (val - minVal) / range;
      },
      translate(value) {
        return `${value}%`;
      }
    };
  }

  updateValue(updatedValue: ChangeContext): void {
    this.modelChangeHandler && this.modelChangeHandler.emit(updatedValue.value);
  }
}

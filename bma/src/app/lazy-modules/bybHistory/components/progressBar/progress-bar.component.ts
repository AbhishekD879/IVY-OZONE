import { Component, Input, OnInit, OnChanges } from '@angular/core';

@Component({
  selector: 'progress-bar',
  templateUrl: './progress-bar.component.html',
  styleUrls: ['./progress-bar.component.scss']
})
export class ProgressBarComponent implements OnInit, OnChanges {
  @Input() min: number = 0;
  @Input() max: number = 100;
  @Input() value: number = 0;

  progress: number = 0; // progress in percents

  ngOnInit(): void {
    this.setProgress();
  }

  ngOnChanges(): void {
    this.setProgress();
  }

  protected setProgress(): void {
    this.progress = this.calcProgress();
  }

  public calcProgress(): number {
    const { min, max, value } = this;

    if (min >= max) {
      return 0;
    }

    if (value < min) {
      return 0;
    }

    if (value > max) {
      return 100;
    }

    return 100 / (max - min) * (value - min);
  }
}

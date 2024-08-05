import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { TimeService } from '@core/services/time/time.service';

@Component({
  selector: 'receipt-header',
  templateUrl: 'receipt-header.component.html',
  styleUrls: ['receipt-header.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ReceiptHeaderComponent implements OnInit {
  @Input() betDate: string;

  betTime: string;
  constructor(
    private timeService: TimeService
  ) {}

  ngOnInit(): void {
    this.betTime = this.betDate && this.timeService.formatByPattern(new Date(this.betDate), 'dd/MM/yyyy, HH:mm');
  }
}

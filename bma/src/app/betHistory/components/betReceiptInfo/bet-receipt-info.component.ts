import { Component, Input, OnInit } from '@angular/core';
import { TimeService } from '@core/services/time/time.service';

@Component({
  selector: 'bet-receipt-info',
  templateUrl: 'bet-receipt-info.component.html',
  styleUrls: ['bet-receipt-info.component.scss']
})
export class BetReceiptInfoComponent implements OnInit {
  @Input() receipt: string;
  @Input() date: string;
  @Input() datePattern = 'MM/dd/yyyy';

  displayDate: string;

  constructor(private timeService: TimeService) {}

  ngOnInit(): void {
    this.displayDate = this.timeService.formatByPattern(this.timeService.getLocalDateFromString(this.date), this.datePattern);
  }
}

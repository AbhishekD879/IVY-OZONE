import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'betslip-receipt-subheader',
  templateUrl: 'betslip-receipt-subheader.component.html',
  styleUrls: ['betslip-receipt-subheader.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class BetslipReceiptSubheaderComponent implements OnInit {
  @Input() events: ISportEvent[];
  @Input() isFootballAvailable: boolean;
  @Input() counter: number;

  betsCounterText: string;
  private title: string;

  constructor(private localeService: LocaleService) {}

  ngOnInit(): void {
    this.title = this.localeService.getString('bs.yourBets');
    this.betsCounterText = this.buildBetsCounterText();
  }

  private buildBetsCounterText(): string {
    return `${this.title}: (${this.counter})`;
  }
}

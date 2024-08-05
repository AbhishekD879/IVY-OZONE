import { IOutcome } from '@core/models/outcome.model';
import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'betslip-fctc-list',
  templateUrl: 'betslip-fctc-list.component.html',
  styleUrls: ['./betslip-fctc-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BetslipFctcListComponent implements OnInit {
  @Input() outcomes: IOutcome[];
  @Input() lines: number | string;
  @Input() modifire: string;

  ngOnInit() {
    if (this.modifire === undefined) {
      this.modifire = 'betslip';
    }
  }

  trackByOutcome(outcome: IOutcome): string {
    return this.modifire === 'betslip' ? outcome.id : outcome.description;
  }
}

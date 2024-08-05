import { Component, OnInit, Input, ChangeDetectionStrategy } from '@angular/core';
import { IOutcome, IRacingPostForm } from '@core/models/outcome.model';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'runner-spotlight-table',
  templateUrl: './runner-spotlight-table.component.html',
  styleUrls: ['./runner-spotlight-table.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RunnerSpotlightTableComponent implements OnInit {

  @Input() outcome: IOutcome;
  @Input() isUKorIRE: boolean;
  @Input() isGreyhoundEdp: boolean;
  formOutcomeOverview: string;
  forms: IRacingPostForm[];

  constructor(
    protected locale: LocaleService
  ) { }

  ngOnInit(): void {
    this.formOutcomeOverview = this.outcome.racingFormOutcome.overview;
  }

  trackByValue(i: number, form: IRacingPostForm): string {
    return form.date;
  }

}

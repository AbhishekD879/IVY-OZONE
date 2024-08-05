import { Component, Input, OnInit } from '@angular/core';
import { BC_PERIOD_TIME_LABELS } from '@app/bigCompetitions/constants/bcPeriodTimeLabels.constant';
import { ITeams } from '@core/models/teams.model';
import { IConstant } from '@core/services/models/constant.model';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';

@Component({
  selector: 'inplay-card-details',
  templateUrl: './inplay-card-details.component.html'
})
export class InplayCardDetailsComponent implements OnInit {
  @Input() event: IBigCompetitionSportEvent;

  teams: ITeams;
  matchTime: string;
  isPenalty: boolean;
  PERIOD_CODE: string;
  private TIME_LABELS: IConstant = BC_PERIOD_TIME_LABELS;

  ngOnInit(): void {
    this.PERIOD_CODE = this.event.clock ? this.event.clock.period_code : this.event.initClock && this.event.initClock.period_code;
    this.teams = this.event.comments && this.event.comments.teams;
    this.setPeriodLabel();
  }

  /**
   * Get period time label
   * @private
   */
  private setPeriodLabel(): void {
    switch (this.PERIOD_CODE) {
      case this.TIME_LABELS.ET_FIRST_HALF.fullName:
      case this.TIME_LABELS.ET_SECOND_HALF.fullName:
      case this.TIME_LABELS.ET_HALF_TIME.fullName:
        this.matchTime = this.TIME_LABELS.ET_FIRST_HALF.abbreviation;
        break;
      case this.TIME_LABELS.PENALTIES.fullName:
        this.matchTime = this.TIME_LABELS.PENALTIES.abbreviation;
        this.isPenalty = true;
        break;
      default:
        this.matchTime = '';
    }
  }
}


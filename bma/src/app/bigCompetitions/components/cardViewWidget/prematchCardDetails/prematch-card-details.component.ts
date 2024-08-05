import { Component, Input, OnInit } from '@angular/core';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';
import { TimeService } from '@core/services/time/time.service';

@Component({
  selector: 'prematch-card-details',
  templateUrl: './prematch-card-details.component.html'
})
export class PrematchCardDetailsComponent implements OnInit {
  @Input() event: IBigCompetitionSportEvent;
  startTime: string;

  constructor(private timeService: TimeService) {}

  ngOnInit(): void {
    this.startTime = this.timeService.getEventTime(this.event.startTime);
  }
}


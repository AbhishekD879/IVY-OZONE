import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'competition-odds-card-result-component',
  templateUrl: 'competition-odds-card-result.component.html',
  styleUrls: ['competition-odds-card-result.component.scss']
})

export class CompetitionCardResultComponent implements OnInit {
  @Input() event: any;

  ngOnInit() {
    this.event.teamA.parsedGoalScorers = this.event.teamA.goalScorers ?
      this.event.teamA.goalScorers.split(/, (?=[A-Za-z])/) : [];
    this.event.teamB.parsedGoalScorers = this.event.teamB.goalScorers ?
      this.event.teamB.goalScorers.split(/, (?=[A-Za-z])/) : [];
  }
}

import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'odds-card-result-component',
  templateUrl: 'odds-card-result.component.html',
  styleUrls: ['odds-card-result.component.scss']
})

export class OddsCardResultComponent implements OnInit {
  @Input() event: any;

  ngOnInit() {
    this.event.teamA.parsedGoalScorers = this.event.teamA.goalScorers ?
      this.event.teamA.goalScorers.split(/, (?=[A-Za-z])/) : [];
    this.event.teamB.parsedGoalScorers = this.event.teamB.goalScorers ?
      this.event.teamB.goalScorers.split(/, (?=[A-Za-z])/) : [];
  }
}

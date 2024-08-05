import { Component, Input, OnInit } from '@angular/core';

import { ISportEvent } from '@core/models/sport-event.model';
import { IScoreType, IScoreData } from '@core/services/scoreParser/models/score-data.model';
import { fallbackScore } from '@edp/enums/fallback-scoreboard.enum';
@Component({
  selector: 'fallback-scoreboard',
  templateUrl: './fallback-scoreboard.html',
  styleUrls: ['./fallback-scoreboard.scss']
})

export class FallbackScoreboardComponent implements OnInit {
  isBoxScore: boolean;
  boxScoreType: string[] = ['SetsGamesPoints', 'SetsPoints', 'GamesPoints', 'BoxScore', 'SetsLegs'];
  @Input() event: ISportEvent;
  @Input() score: IScoreData;
  @Input() scoreType: IScoreType;
  readonly fallbackScore = fallbackScore;
  constructor() {}

  ngOnInit(): void {
    this.isBoxScore = this.boxScoreType.includes(this.scoreType);
  }
}

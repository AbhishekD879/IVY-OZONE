import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { Subscription } from 'rxjs';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { TimeService } from '@coreModule/services/time/time.service';
import { ISportEvent } from '@coreModule/models/sport-event.model';
import { IScoreType, ITypedScoreData } from '@core/services/scoreParser/models/score-data.model';
import { ITeams } from '@core/models/teams.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@coreModule/services/cms/models';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';

@Component({
  selector: 'event-title-bar',
  templateUrl: './event-title-bar.html',
})
export class EventTitleBarComponent implements OnInit, OnDestroy {
  @Input() event: ISportEvent;
  @Input() isSpecial: boolean;
  @Input() sportname: string;
  @Input() isOutright: boolean;
  @Input() fallbackScoreboardType: IScoreType;
  @Input() isFallbackScoreboards: boolean;
  @Input() isFootball: boolean;

  showNewTitleBar: boolean;
  freeBetVisible: boolean = undefined; // Indicator to display free bet icon
  eventStartDate: string;

  private featureConfigSubscription: Subscription;

  constructor(
    protected scoreParserService: ScoreParserService,
    protected freeBetsService: FreeBetsService,
    protected timeService: TimeService,
    protected cmsService: CmsService
  ) {}

  ngOnInit(): void {
    this.featureConfigSubscription = this.cmsService.getFeatureConfig('ScoreboardsSports', false, true).subscribe(
      (data: ISystemConfig) => {
        let datePattern: string;

        this.showNewTitleBar = this.isFootball || (data && data[this.event.categoryId]);
        this.freeBetVisible = this.freeBetsService.isFreeBetVisible(this.event);

        if (this.isOutright) {
          datePattern = 'HH:mm, d MMM';
        } else {
          datePattern = this.showNewTitleBar ? 'HH:mm - dd/MM/yy' : 'EEEE, d-MMM-yy. HH:mm';
        }

        this.eventStartDate = this.timeService.formatByPattern(new Date(this.event.startTime), datePattern);
      });
  }

  ngOnDestroy(): void {
    this.featureConfigSubscription && this.featureConfigSubscription.unsubscribe();
  }

  parseScores(eventName: string, scoreboardType: IScoreType): ITypedScoreData | ITeams {
    if (this.event.comments && this.event.comments.teams) {
      return this.event.comments.teams;
    }
    return this.scoreParserService.parseScores(eventName, scoreboardType);
  }
}

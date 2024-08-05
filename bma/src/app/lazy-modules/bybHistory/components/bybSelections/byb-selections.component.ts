import { Component, Input, OnInit, OnDestroy, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { Subscription } from 'rxjs';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IBetHistoryLeg, IBetHistoryBet } from '@betHistoryModule/models/bet-history.model';
import { IBybSelection } from '@lazy-modules/bybHistory/models/byb-selection.model';
import { BybSelectionsService } from '@lazy-modules/bybHistory/services/bybSelectionsService/byb-selections.service';
import { BetTrackingService } from '@lazy-modules/bybHistory/services/betTracking/bet-tracking.service';
import { IScoreboardStatsUpdate } from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import {
  HandleScoreboardsStatsUpdatesService
} from '@lazy-modules/bybHistory/services/handleScoreboardsStatsUpdates/handle-scoreboards-stats-updates.service';
import { BindDecorator } from '@core/decorators/bind-decorator/bind-decorator.decorator';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { UsedFromWidgetAbstractComponent } from '@core/abstract-components/used-from-widget-abstract.component';
@Component({
  selector: 'byb-selections',
  templateUrl: './byb-selections.component.html',
  styleUrls: ['./byb-selections.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BybSelectionsComponent extends UsedFromWidgetAbstractComponent implements OnInit, OnDestroy {
  @Input() leg: IBetHistoryLeg;
  @Input() bet: IBetHistoryBet;
  @Input() isLastBet: boolean = false;

  selections: IBybSelection[];
  betTrackingEnabled: boolean;
  betSettled: boolean;
  voidedBet: boolean;
  wonBet: boolean;
  lostBet: boolean;
  voidBet: boolean;
  betBuilder: boolean;
  eventEntity: ISportEvent;
  infoTooltipIconXPosition: number;
  isFiveASideBet: boolean;

  private betTrackingEnabledSubscription: Subscription;
  private subscriptionName: string;
  private hideTooltipSubjSubscription: Subscription;

  constructor(
    private bybSelectionsService: BybSelectionsService,
    private handleScoreboardsStatsUpdatesService: HandleScoreboardsStatsUpdatesService,
    private betTrackingService: BetTrackingService,
    private changeDetectorRef: ChangeDetectorRef,
    private pubSubService: PubSubService,
    private coreToolsService: CoreToolsService
  ) {
    super();
  }

  ngOnInit(): void {
    this.betSettled = this.bet.settled === 'Y';
    this.isFiveASideBet = this.bet.source === 'f';
    this.voidBet = this.bet.totalStatus === 'void';
    this.betBuilder = this.bet.source === 'e';
    this.eventEntity = this.leg.eventEntity || this.leg.backupEventEntity;
    this.selections = this.bybSelectionsService.getSortedSelections(this.leg);
    this.voidedBet = this.bet.numLinesVoid === '1' && this.bet.totalStatus === 'void';
    this.wonBet = this.bet.numLinesWin === '1' || this.bet.totalStatus === 'won';
    this.lostBet = this.bet.numLinesLose === '1' || this.bet.totalStatus === 'lost';
    this.setIsVoided();
    this.initBetTracking();
    this.subscriptionName = `BybSelectionsComponent${this.bet.id}-${this.coreToolsService.uuid()}`;

    this.pubSubService.subscribe(
      this.subscriptionName,
      this.pubSubService.API.EVENT_STARTED, (eventID: string) => {
        if (this.bet.event.includes(eventID)) {
          this.eventEntity.isStarted = true;
          this.initBetTracking();
        }
      });
    this.pubSubService.subscribe(this.subscriptionName, this.pubSubService.API.UPDATE_BYB_BET, this.onLiveUpdateHandler);
    this.pubSubService.subscribe(this.subscriptionName, this.pubSubService.API.CLOSE_TOOLTIPS, this.closeSelectionsTooltips);
    this.hideTooltipSubjSubscription = this.bybSelectionsService.hideTooltipTriggerSub.subscribe((storedSelection: IBybSelection) => {
      this.selections.forEach((sel: IBybSelection) => {
        if (!!storedSelection && storedSelection.desc === sel.desc && sel.showTooltip === true) {
          sel.showTooltip = false;
          this.changeDetectorRef.detectChanges();
        }
      });
    });
    if(this.isLastBet) {
      this.pubSubService.publish('UPDATE_ITEM_HEIGHT');
    }  
  }

  ngOnDestroy(): void {
    this.betTrackingEnabledSubscription && this.betTrackingEnabledSubscription.unsubscribe();
    this.betTrackingEnabled && this.handleScoreboardsStatsUpdatesService.unsubscribe(this.eventEntity.id.toString());
    this.pubSubService.unsubscribe(this.subscriptionName);
    this.hideTooltipSubjSubscription && this.hideTooltipSubjSubscription.unsubscribe();
  }

  trackBySelectionId(index: number, selection: IBybSelection): string {
    return `${selection.part.outcome.id}`;
  }

  /**
   * Show/hide tooltip
   * @param event
   * @param selection
   */
  toggleTooltip(event: MouseEvent, selection: IBybSelection): void {
    if (event) {
      event.stopPropagation();
      const element = event.target as HTMLElement;
      if (selection.title.length > 20) {
        this.infoTooltipIconXPosition = element.getBoundingClientRect().right;
      } else {
        this.infoTooltipIconXPosition = element.getBoundingClientRect().left;
      }
      if (!selection.showTooltip) {
        this.closeSelectionsTooltips();
        this.pubSubService.publish(this.pubSubService.API.BET_TRACKER_TOOLTIP, true);
        selection.showTooltip = true;
        this.bybSelectionsService.replaceStoredSelection(selection);
      } else {
        this.pubSubService.publish(this.pubSubService.API.CLOSE_TOOLTIPS);
      }
    }
  }

  /**
   * this method is used to set the isVoided selections
   */
  private setIsVoided(): void {
    this.betSettled && this.bet && this.bet.leg[0] && this.bet.leg[0].part.forEach(part => {
      if (part.outcome[0] && part.outcome[0].result && part.outcome[0].result.value === 'V') {
        const index: number = this.selections.findIndex((selection: IBybSelection) => selection.part.outcomeId === part.outcomeId);
        this.selections[index].isVoided = true;
      }
    });
  }

  private initBetTracking(): void {
    this.betTrackingEnabledSubscription = this.betTrackingService.isTrackingEnabled().subscribe((enabled: boolean) => {
      if (enabled && (this.eventEntity.isStarted || this.betSettled)) {
        this.betTrackingEnabled = enabled;
        this.betTrackingService.extendSelectionsWithTrackingConfig(this.selections);
        this.handleScoreboardsStatsUpdatesService.subscribeForUpdates(this.eventEntity.id.toString());
        this.changeDetectorRef.markForCheck();
      }
    });
  }

  private updateTrackingParameters(update: IScoreboardStatsUpdate): void {
    this.betTrackingService.updateProgress(this.selections, this.bet, update);
  }

  /**
   * Handle scoreboards stats live update
   */
  @BindDecorator
  private onLiveUpdateHandler(update: IScoreboardStatsUpdate): void {
    if (update && String(this.eventEntity.id) === update.obEventId) {
      this.updateTrackingParameters(update);
      this.changeDetectorRef.markForCheck();
    }
  }

  /**
   * Close all selections tooltips when user tap away from tooltip
   */
  @BindDecorator
  private closeSelectionsTooltips(): void {
    this.selections.forEach((sel: IBybSelection) => {
      sel.showTooltip = false;
    });
    this.changeDetectorRef.markForCheck();
  }
}

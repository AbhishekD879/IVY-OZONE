import {
  Component,
  Input,
  ChangeDetectionStrategy
} from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { OptaScoreboardOverlayService } from '@edp/services/optaScoreboard/opta-scoreboard-overlay.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';


@Component({
  selector: 'scoreboard-link',
  templateUrl: 'scoreboard-link.component.html',
  styleUrls: ['./scoreboard-link.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class ScoreboardLinkComponent {
  @Input() market: IMarket;
  @Input() event: ISportEvent;

  constructor(
    private optaScoreboardOverlayService: OptaScoreboardOverlayService,
    private pubSubService: PubSubService,
  ) {
  }

  /**
   * Open Opta overlay
   * @param {IMarket} optaLink
   */
  showStats(optaLink: IMarket): void {
    this.optaScoreboardOverlayService.initOverlay();
    this.optaScoreboardOverlayService.setOverlayData({
      overlayKey: optaLink.marketOptaLink.overlayKey,
      matchId: `${this.event.id}`,
      tabKey: optaLink.marketOptaLink.tabKey
    });
    this.sendGTM(this.event, this.market);
    this.optaScoreboardOverlayService.showOverlay();
  }

  private sendGTM(event: ISportEvent, market: IMarket): void {
    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'in-line stats',
      eventAction: 'view statistics',
      eventLabel: market.name,
      categoryID: event.categoryId,
      typeID: `${event.typeId}`,
      eventID: `${event.id}`
    }]);
  }
}

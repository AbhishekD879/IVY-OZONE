import { Injectable, SecurityContext } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { IBybSelection, IBybConfig, IBybSelectionStatus } from '@lazy-modules/bybHistory/models/byb-selection.model';
import { IBetHistoryBet, IBetHistoryPart } from '@betHistoryModule/models/bet-history.model';
import { IStaticBlock, ISystemConfig } from '@core/services/cms/models';

import { CmsService } from '@core/services/cms/cms.service';
import { BetTrackingRulesService } from '@lazy-modules/bybHistory/services/betTrackingRules/bet-tracking-rules.service';
import {
  BYB_5ASIDE_MARKETS_CONFIG, PRE_PLAY
} from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';
import { IScoreboardStatsUpdate } from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';

@Injectable({ providedIn: 'root' })
export class BetTrackingService {
  isBuildYourBet: boolean = false;
  staticBlockContent: string = '';
  private staticContentObservable: Observable<string>;

  constructor(
    private domSanitizer: DomSanitizer,
    private cmsService: CmsService,
    private betTrackingRulesService: BetTrackingRulesService
  ) {}

  /**
   * Check if "My Bets Tracking" enabled
   */
  isTrackingEnabled(): Observable<boolean> {
    return this.cmsService.getSystemConfig().pipe(map((config: ISystemConfig) => config.BetTracking && config.BetTracking.enabled));
  }

  /**
   * Update stats tracking parameters of selections
   * @param selections   Byb selections array
   * @param bet          History bet
   * @param update
   */
  updateProgress(selections: IBybSelection[], bet: IBetHistoryBet, update: IScoreboardStatsUpdate): void {
    let selectionStatus;

    selections.forEach((selection: IBybSelection) => {
      if (selection.config) {
        switch (selection.config.template) {
          case 'range':
            selectionStatus = this.getSelectionStatusAndProgress(selection, bet, update);
            if (this.prePlayCheckfor2h(selectionStatus)) {
              selection.showBetStatusIndicator = false;
              selection.status = selectionStatus.status;
            } else if (selectionStatus) {
              selection.progress = selectionStatus.progress;
              this.updateSelectionStatus(selection, selectionStatus);
            }
            break;
          case 'binary':
            selectionStatus = this.getSelectionStatusAndProgress(selection, bet, update);
            if (this.prePlayCheckfor2h(selectionStatus)) {
              selection.showBetStatusIndicator = false;
              selection.status = selectionStatus.status;
            } else if (selectionStatus) {
              this.updateSelectionStatus(selection, selectionStatus);
            }
            break;
          default:
            selection.progress = null;
            selection.status = null;
            selection.showBetStatusIndicator = false;
            break;
        }
      } else {
        selection.progress = null;
        selection.status = null;
        selection.showBetStatusIndicator = false;
      }
    });
  }

  /**
   * Update OPTA selection status when part is not settled at OB
   * @param selection   Byb selection
   * @param selectionStatus  OPTA updated stat
   */
  updateSelectionStatus(selection: IBybSelection, selectionStatus: IBybSelectionStatus): void {
    if (!selection.partSettled) {
      selection.status = selectionStatus.status;
      selection.showBetStatusIndicator = !!selectionStatus.status;
    }
  }

  /**
   * checking for 2nd half preplay condition from selection
   * @param selectionStatus  OPTA updated stat
   * @returns { boolean }
   */
  prePlayCheckfor2h(selectionStatus: IBybSelectionStatus): boolean {
    return selectionStatus && selectionStatus.status && selectionStatus.status === PRE_PLAY.PRE_PLAY_2H;
  }

  checkIsBuildYourBet(part:IBetHistoryPart[]): boolean {
    return Array.isArray(part) && /Build Your Bet/gi.test(part[0].eventMarketDesc);
  }

  getStaticContent(): Observable<string> {
    if (!this.staticContentObservable) {
      this.staticContentObservable = this.cmsService.getStaticBlock('opta-disclaimer-short-en-us').pipe(
        map((cmsContent: IStaticBlock) => {
          return this.staticBlockContent = cmsContent.htmlMarkup ?
            this.domSanitizer.sanitize(SecurityContext.NONE, this.domSanitizer.bypassSecurityTrustHtml(cmsContent.htmlMarkup)) : '';
        })
      );
    }
    return this.staticContentObservable;
  }

  /**
   * Extend BYB/5-a-side selections with bet tracking config
   * @param selections
   */
  extendSelectionsWithTrackingConfig(selections: IBybSelection[]): void {
    selections.forEach(selection => {
      const selectionConfig: IBybConfig = BYB_5ASIDE_MARKETS_CONFIG.get(selection.part.eventMarketDesc.toLowerCase());

      if (selectionConfig) {
        selection.config = selectionConfig;
      }
    });
  }

  /**
   * Get current selection status and progress properties if needed. Possible values for statuses('Won|Lost|Winning|Losing')
   * @param selection
   * @param bet
   * @param update
   */
  private getSelectionStatusAndProgress(selection: IBybSelection,
                                        bet: IBetHistoryBet, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const handler = this.betTrackingRulesService[selection.config.methodName];

    if (!handler) {
      console.warn(`Handler for ${selection.config.name} market not found`);
      // Show no available stats for this selection
      return { status: '' };
    }

    const result = handler(selection, update, bet);

    return result ? { status: result.status, progress: result.progress } : { status: '' };
  }
}

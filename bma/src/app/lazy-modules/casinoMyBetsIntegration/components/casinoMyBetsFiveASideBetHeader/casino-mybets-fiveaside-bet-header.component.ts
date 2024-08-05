import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { LEADERBOARD_WIDGET } from '@app/fiveASideShowDown/constants/constants';
import { FiveasideRulesEntryAreaService } from '@app/fiveASideShowDown/services/fiveaside-rules-entry-area.service';
import environment from '@environment/oxygenEnvConfig';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { FiveasideBetHeaderComponent } from '@app/lazy-modules/fiveASideShowDown/components/fiveASideBetHeader/fiveaside-bet-header.component';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';

@Component({
  selector: 'casino-mybets-fiveaside-bet-header',
  templateUrl: './casino-mybets-fiveaside-bet-header.component.html',
  styleUrls: ['../../../fiveASideShowDown/components/fiveASideBetHeader/fiveaside-bet-header.component.scss']
})
export class CasinoMyBetsFiveasideBetHeaderComponent extends FiveasideBetHeaderComponent {
  @Input() bet: any;
  @Input() isMyBetsInCasino: boolean = false;

  showLeavingCasinoDialog: boolean = false;
  readonly homePageUrl: string = environment.HOME_PAGE;

  constructor(router: Router, rulesEntryService: FiveasideRulesEntryAreaService,
    private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService) {
      super(router, rulesEntryService);
    }

  onWidgetClick(): void {
    const LEADERBOARDBETURL = `${LEADERBOARD_WIDGET.LEADERBOARD_URL}/${this.bet.contestId}`;
    
    if (!!this.isMyBetsInCasino && !this.showLeavingCasinoDialog) {
      this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.goToSportsCTABtnClick(eznavconfbox.fivaAsideLeaderboardCta, this.homePageUrl + LEADERBOARDBETURL);
    }
  }

  /**
   * triggers on click of confirmation dialog popup
   * @param event component
   */
  confirmationDialogClick(event: ILazyComponentOutput): void {
    const LEADERBOARDBETURL = `${LEADERBOARD_WIDGET.LEADERBOARD_URL}/${this.bet.contestId}`;
    this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.confirmationPopUpClick(event, this.homePageUrl + LEADERBOARDBETURL);
  }
}

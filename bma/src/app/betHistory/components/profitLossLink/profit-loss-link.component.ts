import { Component, OnInit } from '@angular/core';
import { RtsLinkService } from '@vanillaInitModule/services/rtsLink/rts-link.service';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import environment from '@environment/oxygenEnvConfig';
@Component({
  selector: 'profit-loss-link',
  templateUrl: './profit-loss-link.component.html',
  styleUrls: ['./profit-loss-link.component.scss']
})
export class ProfitLossLinkComponent implements OnInit {
  public rtsLink: string;
  showLeavingCasinoDialog: boolean = false;
  isMyBetsInCasino: boolean = false;
  isCoral: boolean;

  constructor(private rtsLinkService: RtsLinkService,
    private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    private windowRef: WindowRefService) {}

  ngOnInit() {
    this.isCoral = environment && environment.brand === 'bma';
    this.rtsLink = this.generateRtsLink();
    this.isMyBetsInCasino = this.casinoMyBetsIntegratedService.isMyBetsInCasino;
  }

  /**
   * triggers on click of profit loss quick link
   */
  profitLossClick(): void {
    if (!!this.isMyBetsInCasino && !this.showLeavingCasinoDialog) {
      this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.goToSportsCTABtnClick(eznavconfbox.profitLossCta);
    } else {
      this.windowRef.nativeWindow.location.href = this.rtsLink;
    }
  }

  /**
   * triggers on click of confirmation dialog popup
   * @param event component event
   */
  confirmationDialogClick(event: ILazyComponentOutput): void {
    this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.confirmationPopUpClick(event);
  }

  private generateRtsLink(): string {
    return this.rtsLinkService.getRtsLink();
  }
}


import { AfterViewInit, ChangeDetectionStrategy, Component, Input, OnDestroy, OnInit } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Component({
  selector: 'no-bets-section',
  styleUrls: ['./no-bets-section.component.scss'],
  templateUrl: './no-bets-section.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NoBetsSectionComponent implements OnInit, OnDestroy, AfterViewInit {
  @Input() noBetsMessage: string;

  /**
   * Button should not be shown in betslip widget
   */
  @Input() showStartGamingButton = true;
  @Input() isMyBetsInCasino: boolean;

  showLeavingCasinoDialog: boolean = false;
  isBrandLadbrokes: boolean;
  readonly homePageUrl: string = environment.HOME_PAGE;

  constructor(private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    private locale: LocaleService, private windowRefService:WindowRefService) {}

  ngOnInit(): void {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    if(!!this.isMyBetsInCasino) {
      this.casinoMyBetsIntegratedService.noBetsMsgSubj.next(this.noBetsMessage);
    }
  }

  /**
   * Adding padding for the No Bets Text Message based on time filter
   */
  setLayout() {
    const isxDays = /\d/.test(this.noBetsMessage);
    const isLadsText: any = this.windowRefService.document.querySelectorAll('.no-bets-msg.lads-text');
    const dialogBox: any = isLadsText.length ? isLadsText : this.windowRefService.document.querySelectorAll('.no-bets-msg');
    const elementWidth = dialogBox[0].clientWidth;
    if(isLadsText.length) {
      if(elementWidth >= 270 && elementWidth < 300) {
        dialogBox[0].style.padding = '0 calc((100% - 245px) / 2)';
      }
      if(elementWidth >= 300 && elementWidth <= 360) {
        dialogBox[0].style.padding = isxDays?'0 calc((100% - 230px) / 2)' : '0 calc((100% - 240px) / 2)';
      }
    }
    else if(dialogBox.length) {
      if(elementWidth >= 270 && elementWidth < 300) {
        dialogBox[0].style.padding = '0 calc((100% - 230px) / 2)';
      }
      if(elementWidth >= 300 && elementWidth <= 360) {
        dialogBox[0].style.padding = isxDays?'0 calc((100% - 230px) / 2)' : '0 calc((100% - 240px) / 2)';
      }
    }

  }

  ngAfterViewInit(): void {
      this.setLayout();
  }

  ngOnDestroy(): void {
    if(!!this.isMyBetsInCasino) {
      this.casinoMyBetsIntegratedService.noBetsMsgSubj.next('');
    }
  }

  /**
 * triggers on click of GO TO SPORTS button
 */
  goToSportsClick(): void{
    if (!this.showLeavingCasinoDialog) {
      this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.goToSportsCTABtnClick(eznavconfbox.goToSportsCta, this.homePageUrl);
    }
  }

  /**
   * triggers on click of confirmation dialog popup
   * @param event component event
   */
  confirmationDialogClick(event: {checkboxValue: boolean, btnClicked: string}): void {
    this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.confirmationPopUpClick(event, this.homePageUrl);
  }
}

import { Component, OnInit } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';
@Component({
  selector: 'casino-goto-sports-button',
  templateUrl: './casino-goto-sports-button.component.html',
  styleUrls: ['./casino-goto-sports-button.component.scss']
})
export class CasinoGoToSportsComponent implements OnInit {

  showLeavingCasinoDialog: boolean = false;
  noBetsMessage: string = '';

  readonly homePageUrl: string = environment.HOME_PAGE;

  constructor(private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService) {}

  ngOnInit(): void {
    this.casinoMyBetsIntegratedService.noBetsMsgSubj.subscribe((noBetsMessage) => {
      this.noBetsMessage = noBetsMessage;
    });
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
    const eventObj = {output: 'userAction', value: event};
    this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.confirmationPopUpClick(eventObj, this.homePageUrl);
  }
}

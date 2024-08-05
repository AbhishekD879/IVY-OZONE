import { Component, OnInit, ElementRef } from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@core/services/cms/models';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
import environment from '@environment/oxygenEnvConfig';
import { Router } from '@angular/router';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';

@Component({
  selector: 'terms-conditions',
  templateUrl: './terms-conditions.component.html',
  styleUrls: ['./terms-conditions.component.scss']
})
export class TermsConditionsComponent implements OnInit {

  enabled: boolean = false;
  shopBetHistory: boolean = false;
  inShopBets: boolean = false;
  isMyBetsInCasino: boolean = false;
  showLeavingCasinoDialog: boolean = false;
  urlClicked: string = '';
  readonly homePageUrl: string = environment.HOME_PAGE;

  constructor(
    private cmsService: CmsService,
    private domTools: DomToolsService,
    private elementRef: ElementRef,
    private casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.shopBetHistory = config.Connect && config.Connect.shopBetHistory;
      this.inShopBets = config.Connect && config.Connect.inShopBets;
      this.enabled = config.CashOut.terms && !this.domTools.closest(this.elementRef.nativeElement, '#home-betslip-tabs');
    });

    this.isMyBetsInCasino = this.casinoMyBetsIntegratedService.isMyBetsInCasino;
  }

  /**
   * triggers on click of terms&conditions quicklink popup
   * @param url redirectURL as string
   */
  termsAndConditionsUrlClick(url: string): void {
    this.urlClicked = url;
    if (!!this.isMyBetsInCasino && !this.showLeavingCasinoDialog) {
      this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.goToSportsCTABtnClick(eznavconfbox.termsConditionsCta, this.homePageUrl + url);
    } else {
      this.router.navigateByUrl(url);
    }
  }

  /**
   * triggers on click of confirmation dialog popup
   * @param event component
   */
  confirmationDialogClick(event: ILazyComponentOutput): void {
    this.showLeavingCasinoDialog = this.casinoMyBetsIntegratedService.confirmationPopUpClick(event, this.homePageUrl + this.urlClicked);
  }
}

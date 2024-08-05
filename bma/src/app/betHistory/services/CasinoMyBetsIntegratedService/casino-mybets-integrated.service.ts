import { Injectable } from '@angular/core';
import { BetHistoryApiModule } from '@app/betHistory/bet-history-api.module';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { Subject } from 'rxjs';
import { StorageService } from '@core/services/storage/storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import environment from '@environment/oxygenEnvConfig';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';
import { eznavconfbox } from '@app/lazy-modules/locale/translations/en-US/eznavconfbox.lang';

export interface ConfirmationDialogEmit {
  btnClicked: string,
  checkboxValue: boolean
}

@Injectable({ providedIn: BetHistoryApiModule })
export class CasinoMyBetsIntegratedService {
  noBetsMsgSubj: Subject<string> = new Subject<string>();

  private readonly DISPLAY_NONE_CLASS = 'd-none';
  private readonly BMA_TOP_BAR_CLASS = 'top-bar';
  private readonly BMA_FOOTER_WRAPPER_CLASS = 'footer-wrapper';
  private readonly homePageUrl: string = environment.HOME_PAGE;

  constructor(
    private renderer: RendererService,
    private windowRef: WindowRefService,
    private gtmService: GtmService,
    private storageService: StorageService,
    private ezNavVanillaService: EzNavVanillaService) { }

  /**
   * initialises bma with overlay launch
   */
  bmaInit(): void {
    if (this.ezNavVanillaService.isMyBetsInCasino) {
      const myBetsTopBarElement = this.windowRef.document.getElementsByClassName(this.BMA_TOP_BAR_CLASS);
      const bmaFooterSection = this.windowRef.document.getElementsByClassName(this.BMA_FOOTER_WRAPPER_CLASS);

      for (let myBetsElementIndex = 0; myBetsElementIndex < myBetsTopBarElement.length; myBetsElementIndex++) {
        this.renderer.renderer.addClass(myBetsTopBarElement[myBetsElementIndex], this.DISPLAY_NONE_CLASS);
      }
      this.renderer.renderer.addClass(bmaFooterSection[0], this.DISPLAY_NONE_CLASS);
    }
  }

  /**
   * highlights the relevant tab on overlay launch
   * @returns 
   */
  getOpenBetTabActiveStatus(): boolean {
    if (!!this.ezNavVanillaService.isFirstTimeLoading) {
      this.ezNavVanillaService.isFirstTimeLoading = false;
      return true;
    } else {
      return this.ezNavVanillaService.isFirstTimeLoading;
    }
  }

  /**
   * set storage data for the check box of popup
   * @param event event
   * @param btnClicked string
   */
  handleStorageData(event: ConfirmationDialogEmit): void {
    if (event.checkboxValue) {
      this.ezNavVanillaService.confirmationPopupData[this.ezNavVanillaService.userKey] = event.btnClicked;
    } else {
      delete this.ezNavVanillaService.confirmationPopupData[this.ezNavVanillaService.userKey];
    }
    this.storageService.set(this.ezNavVanillaService.storageKey, this.ezNavVanillaService.confirmationPopupData);
  }

  /**
   * click handler for confirmation pop up both yes and no condition
   * @param event Event
   * @param gtmEventLabel GTM event text
   * @param redirectUrl url to redirect
   * @returns boolean value
   */
  confirmationPopUpClick(event: any, redirectUrl?: string): boolean {
    if (event.output === 'userAction') {    
      if (event.value.btnClicked === 'no thanks') {
        this.handleStorageData(event.value);
        return false;
      } else if (event.value.btnClicked === 'yes lets go') {
        this.setGtmData(eznavconfbox.confPopupYesCta);
        this.handleStorageData(event.value);
        const url = redirectUrl ? redirectUrl: this.homePageUrl;
        this.windowRef.nativeWindow.top.location.replace(url);
        return true;
      }
    }
  }

  /**
   * set GA tracking object
   * @param gtmEventLabel string value
   */
  setGtmData(gtmEventLabel: string): void {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'casino ingame',
      'component.LabelEvent': 'sports betting overlay',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'ingameeznav',
      'component.LocationEvent': 'sports redirect pop up',
      'component.EventDetails': gtmEventLabel,
      'component.URLclicked': 'not applicable',
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * click handler for CTA btn
   * @param redirectUrl string
   * @returns boolean value
   */
  goToSportsCTABtnClick(gtmEventLabel: string, redirectUrl?: string): boolean {
    this.setGtmData(gtmEventLabel);
    if (this.ezNavVanillaService.confirmationPopupData[this.ezNavVanillaService.userKey] === 'no thanks'
      || this.ezNavVanillaService.confirmationPopupData[this.ezNavVanillaService.userKey] === 'yes lets go') {
      const url = redirectUrl ? redirectUrl: this.homePageUrl;
      this.windowRef.nativeWindow.top.location.replace(url);
      return false;
    } else {
      return true;
    }
  }

  /**
   * gets isMyBetsInCasino valur from ezNavVanillaService
   * @returns boolean value
   */
  get isMyBetsInCasino(): boolean {
    return this.ezNavVanillaService.isMyBetsInCasino;
  }

  set isMyBetsInCasino(value: boolean) {}
}

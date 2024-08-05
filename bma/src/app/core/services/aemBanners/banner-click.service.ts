import { from as observableFrom } from 'rxjs';
import { Injectable } from '@angular/core';
import { IOffer } from '@core/models/aem-banners-section.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { Router } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class BannerClickService {

  constructor(
    private router: Router,
    private windowRef: WindowRefService,
    private command: CommandService
  ) { }


  public handleBannerClick($event: MouseEvent, offer: IOffer, redirect: boolean): void {
    this.generalMethods(offer.link, offer.target, redirect);
  }

  public handleFeaturedAemSlideClick(linkUrl: string, target: string): void {
    this.generalMethods(linkUrl, target, true);
  }

  private generalMethods(link: string, target: string, redirect: boolean): void {
    if (!link) {
      return;
    }
    const isExternalLink = link.startsWith('http') || target === '_blank' || link.indexOf('#!?') > -1;
    const betslip = this.parseBetslipIdFromLink(link);
    if (isExternalLink) {
      this.windowRef.nativeWindow.open(link, target);
    } else {
      if (betslip.isBetslipLink) {
        observableFrom(
          this.command.executeAsync(
            this.command.API.ADD_TO_BETSLIP_BY_OUTCOME_IDS,
            [betslip.betslipId, true, true, redirect]
          )
        ).subscribe();
      } else {
        this.router.navigateByUrl(link);
      }
    }
  }

  private parseBetslipIdFromLink(link: string): { isBetslipLink: boolean; betslipId: string; } {
    const betslipObj = {
      isBetslipLink: false,
      betslipId: null
    };
    const betslipRegex = /betslip\/add\/(\d+(,\d+)*)/;
    const isBetslipLink = betslipRegex.test(link);
    if (isBetslipLink) {
      betslipObj.isBetslipLink = true;
      betslipObj.betslipId = link.match(betslipRegex)[1];
    }
    return betslipObj;
  }
}


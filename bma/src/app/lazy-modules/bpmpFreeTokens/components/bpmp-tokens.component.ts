import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DatePipe } from '@angular/common';
import { forkJoin } from 'rxjs';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { FreeBetsService } from '@app/core/services/freeBets/free-bets.service';
import { UserService } from '@core/services/user/user.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { BPMP_AVAILABLE_TOKENS_CONSTANTS } from '@app/lazy-modules/bpmpFreeTokens/constants/bpmp-tokens.constant';
import { TimeService } from 'app/core/services/time/time.service';

@Component({
  selector: 'bpmp-tokens',
  templateUrl: './bpmp-tokens.component.html',
  styleUrls: ['./bpmp-tokens.component.scss']
})
export class BpmpTokensProviderComponent implements OnInit {

  viewAllTokenLabel: string;
  viewAllTokenLink: string;
  isLoading: boolean = true;
  toShowList: boolean = false;
  availabletokenData = [];

  constructor(
    private cmsService: CmsService,
    private betpackCmsService: BetpackCmsService,
    private freeBetsService: FreeBetsService,
    private datePipe: DatePipe,
    private gtmService: GtmService,
    private router: Router,
    private userService: UserService,
    private timeService: TimeService,
    private changeDetectorRef: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    forkJoin([
      this.cmsService.getSystemConfig(),
      this.betpackCmsService.getBetPackDetails(),
    ]).subscribe(([
      sysConfig,
      bpCmsData
    ]) => {
      let useraccountFreeBetTokens = [];
      this.viewAllTokenLabel = sysConfig.BetPack.ViewAllTokenLabel;
      this.viewAllTokenLink = sysConfig.BetPack.ViewAllTokenLink;
      useraccountFreeBetTokens = this.freeBetsService.getFreeBetsData();
      bpCmsData.forEach((cmsBetPack) => {
        cmsBetPack.betPackTokenList.forEach((cmsBetPackToken) => {
          const accountTokenFoundArr = useraccountFreeBetTokens.filter((accountFreeBetToken) =>
            accountFreeBetToken.tokenId == cmsBetPackToken.tokenId &&
            accountFreeBetToken.freebetOfferId == cmsBetPack.betPackId &&
            accountFreeBetToken.freebetOfferCategories && accountFreeBetToken.freebetOfferCategories.freebetOfferCategory.toLowerCase() == BPMP_AVAILABLE_TOKENS_CONSTANTS.BETPACK.toLowerCase()
          );
          if (accountTokenFoundArr.length) {
            accountTokenFoundArr.forEach((accountToken) => {
              this.availabletokenData.push(
                {
                  tokenTitle: !(cmsBetPackToken.tokenTitle[0] <= '9' && cmsBetPackToken.tokenTitle[0] >= '0') ? cmsBetPackToken.tokenTitle : this.userService.currencySymbol + cmsBetPackToken.tokenTitle,
                  tokenExpiryDate: this.timeService.parseDateTime(accountToken.freebetTokenExpiryDate),
                  useNowLink: cmsBetPackToken.deepLinkUrl
                }
              );
            });
          }
        })
      });

      if (this.availabletokenData.length) {
        this.availabletokenData.sort((a, b) => a.tokenExpiryDate - b.tokenExpiryDate);//sort based on date
        this.availabletokenData = this.availabletokenData.slice(0, 4);// to get first 4
        this.availabletokenData.forEach(token => token.tokenExpiryDate = this.datePipe.transform(token.tokenExpiryDate, 'dd/MM/yyyy'));//change date format for display
        this.toShowList = true
        this.isLoading = false;
        this.pushGTMdata('render');
      } else {
        this.toShowList = false;
        this.isLoading = false;
      }
      this.changeDetectorRef.detectChanges();
    }, (error) => {
      this.toShowList = false;
      this.isLoading = false;
    });
  }

  pushGTMdata(eventLabel: string, path?: string): void {
    if (path) {
      path = (path[0] === '/' ? path : '/' + path);
      if (path == this.router.url) {
        this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      }
      this.router.navigateByUrl(path);
    }
    this.gtmService.push(BPMP_AVAILABLE_TOKENS_CONSTANTS.GTM_EVENT, {
      event: BPMP_AVAILABLE_TOKENS_CONSTANTS.GTM_EVENT,
      eventAction: BPMP_AVAILABLE_TOKENS_CONSTANTS.GTM_EVENT_ACTION,
      eventCategory: BPMP_AVAILABLE_TOKENS_CONSTANTS.GTM_EVENT_CATEGORY,
      eventLabel: eventLabel
    });
  }
}
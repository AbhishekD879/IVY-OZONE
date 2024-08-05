import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Router } from '@angular/router';
import environment from '@environment/oxygenEnvConfig';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { BannerModel } from '@app/betpackReview/components/betpack-review.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'betpack-banner',
  templateUrl: './betpack-banner.component.html',
  styleUrls: ['./betpack-banner.component.scss']
})
export class BetpackBannerComponent implements OnInit {
  cmsUri: string = environment.CMS_ROOT_URI;
  bpmpBannerImageUrl: string;
  welcomeMsg: SafeHtml;
  enableBanner: boolean = false;
  termsAndCondition: string;
  termsAndConditionLink: string;
  gtmInfo: string[] = ['render', 'click'];
  public isValidImage: boolean;

  constructor(
    private router: Router,
    private domSanitizer: DomSanitizer,
    private betpackCmsService: BetpackCmsService,
    private cmsService: CmsService,
    private gtmService: GtmService,
    protected changeDetectorRef: ChangeDetectorRef,
  ) {}

  /**
   * @returns {void}
   */
  ngOnInit(): void {
    this.betpackCmsService.getBetPackBanners().subscribe((bannerData: BannerModel) => {
      if (bannerData) {
        this.enableBanner = bannerData.enabled;
        this.changeDetectorRef.detectChanges();
        if (bannerData.bannerImage) {
          this.sendGtmData(this.gtmInfo[0]);
          this.bpmpBannerImageUrl = `${this.cmsUri}${bannerData.bannerImage.path}/${bannerData.bannerImage.filename}`;
          this.welcomeMsg = this.domSanitizer.bypassSecurityTrustHtml(bannerData.welcomeMsg);
          this.termsAndCondition = bannerData.termsAndCondition;
          this.termsAndConditionLink = bannerData.termsAndConditionLink;
        }
      }
    });
  }

  /**
   * @returns {void}
   */
  migrateToBPMP(): void {
    this.sendGtmData(this.gtmInfo[1]);
    this.router.navigateByUrl(`/betbundle-market`);
  }

  /**
   * @param  {} event
   * @returns any
   */
  closeBanner(event): any {
    this.enableBanner = false;
  }
  
  /**
  * GATracking
  * @param  {string} Action
  * @returns void
  */
  sendGtmData(action: string): void {
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'entry banner',
      eventCategory: 'bet bundles marketplace',
      eventLabel: action
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
}

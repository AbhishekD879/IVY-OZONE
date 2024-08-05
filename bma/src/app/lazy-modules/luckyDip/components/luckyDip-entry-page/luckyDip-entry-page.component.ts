import { AfterViewInit, ChangeDetectorRef, Component, ComponentFactoryResolver, Input, OnDestroy, OnInit } from '@angular/core';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { VanillaApiService } from '@frontend/vanilla/core';
import { MarketDescriptionPopupComponent } from '@lazy-modules/luckyDip/components/market-description-popup/market-description-popup.component';
import { ILdSiteCoreBanner, ILuckyDip } from '@lazy-modules/luckyDip/models/luckyDip';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
import { LuckyDipCMSService } from '@lazy-modules/luckyDip/services/luckyDip-cms.service';
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';
import { concatMap } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'luckyDip-entry-page',
  templateUrl: './luckyDip-entry-page.component.html',
  styleUrls: ['./luckyDip-entry-page.component.scss']
})
export class LuckyDipEntryPageComponent implements OnInit, AfterViewInit, OnDestroy {

  @Input() event: ISportEvent;
  @Input() market: IMarket;
  @Input() outcome: IOutcome;
  cmsData: ILuckyDip;
  odds: string;
  luckyDipDesc: string;
  overlayBannerImage: string;
  playerPageBoxImgPath: string;
  siteCoreOverlayBanner: ISiteCoreTeaserFromServer[];
  bannerImage: string;
  animationImg: string;
  marketName: string;
  marketDetail: string[];

  constructor(
    public luckyDipCMSService: LuckyDipCMSService,
    public componentFactoryResolver: ComponentFactoryResolver,
    public dialogService: DialogService,
    public storage: SessionStorageService,
    protected vanillaApiService: VanillaApiService,
    protected changeDetectorRef: ChangeDetectorRef,
  ) { }

  ngOnInit(): void {
    this.setMarketDetails();
  }

  ngAfterViewInit(): void {
    this.getLuckyDipCmsData();
  }

  ngOnDestroy(): void {
    this.storage.remove(LUCKY_DIP_CONSTANTS.LUCKY_DIP_STORAGE_KEY);
  }
  /**
* Method to set initial market details
* @returns {void}
*/
  setMarketDetails() {
    this.marketDetail = this.market.name.split(',');
    [this.marketName, this.luckyDipDesc, this.odds] = this.marketDetail;
  }
  /**
  * Method to fetch CMS Configured Lucky Dip Data
  * @returns {void}
  */
  getLuckyDipCmsData() {
    this.luckyDipCMSService.getLuckyDipCMSData().pipe(
      concatMap((res: ILuckyDip) => {
        this.cmsData = res;
        return this.getOverlayBannerFromSiteCore()
      })).subscribe((response: ILdSiteCoreBanner[]) => {
        if (response.length > 0) {
          const [teaserResponse] = response;
          this.siteCoreOverlayBanner = teaserResponse.teasers ?? [];
          this.siteCoreOverlayBanner.forEach((data) => {
            switch (data.itemId) {
              case this.cmsData.luckyDipBannerConfig.animationImgPath:
                this.animationImg = data.backgroundImage.src;
                break;
              case this.cmsData.luckyDipBannerConfig.bannerImgPath:
                this.bannerImage = data.backgroundImage.src;
                break;
              case this.cmsData.luckyDipBannerConfig.overlayBannerImgPath:
                this.overlayBannerImage = data.backgroundImage.src;
                break;
              case this.cmsData.playerPageBoxImgPath:
                this.cmsData.playerPageBoxImgPath = data.backgroundImage.src;
                break;
            }
          });
          this.changeDetectorRef.detectChanges();
        }
      }

      );
  }

  /**
  * on clicking of info Icon
  * @returns {void}
  */
  onInfoIconClick($event: Event) {
    $event.stopPropagation();
    this.openPopUp();
  }

  /**
* get MarketDescriptionPopupComponent
* @returns {typeof MarketDescriptionPopupComponent}
*/
  get dialogComponent(): typeof MarketDescriptionPopupComponent {
    return MarketDescriptionPopupComponent;
  }

  /**
   * handle opening splash popup
   * @returns {void}
   */
  public openPopUp(): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(this.dialogComponent);
    this.dialogService.openDialog(DialogService.API.marketDescription, componentFactory, true, {
      data: {
        marketTitle: this.cmsData && this.cmsData.luckyDipFieldsConfig.title,
        marketDescripton: this.cmsData && this.cmsData.luckyDipFieldsConfig.desc,
        overlayBannerImgPath: this.overlayBannerImage,
      }
    });
  }

  /**
   * fetch entry point banner from sitecore
   * @return {void}
   */
  getOverlayBannerFromSiteCore(): Observable<ILdSiteCoreBanner[]> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get(LUCKY_DIP_CONSTANTS.LUCKY_DIP_TEASER_PATH, '', APIOPTIONS);
  }
}

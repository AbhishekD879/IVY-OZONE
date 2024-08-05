import { ChangeDetectorRef, Component, HostListener, OnInit } from '@angular/core';
import { forkJoin } from 'rxjs';
import { WindowRef } from '@frontend/vanilla/core';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { CmsService } from '@app/core/services/cms/cms.service';
import { DeviceService } from '@core/services/device/device.service';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { IFanzoneVacation } from '@app/fanzone/models/fanzone-vacation.model';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
@Component({
  selector: 'fanzone-vacation',
  template: ``,
})
export class FanzoneAppVacationComponent extends AbstractOutletComponent implements OnInit {
  fanzoneVacation: IFanzoneVacation[] = [];
  fanzoneHead = "Fanzone";
  siteCoreFanzone: ISiteCoreTeaserFromServer[] = [];
  fanzoneBgImage: string = '';
  fanzoneVacationImage: string = '';
  fanzoneLightningImage: string = '';
  isVacationReady: boolean = false;
  containerHeight: string;
  constructor(
    protected cms: CmsService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected device: DeviceService,
    protected fanzoneModuleService: FanzoneAppModuleService,
    protected windowRef: WindowRef
  ) {
    super();
  }
  ngOnInit(): void {
    this.showSpinner();
    this.getContainerHeight();
    // to get fanzone details from CMS and background image from sitecore for fanzone vacation
    forkJoin({ fzVacation: this.cms.getFanzoneNewSeason(), siteCore: this.fanzoneModuleService.getFanzoneImagesFromSiteCore() }).subscribe((data) => {
      const [fzVacation] = data.fzVacation;
      this.fanzoneVacation = data.fzVacation;
      this.changeDetectorRef.detectChanges();
      const fanzoneBgImage = this.getImage(fzVacation.fzNewSeasonBgImageDesktop, fzVacation.fzNewSeasonBgImageMobile);
      const fanzoneVacationImage = this.getImage(fzVacation.fzNewSeasonBadgeDesktop, fzVacation.fzNewSeasonBadgeMobile);
      const fanzoneLightningImage = this.getImage(fzVacation.fzNewSeasonLightningDesktop, fzVacation.fzNewSeasonLightningMobile);
      if (data.siteCore.length > 0) {
        const [teaserResponse] = data.siteCore;
        this.siteCoreFanzone = teaserResponse.teasers ?? [];
        this.siteCoreFanzone.forEach((siteCoreData: ISiteCoreTeaserFromServer) => {
          switch (siteCoreData.itemId) {
            case fanzoneBgImage:
              this.fanzoneBgImage = siteCoreData.backgroundImage.src;
              break;
            case fanzoneVacationImage:
              this.fanzoneVacationImage = siteCoreData.backgroundImage.src;
              break;
            case fanzoneLightningImage:
              this.fanzoneLightningImage = siteCoreData.backgroundImage.src;
              break;
            default:
              break;
          }
        });
        this.hideSpinner();
      }
      this.changeDetectorRef.detectChanges();
    });
  }

  @HostListener('document:click')
  @HostListener('document:touchend')
  clickOutside(): void {
    setTimeout(() => {
      this.getContainerHeight();
    }, 100);
  }

  /**
   * Method to get content height
   */
  getContainerHeight() {
    const window = this.windowRef.nativeWindow;
    if (window.innerWidth <= this.device.mobileWidth) {
      this.containerHeight =  this.windowRef.nativeWindow.document.querySelector('.smart-banner') ? 'calc(100vh - 203px)' : 'calc(100vh - 145px)';
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Method to get appropriate images based on screen resolution
   * @param desktopImg - desktop image
   * @param mobileImg - mobile image
   * @returns 
   */
  getImage(desktopImg, mobileImg): string {
    const window = this.windowRef.nativeWindow;
    return window.innerWidth >= this.device.mobileWidth ? desktopImg : mobileImg;
  }

  /**
   * Method to adjust the width of sitecore image
   * @param imgUrl - url of sitecore background image
   * @returns - url with width param
   */
  getImageWidth(imgUrl: string): string {
    const imgWidth = this.windowRef.nativeWindow.screen.width;
    return imgUrl + '?w=' + imgWidth;
  }
}
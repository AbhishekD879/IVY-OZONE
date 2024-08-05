import { ChangeDetectorRef, Component, Inject, OnInit, ViewChild } from '@angular/core';
import { TimeService } from '@app/core/services/time/time.service';
import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { IFanzoneComingBack } from '../../models/fanzone-cb.model';
import { MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA } from '@angular/material/legacy-dialog';
import { FanzoneSharedService } from '../../services/fanzone-shared.service';
import { forkJoin } from 'rxjs';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { UserService } from '@app/core/services/user/user.service';

@Component({
  selector: 'fanzone-cb-overlay',
  templateUrl: './fanzone-cb-overlay.component.html',
  styleUrls: ['./fanzone-cb-overlay.component.scss']
})
export class FanzoneCbOverlayComponent extends AbstractDialogComponent implements OnInit {
  @ViewChild('fanzoneComingBackDialog', { static: true }) dialog;
  @Inject(MAT_DIALOG_DATA) public fanzoneCbData: IFanzoneComingBack[];
  showModal: boolean = false;
  siteCoreFanzone: ISiteCoreTeaserFromServer[];
  fanzoneBgImage: string;
  fanzoneBadge: string;

  constructor(
    device: DeviceService,
    windowRef: WindowRefService,
    protected timeService: TimeService,
    private fzStorageService: FanzoneStorageService,
    private storageService: StorageService,
    private fanzoneSharedService: FanzoneSharedService,
    private changeDetectorRef: ChangeDetectorRef,
    private user: UserService) {
    super(device, windowRef);
  }

  ngOnInit(): void {
    forkJoin({
      daysDiff: this.timeService.getHydraDaysDifference(this.fanzoneCbData[0].fzSeasonStartDate),
      siteCore: this.fanzoneSharedService.getFanzoneBannerFromSiteCore()
    }).subscribe((data) => {
      this.getSiteCoreImages(data.siteCore);
      this.changeDetectorRef.detectChanges();
      const fzComingBack = this.fzStorageService.get(`fzComingBack-${this.user.username}`) || false;
      if (!fzComingBack && data.daysDiff < 0 && this.getDaysToSeasonStart(data.daysDiff) <= Number(this.fanzoneCbData[0].fzComingBackDisplayFromDays)) {
          this.fzStorageService.set(`fzComingBack-${this.user.username}`, true);
          this.showModal = true;
          super.open();
      } else if (this.getDaysToSeasonStart(data.daysDiff) < 0) {
        this.fanzoneCbData[0]['iterator'].next();
        this.storageService.remove(`fzComingBack-${this.user.username}`);
      } else {
        this.fanzoneCbData[0]['iterator'].next();
      }
    });
  }

  /**
   * Get fanzone coming back background and badge
   * @param data - images
   */
  getSiteCoreImages(data): void {
    if (data.length > 0) {
      const [teaserResponse] = data;
      this.siteCoreFanzone = teaserResponse.teasers ?? [];
      this.siteCoreFanzone.forEach((siteCoreData: ISiteCoreTeaserFromServer) => {
        if (siteCoreData.itemId === this.fanzoneCbData[0].fzComingBackBgImageDesktop) {
          this.fanzoneBgImage = siteCoreData.backgroundImage.src;
        }
        if (siteCoreData.itemId === this.fanzoneCbData[0].fzComingBackBadgeUrlDesktop) {
          this.fanzoneBadge = siteCoreData.backgroundImage.src;
        }
      });
    }
  }

  /**
   * To get number of days left for season to start
   * @param daysDiff - date
   * @returns - number
   */
  private getDaysToSeasonStart(daysDiff): number {
    return Math.ceil(-1 * daysDiff);
  }

  /**
   * On close of dialog
   */
  closeDialog(): void {
    super.closeDialog();
    this.fanzoneCbData[0]['iterator'].next();
    if (this.device.isIos) {
      this.windowRef.document.body.classList.remove('ios-modal-opened');
      this.device.isWrapper && this.windowRef.document.body.classList.remove('ios-modal-wrapper');
    }
  }

}
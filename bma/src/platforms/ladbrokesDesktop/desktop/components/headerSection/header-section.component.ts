import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { IHeaderSubMenu } from '@core/services/cms/models';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { FANZONE, headerChannelName } from '@app/fanzone/constants/fanzoneconstants';
import { FanzoneDetails } from '@app/core/services/fanzone/models/fanzone.model';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'header-section',
  templateUrl: './header-section.component.html',
  styleUrls: ['./header-section.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HeaderSectionComponent implements OnInit, OnDestroy {
  headerSubLinks: IHeaderSubMenu[];
  oddsFormat: string;
  headerSubMenuIsExists = false;
  fanzone: FanzoneDetails;
  channelName: string = headerChannelName;

  private allSubLinks: IHeaderSubMenu[] = [];
  private unsubscribe: Subject<void> = new Subject();

  constructor(
    private filtersService: FiltersService,
    private cmsService: CmsService,
    public user: UserService,
    private pubsub: PubSubService,
    private germanSupportService: GermanSupportService,
    private navigationService: NavigationService,
    private changeDetectorRef: ChangeDetectorRef,
    private fanzoneStorageService: FanzoneStorageService,
    private bonusSuppressionService: BonusSuppressionService
  ) { }

  ngOnInit(): void {
    this.pubsub.subscribe(this.channelName, [this.pubsub.API.FANZONE_DATA, this.pubsub.API.FZ_MENUS_UPDATE], fanzone => {
      this.cmsService.getHeaderSubMenu().pipe(takeUntil(this.unsubscribe))
        .subscribe((data: IHeaderSubMenu[]) => {
          this.fanzone = fanzone;
          this.allSubLinks = data;
          this.filterHeaderData();
        });
    });
    this.cmsService.getHeaderSubMenu().pipe(takeUntil(this.unsubscribe))
      .subscribe((data: IHeaderSubMenu[]) => {
        this.allSubLinks = data;
        this.filterHeaderData();
      });

    this.pubsub.subscribe('HeaderSectionComponent',
      [this.pubsub.API.SESSION_LOGIN, this.pubsub.API.SESSION_LOGOUT], () => {
        this.filterHeaderData();
      });
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe('HeaderSectionComponent');
    this.pubsub.unsubscribe(this.channelName);
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  trackByLink(item: IHeaderSubMenu): string {
    return item.linkTitle;
  }

  /**
   * Pre-redirect callback function before redirect.
   * @param {string} url // if url from coral portal then we need add get params before redirect.
   * @param {boolean} inApp (true/false)
   * @param {string} linkTitle
   * @param {string} eventAction
   */
  goToURL(url: string, inApp: boolean, linkTitle: string, eventAction: string = 'header'): void {
    this.navigationService.openUrl(url, inApp);
    this.navigationService.trackGTMEvent(eventAction, linkTitle);
  }

  /**
   * Filter set correct links
   * @private
   */
  private filterLinks(): void {
    if (!this.headerSubMenuIsExists) {
      return;
    }
    this.headerSubLinks = this.headerSubLinks.map((headerSubLink: IHeaderSubMenu) => {
      headerSubLink.targetUri = this.filtersService.filterLink(headerSubLink.targetUri);
      return headerSubLink;
    });
  }

  /**
   * Filter set correct links
   * @private
   */
  filterHeaderBasedOnRgyellow(): void {
    this.headerSubLinks = this.headerSubLinks.filter((link) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(link.linkTitle);
    })
  }

  private filterHeaderData(): void {
    this.headerSubLinks = this.germanSupportService.toggleItemsList(this.allSubLinks, 'filterRestrictedSports');
    const fanzoneIndex = this.headerSubLinks && this.headerSubLinks.findIndex(link => link.targetUri.includes(FANZONE.fanzoneIndex));
    if (fanzoneIndex !== -1) {
      const fanzoneStorage = this.fanzoneStorageService.get('fanzone');
      this.cmsService.isFanzoneConfigDisabled().subscribe((isFanzoneDisabled) => {
        const isMenuAvaialble = fanzoneStorage && fanzoneStorage.teamId && this.fanzone && this.fanzone.active && this.fanzone.fanzoneConfiguration.sportsRibbon;
        if (isFanzoneDisabled && isMenuAvaialble) { 
          this.headerSubLinks[fanzoneIndex].disabled = false;
          this.headerSubLinks[fanzoneIndex].targetUri = `${ this.headerSubLinks[fanzoneIndex].targetUri}/vacation`;
        }
        else if (isMenuAvaialble) {
          this.headerSubLinks[fanzoneIndex].disabled = false;
          const fanzoneTeam = this.fanzoneStorageService.get('fanzone');
          this.headerSubLinks[fanzoneIndex].targetUri = `${ this.headerSubLinks[fanzoneIndex].targetUri}/${fanzoneTeam.teamName}/${this.cmsService.getFanzoneRouteName(this.fanzone)}`;
        } else {
          this.headerSubLinks[fanzoneIndex].disabled = true;
        }
        this.changeDetectorRef.detectChanges();
      });
    }

    this.headerSubMenuIsExists = this.headerSubLinks && !!this.headerSubLinks.length;
    this.filterLinks();
    this.user.status && this.filterHeaderBasedOnRgyellow();
    this.changeDetectorRef.detectChanges();
  }
}

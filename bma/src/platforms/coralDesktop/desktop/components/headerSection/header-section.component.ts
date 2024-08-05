import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { CmsService } from '@core/services/cms/cms.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IHeaderSubMenu } from '@core/services/cms/models';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';


@Component({
  selector: 'header-section',
  templateUrl: './header-section.component.html',
  styleUrls: ['./header-section.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HeaderSectionComponent implements OnInit, OnDestroy {

  headerSubLinks: IHeaderSubMenu[];
  headerSubMenuIsExists = false;
  private unsubscribe: Subject<void> = new Subject();

  constructor(
    private filtersService: FiltersService,
    private cmsService: CmsService,
    private navigationService: NavigationService,
    private pubsub: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    private bonusSuppressionService: BonusSuppressionService
  ) { }

  ngOnInit(): void {
    this.cmsService.getHeaderSubMenu().pipe(takeUntil(this.unsubscribe))
      .subscribe((data: IHeaderSubMenu[]) => {
        this.headerSubLinks = data.map(headerSubLink => { //RSS
          if (headerSubLink.targetUri.includes('racingsuperseries')) {
            this.pubsub.subscribe('HeaderSectionComponent', this.pubsub.API.USER_CLOSURE_PLAY_BREAK, (val) => {
              if (val) { headerSubLink.targetUri = '/promotions/details/exclusion'; }
              return headerSubLink; //RSS
            });
          }
           return headerSubLink;
        })
        this.headerSubMenuIsExists = this.headerSubLinks && !!this.headerSubLinks.length;
        this.filterLinks();
      this.filterHeaderBasedOnRgyellow();
        this.changeDetectorRef.detectChanges();
      });
    this.pubsub.subscribe('HeaderSectionComponent',
      [this.pubsub.API.SESSION_LOGIN, this.pubsub.API.SESSION_LOGOUT], () => {
        this.filterHeaderBasedOnRgyellow();
        this.changeDetectorRef.detectChanges();
      });
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe('HeaderSectionComponent');
    this.unsubscribe.next();
    this.unsubscribe.complete();
  }

  /**
   * Pre-redirect callback function.
   *
   * @param url
   * @param inApp
   * @param linkTitle
   * @param eventAction
   */
  goToURL(url: string, inApp: boolean, linkTitle: string, eventAction: string = 'header'): void {
    this.navigationService.openUrl(url, inApp);
    this.navigationService.trackGTMEvent(eventAction, linkTitle);
  }

  trackByLink(item: IHeaderSubMenu): string {
    return item.linkTitle;
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
    this.headerSubLinks = this.headerSubLinks.filter((link: IHeaderSubMenu) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(link.linkTitle);
    })
  }
}

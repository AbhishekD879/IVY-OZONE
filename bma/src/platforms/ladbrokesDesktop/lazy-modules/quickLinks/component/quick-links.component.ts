import { Component, OnDestroy, OnInit, Input, ViewEncapsulation } from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IDesktopQuickLink } from '@core/services/cms/models';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { Router } from '@angular/router';
import { FlagSourceService } from '@app/core/services/flagSource/flag-source.service';
@Component({
  selector: 'quick-links',
  templateUrl: './quick-links.component.html',
  styleUrls: ['./quick-links.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class LadsQuickLinksComponent implements OnInit,OnDestroy {
  quickLinks: IDesktopQuickLink[] = [];
  title = "quick-links";
  @Input() applyCss?: boolean;
  isQuickLinksEnabled: boolean = false;

  constructor(
    private cmsService: CmsService,
    private userService: UserService,
    private pubSubService: PubSubService,
    private bonusSuppressionService: BonusSuppressionService,
    private router: Router,
    private flagSourceService: FlagSourceService
  ) { }

  ngOnInit() {
    // TODO reduce amounts of HTTP calls on pages.
    this.cmsService.getDesktopQuickLinks()
      .subscribe((data: IDesktopQuickLink[]) => {
        this.quickLinks = data.map(el => {
          el.target = `/${el.target.replace(/^\/+/, '')}`;
          return el;
        });
        this.userService.status && this.filterQuickLinksBasedOnRGYellow();
      });
    this.flagSourceService.flagUpdate && this.flagSourceService.flagUpdate
      .subscribe((flags) => {
        this.isQuickLinksEnabled = JSON.parse(flags['ShowQuickLinks']);
      });
    this.pubSubService.subscribe(
      this.title,
      [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], () => {
        this.userService.status && this.filterQuickLinksBasedOnRGYellow();
      })
  }

  /**
   * Filter quick links handler
   * @private
   */
  private filterQuickLinksBasedOnRGYellow() {
    this.quickLinks = this.quickLinks.filter((quickLinkItem: IDesktopQuickLink) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(quickLinkItem.title);
    });
  }

  trackByQuickLink(index: number, link: IDesktopQuickLink): string {
    return `${index}${link.target}`;
  }

  ngOnDestroy(){
    this.pubSubService.unsubscribe(this.title);
  }

  navigateByUrl(event, link: string): void {
    event.preventDefault();
    link && this.router.navigateByUrl(link);
  }

}

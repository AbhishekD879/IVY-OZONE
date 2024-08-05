import { Component, OnDestroy, OnInit, Input } from '@angular/core';
import { CmsService } from '@core/services/cms/cms.service';
import { IDesktopQuickLink } from '@core/services/cms/models';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { Router } from '@angular/router';
import { FlagSourceService } from '@app/core/services/flagSource/flag-source.service';

@Component({
  selector: 'quick-links',
  templateUrl: '../../../../platforms/coralDesktop/lazy-modules/quickLinks/component/quick-links.component.html',
  styleUrls: ['../../../../platforms/coralDesktop/lazy-modules/quickLinks/component/quick-links.component.scss']
})
export class QuickLinksComponent implements OnInit,OnDestroy,OnDestroy {
  quickLinks: IDesktopQuickLink[] = [];
  title = 'quick-links';
  @Input() applyCss?: boolean;
  isQuickLinksEnabled: boolean = false;

  constructor(
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private bonusSuppressionService: BonusSuppressionService,
    private router: Router,
    private flagSourceService: FlagSourceService
  ) { }

  ngOnInit() {
    // TODO reduce amounts of HTTP calls on pages.
    this.cmsService.getDesktopQuickLinks()
      .subscribe((data: IDesktopQuickLink[]) => {
        this.quickLinks = data.map(quickLink =>{ //RSS
          if(quickLink.target.includes('racingsuperseries')){
          this.pubSubService.subscribe('QuickLinksComponent', this.pubSubService.API.USER_CLOSURE_PLAY_BREAK,(val) =>{
            if(val){ quickLink.target = 'promotions/details/exclusion';}
          return quickLink; //RSS
        }  );
       } 
        quickLink.target = `/${quickLink.target.replace(/^\/+/, '')}`;
        return quickLink;})
        this.filterQuickLinksBasedOnRGYellow();
      });
      this.flagSourceService.flagUpdate && this.flagSourceService.flagUpdate
        .subscribe((flags) => {
          this.isQuickLinksEnabled = JSON.parse(flags['ShowQuickLinks']);
        });
      this.pubSubService.subscribe(
        this.title,
        [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], () => {
          this.filterQuickLinksBasedOnRGYellow();
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

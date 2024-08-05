import { Component, Input, ChangeDetectionStrategy, OnInit, ChangeDetectorRef, SimpleChanges } from '@angular/core';
import {
  IOFeaturedQuickLinksModel,
  IOquickLinkDataModel
} from '@featured/models/featured-quick-link.model';
import { Router } from '@angular/router';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { FlagSourceService } from '@app/core/services/flagSource/flag-source.service';

@Component({
  selector: 'featured-quick-links',
  templateUrl: './featured-quick-links.component.html',
  styleUrls: ['featured-quick-links.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedQuickLinksComponent implements OnInit {
  @Input() quickLinks: IOFeaturedQuickLinksModel;
  @Input() sportName: string;
  isQuickLinksEnabled: boolean = false;

  private moduleName = 'FeaturedQuickLinks';

  constructor(
    private windowRef: WindowRefService,
    private router: Router,
    private gtmService: GtmService,
    private pubSubService: PubSubService,
    private changeDetector: ChangeDetectorRef,
    private bonusSuppressionService: BonusSuppressionService,
    private flagSourceService: FlagSourceService
  ) { }

  ngOnInit() {
    this.filterQuickLinksBasedOnRGYellow();
    this.pubSubService.subscribe(this.moduleName, this.pubSubService.API.SESSION_LOGIN, () => {
        this.filterQuickLinksBasedOnRGYellow();
    });
    this.flagSourceService.flagUpdate && this.flagSourceService.flagUpdate
      .subscribe((flags) => {
        this.isQuickLinksEnabled = JSON.parse(flags['ShowQuickLinks']);
        this.changeDetector.detectChanges();
      });
  }

  ngOnChanges(changes: SimpleChanges){
     if(changes.quickLinks){
        this.filterQuickLinksBasedOnRGYellow();
     }
  }

  trackByLink(i: number, element: IOquickLinkDataModel): string {
    return `${i}_${element.id}`;
  }

  clickOnLink(event, item: IOquickLinkDataModel, itemPos: number): void {
    const currentDomain = this.windowRef.nativeWindow.location.origin;

    event.preventDefault();

    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'quick links',
      eventAction: this.sportName || 'home',
      eventLabel: item.title,
      position: itemPos
    });

    if (item.destination.indexOf(currentDomain) >= 0) {
      this.router.navigateByUrl(item.destination.replace(currentDomain, ''));
    } else {
      this.windowRef.nativeWindow.location.href = item.destination;
    }
  }


  /**
   * Filters quickLinks based on RG Yellow status of user
   * returns {void} 
  */
  filterQuickLinksBasedOnRGYellow(): void {
    if (this.quickLinks?.data) {
      this.quickLinks.data = this.quickLinks.data.filter((qLink) => {
        return this.bonusSuppressionService.checkIfYellowFlagDisabled(qLink.title);
      })
      this.changeDetector.detectChanges();
    }
  }

  ngOnDestroy(){
    this.pubSubService.unsubscribe(this.moduleName);
  }
  /**
    * Check for the updated format for title
    * returns {string} 
   */
  updateTitle(qLink): string {
    const quickLinkArr = this.quickLinks && this.quickLinks.data;
    const title = qLink && qLink.title;
    const lastItem = quickLinkArr && quickLinkArr.length > 0 ? quickLinkArr[quickLinkArr.length - 1] : null;

    const isOddQL =  quickLinkArr && quickLinkArr.indexOf(lastItem) % 2 === 0 ? true : false; 

    if(lastItem && lastItem.id === qLink.id && isOddQL){
      return title.length > 55 ? `${title.substring(0, 55)}...` : title;
    }
      return title.length > 24 ? `${title.substring(0, 24)}...` : title;
  }
}

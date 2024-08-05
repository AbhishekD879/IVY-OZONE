import { Injectable } from '@angular/core';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { ISportTabs } from '@app/core/services/cms/models/sport-tabs.model';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class VirtualEntryPointsService {
  public bannerBeforeAccorditionHeader: BehaviorSubject<string> = new BehaviorSubject<string>('');
  public sportTabs: BehaviorSubject<ISportConfigTab[]> = new BehaviorSubject<ISportConfigTab[]>([]);
  public targetTab: BehaviorSubject<ISportConfigTab> = new BehaviorSubject<ISportConfigTab>({} as any);
  public accorditionNumber: BehaviorSubject<number> = new BehaviorSubject<number>(0);
  public lastBannerEnabled: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public categoryId: any;
  public mockTab: ISportConfigTab = {} as ISportConfigTab;
  private readonly GREY_HOUND_CATEGORY_ID: string = '19';
  private readonly HORSE_RACING_CATEGORY_ID: string = '21';
  lastRacingModuleIndex = -1;
  virtualMarketName: string;
  uniqueId = 0;
  constructor(
    protected cmsService: CmsService,
    protected windowRef: WindowRefService
  ) { }

  getTabs(categoryId: any, display: any) {
    this.categoryId = categoryId;
    this.cmsService.getSportTabs(categoryId).subscribe((sportTabs: ISportTabs) => {
      this.sportTabs.next(sportTabs.tabs);
      this.setTargetTab(display);
    });
  }

  setTargetTab(currentTab: any) {
    if (this.categoryId === this.GREY_HOUND_CATEGORY_ID && (currentTab == 'today' || currentTab == 'tomorrow')) {
      this.targetTab.next(this.sportTabs.value.find((tab: ISportConfigTab) => tab.id.includes(currentTab)));
    } else if (this.categoryId === this.HORSE_RACING_CATEGORY_ID && currentTab == 'featured') {
      this.targetTab.next(this.sportTabs.value.find((tab: ISportConfigTab) => tab.id.includes('meetings')));
    }
    else {
      this.targetTab.next({} as any);
    }

  }

  findBannerAccordition() {
    const elements = this.windowRef.document.querySelectorAll('.outerAccordionFeatured');
    this.accorditionNumber.next(elements.length);

    elements.forEach((el: any, index) => {
      if (index === Number(this.targetTab?.value?.interstitialBanners?.bannerPosition)) {
        this.lastBannerEnabled.next(false);
        this.bannerBeforeAccorditionHeader.next(el.innerText?.split('\n')[0] || el.innerText);
      }
    });

    if (elements.length <= Number(this.targetTab?.value?.interstitialBanners?.bannerPosition)) {
      const el: any = elements[elements.length-1];
      if(el && el.innerText.includes(this.virtualMarketName?.toUpperCase())) {
        this.lastBannerEnabled.next(false);
        this.bannerBeforeAccorditionHeader.next(this.virtualMarketName + 'after');
      } else {
        this.bannerBeforeAccorditionHeader.next(undefined);
        this.lastBannerEnabled.next(true);
      }
    }
  }
}

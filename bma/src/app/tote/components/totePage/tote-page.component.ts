import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { from, Subscription } from 'rxjs';
import { filter } from 'rxjs/operators';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { ITab, ITabActive } from '@core/models/tab.model';

import { TOTE_CONFIG } from '../../tote.constant';

@Component({
  selector: 'tote-page',
  templateUrl: './tote-page.component.html'
})
export class TotePageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  tabs = TOTE_CONFIG.tabs;
  icon: {
    svg: string;
    svgId: string;
  };
  activeTab: ITabActive = { id: null };
  bannerCategory: string = TOTE_CONFIG.TOTE_BANNER_TARGET_URI;
  routeListener: Subscription;
  showBanner: boolean;

  constructor(
    private router: Router,
    private cms: CmsService,
    private route: ActivatedRoute
  ) {
    super()/* istanbul ignore next */;
    this.showBanner = true;
  }

  ngOnInit(): void {
    this.setActiveTab();

    this.routeListener = this.router
      .events.pipe(
      filter((event: Event) => event instanceof NavigationEnd))
      .subscribe(() => this.setActiveTab());

    from(this.cms.getItemSvg('International Tote')).subscribe((data) => {
      this.icon = data;
      this.hideSpinner();
    }, () => {
      this.showError();
    });
  }

  ngOnDestroy(): void {
    this.routeListener.unsubscribe();
  }

  goToDefaultPage(): void {
    const defaultSportTab: ITab = TOTE_CONFIG.tabs.find((tab: ITab) => tab.originalTitle === TOTE_CONFIG.DEFAULT_TOTE_SPORT);
    this.router.navigateByUrl(defaultSportTab.url);
  }

  private setActiveTab(): void {
    const prefixLength = 4;
    const currentTabTitle = this.route.snapshot.firstChild.url[0].path;
    const tab = this.tabs.find(t => t.id.slice(prefixLength) === currentTabTitle);
    this.activeTab = tab || this.tabs[0];
  }
}

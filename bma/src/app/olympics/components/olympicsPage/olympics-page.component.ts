import { Component, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { OlympicsService } from '@app/sb/services/olympics/olympics.service';
import { ISportCMSConfig } from '@app/olympics/models/olympics.model';
import { LAZY_LOAD_ROUTE_PATHS } from '@bma/constants/lazyload-route-paths.constant';

@Component({
  selector: 'olympics-page',
  templateUrl: './olympics-page.component.html'
})
export class OlympicsPageComponent extends AbstractOutletComponent implements OnInit {
  olympicsMenu: ISportCMSConfig[];
  olympics: string;

  constructor(
    private olympicsService: OlympicsService
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    this.showSpinner();
    this.olympicsService.getCMSConfig()
      .subscribe((cmsConfigs: ISportCMSConfig[]) => {
        this.hideSpinner();
        this.olympicsMenu = this.sortOlympicsMenu(cmsConfigs);
      }, error => {
        this.showError();
        console.warn('CMS Sports Configs:', error && error.error || error);
      });
      this.olympics = LAZY_LOAD_ROUTE_PATHS.olympics;
  }

  trackById(menu: ISportCMSConfig): string {
    return menu.id;
  }

  /**
   * Sort Olympics Menu
   * @param {ISportCMSConfig[]} cmsConfigs
   * @returns {ISportCMSConfig[]}
   */
  private sortOlympicsMenu(cmsConfigs: ISportCMSConfig[]): ISportCMSConfig[] {
    const data: ISportCMSConfig[] = this.olympicsService.getMenuConfigs(cmsConfigs);

    return _(data).chain().sortBy((item: ISportCMSConfig) => {
      return item.imageTitle;
    }).sortBy((item: ISportCMSConfig) => {
      return item.ssCategoryCode !== 'OLYMPICS';
    }).value();
  }
}

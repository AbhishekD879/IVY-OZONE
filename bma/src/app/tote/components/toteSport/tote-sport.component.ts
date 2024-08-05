import { of as observableOf,  Observable } from 'rxjs';
import { concatMap } from 'rxjs/operators';
import { Component, Input, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Router, ActivatedRoute, Params } from '@angular/router';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { TOTE_CONFIG } from '../../tote.constant';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ToteService } from '../../services/mainTote/main-tote.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { ITab, ITabActive } from '@core/models/tab.model';
import { IToteEvents } from '@app/tote/models/tote-event.model';
import { NavigationService } from '@coreModule/services/navigation/navigation.service';

@Component({
  selector: 'tote-sport',
  templateUrl: './tote-sport.component.html'
})
export class ToteSportComponent extends AbstractOutletComponent implements OnInit {
  eventsData: IToteEvents;
  sport: string;
  filter: string;

  @Input() activeTab: ITabActive = { id: null };

  switchers: ISwitcherConfig[];

  constructor(
    public location: Location,
    private router: Router,
    private route: ActivatedRoute,
    private toteService: ToteService,
    private navigationService: NavigationService
  ) {
    super()/* istanbul ignore next */;
  }

  reloadSport(): void {
    this.showSpinner();
    this.toteService.getToteEvents(environment.TOTE_CLASSES[this.sport]).subscribe((data: any) => {
      this.init(data);
    }, () => {
      this.showError();
    });
  }

  ngOnInit(): void {
    this.route
      .params.pipe(
      concatMap((params: Params) => {
        this.filter = params.filter || TOTE_CONFIG.filters[0];
        this.sport = params.sport || TOTE_CONFIG.DEFAULT_TOTE_SPORT;

        // redirect to sport with filter
        if (!_.contains(TOTE_CONFIG.filters, this.filter)) {
          const redirectSport: ITab = TOTE_CONFIG.tabs.find((tab: ITab) => tab.title === this.sport);
          return this.redirectToUrl(redirectSport.url);
        }

        if (!_.contains(_.keys(environment.TOTE_CLASSES), this.sport)) {
          return this.redirectToUrl('/');
        }

        return this.toteService.getToteEvents(environment.TOTE_CLASSES[this.sport]);
      }))
      .subscribe((data: IToteEvents) => {
        if (data === null) { return; }
        this.init(data);
      }, () => {
        this.showError();
      });
  }

  goToFilter(filterName: string): void {
    this.filter = filterName;
    const path = `/tote/${this.sport}/${filterName}`;

    if (path !== this.location.path()) {
      this.navigationService.openUrl(path, true, true);
    }
  }

  /**
   * redirect to Url
   * @param url
   */
  private redirectToUrl(url: string): Observable<null> {
    this.router.navigateByUrl(url);
    return observableOf(null);
  }

  private init(data: IToteEvents): void {
    this.eventsData = data;
    this.activeTab.id = `tab-${this.sport}`;
    this.switchers = [{
      onClick: () => this.goToFilter(TOTE_CONFIG.filters[0]),
      viewByFilters: TOTE_CONFIG.filters[0],
      name: `tt.${TOTE_CONFIG.filtersName[0]}`
    }, {
      onClick: () => this.goToFilter(TOTE_CONFIG.filters[1]),
      viewByFilters: TOTE_CONFIG.filters[1],
      name: `tt.${TOTE_CONFIG.filtersName[1]}`
    }];
    this.hideSpinner();
  }
}

import { environment } from './../../../environments/environment';
import { Component, OnInit } from '@angular/core';
import { ApiClientService } from '../../client/private/services/http/index';
import { ActivatedRoute, Params } from '@angular/router';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { Dashboard } from '../../client/private/models/dashboard.model';
import { HttpResponse } from '@angular/common/http';
import { Breadcrumb } from '../../client/private/models/breadcrumb.model';

@Component({
  selector: 'app-dashboard-view',
  templateUrl: './dashboard-view.component.html',
  styleUrls: ['./dashboard-view.component.scss']
})
export class DashboardViewComponent implements OnInit {

  public purge: Dashboard;
  public isLoading: boolean = false;
  public breadcrumbsData: Breadcrumb[];
  public processUrlSrc: string;

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private activatedRoute: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.activatedRoute.params.subscribe((params: Params) => {
    this.apiClientService.dashboard()
      .getById(params['id']).map((dashboard: HttpResponse<Dashboard>) => {
        const purge: Dashboard = dashboard.body;
        return purge;
      }).subscribe((purge: Dashboard) => {
        this.purge = purge;
        this.setUri();
        this.breadcrumbsData = [{
          label: `Dashboard`,
          url: `/dashboard`
        }, {
          label: `View Purge Data: ${this.purge.purgeID}`,
          url: `/dashboard/${this.purge.id}`
        }];
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }

  setUri(): void {
    const domain: string = environment.apiUrl.match(/^https?\:\/\/([^\/:?#]+)(?:[\/:?#]|$)/i)[0];
    this.processUrlSrc = `${domain}${this.purge.progressURI.substr(1)}`;
  }

}

import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { DatePipe } from '@angular/common';

import { ApiClientService } from '../../client/private/services/http/index';
import { Dashboard } from '../../client/private/models/dashboard.model';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { DialogService } from '../../shared/dialog/dialog.service';
import { BrandService } from '../../client/private/services/brand.service';

@Component({
  selector: 'app-dashboard-list',
  templateUrl: './dashboard-list.component.html',
  styleUrls: ['./dashboard-list.component.scss'],
  providers: [
    DialogService,
    DatePipe
  ]
})
export class DashboardListComponent implements OnInit {

  public isLoading: boolean = false;
  public dashboards: Dashboard[] = [];
  public searchField: string = '';

  public dataTableColumns: any[] = [
    {
      name: 'Time',
      property: 'createdAt',
      link: {
        hrefProperty: 'id'
      },
      type: 'link',
      width: 3
    },
    {
      name: 'Type',
      property: 'type',
      width: 5,
    },
    {
      name: 'Status',
      property: 'status',
      width: 1
    },
    {
      name: 'Est. Time',
      property: 'estimatedTime',
      width: 1
    },
    {
      name: 'User name',
      property: 'createdByUserName',
      width: 2
    }
  ];

  public filterProperties: string[] = [
    'domains'
  ];



  public chosenDate: Date = new Date();
  public maxDate: Date = new Date();

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private brandService: BrandService
  ) {}

  ngOnInit(): void {
    this.loadInitialData();
  }

  public changeDate(): void {
    this.loadInitialData();
  }

  private loadInitialData(): void {
    const datePipe = new DatePipe('en-US');

    this.globalLoaderService.showLoader();
    this.isLoading = true;

    this.apiClientService.dashboard()
        .findAllByBrand(
          this.brandService.brand,
          this.formatDate()
        )
        .map((response: HttpResponse<Dashboard[]>) => {
          return response.body.map((dashboard: Dashboard) => {
            dashboard.createdAt = datePipe.transform(dashboard.createdAt, 'yyyy-MM-dd HH:mm:ss a');
            dashboard.currentTime = datePipe.transform(dashboard.currentTime, 'yyyy-MM-dd HH:mm:ss a');
            dashboard.updatedAt = datePipe.transform(dashboard.updatedAt, 'yyyy-MM-dd HH:mm:ss a');
            return dashboard;
          }).sort((a, b) => a.createdAt < b.createdAt ? 1 : -1);
        })
        .subscribe((dashboards: Dashboard[]) => {
          this.dashboards = dashboards;
          this.isLoading = false;
          this.globalLoaderService.hideLoader();
        },  () => {
          this.isLoading = false;
          this.globalLoaderService.hideLoader();
        });
  }

  private formatDate(): string {
    const datePipe = new DatePipe('en-US');
    return datePipe.transform(new Date(this.chosenDate), 'yyyy-MM-dd');
  }

}

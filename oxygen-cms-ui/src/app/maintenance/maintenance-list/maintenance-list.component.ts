import * as _ from 'lodash';

import { Component, OnInit } from '@angular/core';

import { TableColumn } from '../../client/private/models/table.column.model';

import { MaintenancePage } from '../../client/private/models/maintenancepage.model';
import { DialogService } from '../../shared/dialog/dialog.service';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http';
import { AddMaintenancePageComponent } from '../add-maintenance-page/add-maintenance-page.component';
import { HttpResponse } from '@angular/common/http';

import { AppConstants } from '../../app.constants';

@Component({
  templateUrl: './maintenance-list.component.html',
  styleUrls: ['./maintenance-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class MaintenanceListComponent implements OnInit {

  public isLoading: boolean = false;
  public maintenancePages: MaintenancePage[];
  public searchField: string = '';

  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Target Uri',
      property: 'targetUri'
    },
    {
      name: 'Validity Period Start',
      property: 'validityPeriodStart',
      type: 'date'
    },
    {
      name: 'Validity Period End',
      property: 'validityPeriodEnd',
      type: 'date'
    },
    {
      name: 'Mobile',
      property: 'mobile',
      type: 'boolean'
    },
    {
      name: 'Tablet',
      property: 'tablet',
      type: 'boolean'
    }
    ,
    {
      name: 'Desktop',
      property: 'desktop',
      type: 'boolean'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService.maintenance()
      .findAllByBrand()
      .map((response: HttpResponse<MaintenancePage[]>) => {
        return response.body;
      })
      .subscribe((data: MaintenancePage[]) => {
        this.maintenancePages = data;
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      }, error => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
  }

  public get data(): MaintenancePage[] {
    if (this.searchField.length > 0) {
      return this.maintenancePages.filter(item => {
        return ~item.name.toLowerCase().indexOf(this.searchField.toLowerCase());
      });
    } else {
      return this.maintenancePages;
    }
  }

  public removeMaintenancePage(page: MaintenancePage): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Page',
      message: `Are You Sure You Want to Remove ${page.name} Page`,
      yesCallback: () => {
        this.apiClientService.maintenance()
          .remove(page.id)
          .subscribe(() => {
            _.remove(this.maintenancePages, {id: page.id});
          });
      }
    });
  }

  public addNewPage(): void {
    this.dialogService.showCustomDialog(AddMaintenancePageComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Page',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (page: MaintenancePage) => {
        this.apiClientService.maintenance()
          .add(page)
          .map((response: HttpResponse<MaintenancePage>) => {
            return response.body;
          })
          .subscribe((data: MaintenancePage) => {
            this.maintenancePages.push(data);
          }, error => {
            console.error(error);
          });
      }
    });
  }
}

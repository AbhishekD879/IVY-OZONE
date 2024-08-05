import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AppConstants } from '@app/app.constants';
import { DataTableColumn } from '@app/client/private/models';
import { ConfigRegistryApiService } from '@app/config-registry/services/config-registry.api.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ConfigRegistryDetailsComponent } from '../config-registry-details/config-registry-details.component';

@Component({
  selector: 'app-config-registry-list',
  templateUrl: './config-registry-list.component.html'
})
export class ConfigRegistryListComponent implements OnInit {
  newRegistry: any;
  getDataError: string;

  constructor(private dialog: MatDialog, private dialogRef: DialogService,
              private configRegistryApiService: ConfigRegistryApiService,
              private globalLoaderService: GlobalLoaderService)  { }





  paginationLimitOptions: number[] = [5, 10, 25, 50];
  paginationLimit: number = this.paginationLimitOptions[1];
  searchField: string = '';
  registryData:any;

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'API',
      property:'key',
      link: {
        hrefProperty: 'id',
        path: 'config'
      },
      type: 'link'
    },
    {
      name:'Collections',
      property:'values'
    }
  ];
  filterProperties: Array<string> = [
    'configMap'
  ];

  ngOnInit(): void {
    this.loadRegistryData();
  }

  /**
     * Fetch registry list data.
     * @returns - {void}
     */
  loadRegistryData(){
    this.globalLoaderService.showLoader();
    this.configRegistryApiService.getCampaignsByBrandWithOrdering()
    .subscribe((data: any) => {
      this.registryData = data;
      this.globalLoaderService.hideLoader();
    },error =>{
      this.getDataError = error.message;
      this.globalLoaderService.hideLoader();
    });
    this.globalLoaderService.hideLoader();
  }

 /**
     * Create or Edit single config registry
     * @returns - {void}
     */
  createEditRegistry(registryData){
    const dialogRef = this.dialog.open(ConfigRegistryDetailsComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {registryData: registryData}
    });

    dialogRef.afterClosed().subscribe(newMap => {
      if (newMap) {
        this.globalLoaderService.showLoader();
        console.log(newMap);
       
        if(newMap.data.id){
          this.configRegistryApiService.updateRegistry(newMap.data,false)
          .subscribe((data: any) => {
            this.loadRegistryData();
            this.globalLoaderService.hideLoader();
          },error =>{
            this.getDataError = error.message;
            this.globalLoaderService.hideLoader();
          });
        }else{
          this.configRegistryApiService.postNewRegistry(newMap.data)
          .subscribe((data: any) => {
            this.loadRegistryData();
            this.globalLoaderService.hideLoader();
          },error =>{
            this.getDataError = error.message;
            this.globalLoaderService.hideLoader();
          });
        }
        this.globalLoaderService.hideLoader();
      }
    });
  }

   /**
     * Delete single config registry
     * @returns - {void}
     */

  removeConfig(registry) {
    this.dialogRef.showConfirmDialog({
      title: 'Remove Registry',
      message: 'Are You Sure You Want to Remove Registry?',
      yesCallback: () => {
        this.configRegistryApiService.deleteConfig(registry.id)
          .subscribe((data: any) => {
            this.loadRegistryData();
            this.globalLoaderService.hideLoader();
          },error =>{
            this.getDataError = error.message;
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }
}

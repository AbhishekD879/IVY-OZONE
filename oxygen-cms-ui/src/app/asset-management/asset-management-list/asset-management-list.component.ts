import * as _ from 'lodash';
import {Component, OnInit} from '@angular/core';
import {ApiClientService} from '@app/client/private/services/http';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {AppConstants} from '@app/app.constants';
import {AssetManagement} from '@app/client/private/models/assetManagement.model';
import {AssetManagementCreateComponent} from '@app/asset-management/asset-management-create/asset-management-create.component';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Router } from '@angular/router';

@Component({
  templateUrl: './asset-management-list.component.html',
  styleUrls: ['./asset-management-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class AssetManagementListComponent implements OnInit {

  public assetManagements: AssetManagement[];
  svgList: SafeHtml;
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Team name',
      'property': 'teamName',
      'link': {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      'name': 'Secondary team names',
      'property': 'secondaryNames'
    },
    {
      'name': 'Sport Id',
      'property': 'sportId'
    },
    {
      'name': 'Primary Colour',
      'property': 'primaryColour'
    },
    {
      'name': 'Secondary Colour',
      'property': 'secondaryColour'
    },
    {
      name: 'Image',
      property: 'svg',
      type: 'svgIcon'
    },
    {
      name: 'Image name',
      property: 'imagename',
    },
    {
      name: 'Status',
      property: 'active',
      type: 'boolean',
      alignment: 'center',
    },
  ];
  public searchableProperties: Array<string> = [
    'teamName'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private sanitizer: DomSanitizer,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.assetManagements()
      .findAllAssetManagements()
      .map(response => {
        return response.body;
      })
      .subscribe((assetsData: AssetManagement[]) => {
        assetsData.map( (assetData : AssetManagement)  => {
          assetData.imagename = assetData.teamsImage ? assetData.teamsImage.originalname :''; 
          assetData.size = assetData.teamsImage ? assetData.teamsImage.size : 0;
          assetData.svg = assetData.teamsImage ? assetData.teamsImage.svg :'';
          assetData.svgId = assetData.teamsImage ? this.getSvgId(assetData.teamsImage.svg) :'';
        })
        this.assetManagements = assetsData;
        this.svgList = this.createSvgList();
        this.globalLoaderService.hideLoader();
      }, error => {
         console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createAssetManagement(): void {
    this.dialogService.showCustomDialog(AssetManagementCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Asset Management',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (assetManagement: AssetManagement) => {
        this.apiClientService.assetManagements()
          .createAssetManagement(assetManagement)
          .map(response => {
            return response.body;
          })
          .subscribe((data: AssetManagement) => {
            const ASSET_BASE_PATH = '/byb/asset-management';
            this.assetManagements.push(data);
            this.router.navigate([`${ASSET_BASE_PATH}/${data.id}`]);
          }, error => {
            console.error(error.message);
          });
      }
    });
  }

  /**
   * Create svg list for the icon display
   * @returns { SafeHtml }
   */
  private createSvgList(): SafeHtml {
    const REP_WITHEMPTY = /\\\//g;

    let svgList = '';

    this.assetManagements.forEach((item) => {
      svgList += item.svg;
    });

    svgList = svgList.replace(REP_WITHEMPTY, '');

    return this.sanitizer.bypassSecurityTrustHtml(svgList);
  }

  removeHandler(assetManagement: AssetManagement): void {
    this.dialogService.showConfirmDialog({
      title: 'Asset Management',
      message: 'Are You Sure You Want to Remove Asset Management?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.assetManagements()
          .deleteAssetManagement(assetManagement.id)
          .subscribe(() => {
            _.remove(this.assetManagements, {id: assetManagement.id});
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  /**
   * Get svgid for the svg html string
   * @returns { string }
   */
  private getSvgId(svgString: string) : string {
    const emptyDiv = document.createElement('div');
    emptyDiv.innerHTML = svgString;
    return emptyDiv.querySelector('symbol').id || ''; 
  }
}

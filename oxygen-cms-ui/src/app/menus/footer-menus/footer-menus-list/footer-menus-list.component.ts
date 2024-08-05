import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';
import { HttpResponse } from '@angular/common/http';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {FooterMenu} from '../../../client/private/models/footermenu.model';
import {FooterMenusCreateComponent} from '../footer-menus-create/footer-menus-create.component';

import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants, CSPSegmentConstants, CSPSegmentLSConstants} from '@app/app.constants';
import {Order} from '../../../client/private/models/order.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { ISegmentMsg } from '@root/app/client/private/models/segment.model';

@Component({
  templateUrl: './footer-menus-list.component.html',
  styleUrls: ['./footer-menus-list.component.scss']
})
export class FooterMenusListComponent implements OnInit {

  public footerMenus: Array<FooterMenu>;
  public error: string;
  public searchField: string = '';
  public segmentChanged: boolean = true;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public orderMessage: string;

  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Link Title',
      'property': 'linkTitle',
      'link': {
        hrefProperty: 'id'
      },
      'type': 'link'
    }, {
      'name': 'Segment(s)',
      'property': 'inclusionList',
      'type': 'array'
    }, {
      'name': 'Segment(s) Exclusion',
      'property': 'exclusionList',
      'type': 'array'
    },
    {
      'name': 'Item Type',
      'property': 'itemType'
    },
    {
      'name': 'Target Uri',
      'property': 'targetUri'
    },
    {
      'name': 'In App',
      'property': 'inApp',
      'type': 'boolean'
    },
    {
      'name': 'Show Item For',
      'property': 'showItemFor'
    },
    {
      'name': 'Mobile',
      'property': 'mobile',
      'type': 'boolean'
    },
    {
      'name': 'Tablet',
      'property': 'tablet',
      'type': 'boolean'
    },
    {
      'name': 'Desktop',
      'property': 'desktop',
      'type': 'boolean'
    },
    {
      'name': 'Auth Required',
      'property': 'authRequired',
      'type': 'boolean'
    }
  ];
  public searchableProperties: Array<string> = [
    'linkTitle'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private router: Router,
    private segmentStoreService: SegmentStoreService
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.segmentStoreService.validateSegmentValue();
    
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.FOOTER_MENU_RIBBON) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });

    this.apiClientService.footerMenu().getFooterMenusBySegment(this.selectedSegment)
      .subscribe((footerMenu: HttpResponse<FooterMenu[]>) => {
        this.footerMenus = footerMenu.body;
        this.orderMessage = this.footerMenus.length ? this.footerMenus[0].message : '';
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  createFooterMenu(): void {
    this.dialogService.showCustomDialog(FooterMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Footer Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (footerMenu: FooterMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.footerMenu()
          .save(footerMenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: FooterMenu) => {
            this.footerMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/footer-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(footerMenu: FooterMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Footer Menu',
      message: 'Are You Sure You Want to Remove Footer Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.footerMenu()
          .delete(footerMenu.id)
          .subscribe(() => {
            _.remove(this.footerMenus, {id: footerMenu.id});
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  reorderHandler(newOrder: Order): void {
    this.apiClientService
      .footerMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Footer menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  /**
   * get footerMenu list based on segment selection
   * @param segment value
   */
  segmentHandler(segment: string): void {
    this.segmentChanged = false;
    this.globalLoaderService.showLoader();
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.FOOTER_MENU_RIBBON, segmentValue: segment });
    this.apiClientService.footerMenu().getFooterMenusBySegment(segment).subscribe((data: HttpResponse<FooterMenu[]>) => {
      this.segmentChanged = true;
      this.selectedSegment = segment;
      this.footerMenus = data.body;
      this.orderMessage = this.footerMenus.length ? this.footerMenus[0].message : '';
      this.globalLoaderService.hideLoader();
    });
  }
}

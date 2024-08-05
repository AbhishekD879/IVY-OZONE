import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {FooterLogo} from '../../../client/private/models/footerlogo.model';
import {FooterLogosCreateComponent} from '../footer-logos-create/footer-logos-create.component';

import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './footer-logos-list.component.html',
  styleUrls: ['./footer-logos-list.component.scss']
})
export class FooterLogosListComponent implements OnInit {

  public footerLogos: Array<FooterLogo>;
  public error: string;
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Title',
      'property': 'title',
      'link': {
        hrefProperty: 'id'
      },
      'type': 'link'
    },
    {
      'name': 'Uri',
      'property': 'target'
    }
  ];
  public searchableProperties: Array<string> = [
    'title'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.apiClientService.footerLogo()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: FooterLogo[]) => {
        this.footerLogos = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createFooterLogo(): void {
    this.dialogService.showCustomDialog(FooterLogosCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add new footer logo',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (footerLogo: FooterLogo) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.footerLogo()
          .save(footerLogo)
          .map(response => {
            return response.body;
          })
          .subscribe((data: FooterLogo) => {
            this.footerLogos.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/footer-logos/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(footerLogo: FooterLogo): void {
    this.dialogService.showConfirmDialog({
      title: 'Footer Logo',
      message: 'Are You Sure You Want to Remove Footer Logo?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.footerLogo()
          .delete(footerLogo.id)
          .subscribe(() => {
            _.remove(this.footerLogos, {id: footerLogo.id});
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
      .footerLogo()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Footer logo order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}

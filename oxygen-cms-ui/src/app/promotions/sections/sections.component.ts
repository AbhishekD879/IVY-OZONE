import { forkJoin } from 'rxjs/observable/forkJoin';
import { Order } from './../../client/private/models/order.model';
import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {DialogService} from '../../shared/dialog/dialog.service';
import {Router} from '@angular/router';
import {ApiClientService} from '../../client/private/services/http';
import { PromotionsSections } from '@root/app/client/private/models/promotions-sections.model';
import * as _ from 'lodash';
import {TableColumn} from '../../client/private/models/table.column.model';
import { AddPromotionsSectionsComponent } from '../add-promotions-sections/add-promotions-sections.component';
import {AppConstants} from '../../app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-sections',
  templateUrl: './sections.component.html',
  styleUrls: ['./sections.component.scss']
})
export class SectionsComponent implements OnInit {

  public searchField: string = '';
  public isLoading: boolean = false;
  public promotionsSections: PromotionsSections[] = [];

  filterProperties: Array<string> = [
    'name'
  ];

  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: '/promotions/section/'
      },
      type: 'link'
    },
    {
      name: 'Promotions IDs',
      property: 'promotionIds'
    },
    {
      name: 'Last Updated At',
      property: 'updatedAt',
      type: 'date'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService
        .promotionsSectionsService()
        .findAllByBrand()
        .finally(() => {
          this.hideSpinner();
        })
        .map((data: HttpResponse<PromotionsSections[]>) => {
          return data.body;
        }).subscribe((promotionsSections: PromotionsSections[]) => {
          this.promotionsSections = promotionsSections;
        });
  }

  /**
   * Reorder offers
   */
  reorderHandler(newOrder: Order) {
    this.apiClientService
        .promotionsSectionsService()
        .postNewPromotionsSectionsOrder(newOrder)
        .subscribe(() => {
        this.snackBar.open('New Promotions Sections Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  addPromotionsSections(): void {
    this.dialogService.showCustomDialog(AddPromotionsSectionsComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Static Block',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (promotionsSections: PromotionsSections) => {
        this.apiClientService.promotionsSectionsService()
            .add(promotionsSections)
            .map((result: HttpResponse<PromotionsSections>) => result.body)
            .subscribe((result: PromotionsSections) => {
          this.promotionsSections.unshift(result);
          this.router.navigate([`/promotions/section/${result.id}`]);
        }, () => {
          console.error('Can not create static block');
        });
      }
    });
  }

  removePromotionsSections(promotionsSections: PromotionsSections): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Static Block',
      message: `Are You Sure You Want to Remove Promotions Sections ${promotionsSections.name}`,
      yesCallback: () => {
        this.apiClientService
            .promotionsSectionsService()
            .remove(promotionsSections.id).subscribe(() => {
          _.remove(this.promotionsSections, {
            id: promotionsSections.id
          });
        });
      }
    });
  }

  removeHandlerMulty(promotionsSections: PromotionsSections[]): void {
    this.dialogService.showConfirmDialog({
      title: `Remove Feature Tab Modules (${promotionsSections.length})`,
      message: 'Are You Sure You Want to Remove Feature Tab Modules?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(promotionsSections.map(promotionSection => this.apiClientService.promotionsSectionsService().remove(promotionSection.id)))
          .subscribe(() => {
            this.promotionsSections.forEach((id) => {
              // @ts-ignore
              const index = _.findIndex(this.promotionsSections, { id: id });
              this.promotionsSections.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  private hideSpinner(): void {
    this.isLoading = false;
    this.globalLoaderService.hideLoader();
  }

}

import {CreatePaymentComponent} from '../create-payment/create-payment.component';
import {PaymentMethod} from './../../client/private/models/paymentMethod.model';
import {ApiClientService} from './../../client/private/services/http/index';
import {Component, OnInit} from '@angular/core';
import {DialogService} from '../../shared/dialog/dialog.service';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {HttpResponse} from '@angular/common/http';
import * as _ from 'lodash';
import {TableColumn} from '../../client/private/models/table.column.model';
import {AppConstants} from '../../app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';
import {Order} from '../../client/private/models/order.model';

@Component({
  selector: 'app-list-payments',
  templateUrl: './list-payments.component.html',
  styleUrls: ['./list-payments.component.scss']
})
export class ListPaymentsComponent implements OnInit {

  public isLoading: boolean = false;
  public filterProperties: string[] = [
    'name'
  ];
  public searchField: string = '';
  public paymentMethods: PaymentMethod[];

  public dataTableColumns: TableColumn[] = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Active',
      property: 'active',
      type: 'boolean'
    },
    {
      name: 'Identifier',
      property: 'identifier'
    },
    {
      name: 'Updated By',
      property: 'updatedByUserName'
    },
    {
      name: 'Updated At',
      property: 'updatedAt',
      type: 'date'
    },
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService
        .paymentMethods()
        .findAllByBrand()
        .map((response: HttpResponse<PaymentMethod[]>) => {
          return response.body;
        }).subscribe((methods: PaymentMethod[]) => {
          this.paymentMethods = methods;
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, (error) => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
  }

  public removePaymentMethod(method: PaymentMethod): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Payment Method',
      message: `Are You Sure You Want to Remove ${method.name} Payment Method`,
      yesCallback: () => {
        this.apiClientService.paymentMethods()
          .remove(method.id)
          .subscribe(() => {
            _.remove(this.paymentMethods, {id: method.id});
          });
      }
    });
  }

  public addNewPaymentMethod(): void {
    this.dialogService.showCustomDialog(CreatePaymentComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Payment Method',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (method: PaymentMethod) => {
        console.log(method);
        this.globalLoaderService.showLoader();
        this.apiClientService.paymentMethods()
            .add(method)
            .map((res: HttpResponse<PaymentMethod>) => res.body)
            .subscribe((paymentMethod: PaymentMethod) => {
          this.globalLoaderService.hideLoader();
          this.paymentMethods.unshift(paymentMethod);
          this.router.navigate([`/payment-methods/${paymentMethod.id}`]);
        }, () => {
          this.globalLoaderService.hideLoader();
          console.error('Can not create payment method');
        });
      }
    });
  }

  public reorderHandler(newOrder: Order): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
        .paymentMethods()
        .postNewOrder(newOrder)
        .subscribe(() => {
          this.globalLoaderService.hideLoader();
          this.snackBar.open('New Payment Methods Order Saved!!', 'OK!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }
}

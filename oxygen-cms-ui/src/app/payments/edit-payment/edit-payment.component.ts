import { PaymentsEnum } from '../payments.enum';
import { PaymentMethod } from '../../client/private/models/paymentMethod.model';
import { ActionButtonsComponent } from './../../shared/action-buttons/action-buttons.component';
import { Component, OnInit, ViewChild } from '@angular/core';
import { Breadcrumb } from '../../client/private/models/breadcrumb.model';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { mergeMap } from 'rxjs/operators';
import * as _ from 'lodash';
import { DialogService } from '../../shared/dialog/dialog.service';
import { ApiClientService } from '../../client/private/services/http/index';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';

@Component({
  selector: 'app-edit-payment',
  templateUrl: './edit-payment.component.html',
  styleUrls: ['./edit-payment.component.scss']
})
export class EditPaymentComponent implements OnInit {

  public isLoading: boolean = false;
  public breadcrumbsData: Breadcrumb[];
  public payment: PaymentMethod;
  public identifierTypes: string[];

  private id: string;
  private payments: PaymentMethod[];

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) { }

  ngOnInit(): void {
    this.identifierTypes = Object.keys(PaymentsEnum).map(k => PaymentsEnum[k]);
    this.loadInitialData();
  }

  public saveChanges(): void {
    this.apiClientService
        .paymentMethods()
        .edit(this.payment)
        .map((data: HttpResponse<PaymentMethod>) => data.body)
        .subscribe((payment: PaymentMethod) => {
          this.payment = payment;
          this.actionButtons.extendCollection(this.payment);
          this.dialogService.showNotificationDialog({
            title: `Payment Method Saving`,
            message: `Payment Method is Saved.`
          });
        });
  }

  public get noneUniqIdentifiers(): string {
    return this.payments
               .filter(p => p.identifier === this.payment.identifier)
               .map(p => p.name).join(', ');
  }

  public isUniqIdentifier(): boolean {
    return this.payments.filter(p => p.identifier === this.payment.identifier).length === 0;
  }

  public revertChanges(): void {
    this.loadInitialData();
  }

  public removePaymentMethod(): void {
    this.apiClientService
        .paymentMethods()
        .remove(this.payment.id)
        .subscribe(() => {
          this.router.navigate(['/payment-methods']);
        });
  }

  public isValidForm(payment: PaymentMethod): boolean {
    return !!(payment.name && payment.name.length > 0 && payment.identifier && payment.identifier.length > 0);
  }

  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute
        .params
        .pipe(
          mergeMap((params: Params) => {
            this.id = params['id'];
            return this.apiClientService.paymentMethods().findAllByBrand();
          })
        )
        .map((response: HttpResponse<PaymentMethod[]>) => {
          return response.body;
        })
        .subscribe((data: PaymentMethod[]) => {
          this.payments = data.filter(d => d.id !== this.id);
          this.payment = _.find(data, { id: this.id});
          this.breadcrumbsData = [{
            label: `Payments`,
            url: `/payment-methods`
          }, {
            label: this.payment.name,
            url: `/payment-methods/${this.payment.id}`
          }];
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removePaymentMethod();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

}

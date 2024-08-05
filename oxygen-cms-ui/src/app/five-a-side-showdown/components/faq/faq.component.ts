import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AppConstants } from '@app/app.constants';
import { DataTableColumn } from '@app/client/private/models';
import { Order } from '@app/client/private/models/order.model';
import { ErrorService } from '@app/client/private/services/error.service';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import {
  FAQ_ERROR_LABELS, FAQ_LIST_FORM,
  FAQ_ROUTES, FAQ_SNACKBAR, FAQ_TABLE_COLUMNS,
  FILTER_PROPERTIES, REMOVE_CONFIRMATION_DIALOG, REMOVE_NOTIFICATION_DIALOG
} from '@app/five-a-side-showdown/constants/faq.constants';
import { IFAQ } from '@app/five-a-side-showdown/models/frequently-asked-questions';

@Component({
  selector: 'app-faq',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.scss']
})
export class FaqComponent implements OnInit {
  isLoading: boolean = false;
  faqs: IFAQ[] = [];
  dataTableColumns: DataTableColumn[] = FAQ_TABLE_COLUMNS;
  filterProperties: string[] = FILTER_PROPERTIES;
  searchField: string = '';
  readonly FAQ_LIST_FORM: {[key: string]: string} = FAQ_LIST_FORM;

  constructor(private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService,
    private router: Router,
    public snackBar: MatSnackBar,
    private dialogService: DialogService) { }

  ngOnInit(): void {
    this.apiClientService.faqService()
      .getFAQs()
      .map((response: HttpResponse<IFAQ[]>) => {
        return response.body;
      })
      .subscribe((faqs: IFAQ[]) => {
        this.faqs = faqs;
        this.isLoading = false;
        this.globalLoaderService.hideLoader();
      }, (error) => {
        this.errorService.emitError(
          `${FAQ_ERROR_LABELS.getFAQs}`
        );
        this.isLoading = false;
        this.faqs = [];
        this.globalLoaderService.hideLoader();
      });
  }

  /**
   * To create FAQ
   */
  createFAQ(): void {
    this.router.navigate([`${FAQ_ROUTES.base}/add-edit`]);
  }

  /**
   * To reorder when changed
   * @param {order} newOrder
   */
  reorderHandler(newOrder: Order): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
      .faqService()
      .postNewOrder(newOrder)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.snackBar.open(FAQ_SNACKBAR.message, FAQ_SNACKBAR.action, {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  /**
   * To remove FAQ
   * @param {IFAQ} request
   */
  removeFAQ(request: IFAQ): void {
    this.dialogService.showConfirmDialog({
      title: REMOVE_CONFIRMATION_DIALOG.title,
      message: `${REMOVE_CONFIRMATION_DIALOG.message}?`,
      yesCallback: () => {
        this.faqs = this.faqs.filter((faq: IFAQ) => {
          return faq.id !== request.id;
        });
        this.apiClientService.faqService().removeFAQForId(request.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: REMOVE_NOTIFICATION_DIALOG.title,
            message: REMOVE_NOTIFICATION_DIALOG.message
          });
        });
      }
    });
  }

}

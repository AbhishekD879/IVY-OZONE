import { HttpResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Breadcrumb } from '@app/client/private/models';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import {
  ACTION_TYPE,
  BREADCRUMBS_LABEL,
  FAQFORM,
  FAQ_DEFAULT_VALUS,
  FAQ_ERROR_LABELS,
  FAQ_ROUTES, SAVE_NOTIFICATION_DIALOG
} from '@app/five-a-side-showdown/constants/faq.constants';
import { IFAQ } from '@app/five-a-side-showdown/models/frequently-asked-questions';
import { ErrorService } from '@app/client/private/services/error.service';

@Component({
  selector: 'app-add-edit-faq',
  templateUrl: './add-edit-faq.component.html',
  styleUrls: ['./add-edit-faq.component.scss']
})
export class AddEditFaqComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  breadCrumbs: Breadcrumb[];
  faq: IFAQ;
  faqForm: FormGroup;
  isLoading: boolean = false;
  isEdit: boolean = false;
  readonly FAQFORM: {[key:string]: string} = FAQFORM;
  private faqId: string;

  constructor(private brandService: BrandService,
    private activatedRoute: ActivatedRoute,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private router: Router,
    private dialogService: DialogService,
    private errorService: ErrorService) { }

  ngOnInit(): void {
    this.faqForm = new FormGroup({
      question: new FormControl(''),
      answer: new FormControl('')
    });
    this.faqId = this.activatedRoute.snapshot.params['id'];
    this.isEdit = !!this.faqId;
    if (this.isEdit) {
      this.loadInitData();
    } else {
      this.faq = {
        ...FAQ_DEFAULT_VALUS,
        brand: this.brandService.brand
      };
    }
  }

  /**
   * Update Blurb
   * @param {string}  newBlurbText
   * @param {string} field
   */
  updateBlurb(newBlurbText: string, field: string): void {
    this.faq[field] = newBlurbText || null;
  }

  /**
   * Handler for all the actions
   * @param {string} event
   */
  actionsHandler(event: string): void {
    switch (event) {
      case ACTION_TYPE.remove:
        this.removeFAQ();
        break;
      case ACTION_TYPE.save:
        if (this.isEdit) {
          this.editFAQ();
        } else {
          this.saveFAQ();
        }
        break;
      case ACTION_TYPE.revert:
        this.revertChanges();
        break;
      default:
        break;
    }
  }

  /**
   * Save the market details
   */
  private saveFAQ(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.faqService()
      .createFAQ(this.faq)
      .map((response: HttpResponse<IFAQ>) => {
        return response.body;
      })
      .subscribe((faq: IFAQ) => {
        this.faq = faq;
        this.actionButtons.extendCollection(this.faq);
        this.dialogService.showNotificationDialog({
          title: SAVE_NOTIFICATION_DIALOG.title,
          message: SAVE_NOTIFICATION_DIALOG.message
        });
        this.router.navigate([FAQ_ROUTES.base]);
        this.globalLoaderService.hideLoader();
      }, (error) => {
        this.errorService.emitError(
          `${FAQ_ERROR_LABELS.createFAQ}`
        );
        this.globalLoaderService.hideLoader();
      });
  }

  /**
   * Revert the changes to initial data
   */
  private revertChanges(): void {
    if (this.isEdit) {
      this.loadInitData();
    } else {
      this.faq = {
        ...FAQ_DEFAULT_VALUS,
        brand: this.brandService.brand
      };
    }
  }

  /**
   * To Edit FAQ
   */
  private editFAQ(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.faqService()
      .editFAQById(this.faqId, this.faq)
      .map((response: HttpResponse<IFAQ>) => {
        return response.body;
      })
      .subscribe((faq: IFAQ) => {
        this.faq = faq;
        this.actionButtons.extendCollection(this.faq);
        this.dialogService.showNotificationDialog({
          title: SAVE_NOTIFICATION_DIALOG.title,
          message: SAVE_NOTIFICATION_DIALOG.message
        });
        this.router.navigate([FAQ_ROUTES.base]);
        this.globalLoaderService.hideLoader();
      }, (error) => {
        this.errorService.emitError(
          `${FAQ_ERROR_LABELS.editFAQ}`
        );
        this.globalLoaderService.hideLoader();
      });
  }

  /**
   * Remove the racing edp market
   */
  private removeFAQ(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.faqService().removeFAQForId(this.faq.id).subscribe(() => {
      this.router.navigate([FAQ_ROUTES.base]);
      this.globalLoaderService.hideLoader();
    }, (error) => {
      this.errorService.emitError(
        `${FAQ_ERROR_LABELS.editFAQ}`
      );
      this.globalLoaderService.hideLoader();
    });
  }

  /**
   * To Load initial data
   * @param {boolean} isLoading
   */
  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.apiClientService.faqService().getFAQForId(this.faqId)
      .map((response: HttpResponse<IFAQ>) => response.body)
      .subscribe((faq: IFAQ) => {
        this.faq = faq;
        this.breadCrumbs = [
          {
            label: BREADCRUMBS_LABEL,
            url: FAQ_ROUTES.base
          },
          {
            label: 'Question',
            url: `${FAQ_ROUTES.base}/${this.faq.id}`
          }
        ];
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      }, () => {
        this.errorService.emitError(
          `${FAQ_ERROR_LABELS.getFAQ}`
        );
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
  }

}

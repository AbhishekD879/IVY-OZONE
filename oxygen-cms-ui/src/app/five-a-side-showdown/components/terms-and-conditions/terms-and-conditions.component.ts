import { Component, OnInit, ViewChild } from '@angular/core';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { TinymceComponent } from '@app/shared/tinymce/tinymce.component';
import { TANDC_DEFAULT_VALUS, T_AND_C_FORM } from '@app/five-a-side-showdown/constants/terms-and-conditions.constants';
import { ITermsAndConditions } from '@app/five-a-side-showdown/models/terms-and-conditions';

@Component({
  selector: 'app-terms-and-conditions',
  templateUrl: './terms-and-conditions.component.html',
  styleUrls: ['./terms-and-conditions.component.scss']
})
export class TermsAndConditionsComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('text') headerTextEditor: TinymceComponent;

  termsAndConditions: ITermsAndConditions;
  readonly T_AND_C_FORM: {[key: string]: string} = T_AND_C_FORM;

  constructor(private apiService: ApiClientService,
    private dialogService: DialogService,
    private brandService: BrandService) { }

  ngOnInit(): void {
    this.loadInitialData();
    this.termsAndConditions = TANDC_DEFAULT_VALUS;
  }

  /**
   * To Verify terms and conditions
   * @param {ITermsAndConditions} termsConditions
   * @returns {boolean}
   */
  verifyTermsAndConditions(termsConditions: ITermsAndConditions): boolean {
    return !!termsConditions;
  }

  /**
   * To Update blurb
   * @param {string} newBlurbText
   */
  updateBlurb(newBlurbText: string): void {
    this.termsAndConditions.text =  newBlurbText || null;
  }

  /**
   * To Handle actions
   * @param {string} event
   */
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        break;
    }
  }

  /**
   * To Load initial data
   */
  private loadInitialData(): void {
    this.apiService.termsConditionService()
     .getDetailsByBrand()
     .subscribe((data: {body: ITermsAndConditions}) => {
        this.termsAndConditions = data.body;
        this.headerTextEditor.update(this.termsAndConditions.text);
        this.actionButtons.extendCollection(this.termsAndConditions);
      }, error => {
        if (error.status === 404) {
          this.termsAndConditions = this.getDefaultValues();
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  /**
   * To assign default values
   * @returns {ITermsAndConditions}
   */
  private getDefaultValues(): ITermsAndConditions {
    const popup = {...TANDC_DEFAULT_VALUS};
    popup.brand = this.brandService.brand;
    return popup;
  }

  /**
   * To handle save and edit scenarios
   */
  private save(): void {
    if (this.termsAndConditions.createdAt) {
      this.sendRequest('updateTermsAndConditions');
    } else {
      this.sendRequest('saveTermsAndConditions');
    }
  }

  /**
   * To revert changes
   */
  private revert(): void {
    this.loadInitialData();
  }

  /**
   * To save and edit the t&c
   * @param {string} requestType
   */
  private sendRequest(requestType: string) : void{
    this.apiService.termsConditionService()[requestType](this.termsAndConditions)
      .map((response) => response.body)
      .subscribe((data: ITermsAndConditions) => {
        this.termsAndConditions = data;
        this.actionButtons.extendCollection(this.termsAndConditions);
        this.dialogService.showNotificationDialog({
          title: 'Success',
          message: 'Your changes have been saved'
        });
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

}

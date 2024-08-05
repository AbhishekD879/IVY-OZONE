import { Component, OnInit, ViewChild } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { INewSignPosting } from '@app/client/private/models/fanzone.model';
import { NEWSIGNPOSTING, NEWSIGNPOSTING_CONST } from '@app/fanzone/constants/fanzone.constants';
import { DateRange } from '@app/client/private/models';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { ErrorService } from '@app/client/private/services/error.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BrandService } from '@root/app/client/private/services/brand.service';

@Component({
  selector: 'app-fanzone-new-signposting',
  templateUrl: './fanzone-new-signposting.component.html'
})
export class FanzoneNewSignpostingComponent implements OnInit {
  public form: FormGroup;
  fanzoneNewSignposting: INewSignPosting;
  isReady: boolean;
  public readonly NEWSIGNPOSTING_CONST = NEWSIGNPOSTING_CONST;
  public readonly NEWSIGNPOSTING = NEWSIGNPOSTING;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  breadcrumbsData = [{
    label: `Fanzone`,
    url: `/fanzones`
  }, {
    label: 'New Sign Posting',
    url: `/fanzones/new-signposting`
  }];

  constructor(
    private dialogService: DialogService,
    private brandService: BrandService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.fanzoneNewSignposting = {
      ...NEWSIGNPOSTING,
      brand: this.brandService.brand,
      pageName: 'fanzone-new-signposting'
    };
    this.getNewSignPosting();
  }

  saveSignPosting() {
    const method = this.fanzoneNewSignposting.id ? 'put' : 'post';
    this.fanzonesAPIService.saveNewSignPosting(method, this.fanzoneNewSignposting, this.fanzoneNewSignposting.id || '')
      .subscribe(data => {
        this.fanzoneNewSignposting = data.body;
        this.actionButtons.extendCollection(this.fanzoneNewSignposting);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Fanzone New Sign Posting is Stored'
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  generateForm(): void {
    this.form = new FormGroup({
      active: new FormControl(this.fanzoneNewSignposting.active, [Validators.required]),
    });
  }

  getNewSignPosting(): void {
    this.fanzonesAPIService.getNewSignPosting()
      .subscribe(data => {
        this.fanzoneNewSignposting = data.body?.id ? data.body : this.fanzoneNewSignposting;
        this.isReady = true;
        this.generateForm();
      });
  }

  handleDateUpdate(data: DateRange) {
    this.fanzoneNewSignposting.startDate = data.startDate;
    this.fanzoneNewSignposting.endDate = data.endDate;
  }

  public validationHandler(): boolean {
    return this.form && this.form.valid
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveSignPosting();
        break;
      case 'revert':
        this.getNewSignPosting();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}

import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import {
  ACTION_TYPE,
  BREADCRUMB_DATA,
  CONTESTFORM,
  CONTEST_ERROR_LABELS,
  DOWNLOAD_CSV_BUTTON,
  ICON_SVG_FORM_NAME,
  IMAGE_FORMAT_DIALOG,
  SAVE_NOTIFICATION_DIALOG,
  SAVE_SVG_IMAGES_FAILURE_MSG,
  SPONSOR_SVG_FORM_NAME,
  SUPPORTED_IMAGE_FILE_EXTENSIONS,
  UPLOAD_BTNS,
} from '@app/five-a-side-showdown/constants/contest-manager.constants';
import { PrizePoolComponent } from '@app/five-a-side-showdown/components/prize-pool/prize-pool.component';
import { ErrorService } from '@app/client/private/services/error.service';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import {
  ContestForm,
  HTMLInputEvent,
  IContest,
} from '@app/five-a-side-showdown/models/contest-manager';
import { IPrizePool } from '@app/five-a-side-showdown/models/prize-pool';
import { IPrize } from '@app/five-a-side-showdown/models/prize-manager';
import { environment } from '@environment/environment';
import { BrandService } from '@app/client/private/services/brand.service';
import { Clipboard } from '@angular/cdk/clipboard';

@Component({
  selector: 'edit-contest',
  templateUrl: './edit-contest.component.html',
  styleUrls: ['./edit-contest.component.scss'],
})
export class EditContestComponent implements OnInit {
  @ViewChild('actionButtons') _actionButtons: ActionButtonsComponent;

  @ViewChild('sponsorSvgFileInput')
  sponsorSvgFileInput: ElementRef<HTMLInputElement>;

  @ViewChild('iconSvgFileInput') iconSvgFileInput: ElementRef<HTMLInputElement>;

  @ViewChild(PrizePoolComponent) prizePoolComponent: PrizePoolComponent;

  public breadcrumbsData: Breadcrumb[];

  public contestid: string;

  public contestManagerForm: IContest;

  public iconSvgFileName: string = '';

  public iconSvgFile: File;

  public sponsorSvgFileName: string = '';

  public sponsorSvgFile: File;

  public isLoading: boolean = false;

  public prizePool: IPrizePool;

  public readonly downloadCSV = DOWNLOAD_CSV_BUTTON;

  readonly CONTESTFORM: ContestForm = CONTESTFORM;

  constructor(
    private activatedRoute: ActivatedRoute,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private router: Router,
    private errorService: ErrorService,
    private brandService: BrandService,
    private clipboard: Clipboard
  ) {}

  ngOnInit(): void {
    this.loadContestData();
  }

  /**
   * To convert alpha to Numeric
   * @param {HTMLInputEvent} event
   * @returns {void}
   */
  alphaToNumeric(event: HTMLInputEvent): void {
    event.target.value = event.target.value.replace(/\D/gi, '').trim();
  }

  /**
   * To avoid special characters
   * @param {HTMLInputEvent} event
   * @returns {void}
   */
  blockSpecialChars(event: HTMLInputEvent): void {
    event.target.value = event.target.value.replace(/[^a-zA-Z0-9]/g, '');
  }

  /**
   * To trigger a event when paytable is changed
   * @param payTable
   */
  onPayTableChanged(payTable: IPrize[]): void {
    this.contestManagerForm.payTable = payTable.slice();
  }

  /**
   * To trigger a event when prize pool information is updated
   * @param prizePool
   */
  onPrizePoolChanged(prizePool: IPrizePool): void {
    this.contestManagerForm.prizePool = JSON.parse(JSON.stringify(prizePool));
  }


  /**
   * To trigger a event when contest type information is updated
   */

  onContestTypeChange($event): void {
    if($event.checked){
      this.contestManagerForm.isPrivateContest = true;
    }else{
      this.contestManagerForm.isPrivateContest = null;
    }
  }

  /**
   * Loads contest data based on edited contest id
   */
  private loadContestData(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.contestid = params.contestid;
      this.loadEditData();
    });
  }

  /**
   * Loads contest editable data based on contestid
   */
  private loadEditData(): void {
    this.showHideSpinner();
    this.apiClientService
      .contestManagerService()
      .getContestForId(this.contestid)
      .map((response: HttpResponse<IContest>) => {
        return response.body;
      })
      .subscribe(
        (contestIdData: IContest) => {
          this.contestManagerForm = contestIdData;
          this.prizePool = contestIdData.prizePool;
          this.resetSvgDefaults();
          if (this.contestManagerForm.icon) {
            this.iconSvgFileName = this.contestManagerForm.icon.originalname;
          }
          if (this.contestManagerForm.sponsorLogo) {
            this.sponsorSvgFileName = this.contestManagerForm.sponsorLogo.originalname;
          }
          this.initBreadcrumbs();
          this.showHideSpinner(false);
        },
        (error) => {
          this.errorService.emitError(
            `${CONTEST_ERROR_LABELS.editingContests} ${this.contestid}`
          );
          this.showHideSpinner(false);
        }
      );
  }

  /**
   * Reset svg image Files for icon and sponsor logo
   */
  resetSvgDefaults() {
    this.iconSvgFileName = '';
    this.sponsorSvgFileName = '';
    this.iconSvgFile = null;
    this.sponsorSvgFile = null;
    this.contestManagerForm.isiconSvgChanged = false;
    this.contestManagerForm.isSponsorSvgChanged = false;
  }

  /**
   * Init bredcrumbs paths data to contests.
   */
  private initBreadcrumbs(): void {
    this.breadcrumbsData = [
      {
        label: `${BREADCRUMB_DATA.contestLabel}`,
        url: `${BREADCRUMB_DATA.contests_url}`,
      },
      {
        label: this.contestManagerForm.name,
        url: `${BREADCRUMB_DATA.edit_url}/${this.contestManagerForm.id}`,
      },
    ];
  }

  /**
   * Show or Hide spinner for the api calls
   * @param {boolean} toShow
   */
  private showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * Save the contest manager details
   */
  public saveChanges(): void {
    if (this.prizePoolComponent && this.prizePoolComponent.prizePool) {
      this.contestManagerForm.prizePool = this.prizePoolComponent.prizePool;
    }
    this.globalLoaderService.showLoader();
    this.setUTCDate(this.contestManagerForm);
    this.apiClientService
      .contestManagerService()
      .saveContestChanges(this.contestid, this.contestManagerForm)
      .map((response: HttpResponse<IContest>) => {
        return response.body;
      })
      .subscribe(
        (savedContestData: IContest) => {
          this.contestManagerForm = savedContestData;
          this.initBreadcrumbs();
          if (this.iconSvgFile || this.sponsorSvgFile) {
            this.sendSvgImages();
          } else {
            this.globalLoaderService.hideLoader();
            this._actionButtons.extendCollection(this.contestManagerForm);
            this.dialogService.showNotificationDialog({
              title: SAVE_NOTIFICATION_DIALOG.title,
              message: SAVE_NOTIFICATION_DIALOG.message,
            });
          }
        },
        (error) => {
          this.globalLoaderService.hideLoader();
          this.errorService.emitError(
            `${CONTEST_ERROR_LABELS.savingContest} ${this.contestid}`
          );
        }
      );
  }

  /**
   * To convert start time to UTC date format
   * @param {IContest} contest
   * @returns {void}
   */
   private setUTCDate(contest: IContest): void {
    const startDate: Date = new Date(contest.startDate);
    const utc: Date = new Date(Date.UTC(startDate.getFullYear(), startDate.getMonth(),
    startDate.getDate(), startDate.getHours(), startDate.getMinutes(), startDate.getSeconds()));
    contest.utcStartDate = utc.toISOString();
  }

  /**
   * Send the uploaded svg images against the contestid
   */
  private sendSvgImages(): void {
    const formData = new FormData();
    formData.append(ICON_SVG_FORM_NAME, this.iconSvgFile);
    formData.append(SPONSOR_SVG_FORM_NAME, this.sponsorSvgFile);
    this.apiClientService
      .contestManagerService()
      .uploadSvgImage(this.contestid, formData)
      .map((response: HttpResponse<IContest>) => {
        return response.body;
      })
      .subscribe(
        (savedContestData: IContest) => {
          this.globalLoaderService.hideLoader();
          this.contestManagerForm = savedContestData;
          this.clearSvgImageFields();
          this._actionButtons.extendCollection(this.contestManagerForm);
          this.dialogService.showNotificationDialog({
            title: SAVE_NOTIFICATION_DIALOG.title,
            message: SAVE_NOTIFICATION_DIALOG.message,
          });
        },
        (error: HttpErrorResponse) => {
          this.globalLoaderService.hideLoader();
          this._actionButtons.extendCollection(this.contestManagerForm);
          this.errorService.emitError(
            `${SAVE_SVG_IMAGES_FAILURE_MSG.msg} ${this.contestid}`
          );
        }
      );
  }

  /**
   * Clear the svg image fields for the icon and sponsorLogo
   */
  private clearSvgImageFields(): void {
    this.iconSvgFile = null;
    this.iconSvgFileName = this.contestManagerForm.icon
      ? this.contestManagerForm.icon.originalname
      : '';
    this.contestManagerForm.isiconSvgChanged =  false;
    this.sponsorSvgFile =  null;
    this.sponsorSvgFileName = this.contestManagerForm.sponsorLogo
      ? this.contestManagerForm.sponsorLogo.originalname
      : '';
    this.contestManagerForm.isSponsorSvgChanged =  false;
  }

  /**
   * Check for real and test account selection
   * @returns { void }
   */
  public checkForAccountSel(): void {
    if (!this.contestManagerForm.realAccount && !this.contestManagerForm.testAccount) {
      this.errorService.emitError(
        `${CONTEST_ERROR_LABELS.enableAccountSelection}`
      );
    }
  }

  /**
   * Update the selected date in ISO form from the date selection
   * picker
   * @param {string} date
   */
  public handleStartDate(date: string): void {
    this.contestManagerForm.startDate = new Date(date).toISOString();
  }

  /**
   * Check if all the mandatory fields for contest form are given or not
   * @param {IContest} contestManagerForm
   */
  public isValidModel(contestManagerForm: IContest): boolean {
    return Boolean(
      contestManagerForm.name.length > 0 &&
        contestManagerForm.startDate.length > 0 &&
        contestManagerForm.entryStake &&
        (contestManagerForm.realAccount || contestManagerForm.testAccount)
    );
  }

  /**
   * Selected action for the editing contest
   * @param {string} action
   */
  public actionsHandler(action: string): void {
    switch (action) {
      case ACTION_TYPE.remove:
        this.removeContest();
        break;
      case ACTION_TYPE.save:
        this.saveChanges();
        break;
      case ACTION_TYPE.revert:
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * Remove the contest for the given contest id
   */
  removeContest(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
      .contestManagerService()
      .removeContestForId(this.contestid)
      .subscribe(
        () => {
          this.globalLoaderService.hideLoader();
          this.router.navigate([BREADCRUMB_DATA.contests_url]);
        },
        (error) => {
          this.globalLoaderService.hideLoader();
          this.errorService.emitError(
            `${CONTEST_ERROR_LABELS.removingContest} ${this.contestid}`
          );
        }
      );
  }

  /**
   * Reverr the edited changes for the contest id
   */
  revertChanges(): void {
    this.loadEditData();
  }

  /**
   * Validate the uploaded file for svg and store the file
   * instance for icon and sponsor logo
   * @param {HTMLInputEvent} event
   * @param {string} fieldName
   */
  prepareToUploadFile(event: HTMLInputEvent, fieldName: string): void {
    const ICONSVGFILE: string = 'iconSvgFile';
    const SPONSORSVGFILE: string = 'sponsorSvgFile';
    if (event) {
      const file: File = event.target.files[0];
      const fileType = file.type;

      if (SUPPORTED_IMAGE_FILE_EXTENSIONS.indexOf(fileType) === -1) {
        this.dialogService.showNotificationDialog({
          title: IMAGE_FORMAT_DIALOG.title,
          message: IMAGE_FORMAT_DIALOG.message,
        });
        return;
      }
      if (fieldName === ICONSVGFILE) {
        this.iconSvgFileName = file.name;
        this.iconSvgFile = file;
        this.contestManagerForm.isiconSvgChanged = true;
      } else if (fieldName === SPONSORSVGFILE) {
        this.sponsorSvgFileName = file.name;
        this.sponsorSvgFile = file;
        this.contestManagerForm.isSponsorSvgChanged = true;
      }
    }
  }

  /**
   * Handle the click for upload image
   * @param {HTMLInputEvent} event
   */
  handleUploadImageClick(event: HTMLInputEvent): void {
    const input = event.target.parentElement.previousElementSibling.querySelector(
      'input'
    );
    input.click();
  }

  /**
   * Get the button name for the upload
   * @param {string} fileName
   */
  getButtonName(fileName: string): string {
    return fileName && fileName.length > 0
      ? UPLOAD_BTNS.changeFileLabel
      : UPLOAD_BTNS.uploadFileLabel;
  }

  /**
   * Remove the image based on the selected file input (icon / Sponsor logo)
   * @param {string} fieldName
   */
  removeImage(fieldName: string): void {
    const ICONSVGFILE: string = 'iconSvgFile';
    const SPONSORSVGFILE: string = 'sponsorSvgFile';
    if (fieldName === ICONSVGFILE) {
      this.contestManagerForm.isiconSvgChanged = false;
      this.iconSvgFileName = '';
      this.iconSvgFile = null;
      this.iconSvgFileInput.nativeElement.value = '';
      this.contestManagerForm.icon = null;
    } else if (fieldName === SPONSORSVGFILE) {
      this.contestManagerForm.isSponsorSvgChanged = false;
      this.sponsorSvgFileName = '';
      this.sponsorSvgFile = null;
      this.sponsorSvgFileInput.nativeElement.value = '';
      this.contestManagerForm.sponsorLogo = null;
    }
  }

  /**
   * Updates the new description from the text editor
   * @param {string} newDescription
   */
  updateDescription(newDescription: string): void {
    this.contestManagerForm.description =  newDescription || null;
  }

  /**
   * Updates the new blurb from the text editor
   * @param {string} newBlurbText
   */
  updateBlurb(newBlurbText: string): void {
    this.contestManagerForm.blurb =  newBlurbText || null;
  }

  /**
   * copy contest URL to clipboard
   */
   copyToClipboard(): void{
    this.clipboard.copy(this.contestManagerForm.contestURL);
  }

  /**
   * Updates the new entry confirmation from the text editor
   * @param {string} newEntryConfirmationText
   */
  updateEntryConfirmation(newEntryConfirmationText: string): void {
    this.contestManagerForm.entryConfirmationText =  newEntryConfirmationText || null;
  }

  /**
   * To download csv
   * @param {string} type
   */
  onDownloadCSV(type: string): void {
    const urlType: string = type === 'contest' ? this.downloadCSV.contestURL : this.downloadCSV.prizeReportURL;
    const csvURL: string = `${environment.cmsRoot[this.brandService.brand]}/files/${urlType}_${this.contestid}.csv`;
    const link: HTMLAnchorElement = document.createElement('a');
    link.href = csvURL;
    link.target = '_blank';
    link.download = `${urlType}_${this.contestid}.csv`;
    link.click();
  }
}

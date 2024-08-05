import { Component, Inject, OnInit } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { BrandService } from "@app/client/private/services/brand.service";
import { ConfirmDialogComponent } from "@app/shared/dialog/confirm-dialog/confirm-dialog.component";
import {
  CONTESTFORM,
  CONTEST_DEFAULT_VALUS,
  CONTEST_ERROR_LABELS,
} from "@app/five-a-side-showdown/constants/contest-manager.constants";
import {
  ContestForm,
  HTMLInputEvent,
  IAddContest,
  DialogData,
  IContest
} from "@app/five-a-side-showdown/models/contest-manager";
import { GlobalLoaderService } from "@root/app/shared/globalLoader/loader.service";
import { ApiClientService } from "@root/app/client/private/services/http";
import { HttpResponse } from "@angular/common/http";
import { ErrorService } from "@root/app/client/private/services/error.service";

@Component({
  selector: "app-add-contest",
  templateUrl: "./add-contest.component.html"
})
export class AddContestComponent implements OnInit {
  public contest: IAddContest;
  public readonly CONTESTFORM: ContestForm = CONTESTFORM;
  public isClone: boolean;
  public isLoading: boolean = false;
  private isCloned:boolean = false;
  private cloneModalData: IContest;

  constructor(
    @Inject(MAT_DIALOG_DATA) public modalData: DialogData,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private errorService: ErrorService
  ) {}

  ngOnInit(): void {
    this.loadAddContestDefaults();
    this.isClone = this.modalData.data.dialogType === 'clone';
    if(this.isClone) {
      this.cloneModalData = {...this.modalData.data.dialogData};
      this.cloneModalData.intialContestId = this.cloneModalData.id
      this.cloneModalData.event = "";
      this.cloneModalData.display = false;
      this.cloneModalData.name = "";
      this.populateCloneDetails();
    }
  }

  /**
   * Load default values for add contest
   */
  loadAddContestDefaults(): void {
    this.contest = {
      ...CONTEST_DEFAULT_VALUS,
      brand: this.brandService.brand,
      startDate: new Date().toISOString(),
    };
  }

  /**
   * Click handler for closing of modal dialog
   */
  closeDialog(): void {
    this.dialogRef.close({cloned: this.isCloned, closeCallback: true});
  }

  /**
   * Returns the added contest instance
   * @returns {IAddContest}
   */
  addContest(): IAddContest {
    if(this.isClone) {
      let {name, entryStake, startDate, ...cloneData} = this.cloneModalData
      Object.assign(this.contest, cloneData);
      this.convertToUTCDate(this.contest);
    }
    return this.contest
  }

  /**
   * Click handler for cloning the contest of modal dialog
   */
  cloneContest(): void {
    let clonedContest:any = {};
    Object.assign(clonedContest, this.cloneModalData, this.contest);
    this.showHideSpinner();
    this.convertToUTCDate(clonedContest);
    this.apiClientService
      .contestManagerService()
      .cloneContest(clonedContest)
      .map((response: HttpResponse<IContest>) => {
        return response.body;
      })
      .subscribe(
        (savedcontest: IContest) => {
          this.populateCloneDetails();
          this.showHideSpinner(false);
          this.isCloned = true;
        },
        (error) => {
          this.showHideSpinner(false);
          this.errorService.emitError(
            CONTEST_ERROR_LABELS.createContestLabel
          );
        }
      );
  }

  /**
   * Show or Hide spinner for the api calls
   * @param {boolean} toShow
   */
   public showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
    }

  /**
   * To populate the values of the cloned contest
   */
    private populateCloneDetails(): void{
      Object.keys(this.contest).forEach(key=> this.contest[key] = this.cloneModalData[key]);
    }

  /**
   * To convert start time to UTC date format.
   * @param {IContest} contest
   * @returns {void}
   */
  private convertToUTCDate(contest: IContest | IAddContest): void {
    const currentDate: Date = new Date(contest.startDate);
    const utcDate = new Date(Date.UTC(currentDate.getFullYear(), currentDate.getMonth(),
    currentDate.getDate(), currentDate.getHours(), currentDate.getMinutes(), currentDate.getSeconds()));
    contest.utcStartDate = utcDate.toISOString();
  }

  /**
   * Handler for the date selection from the date picker
   * @param {string} date
   */
  handleStartDate(date: string): void {
    this.contest.startDate =new Date(date).toISOString();
  }

  /**
   * To avoid special characters 
   * @param  event 
   * @returns  
   */
  blockSpecialChars(event: HTMLInputEvent): void {
    event.target.value = event.target.value.replace(/[^a-zA-Z0-9]/g,'');
  }
}

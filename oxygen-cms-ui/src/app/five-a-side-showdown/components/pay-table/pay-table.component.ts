import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { AppConstants } from '@app/app.constants';
import { IPrize } from '@app/five-a-side-showdown/models/prize-manager';
import { DataTableColumn } from '@app/client/private/models';
import {
  ADD_PRIZE_DIALOG,
  EDIT_PRIZE_DIALOG,
  FILTER_PROPERTIES,
  ICON_FILE,
  PAY_TABLE_COLUMNS,
  PRIZE_ERROR_LABELS,
  PRIZE_TYPES_MAPPER,
  REMOVE_PRIZE_DIALOG,
  SIGNPOSTING_FILE
} from '@app/five-a-side-showdown/constants/pay-table.constants';
import { DialogService } from '@app/shared/dialog/dialog.service';
import {
  AddEditPrizeComponent
} from '@app/five-a-side-showdown/components/add-edit-prize/add-edit-prize.component';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { HttpResponse } from '@angular/common/http';
import { ErrorService } from '@app/client/private/services/error.service';
import { concatMap } from 'rxjs/operators';

@Component({
  selector: 'pay-table',
  templateUrl: './pay-table.component.html'
})
export class PayTableComponent implements OnInit {
  @Input()contestId: string;
  @Input() contestData: any;
  @Output()prizesChanged: EventEmitter<IPrize[]> = new EventEmitter<IPrize[]>();

  payTable: IPrize[] = [];
  dataTableColumns: DataTableColumn[] = PAY_TABLE_COLUMNS;
  searchField: string = '';
  isLoading: boolean = false;
  filterProperties: string[] = FILTER_PROPERTIES;

  constructor(private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService.contestManagerService()
    .getAllPrizesByContest(this.contestId)
    .map((response: HttpResponse<IPrize[]>) => response.body)
    .subscribe((payTable: IPrize[]) => {
      this.payTable = payTable;
      this.isLoading = false;
      this.globalLoaderService.hideLoader();
    }, (error) => {
      this.errorService.emitError(
        `${PRIZE_ERROR_LABELS.getPrizeList} ${this.contestId}`
      );
      this.isLoading = false;
      this.payTable = [];
      this.globalLoaderService.hideLoader();
    });
  }

  /**
   * To Add Prize to paytable
   */
  addPrize(): void {
    this.dialogService.showCustomDialog(AddEditPrizeComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: ADD_PRIZE_DIALOG.title,
      data: { defaultOfferIds: { freebetOfferId: this.contestData.freebetOfferId, ticketOfferId: this.contestData.ticketOfferId }} as IPrize,
      yesOption: ADD_PRIZE_DIALOG.yesOption,
      noOption: ADD_PRIZE_DIALOG.noOption,
      yesCallback: (prize: IPrize) => {
        if(prize.type !== PRIZE_TYPES_MAPPER.FREEBET && prize.type !== PRIZE_TYPES_MAPPER.TICKET) {
          prize.freebetOfferId = null;
        }
        prize.contestId = this.contestId;
        this.removeSvgFile(prize);
        this.apiClientService.contestManagerService()
        .addPrizeById(prize)
        .pipe(concatMap((result: HttpResponse<IPrize>) => {
            return this.apiClientService.contestManagerService()
              .uploadPrizeSvgImage(result.body.id, this.getFormData(prize))
              .map((imageResponse: HttpResponse<IPrize>) => {
                return imageResponse.body;
              });
          })
        )
        .subscribe((prizeInfo: IPrize) => {
          this.payTable = [...this.payTable, prizeInfo];
          this.prizesChanged.emit(this.payTable.slice());
        }, (error) => {
          this.errorService.emitError(
            `${PRIZE_ERROR_LABELS.createPrize} ${this.contestId}`
          );
        });
      }
    });
  }

  /**
   * To Edit pize in paytable
   * @param {IPrize} prize
   */
  editPrize(prize: IPrize): void {
    prize.defaultOfferIds = { freebetOfferId: this.contestData.freebetOfferId, ticketOfferId: this.contestData.ticketOfferId }
    this.dialogService.showCustomDialog(AddEditPrizeComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: prize,
      title: EDIT_PRIZE_DIALOG.title,
      yesOption: EDIT_PRIZE_DIALOG.yesOption,
      noOption: EDIT_PRIZE_DIALOG.noOption,
      yesCallback: (updatedPrizeData: IPrize) => {
        this.editPrizeDetails(prize, updatedPrizeData);
      }
    });
  }

  /**
   * To remove prize in paytable
   * @param {IPrize} prize
   */
  removePrize(prize: IPrize): void {
    this.dialogService.showConfirmDialog({
      title: REMOVE_PRIZE_DIALOG.title,
      message: `${REMOVE_PRIZE_DIALOG.message} "${prize.type}"`,
      yesCallback: () => {
        this.apiClientService.contestManagerService()
        .removePrize(prize.id)
        .subscribe(() => {
           this.payTable.splice(this.payTable.indexOf(prize), 1);
           this.prizesChanged.emit(this.payTable.slice());
        }, (error) => {
          this.errorService.emitError(
            `${PRIZE_ERROR_LABELS.removingPrize} ${this.contestId}`
          );
        });
      }
    });
  }


  /**
   * To edit prize details
   * @param {IPrize} prizeData
   * @param {IPrize} updatedPrizeData
   */
  private editPrizeDetails(prizeData: IPrize, updatedPrizeData: IPrize): void {
    this.removeSvgFile(updatedPrizeData);
    
    if(updatedPrizeData.type !== PRIZE_TYPES_MAPPER.FREEBET && updatedPrizeData.type !== PRIZE_TYPES_MAPPER.TICKET) {
      updatedPrizeData.freebetOfferId = null;
    }

    this.apiClientService.contestManagerService()
      .editPrizeById(prizeData.id, updatedPrizeData)
      .pipe(concatMap((result: HttpResponse<IPrize>) => {
        return this.apiClientService.contestManagerService()
          .uploadPrizeSvgImage(result.body.id, this.getFormData(updatedPrizeData))
          .map((imageResponse: HttpResponse<IPrize>) => {
            return imageResponse.body;
          });
      }))
      .subscribe((prizeInfo: IPrize) => {
        this.payTable.splice(this.payTable.indexOf(prizeData), 1, prizeInfo);
        this.prizesChanged.emit(this.payTable.slice());
      }, (error) => {
        this.errorService.emitError(
          `${PRIZE_ERROR_LABELS.editingPrize} ${this.contestId}`
        );
      });
  }

  /**
   * To Remove Svg file when upload file removed
   * @param {IPrize} updatedPrizeData
   * @returns {void}
   */
  private removeSvgFile(updatedPrizeData: IPrize): void {
    if (updatedPrizeData.icon && !updatedPrizeData.icon.originalname) {
      updatedPrizeData.icon = null;
    }
    if (updatedPrizeData.signPosting && !updatedPrizeData.signPosting.originalname) {
      updatedPrizeData.signPosting = null;
    }
  }

  /**
   * To get Form Data for images upload
   * @param {IPrize} prize
   */
  private getFormData(prize: IPrize): FormData {
    const formData = new FormData();
    formData.append(ICON_FILE, prize.prizeIcon);
    formData.append(SIGNPOSTING_FILE, prize.prizeSignposting);
    return formData;
  }

}

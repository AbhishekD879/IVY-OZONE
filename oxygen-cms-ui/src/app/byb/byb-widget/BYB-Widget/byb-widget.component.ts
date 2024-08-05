import { Component, OnInit, ViewChild } from '@angular/core';
import { BybWidget, bybwidgetData } from '@app/byb/byb-widget/BYB-Widget/byb-widget.model';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { DataTableColumn } from '@root/app/client/private/models/dataTableColumn';
import { BYB_HEAD, BYB_VALUES } from './byb-widget.constants';
import { Router } from '@angular/router';
import { ActionButtonsComponent } from '@root/app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { HttpResponse } from '@angular/common/http';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants, TIME_SEPARATOR } from '@app/app.constants';
import { Order } from '@root/app/client/private/models/order.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ISegmentMsg } from '@root/app/client/private/models/segment.model';
import { SegmentStoreService } from '@root/app/client/private/services/segment-store.service';
import { BigCompetitionAPIService } from '@root/app/sports-pages/big-competition/service/big-competition.api.service';

@Component({
  selector: 'app-byb-widget',
  templateUrl: './byb-widget.component.html',
  styleUrls: ['./byb-widget.component.scss']
})
export class BybWidgetComponent implements OnInit {
  bybForm: FormGroup;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  public BYB_HEAD = BYB_HEAD;
  public isAddRowValue: boolean = false;
  public intialData: BybWidget;
  public cmsDatatable: boolean = true;

  isAddTable: boolean = false;
  removebybdata: boolean = true;
  bybData: any = { data: [] };
  marketsData: any = [];
  expiredData: any = [];
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      width: 2,
    },
    {
      name: 'Event ID',
      property: 'eventId',
      width: 2,
    },
    {
      name: 'Market ID',
      property: 'marketId',
      width: 2,
    },
    {
      name: 'From',
      property: 'displayFrom',
      type: 'date',
      width: 1
    },
    {
      name: 'To',
      property: 'displayTo',
      type: 'date',
      width: 1
    },
    {
      name: 'Location',
      property: 'location',
      width: 2
    }
  ];
  isMarketsEdited: boolean;
  segementStatus: any = { active: false };
  dataLoaded: Boolean = false;
  showaddButton: Boolean = false;
  brand: any;
  bybFormData: any = 'BYBForm data';
  callSaveApi: any = 0;
  marketdataCopy: any = [];
  showAllCheck: boolean;
  addRowForsaveAdd: boolean;
  showCmsDataTable: boolean;
  callApiType: any;
  showMaxError: boolean;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  competionList: any = [];
  competionList1: any = [];
  expiredCompetionList: any = [];
  savedSuccessFully: boolean = false;
  showExpiredDataTable: boolean = false;
  checkBox: any = [
    { title: 'Sportsbook Homepage', bybVisble: true, id: 0, routerId: '/sports-pages/homepage' },
    { title: 'Football Landingpage', bybVisble: true, id: 16, routerId: '/sports-pages/sport-categories' },
    { title: 'BYB Homepage(Mobile Only)', bybVisble: false, id: 'BybHomePage', routerId: '/module-ribbon-tabs' }
  ];

  brandType: any;

  constructor(
    private brandService: BrandService,
    public router: Router,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar, private segmentStoreService: SegmentStoreService, private bigCompetitionApiService: BigCompetitionAPIService
  ) {
    this.bybData.data = [];
  }

  ngOnInit(): void {
    this.brand = this.brandService.brand;
    this.getBigcompetionList();
  }

  goToHomepage(router, ind) {
    if (ind == 2) {
      this.router.navigate([router + '/' + this.brandType.id]);
    } else {
      this.router.navigate([router]);
    }
  }

  getBigcompetionList() {
    this.bigCompetitionApiService.getCompetitionsListInByb().map((response) => { return response.body })
      .subscribe((data: any) => {
        this.loadInitialData();
        this.loadingSegmentTableData();
        this.loadmoduletype();
        this.loadModuleRibbon();
        this.competionList = data;
        this.competionList.forEach(val => {
          if (val.enabled) {
            this.competionList1.push({ id: val.id, name: val.name });
          }
        });
        this.competionList1.unshift({ name: 'BYB Homepage(Mobile)', id: 'Byb Homepage' });
        this.competionList1.unshift({ name: 'Football Landingpage', id: 'Football Homepage' });
        this.competionList1.unshift({ name: 'Sportsbook Homepage', id: 'Sportbook Homepage' });
      });
  }

  gotoBigCompetion() {
    this.router.navigate(['/sports-pages/big-competition']);
    let routPath: any = 'sports-pages/big-competition';
    this.router.navigate([`${routPath}`]);
  }

  loadInitialData(): void {
    this.showCmsDataTable = false;
    this.globalLoaderService.showLoader();
    this.apiClientService.bybWidgetService()
      .findAllByBrand(this.brand).map((response: any) => { return response.body })
      .subscribe((resp: any) => {
        if (resp) {
          this.showAllCheck = resp.showAll;
          this.bybData = resp;
          this.intialData = resp;
          const data = resp.displayOn;
          this.checkBox.forEach((item) => {
            if (data.hasOwnProperty(item.id)) {
              item.bybVisble = data[item.id];
            }
          });
          this.addRowForsaveAdd = true;
          if (resp && resp.data) {
            const bybMarketsData = this.formatBYBData(resp.data);
            this.marketdataCopy = bybMarketsData;
            this.marketsData = bybMarketsData;
            this.bybData.data = this.marketsData;
            if (resp && resp?.data?.length > 0) {
              this.isAddRowValue = true;
            }
          }
          this.showCmsDataTable = true;
          this.bybformData();
          this.dataLoaded = true;
          if (this.callSaveApi == 1) {
            this.showaddButton = false;
            if (this.callSaveApi && this.addRowForsaveAdd) {
              this.addRow();
            }
          } else {
            this.showaddButton = true;
          }
        } else {
          this.intialData = BYB_VALUES;
        }
        this.globalLoaderService.hideLoader();
        this.actionButtons?.extendCollection(this.bybForm.value);
      }, error => {
        if (error.status === 404) {
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  getConvertedToDate(date) {
    const dateNow = new Date();
    return new Date(new Date(date).getTime() + (dateNow.getTimezoneOffset() - 60000));
  }

  loadmoduletype() {
    this.segmentStoreService.validateSegmentValue();
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.MODULE_RIBBON_TAB) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
  }

  loadModuleRibbon() {
    this.apiClientService.bybWidgetService()
      .getModuleRibbonBySegment(this.selectedSegment).map((response: any) => { return response.body })
      .subscribe((resp: any) => {
        if (resp) {
          this.brandType = resp[resp.findIndex((val: any) => val.directiveName == "BuildYourBet")];

        }
      })


  }

  loadingSegmentTableData() {
    this.apiClientService.bybWidgetService()
      .getsegmentdata(this.brand, this.segementStatus).map((response: any) => { return response.body })
      .subscribe((data: any) => {
        this.expiredData = this.formatBYBData(data);
        this.expiredData.forEach(val => {
          let data: any = [];
          this.competionList1.forEach(((res: any) => {
            if (val.locations.includes(res.id)) {
              data.push(res.name);
            }
          }));
          if (!val['location']) {
            val['location'] = [];
          }
          val['location'].push(data);
          val['location'] = val['location'].join(',');
          this.showExpiredDataTable = true;
        })
      }, error => {
        if (error.status === 404) {
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  /**
   * Method to format the BYB data
   * @param bybwidgetData - widget
   * @returns - formats and returns the byb widget data
   */
  private formatBYBData(bybwidgetData: bybwidgetData[]): bybwidgetData[] {
    bybwidgetData.forEach((bybWidget: bybwidgetData) => {
      bybWidget.displayFrom1 = new Date(bybWidget.displayFrom).toLocaleString();
      bybWidget.displayTo1 = new Date(bybWidget.displayTo).toLocaleString();
      bybWidget.displayFrom = bybWidget.displayFrom.split(TIME_SEPARATOR).shift();
      bybWidget.fromTime = this.formatDateTime(bybWidget.displayFrom);
      bybWidget.displayTo = bybWidget.displayTo.split(TIME_SEPARATOR).shift();
      bybWidget.toTime = this.formatDateTime(bybWidget.displayTo);
      bybWidget.saved = true;
      bybWidget.showDate = false;
      bybWidget.fromdateChange = false;
      bybWidget.todateChange = false;
    })
    return bybwidgetData;
  }

  /**
   * Method to convert date to HH-MM-SS format
   * @param date - date to be formatted
   * @returns - transformed date
   */
  private formatDateTime(dateTime: Date): string {
    const date = new Date(dateTime);
    return date.getHours() + '-' + date.getMinutes() + '-' + date.getSeconds();
  }

  removeBybRow(data: any): void {
    this.callSaveApi = false;
    if (data.id != null && data.id != '') {
      this.dialogService.showConfirmDialog({
        title: 'Remove Active Card Market',
        message: 'Are You Sure You Want to Remove Byb Active Card Market?',
        yesCallback: () => {
          this.sendRemoveRequest(data.id);
        },
        noCallback: () => {
          this.showCmsDataTable = true;
        }
      });
    } else {
      this.loadInitialData();
      this.loadingSegmentTableData();
    }
  }

  sendRemoveRequest(id) {
    this.apiClientService
      .bybWidgetService()
      .deleteBybMarket(id)
      .map((data) => data.body)
      .subscribe((data) => {
        this.loadInitialData();
        this.loadingSegmentTableData();
        this.showaddButton = true;
        this.snackBar.open('Data Removed Successfully!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION
        });
      });
  }

  bybformData(): void {
    this.bybForm = new FormGroup({
      title: new FormControl(this.intialData?.title || '', [Validators.required, Validators.maxLength(50)]),
      marketCardVisibleSelections: new FormControl(+this.intialData?.marketCardVisibleSelections || null, [Validators.required, Validators.min(2), Validators.max(5)]),
      showAll: new FormControl(this.intialData?.showAll || false, [Validators.required]),
    });

  }

  public isValidForm(intialData): boolean {
    return !!(intialData.title && intialData.title.length <= 50 && intialData.marketCardVisibleSelections >= 2
      && intialData.marketCardVisibleSelections <= 5 && (intialData.showAll || !intialData.showAll))
  }

  onMarketCardSelectionsChange(value: any) {
    const intValue = parseInt(value, 10); // Parse value to integer
    this.bybForm.patchValue({ marketCardVisibleSelections: intValue }); // Update form control value
  }

  addRow() {
    let dataModal: any = {
      'title': '',
      'eventId': '',
      'marketId': '',
      'displayFrom': '',
      'displayTo': '',
      'locations': [],
      'saved': false,
      'showDate': true,
      id: "",
      brand: this.brand,
      todateChange: false,
      fromdateChange: false

    };
    this.marketsData.push(dataModal);
    this.isAddRowValue = true;
  }

  public reorderHandler(order: Order) {
    this.apiClientService.bybWidgetService().reOrder(order)
      .subscribe(() => {
        this.snackBar.open('BYB ORDER SAVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  // For Save and Add Button
  addList(addData: any) {
    this.forDateConvertion = true;
    this.savedSuccessFully = true;
    this.callApiType = addData;
    this.bybData.data = [];
    this.callSaveApi = addData.type;
    if (addData && addData?.data && addData?.data?.length > 0) {
      addData.data.forEach(data => {
        this.bybData.data.push({
          title: data.title,
          eventId: data.eventId,
          marketId: data.marketId,
          displayFrom: data.displayFrom + 'T' + data.fromTime,
          displayTo: data.displayTo + 'T' + data.toTime,
          locations: data.locations,
          "brand": this.brand,
        });
        this.isAddTable = false;
        this.isMarketsEdited = true;
      })
    }
    if (this.callSaveApi == 1) {
      this.saveChanges('Market Switcher Labels is saved!');
    } else {
      this.addRow();
    }
  }

  forDateConvertion: boolean = false;
  addNewBybRow(data): void {
    this.forDateConvertion = true;
    this.savedSuccessFully = false;
    this.callSaveApi = data.type;
    this.callApiType = data;
    this.bybData.data = [];
    if (!this.bybData.data) {
      this.bybData.data = [];
    }
    this.bybData.data.push({
      'title': data.title,
      'eventId': data.eventId,
      'marketId': data.marketId,
      'displayFrom': data.displayFrom + ':40.994Z',
      'displayTo': data.displayTo + ':40.994Z',
      'locations': data.location,
      "brand": this.brand,
      id: data.id
    });
    this.isAddTable = false;
    this.isMarketsEdited = true;
    this.saveChanges('Market Switcher Labels is saved!');
  }

  public saveChanges(message?): void {
    this.submitChanges(message);
  }

  public submitChanges(message?): void {
    let seconds: any = new Date().getSeconds() < 10 ? '0' + new Date().getSeconds().toString() : new Date().getSeconds().toString();
    this.globalLoaderService.showLoader();
    let apiCall: any
    let objData: any;
    this.callApiType.data.forEach(data => {
      objData = {
        'title': data.title,
        'eventId': data.eventId,
        'marketId': data.marketId,
        'displayFrom': this.getConvertedDate(new Date(`${data.displayFrom}:${data.fromdateChange ? data.fromSeconds : seconds}.994Z`)),
        'displayTo': this.getConvertedDate(new Date(`${data.displayTo}:${data.todateChange ? data.toSeconds : seconds}.994Z`)),
        'locations': data.locations,
        "brand": this.brand,
        "id": data.id,
        sortOrder: data.sortOrder
      }
    })
    if (this.callApiType.data[0].id && this.callApiType.data[0].id != null) {
      apiCall = this.apiClientService.bybWidgetService().updateValues(objData)
    } else {
      apiCall = this.apiClientService.bybWidgetService().postNewOrder(objData);
    }
    apiCall.map((data: HttpResponse<BybWidget>) => data.body)
      .subscribe((bybData: BybWidget) => {
        this.globalLoaderService.hideLoader();
        this.isMarketsEdited = false;
        this.loadInitialData();
        this.loadingSegmentTableData();
        this.snackBar.open('Data Saved Successfully!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.showaddButton = false;
      }, (err => {
        this.showCmsDataTable = false;
        this.marketsData = this.marketdataCopy;
        this.marketsData = this.marketsData.filter(val => val.id != '');
        this.showaddButton = true;
        this.snackBar.open('Invalid Market Data Failed!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION,
        });
        setTimeout(() => {
          this.showCmsDataTable = true;
          this.globalLoaderService.hideLoader();
        }, 500);

      }));
  }

  getConvertedDate(date) {
    const dateNow = new Date();
    return new Date(new Date(date).getTime() + (dateNow.getTimezoneOffset() * 60000));
  }

  // For Byb data Fields
  public saveChangesData() {
    this.globalLoaderService.showLoader();
    let payloaddata: any;
    let bybapiCall: any
    let dataa: any = {
      "brand": this.brand,
      "title": this.bybForm.get('title').value,
      "marketCardVisibleSelections": +(this.bybForm.get('marketCardVisibleSelections').value),
      "showAll": this.bybForm.get('showAll').value,
      id: this.bybData.id,
    }
    payloaddata = dataa;

    if (payloaddata.id && payloaddata.id != null) {
      bybapiCall = this.apiClientService.bybWidgetService().updateWidgetData(payloaddata)
    } else {
      bybapiCall = this.apiClientService.bybWidgetService().postNew(payloaddata);
    }

    bybapiCall.map((data: HttpResponse<BybWidget>) => data.body)
    .subscribe((bybData: any) => {
      this.globalLoaderService.hideLoader();
      this.snackBar.open('Data Saved Successfully!!', 'OK!', {
        duration: AppConstants.HIDE_DURATION,
      });
      this.actionButtons?.extendCollection(this.bybForm.value);
    }, (err => {
      this.globalLoaderService.hideLoader();
      this.snackBar.open('Data Failed!!', 'OK!', {
        duration: AppConstants.HIDE_DURATION,
      });
  
    }));
  }

  /**
  * To Handle actions
  * @param {string} event
  */

  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.saveChangesData();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        break;
    }
  }

  revertChanges(): void {
    this.loadInitialData();
  }

  removeExpiredData(data: any) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Expired Card Market',
      message: 'Are You Sure You Want to Remove Byb Expired Card Market?',
      yesCallback: () => {
        this.sendExpiredCardRemoveRequest(data.id);
      }
    });

  }

  updateTableValues(data) {
    this.bybData.data = {
      'title': data.title,
      'eventId': data.eventId,
      'marketId': data.marketId,
      'displayFrom': data.displayFrom,
      'displayTo': data.displayTo,
      'locations': data.locations,
      "brand": this.brand,
      "id": data.id
    };

    this.apiClientService.bybWidgetService().updateValues(this.bybData.data).subscribe((value: any) => {
    })

  }


  marketVisibleSelection(eve: any) {
    if (Number(eve.target.value) > 5) {
      this.showMaxError = true;
    } else {
      this.showMaxError = false;
    }
  }

  sendExpiredCardRemoveRequest(id) {
    this.apiClientService
      .bybWidgetService()
      .deleteBybMarket(id)
      .map((data) => data.body)
      .subscribe((data) => {
        this.loadingSegmentTableData();
        this.snackBar.open('Data Removed Successfully!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION
        });
      });
  }

}

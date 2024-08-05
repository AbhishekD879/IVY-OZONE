import { Component, OnInit, ViewChild } from '@angular/core';
import { BrandService } from '../../client/private/services/brand.service';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpResponse } from '@angular/common/http';
import { AppConstants } from '../../app.constants';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { TinymceComponent } from '../../shared/tinymce/tinymce.component';
import { DialogService } from '../../shared/dialog/dialog.service';
import * as _ from 'lodash';
import { popularAccasMock } from './popular-accas-widget.mock';
import { PopularAccasCard, PopularAccasWidget } from './popular-accas-widget.model';
import { DataTableColumn } from '../../client/private/models/dataTableColumn';
import { ErrorService } from '../../client/private/services/error.service';
import { Router } from '@angular/router';
import { ActionButtonsComponent } from '../../shared/action-buttons/action-buttons.component';

@Component({
  selector: 'app-popular-accas-widget',
  templateUrl: './popular-accas-widget.component.html',
  styleUrls: ['./popular-accas-widget.component.scss']
})
export class PopularAccasWidgetComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('informationTextEditor') informationTextEditor: TinymceComponent;
  popularAccasWidgetForm: FormGroup;
  popularAccasWidgetData: PopularAccasWidget;
  isLoading: boolean = true;
  widgetAvailablePagesLst: any = [
    { title: 'Sportsbook Homepage', popularAccaWidgetVisble: true, id: 0, routerId: '/sports-pages/homepage' },
    { title: 'Football Landingpage', popularAccaWidgetVisble: true, id: 16, routerId: '/sports-pages/sport-categories' }
  ];
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
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
      name: 'Locations',
      property: 'locations',
      width: 2
    }
  ];
  activeModules: PopularAccasCard[];
  expiredModules: PopularAccasCard[];

  constructor(
    public router: Router,
    private brandService: BrandService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private dialogService: DialogService,
    private errorService: ErrorService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    Object.assign(popularAccasMock, {
      brand: this.brandService.brand,
    })
    this.popularAccasWidgetData = JSON.parse(JSON.stringify(popularAccasMock));
    this.loadInitialData();
    this.loadingSegmentTableData();
  }

  /*
  *popularAccasWidgetForm controls
  */
  get formControls() {
    return this.popularAccasWidgetForm?.controls;
  }

  /**
   * it loads the initial data
   * loadInitialData()
   */
  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.
      popularAccasWidgetService()
      .getPopularAccasWidgetData().subscribe((data: { body: any }) => {
        this.popularAccasWidgetData = data.body;
        if (!data.body.brand && !data.body.id) {
          this.popularAccasWidgetData = JSON.parse(JSON.stringify(popularAccasMock));
        } else {
          this.activeModules = this.popularAccasWidgetData.data;
        }
        this.widgetAvailablePagesLst.forEach((item) => {
          if(item.id === 16 && data.body.categoryIds && data.body.categoryIds[item.id]) {
            item.routerId = `${item.routerId}/${data.body.categoryIds[item.id]}`;
          }
          item.popularAccaWidgetVisble = this.popularAccasWidgetData.displayOn[item.id];
        });
        this.createPopularAccaWidgetFormGroup();
        this.isLoading = false;
        this.actionButtons?.extendCollection(this.popularAccasWidgetForm.value);
        this.globalLoaderService.hideLoader();

      },
        error => {
          this.isLoading = false;
          this.globalLoaderService.hideLoader();
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        });
  }

  /**
   * create form data
   */
  createPopularAccaWidgetFormGroup(): void {
    this.popularAccasWidgetForm = new FormGroup({
      displayOn: new FormControl(this.popularAccasWidgetData.displayOn || ''),
      title: new FormControl(this.popularAccasWidgetData.title || '', [Validators.required, Validators.maxLength(50)]),
      cardCta: new FormControl(this.popularAccasWidgetData.cardCta || '', [Validators.required, Validators.maxLength(20)]),
      cardCtaAfterAdd: new FormControl(this.popularAccasWidgetData.cardCtaAfterAdd || '', [Validators.required, Validators.maxLength(20)])
    });
  }

  /**
   * 
   * @param message save changes
   */
  public saveChanges(message?): void {
    if (this.popularAccasWidgetData?.id) {
      this.submitChanges('putPopularAccasWidgetData', message);
    } else {
      this.submitChanges('postPopularAccasWidgetData', message);
    }
  }

  /**
   * submit changes
   * @param reQuestType
   * @param message 
   */
  public submitChanges(reQuestType, message?): void {
    Object.assign(this.popularAccasWidgetForm.value, {
      brand: this.brandService.brand,
      id : this.popularAccasWidgetData.id
    })
    this.apiClientService.
      popularAccasWidgetService()[reQuestType](this.popularAccasWidgetForm.value)
      .map((data: HttpResponse<any>) => data.body)
      .subscribe((bsData: PopularAccasWidget) => {
        this.popularAccasWidgetData = bsData;
        this.actionButtons?.extendCollection(this.popularAccasWidgetForm.value);
        this.snackBar.open(message ? message : `Popular accas widget saved!`, "Ok!", {
          duration: AppConstants.HIDE_DURATION,
        });
      }, () => {
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

  /**
   * action handlers on save button 
   * @param event 
   */
  public actionsHandler(event): void {
    switch (event) {
      case "save":
        this.saveChanges();
        break;
      case "revert":
        this.revertChanges();
        break;
      default:
        console.error("Unhandled Action");
        break;
    }
  }

  /**
   * revrting the changes to onload 
   */
  public revertChanges(): void {
    this.loadInitialData();
    this.loadingSegmentTableData();
  }



  /**
   *popularAccasWidgetForm validation
   */
  public validationHandler(): boolean {
    return this.popularAccasWidgetForm && this.popularAccasWidgetForm.valid;
  }

  /**
   * expired cards data formation
   */
  loadingSegmentTableData() :void {
    this.apiClientService.popularAccasWidgetService()
      .getsegmentdata({ active: false }).map((response: any) => { return response.body })
      .subscribe((data: any) => {
        this.expiredModules = data;
      }, error => {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        }
      );
  }

  /**
   * form controls for popular acca widget
   */
  get popularAccasWidgetFormControls() {
    return this.popularAccasWidgetForm?.controls;
  }

  /**
   * updates the list order to backend once the order id's array is emitted here.
   * @param list 
   */
  reorderHandler(list): void {
    this.apiClientService
      .popularAccasWidgetService()
      .reorderPopularAccasWidgetcardData(list)
      .subscribe(() => {
        this.snackBar.open(`Popular Acca Widget Cards order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  /**
   * naviagition to spcific sports page/ home page on hyperlink navigation
   * @param router 
   */
  goToHomepage(router): void {
    this.router.navigate([router]);
  }

  /**
   * remove card data
   * @param bet 
   */
  public removeHandler(bet: PopularAccasCard): void {
    this.dialogService.showConfirmDialog({
      title: 'Popular Acca Card',
      message: 'Are You Sure You Want to Remove Popular Acca Card?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.popularAccasWidgetService()
          .deletePopularAccasWidgetCardData(bet.id)
          .subscribe(() => {
            _.remove(this.popularAccasWidgetData.data, { id: bet.id });
            _.remove(this.activeModules, { id: bet.id });
            _.remove(this.expiredModules, { id: bet.id });
            this.snackBar.open(`Popular accas widget card removed!`, "Ok!", {
              duration: AppConstants.HIDE_DURATION,
            });
            this.globalLoaderService.hideLoader();
          }, error => {
            this.errorService.emitError(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }
}

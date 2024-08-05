import { initVariants } from '@app/shared/formElements/customer-variants-select/customer-variants.enum';
import { Component, OnInit } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ModuleRibbonTab } from '@app/client/private/models/moduleribbontab.model';
import { CreateModuleRibbonTabComponent } from '../create-module-ribbon-tab/create-module-ribbon-tab.component';
import { Router } from '@angular/router';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { ISegmentMsg } from '@root/app/client/private/models/segment.model';

@Component({
  selector: 'app-module-ribbon-list',
  templateUrl: './module-ribbon-list.component.html',
  styleUrls: ['./module-ribbon-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class ModuleRibbonListComponent implements OnInit {

  public isLoading: boolean = false;
  public searchField: string = '';
  public segmentChanged: boolean = true;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public moduleRibbonTabs: ModuleRibbonTab[] = [];
  public orderMessage: string;
  dataTableColumns: any[] = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    }, {
      'name': 'Segment(s)',
      'property': 'inclusionList',
      'type': 'array'
    }, {
      'name': 'Segment(s) Exclusion',
      'property': 'exclusionList',
      'type': 'array'
    },
    {
      name: 'Directive Name',
      property: 'directiveName'
    },
    {
      name: 'Visible',
      property: 'visible',
      type: 'boolean'
    },
    {
      name: 'Show Tab On',
      property: 'showTabOn'
    }
  ];

  filterProperties: string[] = [
    'title'
  ];
  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
    public snackBar: MatSnackBar,
    private segmentStoreService: SegmentStoreService
  ) {
  }

  ngOnInit(): void {
    this.segmentStoreService.validateSegmentValue();

    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.MODULE_RIBBON_TAB) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
    this.showHideSpinner();

    this.apiClientService.moduleRibbonTab().getModuleRibbonBySegment(this.selectedSegment)
      .map((moduleRibbonResponse: HttpResponse<ModuleRibbonTab[]>) => {
        return moduleRibbonResponse.body.map((tab: ModuleRibbonTab) => {
          tab.showTabOn = initVariants[tab.showTabOn];
          return tab;
        });
      })
      .subscribe((moduleRibbonList: ModuleRibbonTab[]) => {
        this.moduleRibbonTabs = moduleRibbonList;
        this.orderMessage = this.moduleRibbonTabs.length ? this.moduleRibbonTabs[0].message : '';
        this.showHideSpinner(false);
      }, () => {
        this.showHideSpinner(false);
      });
  }

  public get visibleItems(): number {
    return this.moduleRibbonTabs.filter(m => m.visible).length;
  }

  public reorderHandler(newOrder: Order) {
    this.apiClientService.moduleRibbonTab().setOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('MODULE RIBBON ORDER SAVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  public removeModuleRibbonTab(moduleRibbonTab: ModuleRibbonTab): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Module Ribbon Tab',
      message: 'Are You Sure You Want to Remove Module Ribbon Tab?',
      yesCallback: () => {
        this.moduleRibbonTabs = this.moduleRibbonTabs.filter((l) => {
          return l.id !== moduleRibbonTab.id;
        });
        this.apiClientService.moduleRibbonTab().remove(moduleRibbonTab.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Module Ribbon Tab is Removed.'
          });
        });
      }
    });
  }

  public createModuleRibbonTab(): void {
    this.dialogService.showCustomDialog(CreateModuleRibbonTabComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Static Block',
      yesOption: 'Save',
      noOption: 'Cancel',
      data: {
        currentTabs: this.moduleRibbonTabs
      },
      yesCallback: (moduleRibbonTab: ModuleRibbonTab) => {
        this.apiClientService.moduleRibbonTab()
          .add(moduleRibbonTab)
          .map((res: HttpResponse<ModuleRibbonTab>) => res.body)
          .subscribe((ribbonTab: ModuleRibbonTab) => {
            this.moduleRibbonTabs.unshift(ribbonTab);
            this.router.navigate([`/module-ribbon-tabs/${ribbonTab.id}`]);
          }, () => {
            console.error('Can not create Module Ribbon Tab');
          });
      }
    });
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * get moduleRibbonTabs list based on segment selection
   * @param segment value
   */
   segmentHandler(segment: string): void {
    this.segmentChanged = false;
    this.globalLoaderService.showLoader();
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.MODULE_RIBBON_TAB, segmentValue: segment });
    this.apiClientService.moduleRibbonTab().getModuleRibbonBySegment(segment).subscribe((data: HttpResponse<ModuleRibbonTab[]>) => {
      this.segmentChanged = true;
      this.selectedSegment = segment;
      this.moduleRibbonTabs = data.body;
      this.orderMessage = this.moduleRibbonTabs.length ? this.moduleRibbonTabs[0].message : '';
      this.globalLoaderService.hideLoader();
    });
  }
}

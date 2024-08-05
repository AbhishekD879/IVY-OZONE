import { Component, OnChanges, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http/index';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { HttpResponse } from '@angular/common/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { NavigationParentGroup, PromotionsNavigationGroup } from '@app/client/private/models/promotions-navigation.model';
import { SortableTableService } from '@app/client/private/services/sortable.table.service';
import * as _ from 'lodash';
import { Order } from '@app/client/private/models/order.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation-edit.component.html',
  styleUrls: ['./navigation-edit.component.scss'],
  providers: [SortableTableService]
})

export class NavigationEditComponent implements OnInit, OnChanges {

  public breadcrumbsData: Breadcrumb[];
  public isLoading: boolean = false;
  editRowIndex: number;
  isDisabledBtn: boolean = false;
  tableUniqueClass: string = _.uniqueId('reorder_');
  public navigationGroups:PromotionsNavigationGroup;
  public navParentGrp: PromotionsNavigationGroup = {
    id : '',
    status : false, 
  };
  id: string;
  navdisplayType: string;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router,
    private snackBar: MatSnackBar,
    protected sortableTableService: SortableTableService
  ) {
    this.isValidForm = this.isValidForm.bind(this);
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.id = params['id'];
    })
    this.loadInitData(this.id);
  }

  /**
 * Revert the Navigation Content
 * @returns null
 */
  revertChanges(): void {
    this.loadInitData(this.id, false);
  }

  /**
   * Removes Navigation Group
   * @param {navigationGroup} PromotionsNavigationGroup
   * @returns null
   */
  removeNavigationGroups(): void {
    this.apiClientService.promotionsNavigationsService().remove(this.navigationGroups.id,
      this.navigationGroups.promotionIds.length > 0 ? this.navigationGroups.promotionIds : `""`).subscribe(() => {
        this.router.navigate(['/promotions/navigations']);
      });

  }

  /**
  * Nav group form validation
  * @param {navigationGroups}
  * @returns null
  */
  isValidForm(navigationGroups: NavigationParentGroup): boolean {
    return !!(navigationGroups.title) && this.navigationGroups.navItems.length > 0;
  }

  /**
   * Action handler for the action button
   * @param {event}
   * @returns null
   */
  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveNavigationGroup();
        break;
      case 'remove':
        this.removeNavigationGroups();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * Loads Initial Nav group data
   * @param {isLoading}
   * @returns void
   */
  private loadInitData(id, isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.apiClientService.promotionsNavigationsService().getNavListById(id)
      .map((navigationGroups) => {
        return navigationGroups.body;
      }).subscribe((data: PromotionsNavigationGroup) => {
        this.navigationGroups = data;
        Object.assign(this.navParentGrp || {}, {
          id: data.id,
          title: data.title,
          status: data.status,
          updatedAt: data.updatedAt,
        })
        this.globalLoaderService.hideLoader();
        this.addReorderingToTable();
        this.isLoading = false;
        this.breadcrumbsData = [{
          label: `Promotions Navigation`,
          url: `/promotions/navigations`
        }, {
          label: this.navigationGroups.title,
          url: `/promotions/navigation/${this.navigationGroups.id}`
        }];
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });

  }

  setNavItemStatus(value) {
    return typeof(value) == 'boolean';
  }

  /**
   * Add new line item to Navigation childs
   * @param null
   * @returns void
   */

  addNavItem() {
    if (this.navigationGroups?.navItems.length >= 9) {
      this.dialogService.showNotificationDialog({
        title: `Promotions Navigation`,
        message: `Maximum number of Nav Items that can be added is 9`
      })
    } else {
      this.router.navigateByUrl(`/promotions/navigationCreate/${this.id}`);
    }
  }

  /**
  * delete Nav Items
  * @param {i} index
  * 
  */
  removeNavItems(i) {
    if (this.navigationGroups?.navItems[i].id) {
      if(this.navigationGroups?.navItems?.length == 1){
        this.dialogService.showNotificationDialog({
          title: `Remove Nav Items`,
          message: `Minimum 1 Nav Item is required`
        })
      } else {
      this.dialogService.showConfirmDialog({
        title: 'Remove Nav Items',
        message: 'Are You Sure You Want to Remove the Nav Items?',
        yesCallback: () => {
          this.apiClientService.promotionsNavigationsService().removeNavContent(
            this.navigationGroups?.navItems[i].id
          ).subscribe(data => {
            this.isDisabledBtn = false;
            this.navigationGroups?.navItems.splice(i, 1);
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'NavItem is Removed.'
            });
          })
        }
      })
    }
    } else {
      this.navigationGroups?.navItems.splice(i, 1);
      this.isDisabledBtn = false;
    }
    i == this.editRowIndex || this.editRowIndex != this.navigationGroups?.navItems.length - 1 ?
      this.editRowIndex = -1 : this.editRowIndex = this.editRowIndex - 1;
  }

  /**
 * Add drag-n-drop reorder functionality to table
 * 
 */
  addReorderingToTable() {
    const self = this;
    this.sortableTableService.addSorting({
      dataToReorder: self.navigationGroups?.navItems,
      mainSelector: `.custom-table.${self.tableUniqueClass} tbody`,
      handlerSelector: '.drag-handler',
      onReorderEnd(data, indexOfDraggedElement) {
        const newOrder = {
          order: self.navigationGroups?.navItems.map(element => element.id),
          id: self.navigationGroups?.navItems[indexOfDraggedElement].id
        };
        self.reorderHandler(newOrder);
      }
    });
  }

  /**
  * Navigate to the Navigation Edit page
  */
  navigateToEdit(navItems) {
    this.router.navigate([`/promotions/navigationEdit/${this.id}/${navItems.id}`]);
  }


  /**
   * Reorder navitems
   * @param {newOrder} Order
   */
  reorderHandler(newOrder: Order) {
    this.apiClientService
      .promotionsNavigationsService()
      .postNewNavItemOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('New Promotions Navigations Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  ngOnChanges() {
    this.addReorderingToTable();
  }

  /**
  * Save Nav Parent group
  * @return {navParentGrp}
  * 
  */
  saveNavigationGroup() {
    this.globalLoaderService.showLoader();
    this.apiClientService.promotionsNavigationsService().
      updateNavGroup(this.navParentGrp)
      .map((navigationGroups: HttpResponse<PromotionsNavigationGroup>) => {
        return navigationGroups.body;
      }).subscribe((data :PromotionsNavigationGroup) => {
        this.globalLoaderService.hideLoader();
        this.navParentGrp = data;
        this.navigationGroups
        this.actionButtons.extendCollection(this.navParentGrp);
        this.dialogService.showNotificationDialog({
          title: `Promotions Navigation`,
          message: `Promotions Navigation Group is Saved.`
        });
      })
  }

  /**
  * display Type of Nav Type
  * @return {navdisplayType}
  * 
  */
  displayType(navType) {
    switch (navType?.toLowerCase()) {
      case 'leaderboard':
        this.navdisplayType = 'Leaderboard'
        break;
      case 'description':
        this.navdisplayType = 'Description'
        break;
      default:
        this.navdisplayType = 'URL'
    }
    return this.navdisplayType;
  }

  onNavItemListChanged(data) {
    this.navigationGroups.navItems = data.slice();
  }
}

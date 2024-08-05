import {Component, OnInit, ViewChild} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import * as _ from 'lodash';

import {DialogService} from '../../../shared/dialog/dialog.service';

import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {ApiClientService} from '../../../client/private/services/http';
import {BrandService} from '../../../client/private/services/brand.service';
import {MenuAddComponent} from '../menu-add/menu-add.component';

import {MenuItem} from '../../../client/private/models';
import {ActivatedRoute, Router} from '@angular/router';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {ComponentCanDeactivate} from '../../../client/private/interfaces/pending-changes.guard';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';


@Component({
  templateUrl: './menu-item-manage.component.html'
})
export class MenuItemManageComponent implements OnInit, ComponentCanDeactivate {
  menuSubTree: any;
  menuItemEditable: any = {};
  rootMenus: Array<any> = [];
  rootMenusId: string;
  searchField: '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Name',
      property: 'label',
      link: {
        hrefProperty: 'id',
        sibling: false
      },
      type: 'link'
    },
    {
      name: 'Display order',
      property: 'displayOrder'
    },
    {
      name: 'Active',
      property: 'active',
      type: 'boolean'
    }
  ];
  filterProperties: Array<string> = [
    'label'
  ];
  CONFIGURATION_BASE_URL = '/menu-configuration';

  public breadcrumbsData: Breadcrumb[] = [];
  public form: FormGroup;
  @ViewChild('actionButtons')
  public actionButtons;

  constructor(
    private dialogService: DialogService,
    private dialog: MatDialog,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private brandService: BrandService,
    private apiClientService: ApiClientService) {
  }

  ngOnInit() {
    this.activatedRoute.params.subscribe(
      params => {
        this.initComponentData(params.menuItemId);
      });
  }

  public initComponentData(nodeId: string) {
    this.apiClientService.menues().getMenu()
      .subscribe((data: any) => {
        this.rootMenus = data.body.menu;
        this.rootMenusId = data.body.id;
        this.menuSubTree = this.wrapRootMenuInTree(this.rootMenus);

        if (nodeId) {
          const subTreeAndPath = this.getSubTree(String(nodeId), this.menuSubTree);
          this.menuSubTree = subTreeAndPath.result;
          this.menuSubTree.pathToSubTree = JSON.parse('[' + subTreeAndPath.path + ']');
          this.dataTableColumns[0].link.sibling = true;
          this.updateBreadcrumb();
          this.copyPrimitives(this.menuSubTree, this.menuItemEditable);
          this.initForm();
          if (this.actionButtons) {
            this.actionButtons.ngOnInit();
          }
        }
      });
  }

  public initForm() {
    this.form = new FormGroup({
      label: new FormControl(this.menuItemEditable.label, [Validators.required]),
      path: new FormControl(this.menuItemEditable.path, [Validators.required]),
      displayOrder: new FormControl(this.menuItemEditable.displayOrder, []),
      icon: new FormControl(this.menuItemEditable.icon, []),
      active: new FormControl(this.menuItemEditable.active, [Validators.required]),
    });
  }

  private copyPrimitives(src: MenuItem, dest: MenuItem): any {
    dest.label = src.label;
    dest.path = src.path;
    dest.displayOrder = src.displayOrder;
    dest.icon = src.icon;
    dest.active = src.active;
    dest.id = src.id;
  }

  public updateBreadcrumb() {
    this.breadcrumbsData = [{label: 'Menu Configuration', url: this.CONFIGURATION_BASE_URL}];
    this.menuSubTree.pathToSubTree.forEach(item => {
      this.breadcrumbsData.push({label: item.label, url: this.CONFIGURATION_BASE_URL + '/' + item.id});
    });
  }

  public canDeactivate() {
    const equal = _.isEqual(this.menuItemEditable.id, this.menuSubTree.id) &&
      _.isEqual(this.menuItemEditable.path, this.menuSubTree.path) &&
      _.isEqual(this.menuItemEditable.label, this.menuSubTree.label) &&
      _.isEqual(this.menuItemEditable.active, this.menuSubTree.active) &&
      this.equalOrEmptyAndNull(this.menuItemEditable.displayOrder, this.menuSubTree.displayOrder) &&
      this.equalOrEmptyAndNull(this.menuItemEditable.icon, this.menuSubTree.icon);
    return equal;
  }

  private equalOrEmptyAndNull(value1, value2) {
    return _.isEqual(value1, value2) || ((value1 === '' && value2 === null) || (value2 === '' && value1 === null));
  }

  public isValidForm(item) {
    // label and path not empty
    return item.label && item.path;
  }

  public revertChanges() {
    this.copyPrimitives(this.menuSubTree, this.menuItemEditable);
  }

  public saveChanges() {
    // copy values from variables to edit to actual structure
    this.copyPrimitives(this.menuItemEditable, this.menuSubTree);

    this.sendUpdateMenuStructureRequest((menuStructureReturned) => {
      if (menuStructureReturned) {
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Menu Item is Updated'
        });
      }
    },  (error) => {
      this.dialogService.showNotificationDialog({
        title: 'Error occurred while updating menu item',
        message: 'Refresh the page to see actual state'
      });
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeThisMenuItem();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private wrapRootMenuInTree(menu): any {
    return {id: 'root', label: 'root', 'sub-menus': menu};
  }

  private getSubTree(id, tree, path = '') {
    let result;
    if (tree.id === id) {
      result = tree;
    } else {
      for (const child of tree['sub-menus']) {
        // updating nested path here
        const newPath = path + (path === '' ? '' : ',') + JSON.stringify({id: child.id, label: child.label});
        const rv = this.getSubTree(id, child, newPath);
        if (rv.result != null) {
          return rv;
        }
      }
    }
    return {result, path};
  }

  private generateUuid(): string {
    function S4(): string {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }

    return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4());
  }

  /**
   * Opens modal dialog for new menu item creation.
   */
  public createMenuItem(): void {
    const dialogRef = this.dialog
      .open(MenuAddComponent, {width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH});

    dialogRef.afterClosed().subscribe((menuItem: MenuItem) => {
      if (menuItem) {
        menuItem.label = _.trim(menuItem.label);
        menuItem.path = _.trim(menuItem.path);
        menuItem.icon = _.trim(menuItem.icon);
        menuItem.id = this.generateUuid();

        this.menuSubTree['sub-menus'].push(menuItem);
        this.sendUpdateMenuStructureRequest((menuStructureReturned) => {
          if (menuStructureReturned) {
            this.dialogService.showNotificationDialog({
              title: 'Save Completed',
              message: 'Menu Item is Created and Stored'
            });
          }
        }, (error) => {
          this.menuSubTree['sub-menus'].pop();
          this.dialogService.showNotificationDialog({
            title: 'Error occurred while adding submenu',
            message: 'Refresh the page to see actual state'
          });
        });
      }
    });
  }

  public removeThisMenuItem(): void {
    const pathToSubTree = this.menuSubTree.pathToSubTree;
    let menuToRemoveFrom;
    let pathToRedirect;
    if (pathToSubTree.length < 2) {
      pathToRedirect = '/menu-configuration';
      menuToRemoveFrom = this.rootMenus;
    } else {
      pathToRedirect = '/menu-configuration/' + pathToSubTree[pathToSubTree.length - 2].id;
      menuToRemoveFrom = this.getSubTree(pathToSubTree[pathToSubTree.length - 2].id, this.wrapRootMenuInTree(this.rootMenus))
        .result['sub-menus'];
    }
    const removedItems: Array<MenuItem> = _.remove(menuToRemoveFrom, (item: MenuItem) => item.id === this.menuSubTree.id);

    this.sendUpdateMenuStructureRequest( (menuStructureReturned) => {
      if (menuStructureReturned) {
        this.router.navigate([pathToRedirect]);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Menu Item is Removed from Parent'
        });
      }
    },  (error) => {
      menuToRemoveFrom.push(...removedItems);
      this.dialogService.showNotificationDialog({
        title: 'Error occurred while removing menu item',
        message: 'Refresh the page to see actual state'
      });
    });
  }

  public sendUpdateMenuStructureRequest(successFunc, errorFunc) {
    this.apiClientService.menues().updateMenu({brand: this.brandService.brand, menu: this.rootMenus}, this.rootMenusId)
      .map((menuStructureResponse: HttpResponse<any>) => {
        return menuStructureResponse.body;
      })
      .subscribe((menuStructureReturned: any) => {
        successFunc(menuStructureReturned);
      }, error => {
        errorFunc(error);
      });
  }
}

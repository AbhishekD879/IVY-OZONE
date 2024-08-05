import {Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import { MatDialog } from '@angular/material/dialog';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ITreeOptions, TreeComponent} from 'angular-tree-component';
import {AppConstants} from '@app/app.constants';
import {AddStreamAndBetNodeComponent} from '../add-stream-and-bet-node/add-stream-and-bet-node.component';
import {EditStreamAndBetNodeComponent} from '../edit-stream-and-bet-node/edit-stream-and-bet-node.component';
import {StreamAndBetAPIService} from '../service/streamAndBet.api.service';
import {SABChildElement} from '@app/client/private/models/SABChildElement.model';

@Component({
  selector: 'stream-and-bet-category-table',
  templateUrl: './stream-and-bet-category.component.html',
  styleUrls: ['./stream-and-bet-category.component.scss'],
  providers: [
    DialogService
  ]
})
export class StreamAndBetCategoryComponent implements OnInit {
  @Output() applyCategoryChanges = new EventEmitter();
  @Output() callRemoveCategory = new EventEmitter();
  @Input() category: SABChildElement;
  @Input() isNewCategory: boolean;

  // backup children to revert group state after any changes
  categoryBackupItems: Array<SABChildElement>;

  // flag after some changes was made in category. enables save and revert button
  isDataChanged: boolean;
  isLoading: boolean;

  @ViewChild('tree') public tree: TreeComponent;

  options: ITreeOptions = {
    idField: 'siteServeId',
    displayField: 'name',
    childrenField: 'children'
  };

  constructor(private dialogService: DialogService,
              private dialog: MatDialog,
              private globalLoaderService: GlobalLoaderService,
              private streamAndBetAPIService: StreamAndBetAPIService) {
  }

  categoryArray: Array<SABChildElement>;
  availableDataMap: Map<number, Array<SABChildElement>>;
  focusNode: SABChildElement;

  ngOnInit() {
    this.availableDataMap = new Map();
    this.categoryBackupItems = JSON.parse(JSON.stringify(this.category.children));
    this.categoryArray = new Array(this.category);
    if (this.isNewCategory) {
      this.isDataChanged = true;
      this.loadAvailableDataMap(this.category.siteServeId, this.stub);
    }
  }

  stub() {
  }

  addChildNode(parentNode: SABChildElement) {
    this.focusNode = parentNode;
    this.loadAvailableDataMap(this.category.siteServeId, this.addChildNodeCallback.bind(this));
  }

  private updateSuggestionsList(parentNode: SABChildElement) {
    const valuesToRemove = [];
    const possibleValues = this.availableDataMap[parentNode.siteServeId] || [];
    for (let i = 0, len_i = possibleValues.length; i < len_i; i++) {
      for (let j = 0, len_j = parentNode.children.length; j < len_j; j++) {
        if (possibleValues[i].id === parentNode.children[j].siteServeId) {
          valuesToRemove.push(i);
        }
      }
    }
    valuesToRemove.sort(function (a, b) {
      return b - a;
    });
    for (let i = 0, len = valuesToRemove.length; i < len; i++) {
      this.availableDataMap[parentNode.siteServeId].splice(valuesToRemove[i], 1);
    }
  }

  private addChildNodeCallback() {
    const parentNode = this.focusNode;
    this.updateSuggestionsList(this.focusNode);
    const possibleValues = this.availableDataMap[parentNode.siteServeId];

    const dialogRef = this.dialog.open(AddStreamAndBetNodeComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        title: 'Add New StreamAndBetNode',
        yesOption: 'Save',
        noOption: 'Cancel',
        possibleValues: possibleValues
      }
    });
    dialogRef.afterClosed().subscribe(childNode => {
      if (childNode) {
        childNode.selection = this.getChildSelection(parentNode.selection);
        childNode.parentId = parentNode.siteServeId;
        if (!parentNode.children) {
          parentNode.children = [];
        }
        parentNode.children.push(childNode);
        this.tree.treeModel.update();
        this.isDataChanged = true;
      }
    });
  }

  getChildSelection(parentSelection: string) {
    switch (parentSelection) {
      case 'category' :
        return 'class';
      case 'class' :
        return 'type';
      case 'type' :
        return 'event';
    }
  }

  editNode(node: SABChildElement) {
    this.focusNode = node;
    this.loadAvailableDataMap(this.category.siteServeId, this.editChildNodeCallback.bind(this));
  }

  private editChildNodeCallback() {
    const dialogRef = this.dialog.open(EditStreamAndBetNodeComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        title: 'Edit StreamAndBetNode',
        yesOption: 'Save',
        noOption: 'Cancel',
        node: this.focusNode
      }
    });
    dialogRef.afterClosed().subscribe(updatedNode => {
      if (updatedNode) {
        this.focusNode.showItemFor = updatedNode.showItemFor;
        this.tree.treeModel.update();
        this.isDataChanged = true;
      }
    });
  }

  removeNode(node: SABChildElement) {
    const notificationMessage = 'Are you sure you want to delete ' + node.selection + ' ' + node.name + ' ?';
    this.dialogService.showConfirmDialog({
      title: 'Remove Node',
      message: notificationMessage,
      yesCallback: () => {
        const parentNode = this.findParentNode(node.parentId, node.selection);
        if (parentNode) {
          parentNode.children.splice(parentNode.children.indexOf(node), 1);
          this.tree.treeModel.update();
          this.isDataChanged = true;
          this.updateSuggestionsList(parentNode);
        }
      }
    });
  }

  // tree traversal
  findParentNode(parentId: number, selection: string) {
    let resultNode = null;
    const categories = [this.category];

    categories_loop :
      for (let i = 0, len_i = categories.length; i < len_i; i++) {
        resultNode = this.checkIfParentNode(categories[i], parentId);
        if (resultNode) {
          break categories_loop;
        }
        if (selection === 'category') {
          continue;
        }
        const classes = categories[i].children;
        if (!classes) {
          continue;
        }

        for (let j = 0, len_j = classes.length; j < len_j; j++) {
          resultNode = this.checkIfParentNode(classes[j], parentId);
          if (resultNode) {
            break categories_loop;
          }
          if (selection === 'class') {
            continue;
          }
          const types = classes[j].children;
          if (!types) {
            continue;
          }

          for (let k = 0, len_k = types.length; k < len_k; k++) {
            resultNode = this.checkIfParentNode(types[k], parentId);
            if (resultNode) {
              break categories_loop;
            }
            if (selection === 'type') {
              continue;
            }
            const events = types[k].children;
            if (!events) {
              continue;
            }

            for (let l = 0, len_l = events.length; l < len_l; l++) {
              resultNode = this.checkIfParentNode(events[l], parentId);
              if (resultNode) {
                break categories_loop;
              }
            }
          }
        }
      }

    return resultNode;
  }

  checkIfParentNode(node: SABChildElement, parentId: number) {
    return node.siteServeId === parentId ? node : null;
  }

  isAnroidEnabled(text: string): boolean {
    return text === 'android' || text === 'both';
  }

  isIOSEnabled(text: string): boolean {
    return text === 'ios' || text === 'both';
  }

  /**
   * Remove category group.
   */
  removeCategory() {
    this.dialogService.showConfirmDialog({
      title: 'Remove Category',
      message: 'Are You Sure You Want to category? This Action Could Not Be Reverted!',
      yesCallback: () => {
        this.callRemoveCategory.emit(this.category);
      }
    });
  }

  /**
   * Revert changes. got category children from backup and reset main properties array.
   */
  revertCategoryChanges() {
    this.dialogService.showConfirmDialog({
      title: 'Cancel All Category Changes',
      message: 'Are You Sure You Want to Revert Category Changes?',
      yesCallback: () => {
        this.category.children = JSON.parse(JSON.stringify(this.categoryBackupItems));
        this.resetEditState();
      }
    });
  }

  /**
   * Save all category changes.
   * renew children in backup for future reverts.
   */
  saveCategoryChanges() {
    this.categoryBackupItems = JSON.parse(JSON.stringify(this.category.children));
    this.applyCategoryChanges.emit(this.category);

    this.resetEditState();
  }

  /**
   * Reset flags.
   */
  resetEditState() {
    this.isDataChanged = false;
    this.isNewCategory = false;
  }

  private loadAvailableDataMap(categoryId: number, callbackFunc) {
    if (!this.availableDataMap || this.availableDataMap.size <= 0) {
      this.isLoading = true;
      this.globalLoaderService.showLoader();
      this.streamAndBetAPIService.getSiteServeEvents(categoryId)
        .map((data: any) => {
          return data;
        }).subscribe((data: any) => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.availableDataMap = data.body;

        callbackFunc();

      }, () => {
        this.isLoading = false;
        this.globalLoaderService.hideLoader();
      });
    } else {
      callbackFunc();
    }
  }
}

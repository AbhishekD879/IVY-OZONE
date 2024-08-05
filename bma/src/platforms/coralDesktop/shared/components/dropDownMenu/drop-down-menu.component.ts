import {
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
  OnChanges, SimpleChanges
} from '@angular/core';
import * as _ from 'underscore';
import { IMenuItem } from '@shared/components/dropDownMenu/drop-down-menu.model';

@Component({
  selector: 'drop-down-menu',
  templateUrl: './drop-down-menu.component.html',
  styleUrls: ['./drop-down-menu.component.scss']
})
export class DropDownMenuComponent implements OnInit, OnChanges {
  @Input() selectedItem: string;
  @Input() menuList: IMenuItem[];
  @Input() icon?: string;
  @Input() selectionKey: string;
  @Input() dropDownCss: boolean;

  @Output() readonly clickFunction?: EventEmitter<any> = new EventEmitter();

  showMenu: boolean;
  selectedListItem: any;
  active: boolean[] = [];

  private _selectionKey: any;
  private _index: number;

  constructor() {
    this.clickItem = this.clickItem.bind(this);
  }

  ngOnInit(): void {
    this._selectionKey = this.selectionKey || 'name' || 'title';
    this.selectedListItem = this.getSelectedItemName(this.selectedItem, this._selectionKey);
  }

  ngOnChanges(changes: SimpleChanges): void {
    const isListItemChanged = changes.menuList &&
                            changes.menuList.currentValue &&
                            changes.menuList.previousValue !== undefined &&
                            (changes.menuList.currentValue.length !== changes.menuList.previousValue.length);
    const isSelectedItemChanged = changes.selectedItem &&
                            changes.selectedItem.currentValue &&
                            changes.selectedItem.previousValue !== undefined &&
                            (changes.selectedItem.currentValue !== changes.selectedItem.previousValue);
    if (isListItemChanged) {
      const selectedListItem = changes.menuList.currentValue[0];
      this.selectedListItem = selectedListItem.text || selectedListItem.name || selectedListItem.title;
    }

    if (isSelectedItemChanged) {
      this.selectedListItem = this.getSelectedItemName(changes.selectedItem.currentValue, this._selectionKey);
    }
  }

  trackByName(index: number, item: IMenuItem): string {
    return item.name;
  }

  /**
   * Function on item click
   * @param {String} parentOption
   * @param {String} childOption
   * @param {Number} index
   */
  clickItem(parentOption: IMenuItem, childOption: IMenuItem | any, index: number) {
    const selection = childOption ? {
      parent: parentOption[this._selectionKey] || parentOption.name || parentOption.title,
      child: childOption[this._selectionKey] || childOption.name || childOption.title
    } : (parentOption[this._selectionKey] || parentOption.name  || parentOption.title);

    this.clickFunction.emit(selection);

    if (!parentOption.hasChild) {
      this.showMenu = !this.showMenu;
      this.selectedListItem = parentOption.text || parentOption.name || parentOption.title;
    } else {
      if (this._index === index) {
        this.active[index] = !this.active[index];
      } else {
        this.active = [];
        this.active[index] = true;
        this._index = index;
      }
    }
  }

  getSelectedItemName(selectedItem: string, selectionKey?: string): string {
    const menuItemKey = selectionKey || 'name';

    const item: IMenuItem = _.find(this.menuList, { [menuItemKey]: selectedItem });
    if (!item) {
      return selectedItem;
    }
    return item.text || item.name || item.title;
  }
}

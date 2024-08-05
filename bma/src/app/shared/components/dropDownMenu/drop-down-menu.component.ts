import {
  Component,
  EventEmitter,
  Input, OnChanges,
  OnInit,
  Output,
  SimpleChanges,
  ChangeDetectorRef
} from '@angular/core';
import * as _ from 'underscore';

import { IMenuItem } from './drop-down-menu.model';

@Component({
  selector: 'drop-down-menu',
  templateUrl: './drop-down-menu.component.html',
  styleUrls: ['./drop-down-menu.component.scss']
})
export class DropDownMenuComponent implements OnInit, OnChanges {
  @Input() selectedItem: string;
  @Input() menuList: IMenuItem[];
  @Input() selectionNameKey: string;
  @Input() selectionValueKeys: string[];
  @Input() toggleTitle: string;
  @Input() isFromCoupon: boolean = false;

  @Output() readonly clickFunction?: EventEmitter<string[]> = new EventEmitter();

  showMenu: boolean = false;
  selectedListItem: string;
  nameKey: string;
  valueKeys: string[];

  private readonly nameKeys = ['title', 'text', 'name'];

  constructor(private changeDetectorRef: ChangeDetectorRef) {
    this.clickItem = this.clickItem.bind(this);
    this.trackByFn = this.trackByFn.bind(this);
  }

  ngOnInit(): void {
    this.initMenu();
  }

  ngOnChanges(changes: SimpleChanges): void {
    const menuListCurrent = changes.menuList && changes.menuList.currentValue && changes.menuList.currentValue.length;
    const menuListPrevious = changes.menuList && changes.menuList.previousValue && changes.menuList.previousValue.length;
    const isSelectedItemChanged = changes.selectedItem &&
      changes.selectedItem.currentValue &&
      changes.selectedItem.previousValue !== undefined &&
      (changes.selectedItem.currentValue !== changes.selectedItem.previousValue);

    if (isSelectedItemChanged) {
      this.selectedListItem = this.getSelectedItemName(changes.selectedItem.currentValue);
    }

    // if we have update for menu items and items amount was changed.
    if (menuListCurrent !== undefined && menuListPrevious !== undefined && (menuListCurrent !== menuListPrevious)) {
      const isCurrentItemPresent = changes.menuList.currentValue
                                      .find((menuItem) => menuItem.templateMarketName === this.selectedListItem);

      // if current selected Option is not present anymore in list, we will re-init dropdown;
      if (!isCurrentItemPresent) {
        this.initMenu();
      }
    }
  }

  initMenu(): void {
    this.nameKey = this.selectionNameKey || this.nameKeys.find((key: string) => this.menuList[0][key]);
    this.valueKeys = this.selectionValueKeys || [this.nameKey];
    this.selectedListItem = this.getSelectedItemName(this.selectedItem);
  }

  trackByFn(index: number, item: IMenuItem): string {
    return item[this.nameKey];
  }

  /**
   * Function on item click
   * @param {String} parentOption
   * @param {String} childOption
   * @param {Number} index
   */
  clickItem(item: IMenuItem): void {
    const selection: string[] = this.getItemValues(item);
    this.clickFunction.emit(selection);

    this.menuToggle(false);
    this.selectedListItem = item[this.nameKey];
  }


  menuToggle(show?: boolean): void {
    if (this.showMenu === show) { return; }

    this.showMenu = show !== undefined ? show : !this.showMenu;
    this.changeDetectorRef.detectChanges();
  }

  clickHandler(event: Event): void {
    if (!event.cancelable) { return; }

    event.preventDefault();
    this.menuToggle(false);
  }

  private getSelectedItemName(selectedItem: string): string {
    const item: IMenuItem = _.find(this.menuList, { [this.valueKeys[0]]: selectedItem });
    if (!item) {
      return selectedItem;
    }
    return item[this.nameKey];
  }

  private getItemValues(item: IMenuItem): string[] {
    return this.valueKeys.map((key: string) => item[key]);
  }
}

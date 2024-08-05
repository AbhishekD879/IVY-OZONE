import { Component, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';

import { ILpSpDropdowmItem } from './lp-sp-dropdown.model';

@Component({
  selector: 'lp-sp-dropdown',
  templateUrl: 'lp-sp-dropdown.component.html',
  styleUrls: ['./lp-sp-dropdown.component.scss']
})

export class LpSpDropdownComponent implements OnInit {
  selectedItem: ILpSpDropdowmItem;
  listOpen: boolean = false;
  clickInside: boolean = false;

  @Input() disabled: boolean;
  @Input() mode: string;
  @Output() readonly valueChange: EventEmitter<string> = new EventEmitter();

  private _selectedValue: string;
  private _options: ILpSpDropdowmItem[] = [];

  @Input()
  set options(options: ILpSpDropdowmItem[]) {
    this._options = options;
    this.updateSelectedItem();
  }
  get options() {
    return this._options;
  }
 
  @Input()
  set selectedValue(value: string) {
    this._selectedValue = value;
    this.updateSelectedItem();
  }
  get selectedValue() {
    return this._selectedValue;
  }

  @HostListener('document:click', ['$event']) clickOutside(): void {
    if (!this.clickInside) {
      this.closeList();
    }

    this.clickInside = false;
  }

  ngOnInit(): void {
    this.updateSelectedItem();
  }

  toggleList(): void {
    if (this.disabled) {
      return;
    }

    this.listOpen = !this.listOpen;
  }

  selectItem(item: ILpSpDropdowmItem): void {
    if (this.disabled) {
      return;
    }

    this.selectedItem = item;
    this.valueChange.emit(item.name);
    this.closeList();
  }

  trackByName(index, item: ILpSpDropdowmItem): string {
    return `${index}_${item.name}`;
  }

  private closeList(): void {
    this.listOpen = false;
  }

  private updateSelectedItem(): void {
    if (this.selectedValue && this.options) {
      this.selectedItem = this.options.find(o => o.name === this.selectedValue);
    }
  }
}

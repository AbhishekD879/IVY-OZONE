import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'cms-simple-select-list',
  templateUrl: './cms-simple-select-list.component.html',
  styleUrls: ['./cms-simple-select-list.component.scss']
})
export class CmsSimpleSelectListComponent implements OnInit {
  @Input() clearSpaces: boolean;
  @Input() disabled: boolean;
  @Input() options: Array<any>;

  @Input() selected: string;

  @Output() onDataChange: EventEmitter<any> = new EventEmitter();

  /**
   * Added Support Array of Objects
   */
  @Input() optionsData: any;

  // Object property name to use value as option text
  @Input() optionsDataTitle: string;

  // Object property name to use value as model value
  @Input() optionsDataValue: string;
  constructor() { }

  ngOnInit() {
  }

  /**
   * Remove blank spaces from string
   * @param {string} str
   * @returns {string}
   */
  public removeBlankSpaces (str: string): string {
    if (this.clearSpaces === false) {
      return str;
    }
    return str.split(' ').join('');
  }

  /**
   * Change option value
   * @param {string} value
   */
  public onChange(value: string): void {
    this.onDataChange.emit(value);
  }

}

import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import {
  deviceVariants,
  loggedInUserVariants,
  newExistingUserVariants,
  initVariants
} from './customer-variants.enum';

@Component({
  selector: 'customer-variants-select',
  templateUrl: './customer-variants-select.component.html'
})
export class CustomerVariantsSelectComponent implements OnInit {
  @Input() customerType: string;
  @Input() placeholder?: string = 'Show To Customer';
  @Input() optionsType?: string;
  @Output() onChange: EventEmitter<any> = new EventEmitter();

  public showToCustomerVariants: Array<string>;
  public variantsEnum: any;

  constructor() {}

  public onChangeHandler(value: string): void {
    this.onChange.emit(value);
  }

  ngOnInit() {
    switch (this.optionsType) {
      case 'loggedIn':
        this.showToCustomerVariants = Object.keys(loggedInUserVariants);
        this.variantsEnum = loggedInUserVariants;
        break;
      case 'existing':
        this.showToCustomerVariants = Object.keys(newExistingUserVariants);
        this.variantsEnum = newExistingUserVariants;
        break;
      case 'device':
        this.showToCustomerVariants = Object.keys(deviceVariants);
        this.variantsEnum = deviceVariants;
        break;
      case 'init':
        this.showToCustomerVariants = Object.keys(initVariants);
        this.variantsEnum = initVariants;
        break;
    }
  }
}

import { Component } from '@angular/core';
import {
  ShowAllButtonComponent as AppShowAllButtonComponent
} from '@shared/components/showAllButton/show-all-button.component';

@Component({
  selector: 'show-all-button',
  styleUrls: ['show-all-button.component.scss'],
  templateUrl: 'show-all-button.component.html'
})

export class ShowAllButtonComponent extends AppShowAllButtonComponent {}

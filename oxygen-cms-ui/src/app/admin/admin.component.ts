import {Component} from '@angular/core';

@Component({
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent {
  links = [{
    label: 'Users',
    path: './users'
  }, {
    label: 'Brands',
    path: './brands'
  }];
}

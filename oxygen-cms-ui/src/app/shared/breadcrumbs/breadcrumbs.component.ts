import { Component, OnInit, Input } from '@angular/core';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';

@Component({
  selector: 'breadcrumbs',
  templateUrl: './breadcrumbs.component.html',
  styleUrls: ['./breadcrumbs.component.scss']
})
export class BreadcrumbsComponent implements OnInit {
  @Input() breadcrumbsData: Array<Breadcrumb>;

  constructor() {}

  ngOnInit() {}
}

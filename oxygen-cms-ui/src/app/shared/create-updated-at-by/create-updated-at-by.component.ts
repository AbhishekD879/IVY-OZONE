import { Component, OnInit, Input } from '@angular/core';
import { Base } from '../../client/private/models/base.model';

@Component({
  selector: 'create-updated-at-by',
  templateUrl: './create-updated-at-by.component.html',
  styleUrls: ['./create-updated-at-by.component.scss']
})
export class CreateUpdatedAtByComponent implements OnInit {

  @Input()
  public collection: Base;

  constructor() { }

  ngOnInit(): void {
  }

}

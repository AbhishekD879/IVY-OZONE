import { Component, OnInit, Input } from '@angular/core';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';

@Component({
  selector: 'active-inactive-expired',
  templateUrl: './active-inactive-expired.component.html',
  styleUrls: ['./active-inactive-expired.component.scss']
})
export class ActiveInactiveExpiredComponent implements OnInit {
  @Input() collection: ActiveInactiveExpired;

  constructor() { }

  ngOnInit() {
  }

  get total(): number {
    return this.collection.active +
      (this.collection.inactive ? this.collection.inactive : 0) +
        (this.collection.expired ? this.collection.expired : 0);
  }

}

import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CompetitionModule} from '../../../../../client/private/models';

@Component({
  selector: 'app-knockouts-module',
  templateUrl: './knockouts-module.component.html'
})
export class KnockoutsModuleComponent implements OnInit {

  @Input() module: CompetitionModule;
  @Output() changed: EventEmitter<any> = new EventEmitter();
  constructor() { }

  ngOnInit() {
  }

  public handleModuleChange(data) {
    this.changed.emit(data);
  }
}

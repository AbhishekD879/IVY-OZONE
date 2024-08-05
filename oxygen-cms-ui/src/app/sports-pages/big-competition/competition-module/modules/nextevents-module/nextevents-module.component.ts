import {Component, Input, OnInit} from '@angular/core';
import {CompetitionModule} from '../../../../../client/private/models';

@Component({
  selector: 'app-nextevents-module',
  templateUrl: './nextevents-module.component.html',
  styleUrls: ['./nextevents-module.component.scss']
})
export class NexteventsModuleComponent implements OnInit {
  @Input() module: CompetitionModule;

  constructor() {}

  ngOnInit() {}

  /**
   * Check if fields typeId and maxDisplay is valid(not empty)
   * @returns {boolean}
   */
  public isValidForm(): boolean {
    return !!(this.module.typeId && this.module.maxDisplay);
  }

}

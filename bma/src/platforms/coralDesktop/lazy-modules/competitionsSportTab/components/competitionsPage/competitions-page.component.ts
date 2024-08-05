import { Component, OnInit, AfterViewInit } from '@angular/core';
// not used @lazy-modules alias because for Vanilla Desktop it points to excluded /vanilla/lazy-modules/competitionsSportTab/...
import {
  CompetitionsPageComponent
} from '@app/lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.component';
import { IWidgetParams } from '@desktop/models/wigets.model';
import * as _ from 'underscore';

@Component({
  selector: 'competitions-page',
  styleUrls: ['competitions-page.component.scss'],
  templateUrl: 'competitions-page.component.html'
})

export class DesktopCompetitionsPageComponent extends CompetitionsPageComponent implements OnInit, AfterViewInit {
  competitionConfig: { id: string, name: string }[];
  switcherPosition: number;
  switchers: { label: string, onClick: Function }[];
  ngOnInit(): void {
    super.ngOnInit();
    this.competitionConfig = [{ id: 'competitionsPage', name: 'competitionsPage' }];
    this.switcherPosition = 0;
    this.switchers = [
      {
        label: 'matches',
        onClick: () => {
          this.switcherPosition = 0;
          this.eventsByCategory = {...this.eventsByCategoryCopy};
        }
      }
    ];
  }

  get widgetParams(): IWidgetParams {
    return {
      typeId: this.typeId,
      classId: this.classId
    };
  }
  set widgetParams(value: IWidgetParams){}

  ngAfterViewInit(): void {
    // Replace Mobile Function
  }

  protected generateSwitchers() {
    if (!_.isEmpty(this.outrights) && !_.findWhere(this.switchers, { label: 'outrights' })) {
      this.switchers.push({
        label: 'outrights',
        onClick: () => {
          this.switcherPosition = 1;
        }
      });
    }
  }
}

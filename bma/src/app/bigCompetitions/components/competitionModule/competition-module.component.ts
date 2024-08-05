import { Component, OnDestroy, Input, ViewChild, ViewContainerRef,
  AfterContentInit, ComponentRef, ChangeDetectionStrategy } from '@angular/core';
import { CompetitionOutrightsComponent } from '@app/bigCompetitions/components/competitionOutrights/competition-outrights.component';
import {
  CompetitionGroupsWidgetComponent
} from '@app/bigCompetitions/components/competitionGroupsWidget/competition-groups-widget.component';

import { CompetitionModuleDirective } from '../../directives/competition-module.directive';
import { CompetitionNextEventsComponent } from '@app/bigCompetitions/components/competitionNextEvents/competition-next-events.component';
import { CompetitionGroupAllComponent } from '@app/bigCompetitions/components/competitionGroupAll/competition-groups-all.component';
import {
  CompetitionGroupIndividualComponent
} from '@app/bigCompetitions/components/competitionGroupIndividual/competition-groups-individual.component';
import { CompetitionSpecialsComponent } from '@app/bigCompetitions/components/competitionSpecials/competition-specials.component';
import {
  CompetitionSpecialsOverviewComponent
} from '@app/bigCompetitions/components/competitionSpecialsOverview/competition-specials-overview.component';
import { CompetitionKnockoutsComponent } from '@app/bigCompetitions/components/competitionKnockouts/competition-knockouts.component';
import { CompetitionPromotionsComponent } from '@app/bigCompetitions/components/competitionPromotions/competition-promotions.component';
import { CompetitionResultsComponent } from '@app/bigCompetitions/components/competitionResults/competition-results.component';
import { IBCModule } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';

type IComponentsRef = any | (CompetitionNextEventsComponent
  & CompetitionGroupsWidgetComponent
  & CompetitionOutrightsComponent
  & CompetitionSpecialsComponent
  & CompetitionSpecialsOverviewComponent
  & CompetitionKnockoutsComponent
  & CompetitionPromotionsComponent
  & CompetitionResultsComponent
  & CompetitionGroupAllComponent
  & CompetitionGroupIndividualComponent);

@Component({
  selector: 'competition-module',
  template: `<div><ng-template [competition-module]></ng-template></div>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CompetitionModuleComponent implements AfterContentInit, OnDestroy {

  @ViewChild(CompetitionModuleDirective, { read: ViewContainerRef, static: true }) entry: ViewContainerRef;
  competitioinComponents: { [key: string]: any };
  componentRef: ComponentRef<IComponentsRef>;

  @Input() name: string;
  @Input() module: IBCModule;

  constructor() {
    this.competitioinComponents = {
      'NEXT_EVENTS': CompetitionNextEventsComponent,
      'NEXT_EVENTS_INDIVIDUAL': CompetitionNextEventsComponent,
      'GROUP_WIDGET': CompetitionGroupsWidgetComponent,
      'OUTRIGHTS': CompetitionOutrightsComponent,
      'SPECIALS': CompetitionSpecialsComponent,
      'SPECIALS_OVERVIEW': CompetitionSpecialsOverviewComponent,
      'KNOCKOUTS': CompetitionKnockoutsComponent,
      'PROMOTIONS': CompetitionPromotionsComponent,
      'RESULTS': CompetitionResultsComponent,
      'GROUP_ALL': CompetitionGroupAllComponent,
      'GROUP_INDIVIDUAL': CompetitionGroupIndividualComponent
    };
  }

  ngAfterContentInit(): void {
    this.entry.clear();
    const component = this.selectComponent(this.name);
    this.componentRef = this.entry.createComponent(component);
    this.componentRef.instance.moduleConfig = this.module;
  }

  ngOnDestroy(): void {
    this.componentRef && this.componentRef.destroy();
  }

  private selectComponent(name: string = ''): any {
    return name in this.competitioinComponents ? this.competitioinComponents[name] : null;
  }
}

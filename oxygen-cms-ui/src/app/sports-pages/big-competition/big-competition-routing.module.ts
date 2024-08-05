import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CompetitionsListComponent} from './competition/competitions-list/competitions-list.component';
import {CompetitionEditComponent} from './competition/competition-edit/competition-edit.component';
import {TabEditComponent} from './competition-tab/tab-edit/tab-edit.component';
import {CompetitionSubTabEditComponent} from './competition-sub-tab/competition-sub-tab-edit/competition-sub-tab-edit.component';
import {CompetitionModuleEditComponent} from './competition-module/competition-module-edit/competition-module-edit.component';
import {ParticipantEditComponent} from './participant/participant-edit/participant-edit.component';
// tslint:disable-next-line:max-line-length
import {RoundNamesEditComponent} from './competition-module/modules/knockouts-module/round-names/round-names-edit/round-names-edit.component';

import {PendingChangesGuard} from '../../client/private/classes/PendingChangesGuard.class';
import {MatchEditComponent} from './competition-module/modules/knockouts-module/matches/match-edit/match-edit.component';

const routes: Routes = [
  {
    path: '',
    children: [
      {
        path: '',
        children: [{
          path: '',  component: CompetitionsListComponent
        }, {
          path: ':competitionId',
          component: CompetitionEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/participant/:participantId',
          component: ParticipantEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId',
          component: TabEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId/subtab/:subTabId',
          component: CompetitionSubTabEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId/module/:moduleId',
          component: CompetitionModuleEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId/module/:moduleId/round-name/:abbreviation',
          component: RoundNamesEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId/subtab/:subTabId/module/:moduleId',
          component: CompetitionModuleEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId/subtab/:subTabId/module/:moduleId/round-name/:abbreviation',
          component: RoundNamesEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId/module/:moduleId/matches/:abbreviation',
          component: MatchEditComponent,
          canDeactivate: [PendingChangesGuard]
        }, {
          path: ':competitionId/tab/:tabId/subtab/:subTabId/module/:moduleId/matches/:abbreviation',
          component: MatchEditComponent,
          canDeactivate: [PendingChangesGuard]
        }]
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: [PendingChangesGuard]
})

export class BigCompetitionRoutingModule { }

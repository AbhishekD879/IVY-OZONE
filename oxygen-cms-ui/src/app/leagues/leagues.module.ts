import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';

import { LeaguesListComponent } from './leagues-list/leagues-list.component';
import { EditLeagueComponent } from './edit-league/edit-league.component';
import { CreateLeagueDialogComponent } from './create-league-dialog/create-league-dialog.component';

import { LeaguesConfigurationRoutingModule } from './leagues-routing.module';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    LeaguesConfigurationRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    LeaguesListComponent,
    EditLeagueComponent,
    CreateLeagueDialogComponent
  ],
  entryComponents: [
    CreateLeagueDialogComponent
  ]
})
export class LeaguesModule { }

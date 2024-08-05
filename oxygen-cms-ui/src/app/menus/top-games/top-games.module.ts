import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';

import { TopGamesRoutingModule } from './top-games-routing.module';
import { TopGamesListComponent } from './top-games-list/top-games-list.component';
import { TopGamesCreateComponent } from './top-games-create/top-games-create.component';
import { TopGamesEditComponent } from './top-games-edit/top-games-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    TopGamesRoutingModule
  ],
  declarations: [
    TopGamesListComponent,
    TopGamesCreateComponent,
    TopGamesEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class TopGamesModule { }

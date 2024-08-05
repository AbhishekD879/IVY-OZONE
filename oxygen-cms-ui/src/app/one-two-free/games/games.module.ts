import { NgModule } from '@angular/core';
import { SharedModule } from '../../shared/shared.module';
import { GamesRoutingModule } from './games-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { GamesPageComponent } from './games-list/games.page.component';
import { GamePageComponent } from './game-edit/pageComponent/game.page.component';
import { GameCreateComponent } from './game-create/game.create.component';
import { GameAPIService } from '../service/game.api.service';
import { EventCreateComponent } from './game-edit/event-create/event.create.component';
import {TeamKitAPIService} from '@app/one-two-free/teamKit.api.service';
import { SeasonsApiService } from '@app/one-two-free/service/seasons.api.service';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    GamesRoutingModule
  ],
  declarations: [
    GamesPageComponent,
    GamePageComponent,
    GameCreateComponent,
    EventCreateComponent
  ],
  providers: [
    GameAPIService,
    TeamKitAPIService, SeasonsApiService
  ],
  entryComponents: [
    GameCreateComponent
  ]
})
export class GamesModule { }

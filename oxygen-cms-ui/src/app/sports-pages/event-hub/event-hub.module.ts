import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EventHubRoutingModule } from './event-hub-routing.module';
import { SharedModule } from '@app/shared/shared.module';

import { EventHubPageComponent } from './components/event-hub-page/event-hub.page.component';
import { EventHubService } from '@app/sports-pages/event-hub/services/event-hub.service';
import { EventHubListPageComponent } from '@app/sports-pages/event-hub/components/event-hub-list-page/event-hub-list.page.component';
import { SportsModulesModule } from '@app/sports-modules/sports-modules.module';
import { EventHubCreateComponent } from './components/event-hub-create/event-hub-create.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SportsModulesModule,
    EventHubRoutingModule
  ],
  declarations: [
    EventHubListPageComponent,
    EventHubPageComponent,
    EventHubCreateComponent
  ],
  providers: [
    EventHubService
  ],
  entryComponents: [
    EventHubPageComponent,
    EventHubCreateComponent
  ]
})
export class EventHubModule { }

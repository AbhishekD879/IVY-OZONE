import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {SharedModule} from '@root/app/shared/shared.module';

import {VirtualSportsRoutingModule} from './virtual-sports-routing.module';

import {ParentSportsListComponent} from './parent-sports/parent-sports-list/parent-sports-list.component';
import {ParentSportsCreateComponent} from './parent-sports/parent-sports-create/parent-sports-create.component';
import {ParentSportsEditComponent} from './parent-sports/parent-sports-edit/parent-sports-edit.component';
import {VirtualSportsService} from '@app/virtual-sports/virtual-sports.service';
import {ChildSportsListComponent} from '@app/virtual-sports/child-sports/child-sports-list/child-sports-list.component';
import {ChildSportsCreateComponent} from '@app/virtual-sports/child-sports/child-sports-create/child-sports-create.component';
import {ChildSportsEditComponent} from '@app/virtual-sports/child-sports/child-sports-edit/child-sports-edit.component';
import {VirtualSportsChildService} from '@app/virtual-sports/virtual-sports-child.service';
import {CommonModule} from '@angular/common';
import {TrackImageListComponent} from './child-sports/track-image-list/track-image-list.component';
import {EventDialogComponent} from '@app/virtual-sports/child-sports/event-dialog.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    VirtualSportsRoutingModule
  ],
  providers: [
    VirtualSportsService,
    VirtualSportsChildService
  ],
  entryComponents: [
    ParentSportsCreateComponent,
    ChildSportsCreateComponent,
    EventDialogComponent
  ],
  declarations: [
    ParentSportsListComponent,
    ParentSportsCreateComponent,
    ParentSportsEditComponent,
    ChildSportsListComponent,
    ChildSportsCreateComponent,
    ChildSportsEditComponent,
    TrackImageListComponent,
    EventDialogComponent
  ]
})
export class VirtualSportsModule {
}

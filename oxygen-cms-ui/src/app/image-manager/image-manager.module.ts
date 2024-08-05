import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '@app/shared/shared.module';
import { ImageManagerRoutingModule } from '@app/image-manager/image-manager-routing.module';
import { ImageManagerListComponent } from '@app/image-manager/image-manager-list/image-manager-list.component';
import { DetailsPageComponent } from '@app/image-manager/details-page/details-page.component';
import { ImageManagerService } from '@app/image-manager/services/image-manager.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    ImageManagerRoutingModule
  ],
  declarations: [
    ImageManagerListComponent,
    DetailsPageComponent
  ],
  providers: [
    ImageManagerService
  ]
})
export class ImageManagerModule { }

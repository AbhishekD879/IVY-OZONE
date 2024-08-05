import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ImageManagerListComponent } from '@app/image-manager/image-manager-list/image-manager-list.component';
import { DetailsPageComponent } from '@app/image-manager/details-page/details-page.component';

import { IMAGE_MANAGER_ROUTES } from '@app/image-manager/constants/image-manager.constant';

const moduleIconListConfigurationRoutes: Routes = [
  { path: '', component: ImageManagerListComponent },
  { path: IMAGE_MANAGER_ROUTES.add, component: DetailsPageComponent },
  { path: IMAGE_MANAGER_ROUTES.details, component: DetailsPageComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(moduleIconListConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class ImageManagerRoutingModule {}

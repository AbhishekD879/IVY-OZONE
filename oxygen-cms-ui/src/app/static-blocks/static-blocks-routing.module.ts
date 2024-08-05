import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { StaticBlocksPageComponent } from './static-blocks-page/static-blocks-page.component';
import { EditStaticBlockComponent } from './edit-static-block/edit-static-block.component';

const staticBlocksConfigurationRoutes: Routes = [
  {
    path: '',
    component: StaticBlocksPageComponent,
  },
  { path: ':id',  component: EditStaticBlockComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(staticBlocksConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class StaticBlocksConfigurationRoutingModule { }

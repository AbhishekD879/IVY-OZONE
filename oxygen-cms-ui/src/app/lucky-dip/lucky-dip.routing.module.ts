import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LuckyDipComponent } from './lucky-dip.component';
import { LuckyDipCreateComponent } from './lucky-dip-create/lucky-dip-create.component';
import { LuckyDipEditComponent } from './lucky-dip-edit/lucky-dip-edit.component';
import { LuckyDipMappingComponent } from './lucky-dip-mapping/lucky-dip-mapping.component';
import { LuckyDipMappingCreateComponent } from './lucky-dip-mapping-create/lucky-dip-mapping-create.component';
import { LuckyDipMappingEditComponent } from './lucky-dip-mapping-edit/lucky-dip-mapping-edit.component';
import { LuckyDipV2Component } from './lucky-dip-v2/lucky-dip-v2.component';

const luckyDipRoutes: Routes = [
  { path: '',   component: LuckyDipComponent},
  { path: 'v2',   component: LuckyDipV2Component},
  { path: 'create', component: LuckyDipCreateComponent },
  { path: 'v2/edit/:id', component: LuckyDipEditComponent },
  { path: 'mapping', component: LuckyDipMappingComponent },
  { path: 'mapping-create', component: LuckyDipMappingCreateComponent },
  { path: 'mapping/edit/:id', component: LuckyDipMappingEditComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(luckyDipRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class LuckyDipRoutingModule { }
import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {AdminComponent} from './admin.component';

import { UsersComponent } from './users/users.component';
import { UserPageComponent } from './users/user-page/user-page.component';
import { BrandsListComponent } from './brands/brands-list/brands-list.component';
import { EditBrandComponent } from './brands/edit-brand/edit-brand.component';

const adminRoutes: Routes = [
  {
    path: '',
    component: AdminComponent,
    children: [
      {
        path: '',
        children: [
          { path: 'brands',  component: BrandsListComponent },
          { path: 'brands/:id',  component: EditBrandComponent },
          { path: 'users', component: UsersComponent },
          { path: 'users/:id', component: UserPageComponent }
        ]
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(adminRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class AdminRoutingModule { }

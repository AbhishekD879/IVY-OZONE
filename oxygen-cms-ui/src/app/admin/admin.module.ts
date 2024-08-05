import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';

import { FilterPipe } from '../client/private/pipes/filter.pipe';

import { AdminComponent } from './admin.component';
import { AdminRoutingModule } from './admin-routing.module';

// Users component
import { UsersComponent } from './users/users.component';
import { UserPageComponent } from './users/user-page/user-page.component';
import { CreateUserDialogComponent } from './users/create-user-dialog/create-user-dialog.component';

// Brands Component
import { BrandsAPIService} from './brands/service/brands.api.service';
import { BrandsListComponent } from './brands/brands-list/brands-list.component';
import { AddBrandComponent } from './brands/add-brand/add-brand.component';
import { EditBrandComponent } from './brands/edit-brand/edit-brand.component';
import { FullNamePipe } from './users/full-name.pipe';

@NgModule({
  imports: [
    SharedModule,
    AdminRoutingModule
  ],
  declarations: [
    AdminComponent,
    UsersComponent,
    UserPageComponent,
    FilterPipe,
    FullNamePipe,
    CreateUserDialogComponent,
    BrandsListComponent,
    AddBrandComponent,
    EditBrandComponent
  ],
  entryComponents: [
    CreateUserDialogComponent,
    AddBrandComponent
  ],
  providers: [
    BrandsAPIService
  ]
})
export class AdminModule { }

import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {PendingChangesGuard} from '../client/private/classes/PendingChangesGuard.class';
import {MenuItemManageComponent} from './menu-management/menu-item-manage/menu-item-manage.component';

const routes: Routes = [
  {
    path: '',
    children: [
      {
        path: '',
        children: [{
           path: '',  component: MenuItemManageComponent
        }, {
          path: ':menuItemId',
          component: MenuItemManageComponent,
          canDeactivate: [PendingChangesGuard]
        }]
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: [PendingChangesGuard]
})
export class MenuConfigurationRoutingModule { }

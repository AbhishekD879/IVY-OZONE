import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {WidgetsPageComponent} from './all-widgets-page/pageComponent/widgets.page.component';
import {WidgetPageComponent} from './single-widget-page/pageComponent/widget.page.component';

const promotionsRoutes: Routes = [
  {
    path: '',
    component: WidgetsPageComponent,
    children: [

    ]
  },
  { path: ':id',  component: WidgetPageComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(promotionsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class WidgetsRoutingModule { }

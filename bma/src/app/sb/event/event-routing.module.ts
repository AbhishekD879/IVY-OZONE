import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SportMainComponent } from '@sbModule/components/sportMain/sport-main.component';
import { SportEventComponent } from '@sbModule/components/sportEvent/sport-event.component';
import { CanDeactivateGuard } from '@core/guards/can-deactivate-guard.service';

const routes: Routes = [
  {
    path: ':sport',
    children: [{
      /*
       * This component is in use for banner links (as well as automation tests),
       * it processes direct links like "event/1234567" and relies on enumerable sportId as router parameter, not the human-friendly strings
       */
      path: '',
      pathMatch: 'full',
      data: {
        segment: 'event.eventId'
      },
      component: SportEventComponent
    }, {
      path: ':className/:typeName/:eventName/:id',
      pathMatch: 'full',
      redirectTo: ':className/:typeName/:eventName/:id/main-markets'
    }, {
      path: ':className/:typeName/:eventName/:id/:market',
      component: SportMainComponent,
      canDeactivate: [CanDeactivateGuard],
      data: {
        segment: 'eventMain'
      },
      children: [{
        path: ':pitch',
        component: SportMainComponent,
        data: {
          segment: 'eventMain'
        }
      },
      {
        path: ':pitch/:formation/:player1',
        component: SportMainComponent,
        data: {
          segment: 'eventMain'
        }
      },
      {
        path: ':pitch/:formation/:player1/:player2',
        component: SportMainComponent,
        data: {
          segment: 'eventMain'
        }
      },{
        path: ':pitch/:formation/:player1/:player2/:player3',
        component: SportMainComponent,
        data: {
          segment: 'eventMain'
        }
      },{
        path: ':pitch/:formation/:player1/:player2/:player3/:player4',
        component: SportMainComponent,
        data: {
          segment: 'eventMain'
        }
      },{
        path: ':pitch/:formation/:player1/:player2/:player3/:player4/:player5',
        component: SportMainComponent,
        data: {
          segment: 'eventMain'
        }
      }]
    }]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazyEventRoutingModule { }

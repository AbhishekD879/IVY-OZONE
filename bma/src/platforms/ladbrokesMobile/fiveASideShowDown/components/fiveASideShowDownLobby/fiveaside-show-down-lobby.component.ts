import { Component, OnInit } from '@angular/core';
import {
  FiveASideShowDownLobbyComponent
    as AppFiveASideShowDownLobbyComponent
} from '@app/fiveASideShowDown/components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import { animate, style, transition, trigger } from '@angular/animations';
@Component({
  selector: 'fiveaside-show-down-lobby',
  templateUrl: './fiveaside-show-down-lobby.component.html',
  styleUrls: ['./fiveaside-show-down-lobby.component.scss'],
  animations: [
    trigger('slideOutRight', [
      transition(':leave', [
        style({transform: 'translateX(0%)'}),
        animate('1s ease-in', style({transform: 'translateX(100%)'}))
      ])
    ]),
    trigger('slideOutLeft', [
      transition(':leave', [
        style({transform: 'translateX(0%)'}),
        animate('1s ease-in', style({transform: 'translateX(-100%)'}))
      ])
    ])
  ]
})
export class FiveASideShowDownLobbyComponent extends AppFiveASideShowDownLobbyComponent implements OnInit {
}

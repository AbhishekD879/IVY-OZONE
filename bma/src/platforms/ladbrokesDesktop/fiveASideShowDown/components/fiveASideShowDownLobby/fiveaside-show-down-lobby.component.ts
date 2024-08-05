import { Component } from '@angular/core';
import { LAZY_LOAD_ROUTE_PATHS } from '@app/bma/constants/lazyload-route-paths.constant';
import {
  FiveASideShowDownLobbyComponent
    as AppFiveASideShowDownLobbyComponent
} from '@app/fiveASideShowDown/components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
@Component({
  selector: 'fiveaside-show-down-lobby',
  templateUrl: './fiveaside-show-down-lobby.component.html',
  styleUrls: ['./fiveaside-show-down-lobby.component.scss']
})
export class FiveASideShowDownLobbyComponent extends AppFiveASideShowDownLobbyComponent {
  public showDownHome: string = LAZY_LOAD_ROUTE_PATHS.showDownHome;
}

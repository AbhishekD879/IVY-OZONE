import { Injectable } from '@angular/core';
import { OnAppInit } from '@frontend/vanilla/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BehaviorSubject } from 'rxjs';
import { IFlagSource } from './models/flag-source.model';


@Injectable({
  providedIn: 'root'
})
export class FlagSourceService implements OnAppInit {

  flagStore: string;
  flagUpdate: BehaviorSubject<IFlagSource> = new BehaviorSubject<IFlagSource>({});
  constructor(private windowRefService: WindowRefService) { }

  /**
   * On app init populate flag store
   */
  onAppInit() {
    this.getServerFlags();
  }

  /**
   * Method to get Server flags from window ldkeys 
   */
  getServerFlags() {
   this.flagStore = this.windowRefService.nativeWindow.ldkeys;
  }

  updateFlagstore(updatedFlags){
    this.flagUpdate.next(updatedFlags);
  }
}

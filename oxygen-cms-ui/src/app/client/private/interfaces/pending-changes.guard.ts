import { Observable } from 'rxjs/Observable';

export interface ComponentCanDeactivate {
  confirmDialogMsg?: string;
  /*
  * Method should return false in case if confirmation popup needed to be shown
  * */
  canDeactivate: () => boolean | Observable<boolean>;
}

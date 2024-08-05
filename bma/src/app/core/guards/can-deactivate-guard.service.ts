import { CanDeactivateFn } from '@angular/router';
import { IComponentCanDeactivate } from '@app/core/models/component-can-deactivate.model';

/**
 * Description
 * Guard deciding if a route can be deactivated.
 * If it returns true, navigation will continue
 * Otherwise, onChangeRoute()  is called and navigation will be cancelled
 */

export const CanDeactivateGuard:CanDeactivateFn<any> = (component: IComponentCanDeactivate) => {
  if (component.canChangeRoute()) { return true; }
  component.onChangeRoute();
  return false;
}

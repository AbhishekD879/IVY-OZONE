export interface IRouteData<T> {
  feature?: keyof T;
  path?: string;
  segment?: string;
}

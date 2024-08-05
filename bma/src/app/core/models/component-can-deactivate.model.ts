export interface IComponentCanDeactivate {
  canChangeRoute(): boolean;
  onChangeRoute(): void;
}

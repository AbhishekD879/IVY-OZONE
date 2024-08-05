export interface IComponentInstance {
  [key: string]: any;
}

export interface IDynamicComponent {
  destroy: Function;
  instance: IComponentInstance;
}

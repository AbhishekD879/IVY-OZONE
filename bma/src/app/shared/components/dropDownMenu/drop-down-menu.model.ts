export interface IMenuItem {
  text: string;
  name: string;
  templateMarketName?: string;
  title?: string;
  hasChild?: boolean;
  default?: boolean;
  list?: IMenuItem[];
}

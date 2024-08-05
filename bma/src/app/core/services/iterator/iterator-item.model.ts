export interface IIteratorItem {
  priority?: number;
  title?: string;
  description?: string;
  data?: any;
  run: Function;
}

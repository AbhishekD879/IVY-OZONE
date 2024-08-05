export interface IWidget {
  title: string;
  directiveName: string;
  showExpanded: boolean;
  publishedDevices: string[];
  columns: string[];
  showOn?: IShowOn;
  name?: string;
}

export interface IShowOn {
  sports: string[];
  routes: string;
}

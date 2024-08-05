export interface ISeoPagesPaths {
  [key: string]: string;
}
export interface IAutoSeoPages {
  [autoSeoUrl: string]: {
    metaTitle?: string,
    metaDescription?: string
  }
}

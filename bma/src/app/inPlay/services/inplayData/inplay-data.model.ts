export interface IDataTypes {
  ribbon: IDataType;
  structure: IDataType;
  ls_structure: IDataType;
  sports: IDataType;
  competition: IDataType;
  virtuals: IDataType;
}

interface IDataType {
  requestMessage: string;
  additionalRequestParams?: {
    emptyTypes?: string;
    autoUpdates?: string;
  };
  buildResponseMessage(data?: any): string;
}

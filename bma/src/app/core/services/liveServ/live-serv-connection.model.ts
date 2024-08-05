export interface ISocketIO {
  connected: boolean;
  disconnected: true;
  id: string;
  ids: number;
  nsp: string;
  [key: string]: any;
}


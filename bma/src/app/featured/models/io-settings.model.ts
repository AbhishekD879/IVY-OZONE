export interface IIoSettings {
  transports: string[];
  upgrade: boolean;
  reconnectionDelay: number;
  forceNew: boolean;
  timeout: number;
  reconnectionAttempts: number;
  query: string;
  pingDelay: number;
}

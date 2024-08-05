export interface IScrollEvent {
  target: IEventTarget;
}

interface IEventTarget {
  scrollHeight: number;
  scrollTop: number;
  clientHeight: number;
}

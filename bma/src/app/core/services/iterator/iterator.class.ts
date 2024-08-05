import { IIteratorItem } from './iterator-item.model';
import * as _ from 'underscore';

export class Iterator {
  /**
   * The list of items to iterate through.
   * @type {Array}
   */
  items: IIteratorItem[];

  private onFinishCallback: Function;

  /**
   * Current iterating index.
   * @type {number}
   * @private
   */
  private index: number = 0;

  /**
   * Indicator of start process.
   * @type {boolean}
   * @private
   */
  private isStartedFlag: boolean = false;
  /**
   * Indicator of current progress.
   * @type {boolean}
   * @private
   */
  private iterating: boolean = false;


  constructor(items?: IIteratorItem[]) {
    /**
     * The list of items to iterate through.
     * @type {Array}
     */
    this.items = items || [];
  }

  /**
   * Starts iterating over items from first item.
   * @param {Function=} callback
   */
  start(callback?: Function): void {
    this.onFinishCallback = callback;
    this.isStartedFlag = true;
    this.first();
  }

  /**
   * Public getter for isStarted
   * @return {boolean}
   */
  isStarted() {
    return this.isStartedFlag;
  }

  /**
   * Starts iterating over items from item by given index.
   * @param {number} index
   * @param {Function=} callback
   */
  startFrom(index: number, callback: Function): void {
    if (_.isFunction(callback)) {
      callback();
    }

    this.index = index;
    this.isStartedFlag = true;
    this.next();
  }

  /**
   * Adds new item or list of new items.
   * @param {Object|Array} items
   */
  add(items: IIteratorItem[] | IIteratorItem): void {
    this.items = this.items.concat(_.isArray(items) ? items : [items]);

    if (this.isStartedFlag && !this.iterating) {
      this.next();
    }
  }

  /**
   * Sets iterating index to first position and starts iteration from first item.
   */
  first(): void {
    this.index = 0;
    this.next();
  }

  /**
   * If iteration index is not on the last position -
   *   runs iterating function of current item,
   *   otherwise stops iteration.
   */
  next(): void {
    this.iterating = true;

    if (this.hasNext()) {
      const item = this.items[this.index++];
      item.run(this, item.data);
    } else {
      this.stop();
      if (_.isFunction(this.onFinishCallback)) {
        this.onFinishCallback();
      }
    }
  }

  /**
   * Checks if iteration index is not on the last position.
   * @return {Boolean}
   */
  hasNext(): boolean {
    return this.index < this.items.length;
  }

  /**
   * Resets iteration process.
   */
  reset(): void {
    this.index = 0;
    this.isStartedFlag = false;
    this.iterating = false;
    this.items = [];
  }

  /**
   * Stops iteration.
   */
  stop(): void {
    this.iterating = false;
  }
}

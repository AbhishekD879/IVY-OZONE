import {Base} from './base.model';
import {Filename} from '@app/client/private/models/filename.model';

export interface Upsell extends Base {
  /**
   * Key: two answer ids combined with ';',
   * Value: selection id.
   *
   * Assuming there're 4 Questions with 4 possible Answers each:
   * {
   * "questions[0].answers[0].id + ';' + questions[1].answers[0].id": 11111111, // first selection id
   * "questions[0].answers[0].id + ';' + questions[1].answers[1].id": 22222222, // second selection id
   * "questions[0].answers[0].id + ';' + questions[1].answers[2].id": 33333333, // third selection id
   * ...
   *  "questions[2].answers[3].id + ';' + questions[3].answers[3].id": 16161616, // last selection id
   * }
   */
  options: Options;
  defaultUpsellOption: number;
  fallbackImage: Filename;
  fallbackImageToUpload: File;
  imageUrl: string;
}

export interface Options {
  [answersIds: string]: number;
}

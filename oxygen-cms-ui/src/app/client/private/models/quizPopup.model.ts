import {Filename} from '@app/client/public/models/filename.model';

export interface QuizPopup {
  icon: Filename;
  header: string;
  description: string;
  submitCTAText: string;
  closeCTAText: string;
}

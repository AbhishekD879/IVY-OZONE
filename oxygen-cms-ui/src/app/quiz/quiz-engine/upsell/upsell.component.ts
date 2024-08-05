import {Component, Inject, OnInit} from '@angular/core';
import {Quiz} from '@app/client/private/models/quiz.model';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {Answer, Question} from '@app/client/private/models/question.model';
import {DataSource} from '@angular/cdk/table';
import {CollectionViewer} from '@angular/cdk/collections';
import {Observable} from 'rxjs/Observable';
import {Options, Upsell} from '@app/client/private/models/upsell';
import {QuizEngineEditComponent} from '@app/quiz/quiz-engine/quiz-engine-edit/quiz-engine-edit.component';
import {FormControl, FormGroup} from '@angular/forms';
import {DialogService} from '@app/shared/dialog/dialog.service';

class UpsellTable extends DataSource<UpsellTableRow> {
  columns: Array<String>;
  headerRowTipsAndNames: Array<any>;

  constructor(public rows: Array<UpsellTableRow>, columns: Array<String>) {
    super();
    const headerRowTipsAndNames = rows[0].horizontalAnswers.map((answer, index) => {
        return {
          name: columns[index],
          tip: answer.text
        };
      }
    );
    this.headerRowTipsAndNames = [{name: 'empty-cell'}, ...headerRowTipsAndNames];  // Empty cell for vertical Answers header column
    this.columns = this.headerRowTipsAndNames.map(tipAndName => tipAndName.name);
  }

  connect(collectionViewer: CollectionViewer): Observable<UpsellTableRow[]> {
    return Observable.of(this.rows);
  }

  disconnect(collectionViewer: CollectionViewer): void {
  }
}


@Component({
  selector: 'upsell',
  templateUrl: './upsell.component.html',
  styleUrls: ['upsell.component.scss']
})
export class UpsellComponent implements OnInit {
  upsellTable: UpsellTable;
  quiz: Quiz;
  upsell: Upsell;
  allQuestions: Array<Question> = [];

  firstSelectedQuestionOption: Option;
  secondSelectedQuestionOption: Option;
  allQuestionsOptions: Array<Option> = [];

  selectQuestionsFromGroup: FormGroup;
  firstQuestionSelectControl: FormControl;
  secondQuestionSelectControl: FormControl;

  constructor(
    @Inject(MAT_DIALOG_DATA) data: any,
    private dialogService: DialogService,
    private dialogRef: MatDialogRef<QuizEngineEditComponent>
  ) {
    this.dialogRef.disableClose = true;
    this.quiz = data.quiz;
    this.upsell = JSON.parse(JSON.stringify(data.quiz.upsell));

    this.allQuestions = data.flattenQuestions;
    if (this.upsell) {
      this.upsell.fallbackImage = data.quiz.upsell.fallbackImage;
      this.upsell.fallbackImageToUpload = data.quiz.upsell.fallbackImageToUpload;
    }
  }

  /**
   * We assume that only two questions can be combined to configure upsell. Might change in the future, though.
   */
  ngOnInit() {
    this.allQuestionsOptions = this.allQuestions
      .filter(question => question.text && question.answers && question.answers.length)
      .map((question, index) => {
        return {
          id: question.id,
          index: index,
          title: `${index + 1}. "${question.text}"`,
          data: question
        };
      });
    if (this.upsell) {
      if (Object.keys(this.upsell.options).length) {
        const firstQuestionAnswerId = this.answerIds()[0];
        const secondQuestionAnswerId = this.answerIds()[1];

        this.allQuestionsOptions.forEach(option => option.data.answers.forEach(answer => {
          if (answer.id === firstQuestionAnswerId) {
            this.firstSelectedQuestionOption = option;
          } else if (answer.id === secondQuestionAnswerId) {
            this.secondSelectedQuestionOption = option;
          }
        }));
        this.redrawAnswersTable();
      }
    } else {
      this.upsell = {
        defaultUpsellOption: null,
        fallbackImage: null,
        fallbackImageToUpload: null,
        options: {},
        brand: '',
        createdAt: '',
        createdBy: '',
        createdByUserName: '',
        id: '',
        updatedAt: '',
        updatedBy: '',
        updatedByUserName: '',
        imageUrl: ''
      };
    }
    this.firstQuestionSelectControl = new FormControl(this.firstSelectedQuestionOption, []);
    this.secondQuestionSelectControl = new FormControl(this.secondSelectedQuestionOption, []);
    this.selectQuestionsFromGroup = new FormGroup({
      firstQuestionSelect: this.firstQuestionSelectControl,
      secondQuestionSelect: this.secondQuestionSelectControl
    });
  }

  answerIds() {
    return Object.keys(this.upsell.options)[0].split(';');
  }

  redrawAnswersTable() {
    if (this.firstSelectedQuestionOption && this.secondSelectedQuestionOption) {
      const rows = Array.prototype.concat(...this.firstSelectedQuestionOption.data.answers
        .map((verticalAnswer, index) => {
            return {
              verticalAnswer: verticalAnswer,
              verticalHeader: this.headerTitle(this.firstSelectedQuestionOption.index, index),
              horizontalAnswers: this.secondSelectedQuestionOption.data.answers,
              options: this.upsell.options
            };
          }
        )
      );
      this.upsellTable = new UpsellTable(
        rows,
        this.secondSelectedQuestionOption.data.answers.map((answer, index) =>
          this.headerTitle(this.secondSelectedQuestionOption.index, index)
        )
      );
    } else {
      this.upsellTable = null;
    }
  }

  assignFirstQuestion(option: Option) {
    this.openConfirmationDialogIfBreakingChanges(
      () => {
        this.upsell.options = {};
        this.firstSelectedQuestionOption = option;

        if (this.shouldReset()) {
          this.secondSelectedQuestionOption = null;
          this.secondQuestionSelectControl.setValue(null);
        }
        this.redrawAnswersTable();
      },
      () => this.firstQuestionSelectControl.setValue(this.firstSelectedQuestionOption));
  }

  assignSecondQuestion(option: Option) {
    this.openConfirmationDialogIfBreakingChanges(
      () => {
        this.upsell.options = {};
        this.secondSelectedQuestionOption = option;

        if (this.shouldReset()) {
          this.firstSelectedQuestionOption = null;
          this.firstQuestionSelectControl.setValue(null);
        }
        this.redrawAnswersTable();
      },
      () => this.secondQuestionSelectControl.setValue(this.secondSelectedQuestionOption));
  }

  closeDialog(): void {
    this.dialogService.showConfirmDialog({
      title: 'Confirm cancellation',
      message: 'Your changes will be lost. Are you sure?',
      yesCallback: () => {
        this.dialogRef.close();
      }
    });
  }

  shouldReset(): boolean {
    return !!this.firstQuestionSelectControl
      && !!this.secondSelectedQuestionOption
      && (this.secondSelectedQuestionOption && this.secondSelectedQuestionOption.index <= this.firstSelectedQuestionOption.index);
  }

  headerTitle(optionIndex: number, answerIndex: number): string {
    return `Q${optionIndex + 1}A${answerIndex + 1}`;
  }

  save() {
    Object.keys(this.upsell.options)
      .filter(answersIds => !this.upsell.options[answersIds])
      .forEach(answersIds => delete this.upsell.options[answersIds]);

    this.dialogRef.componentInstance.quiz.upsell = this.upsell;
  }

  clear() {
    this.firstSelectedQuestionOption = null;
    this.secondSelectedQuestionOption = null;
    this.upsell = null;
    this.redrawAnswersTable();
    this.firstQuestionSelectControl.setValue(null);
    this.secondQuestionSelectControl.setValue(null);
  }

  openConfirmationDialogIfBreakingChanges(yes: () => void, no: () => void) {
    if (this.firstSelectedQuestionOption && this.secondSelectedQuestionOption && Object.keys(this.upsell.options).length) {
      this.dialogService.showConfirmDialog({
        title: 'Confirm upsell options rewrite',
        message: 'By changing question you are going to lost everything that was configured so far. Are your sure? ',
        yesCallback: () => {
          yes();
        },
        noCallback() {
          no();
        }
      });
    } else {
      yes();
    }
  }

  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const supportedTypes = ['image/svg', 'image/svg+xml', 'image/png', 'image/jpeg', 'image/gif'];
    if (supportedTypes.indexOf(file.type) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\", \"jpeg\", \"png\" and \"gif\".'
      });
      return;
    }
    this.upsell.fallbackImageToUpload = file;
  }

  handleUploadImageClick(event): void {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  removeImage(): void {
    this.upsell.fallbackImage = null;
    this.upsell.fallbackImageToUpload = null;
  }
}

export abstract class Option {
  id: string;
  index: number;
  title: string;
  data: Question;
}

interface UpsellTableRow {
  verticalAnswer: Answer;
  verticalHeader: string;
  horizontalAnswers: Answer[];
  options: Options;
}

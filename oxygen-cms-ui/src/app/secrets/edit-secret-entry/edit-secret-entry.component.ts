import { AfterViewInit, Component, ElementRef, Inject, OnInit, QueryList, ViewChildren } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { SecretEntry, SecretItem } from '@app/client/private/models/secret.model';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-edit-secret-entry',
  templateUrl: './edit-secret-entry.component.html',
  styleUrls: ['./edit-secret-entry.component.scss']
})
export class EditSecretEntryComponent implements OnInit, AfterViewInit {
  title: string;
  secret: SecretEntry;

  @ViewChildren('itemRef') itemRefs: QueryList<ElementRef>;

  private readonly emptySecret: Partial<SecretEntry> = {
    brand: this.brandService.brand,
    uri: '',
    name: '',
    enabled: false,
    items: []
  };

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    @Inject(MAT_DIALOG_DATA) public dialog: any
  ) {}

  get isValidSecretEntry(): boolean {
    return !!(this.secret.name && this.secret.uri && this.secret.items.every(item => !item.emptyKey && !item.duplicateKey));
  }

  ngOnInit(): void {
    this.title = this.dialog.title;
    this.secret = { ...this.emptySecret, ...this.dialog.data };
  }

  ngAfterViewInit(): void {
    this.itemRefs.changes.subscribe((itemRefs: QueryList<ElementRef>) => itemRefs && itemRefs.last && itemRefs.last.nativeElement &&
      itemRefs.last.nativeElement.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' }));
  }

  addItem(): void {
    this.secret.items.push({ key: '', value: ''});
    this.validateKeys();
  }

  toggleItem(item: SecretItem): void {
    if (!item.key && !item.value) {
      this.secret.items.splice(this.secret.items.indexOf(item), 1);
    } else {
      item.removed = !item.removed;
    }
    this.validateKeys();
  }

  validateKeys(): void {
    this.secret.items.forEach((item: SecretItem) => {
      item.emptyKey = !item.removed && !item.key;
      item.duplicateKey = !item.removed && !!item.key && this.secret.items.some((comparedItem: SecretItem) =>
        item !== comparedItem && !comparedItem.removed && item.key === comparedItem.key);
    });
  }

  normalizeEntry(): void {
    this.secret.name = this.secret.name.trim();
    this.secret.uri = this.secret.uri.trim();
    this.secret.items = this.secret.items.filter((item: SecretItem): boolean => {
      if (!item.removed) {
        delete item.emptyKey;
        delete item.duplicateKey;
        delete item.removed;
        item.key = item.key.trim();
        item.value = item.value.trim();
        return true;
      }
    });
  }

  closeDialog() {
    this.dialogRef.close();
  }
}
